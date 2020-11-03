let Events = function () {

    let calendarEl = document.getElementById('calendar');
    let calendar;
    let config_calendar = {initialView: 'dayGridMonth',
        initialDate: '2020-10-07',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: 'get_events',
        views: {
            timeGrid: {
                dayMaxEventRows: 5 // adjust to 6 only for timeGridWeek/timeGridDay
            }
        },
        eventClick: function(info) {
            // alert('Event: ' + info.event.title);
            // alert('Coordinates: ' + info.jsEvent.pageX + ',' + info.jsEvent.pageY);
            // alert('View: ' + info.view.type);
            console.log(info.event.extendedProps);
            $(info.el).popover({
                title: info.event.title,
                placement:'top',
                trigger : 'hover',
                container:'body'
            }).popover('show');
        }
    };

    let init_elements = function(){
        render_calendar();
    };

    let render_calendar = function () {
        calendar = new FullCalendar.Calendar(calendarEl, config_calendar);
        calendar.render();
    };

    return{
        init: function () {
            init_elements();
        },
        render_calendar: render_calendar
    }
}();