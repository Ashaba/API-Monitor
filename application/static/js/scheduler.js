$(function () {

    var MINUTE = {name: "min", nsecs: 60};
    var HOUR = {name: "hour", nsecs: MINUTE.nsecs * 60};
    var DAY = {name: "day", nsecs: HOUR.nsecs * 24};
    var WEEK = {name: "week", nsecs: DAY.nsecs * 7};
    var UNITS = [WEEK, DAY, HOUR, MINUTE];

    var secsToText = function (total) {
        var remainingSeconds = Math.floor(total);
        var result = "";
        for (var i = 0, unit; unit = UNITS[i]; i++) {
            if (unit === WEEK && remainingSeconds % unit.nsecs != 0) {
                // Say "8 days" instead of "1 week 1 day"
                continue
            }

            var count = Math.floor(remainingSeconds / unit.nsecs);
            remainingSeconds = remainingSeconds % unit.nsecs;

            if (count == 1) {
                result += "1 " + unit.name + " ";
            }

            if (count > 1) {
                result += count + " " + unit.name + "s ";
            }
        }

        return result;
    }

    var periodSlider = document.getElementById("period-slider");
    noUiSlider.create(periodSlider, {
        start: [20],
        connect: "lower",
        range: {
            'min': [60, 60],
            '20%': [3600, 3600],
            '40%': [86400, 86400],
            '60%': [604800, 604800],
            '80%': [2592000, 864000],
            'max': 5184000,
        },
        pips: {
            mode: 'values',
            values: [60, 1800, 3600, 43200, 86400, 604800, 2592000, 5184000],
            density: 4,
            format: {
                to: secsToText,
                from: function () {
                }
            }
        }
    });

    periodSlider.noUiSlider.on("update", function (a, b, value) {
        var rounded = Math.round(value);
        $("#period-slider-value").text(secsToText(rounded));
        $("#update-timeout-timeout").val(rounded);
    });

    $('[data-toggle="tooltip"]').tooltip();

    $(".check-menu-remove").click(function () {
        var $this = $(this);

        $("#remove-check-form").attr("action", $this.data("url"));
        $(".remove-check-name").text($this.data("name"));
        $('#remove-check-modal').modal("show");

        return false;
    });

});

$(".update-timeout-form").submit(updateScheduler);

function updateScheduler(event) {
    event.preventDefault();
    var form = $(this);
    var id = form.attr('id');
    console.log(id);

    var form_data = $(this).serializeArray();
    console.log(form_data);
    $.ajax({
        type: 'PUT',
        url: '/collection-details/' + id,
        data: form_data,
        success: function (data) {
            console.log('Put was performed.');
        }
    });
}
