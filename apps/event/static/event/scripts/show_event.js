$(document).ready(function() {
    $('[data-toggle="popover"]').popover();
    ShowEvent.init();
});

let ShowEvent = function () {
    let a_save_events_from_json_file;

    let init_variables = function(){
        a_save_events_from_json_file = $('#a_save_events_from_json_file');
    };

    let handle_events = function(){
        a_save_events_from_json_file.on('click', save_events_from_json_file);
    };

    let save_events_from_json_file = function (ev) {
        let span_save_events_from_json_file$ = $('#span_save_events_from_json_file');
        span_save_events_from_json_file$.addClass('fas fa-spinner fa-spin fa-lg');
        ev.preventDefault();
        $.ajax({
            url: a_save_events_from_json_file.attr('href'),
            success: function (data) {
                Core.show_notification(data);
                span_save_events_from_json_file$.removeClass('fas fa-spinner fa-spin fa-lg');
                a_save_events_from_json_file.blur();
                Events.render_calendar();
            }
        });
    };

    return{
        init: function () {
            Events.init();
            init_variables();
            handle_events();
        }
    }

}();
