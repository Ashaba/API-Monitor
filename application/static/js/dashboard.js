const requestHeaderTemplate = `
    <div class="form-inline">
        <input name="headerKey" type="text" class="form-control" placeholder="KEY">
        <input name="headerValue" type="text" class="form-control" placeholder="VALUE">
        <input name="headerId" type="text" class="hidenIds">
        <span class="removeHeader">&times;</span>
    </div>
`,
    checkAssertionTemplate = `
    <div class="assertion">
        <input name="assertionId" type="text" class="hidenIds">
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
        <nav class="nav requestAssertion" role="tablist">
            <a class="nav-link active" data-toggle="tab" href="#request" role="tab">Request</a>
            <a class="nav-link" data-toggle="tab" href="#assertions" role="tab">Assertions</a>
        </nav>
        <span class="serverReportedError"></span>
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
                        <input name="id" type="text" class="hidenIds">
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
var error_in_forms = false;

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
        headerIds: [],
        assertionSources: [],
        assertionComparisons: [],
        assertionTargetValues: [],
        assertionIds: [],
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
        if (field.hasClass('hidenIds') == false && value == "") {
            error_in_forms = true;
            field.addClass('error');
        } else {
            field.removeClass('error');
            if (name == 'url') {
                if(isURL(value) == false) {
                    field.addClass('error');
                    error_in_forms = true;
                }
            }
            if (plural_name in list_entries) {
                list_entries[plural_name].push(value);
            } else {
                data[name] = value;
            }
        }
    });

    $.each(list_entries.headerKeys, function(index, keyName) {
        headersAndAssertions.headers.push({
            key: keyName,
            value: list_entries.headerValues[index],
            id: list_entries.headerIds[index]
        });
    });

    $.each(list_entries.assertionSources, function(index, sourceName) {
        headersAndAssertions.assertions.push({
            assertion_type: sourceName,
            comparison: list_entries.assertionComparisons[index],
            value: list_entries.assertionTargetValues[index],
            id: list_entries.assertionIds[index]
        });
    });

    $.extend(data, headersAndAssertions);
    return data;
}

function postData(data, callback) {
    url = ($(location).attr('pathname')) + '/update';
    var delay = 3000; //add a delay to simulate network request
    if (data.constructor === Array && data.length > 0) {
        // show the spinner when the request is initiated
        $('.loading-spinner').show();
        $.ajax({
            url: url,
            type: 'POST',
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            success: callback
        });
    } else {
        return false;
    }
}

$('#addCheck').on('click', function () {
    createCheck(-1, {})
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
    check.attr('id', checkData.id);

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
        check.find('[name="id"]').val(checkData.id);
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
    header.find('[name="headerId"]').val(headerData.id);
    header.find('.removeHeader').click(function(){
        header.remove();
    });
    header.appendTo(check.find('.headers'));
}

function createAnAssertion(check, assertionData) {
    var assertion = $($.trim(checkAssertionTemplate));
    if($.isEmptyObject(assertionData) == false){
        assertion.find('[name="assertionSource"]').val(assertionData.assertion_type);
        assertion.find('[name="assertionComparison"]').val(assertionData.comparison);
        assertion.find('[name="assertionTargetValue"]').val(assertionData.value);
        assertion.find('[name="assertionId"]').val(assertionData.id);
    }
    assertion.find('.remove-assertion').click(function(){
        assertion.remove();
    });
    assertion.appendTo(check.find('.assertions'));
}

function isURL(str) {
    var urlregex = /^(https?|ftp):\/\/([a-zA-Z0-9.-]+(:[a-zA-Z0-9.&%$-]+)*@)*((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}|([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|[a-zA-Z]{2}))(:[0-9]+)*(\/($|[a-zA-Z0-9.,?'\\+&%$#=~_-]+))*$/;
    return urlregex.test(str);
}

$.each(context.checks, createCheck)
