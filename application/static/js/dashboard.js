$('#submitForms').click(function () {
    var data = [];
    $('.form').each(function (index, value) {
        var form = $(this),
            check = {};
        form.find('[name]').each(function (index1, value1) {
            if (index == 0) {
                return;
            }
            var field = $(this),
                name = field.attr('name'),
                value = field.val();
            if (name in check) {
                if (check[name].constructor === Array) {
                    check[name].push(value);
                } else {
                    const tempValue = check[name];
                    check[name] = [tempValue, value];
                }
            } else {
                check[name] = value;
            }
        });
        data.push(check);
    });
    $.ajax({
        url: 'http://127.0.0.1:5000/dashboard',
        type: 'POST',
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        success: function (response) {
            console.log("here", response);
        }
    });
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
        });
        clone.appendTo(headersBox);
        headerIndex++;
    });
    assertionsPane.attr('id', 'assertions' + checkIndex);
    var assertionsBox = assertionsPane.children('#assertions-box');
    assertionsBox.attr('id', 'assertions' + checkIndex);
    assertionsPane.children(".add-button").click(function () {
        var clone = $("#assertion0").clone().attr('id', 'assertion' + assertionIndex);
        clone.children('.remove-assertion').click(function () {
            $(this).parent().remove();
        });
        clone.appendTo(assertionsBox);
        assertionIndex++;
    });
    const navTabs = clone.children(".nav").children(".nav-link");
    $(navTabs[0]).attr('href', '#request' + checkIndex);
    $(navTabs[1]).attr('href', '#assertions' + checkIndex);
    clone.children('.removeCheck').click(function () {
        $(this).parent().remove();
    });
    clone.appendTo("#checksFormContainer");
    checkIndex++;
});
