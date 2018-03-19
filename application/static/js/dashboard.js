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
            <option>Status Code</option>
            <option>Response Time (ms)</option>
        </select>
        <select name="assertionComparison" class="form-control assertion-value">
            <option>equal (number)</option>
            <option>less than</option>
            <option>less than or equal to</option>
            <option>greater than</option>
            <option>greater than or equal to</option>
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
                            <option>GET</option>
                            <option>POST</option>
                            <option>PUT</option>
                            <option>DELETE</option>
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
function addElement(event) {
    var element = $($.trim(event.data.template));
    var removeButton = element.children("[class^=remove]");
    removeButton.on('click', { element: removeButton }, removeParent);
    if (event.data.template == checkTemplate) {
        var navLinks = element.find('.nav-link');
        $(navLinks[0]).attr('href', `#request${checkId}`);
        $(navLinks[1]).attr('href', `#assertions${checkId}`);
        var tabPanes = element.find('.tab-pane');
        $(tabPanes[0]).attr('id', `request${checkId}`);
        $(tabPanes[1]).attr('id', `assertions${checkId}`);
        var headersContainer = element.find('#headers');
        element.find('.addHeader').on(
            'click',
            {
                container: headersContainer,
                template: requestHeaderTemplate
            },
            addElement
        )

        var assertionsContainer = element.find('#assertionsBox');
        var assertionsEvent = {
            data: {
                container: assertionsContainer,
                template: checkAssertionTemplate
            }
        };
        addElement(assertionsEvent);
        element.find('.addAssertion').on(
            'click',
            assertionsEvent.data,
            addElement
        )
        checkId++;
    }
    event.data.container.append(element);
}

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
        assertionTargetValues: []
    };

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

    $.extend(data, list_entries);
    return data

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

$('#addCheck').on(
    'click',
    {
        container: $('#checksFormContainer'),
        template: checkTemplate
    },
    addElement
);

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
