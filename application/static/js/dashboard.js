$('#submitForms').click(function () {
    var data = [];
    $('.form').each(function (index, value) {
        var form = $(this),
            check = {};

        if(form.is(':hidden')) {
            return;
        }

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
                check[name] = value;
            }
        });

        $.extend(check, list_entries);
        data.push(check);
    });

    if(data.length > 0) {
        $.ajax({
            url: '/dashboard',
            type: 'POST',
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            success: function (response) {
                
            }
        });
    }

});

var headerIndex = 0;
var assertionIndex = 1;
var checkIndex = 0;
$("#addCheck").click(function () {
    var clone = $("#checkTemplate").clone().attr('id', 'check' + checkIndex);
    const tabPanes = clone.children(".form").children(".tab-content").children(".tab-pane");
    const requestPane = $(tabPanes[0]);
    const assertionsPane = $(tabPanes[1]);
    requestPane.attr('id', 'request' + checkIndex);
    var headersBox = requestPane.children('#headers');
    headersBox.attr('id', 'headers' + checkIndex);
    const requestForm = requestPane.children('.requestForm');
    requestPane.children(".add-button").click(function () {
        var clone = $("#header").clone().attr('id', 'header' + headerIndex);
        clone.children('.remove-header').click(function () {
            $(this).parent().remove();
        })
        clone.appendTo(headersBox);
        headerIndex++;
    });
    assertionsPane.attr('id', 'assertions' + checkIndex);
    var assertionsBox = assertionsPane.children('#assertions-box')
    assertionsBox.attr('id', 'assertions' + checkIndex);
    assertionsPane.children(".add-button").click(function () {
        var clone = $("#assertion0").clone().attr('id', 'assertion' + assertionIndex);
        clone.children('.remove-assertion').click(function () {
            $(this).parent().remove();
        })
        clone.appendTo(assertionsBox);
        assertionIndex++;
    });
    const navTabs = clone.children(".nav").children(".nav-link");
    $(navTabs[0]).attr('href', '#request' + checkIndex);
    $(navTabs[1]).attr('href', '#assertions' + checkIndex);
    clone.children('.removeCheck').click(function () {
        $(this).parent().remove();
    })
    clone.appendTo("#checksFormContainer");
    checkIndex++;
});
