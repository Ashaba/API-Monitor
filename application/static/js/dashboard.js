const requestHeaderTemplate = `
    <div class="form-inline">
        <input name="headerKey" type="text" class="form-control" placeholder="KEY">
        <input name="headerValue" type="text" class="form-control" placeholder="VALUE">
        <span class="removeHeader">&times;</span>
    </div>
`,
    checkAssertionTemplate = `
    <div class="assertion">
        <select name="assertionSource" class="form-control assertion-value">
            <option value="Status Code">Status Code</option>
            <option value="Response Time (ms)">Response Time (ms)</option>
        </select>
        <select name="assertionComparison" class="form-control assertion-value">
            <option value="equal (number)">equal (number)</option>
            <option value="less than">less than</option>
            <option value="less than or equal to">less than or equal to</option>
            <option value="greater than">greater than</option>
            <option value="greater than or equal to">greater than or equal to</option>
        </select>
        <input name="assertionTargetValue" type="text" class="form-control assertion-value" id="targetValue" placeholder="Enter value">
        <span class="remove-assertion">&times;</span>
    </div>
`,
    checkTemplate = `
    <div class="check" id="checkTemplate">
        <span class="removeCheck">
            <i class="fas fa-times"></i>
        </span>
        <nav class="nav" role="tablist">
            <a class="nav-link active" data-toggle="tab" href="#request" role="tab">Request</a>
            <a class="nav-link" data-toggle="tab" href="#assertions" role="tab">Assertions</a>
        </nav>
        <form class="form">
            <div class="tab-content">
                <div class="tab-pane active" id="request" role="tabpanel">
                    <span class="tab-pane-heading">ENDPOINT</span>
                    <div class="form-inline requestForm">
                        <select name="method" class="form-control">
                            <option value="GET">GET</option>
                            <option value="POST">POST</option>
                            <option value="PUT">PUT</option>
                            <option value="DELETE">DELETE</option>
                        </select>
                        <input name="url" type="text" class="form-control url-input" placeholder="URL">
                    </div>
                    <span class="tab-pane-heading">HEADERS</span>
                    <div class="headers" id="headers"></div>
                    <span class="addHeader">+ Add header</span>
                </div>
                <div class="tab-pane" id="assertions" role="tabpanel">
                    <div class="assertions" id="assertionsBox">
                        <div class="headings">
                            <span>SOURCE</span>
                            <span>COMPARISON</span>
                            <span>TARGET VALUE</span>
                        </div>
                    </div>
                    <span class="addAssertion">+ Add assertion</span>
                </div>
            </div>
        </form>
    </div>
`;

var checkId = 0;

function removeParent(event) {
    event.data.element.parent().remove();
}

function getFormData(form) {

    var form = form,
        data = {};

    const list_entries = {
        headerKeys: [],
        headerValues: [],
        assertionSources: [],
        assertionComparisons: [],
        assertionTargetValues: [],
    };

    var headersAndAssertions = {
        headers: [],
        assertions: []
    }

    form.find('[name]').each(function (index1, value1) {
        var field = $(this),
            name = field.attr('name'),
            value = field.val(),
            plural_name = name + 's';
        
        if (plural_name in list_entries) {
            list_entries[plural_name].push(value);
        } else {
            data[name] = value;
        }
    });

    $.each(list_entries.headerKeys, function(index, keyName) {
        headersAndAssertions.headers.push({
            key: keyName,
            value: list_entries.headerValues[index]
        });
    });

    $.each(list_entries.assertionSources, function(index, sourceName) {
        headersAndAssertions.assertions.push({
            source: sourceName,
            comparison: list_entries.assertionComparisons[index],
            value: list_entries.assertionTargetValues[index]
        });
    });

    $.extend(data, headersAndAssertions);
    return data;
}

function postData(data, callback) {
    var delay = 3000; //add a delay to simulate network request
    if (data.constructor === Array && data.length > 0) {
        // show the spinner when the request is initiated
        $('.loading-spinner').show();
        $.ajax({
            url: '/dashboard',
            type: 'POST',
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            success: callback,
            complete: function(){
                //add a delay
                setTimeout(function() {
                    // hide the spinner when the request completes
                    $('.loading-spinner').hide();
                    // empty the form fields
                    $('.form').trigger('reset');
                }, delay);
            }
        });
    } else {
        return false;
    }
}

function onPostData() {

}

$('#addCheck').on('click', function () {
    createCheck(-1, {})
});

$('#submitForms').on('click', function() {
    var data = [];
    $('.form').each(function() {
        data.push(getFormData($(this)));
    });
    postData(data, onPostData);
});

$('#runChecks').on('click', function() {
    var data = [];
    $('.form').each(function() {
        data.push(getFormData($(this)));
    });
    postData(data, onPostData);
    console.log(data)
    postData(data, onPostData)
});

if(typeof module !== 'undefined') {
    module.exports.main = {
        requestHeaderTemplate,
        checkAssertionTemplate,
        checkTemplate,
        getFormData,
        addElement,
        removeParent,
        postData
    }
}

function createCheck(index, checkData) {
    var check = $($.trim(checkTemplate));

    var removeButton = check.children("[class^=remove]");
    removeButton.on('click', { element: removeButton }, removeParent);

    var navLinks = check.find('.nav-link');
    $(navLinks[0]).attr('href', `#request${checkId}`);
    $(navLinks[1]).attr('href', `#assertions${checkId}`);
    var tabPanes = check.find('.tab-pane');
    $(tabPanes[0]).attr('id', `request${checkId}`);
    $(tabPanes[1]).attr('id', `assertions${checkId}`);
    var headersContainer = check.find('#headers');
    check.find('.addHeader').click(function() {
        createHeader(check, {});
    })

    check.find('.addAssertion').click(function() {
        createAnAssertion(check, {});
    })
    checkId++;

    if($.isEmptyObject(checkData) == false) {
        check.find('[name="method"]').val(checkData.method);
        check.find('[name="url"]').val(checkData.url);
        if('headers' in checkData && checkData.headers.length > 0) {
            $.each(checkData.headers, function(index, headerData) {
                createHeader(check, headerData);
            });
        }
        if('assertions' in checkData && checkData.assertions.length > 0) {
            $.each(checkData.assertions, function(index, assertionData) {
                createAnAssertion(check, assertionData);
            });
        } else {
            createAnAssertion(check, {});
        }
    } else {
        createAnAssertion(check, {});
    }
    check.appendTo($('#checksFormContainer'));
}

function createHeader(check, headerData) {
    var header = $($.trim(requestHeaderTemplate));
    header.find('[name="headerKey"]').val(headerData.key);
    header.find('[name="headerValue"]').val(headerData.value);
    header.find('.removeHeader').click(function(){
        header.remove();
    });
    header.appendTo(check.find('.headers'));
}

function createAnAssertion(check, assertionData) {
    var assertion = $($.trim(checkAssertionTemplate));
    if($.isEmptyObject(assertionData) == false){
        assertion.find('[name="assertionSource"]').val(assertionData.type);
        assertion.find('[name="assertionComparison"]').val(assertionData.comparison);
        assertion.find('[name="assertionTargetValue"]').val(assertionData.value);
    }
    assertion.find('.remove-assertion').click(function(){
        assertion.remove();
    });
    assertion.appendTo(check.find('.assertions'));
}

$.each(context.checks, createCheck)
