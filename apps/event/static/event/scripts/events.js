let Events = function () {

    let calendarEl = document.getElementById('calendar');
    let calendar;
    let config_calendar = {
        initialView: 'dayGridMonth',
        timeZone:  moment.tz.guess(),
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
        init_time_zone_select();
    };

    let init_time_zone_select = function(){
        let time_zones = moment.tz.names();
        let time_zone_local = moment.tz.guess();

        time_zones.forEach(function (tz) {
            $('#select_time_zones').append('<option value='+tz+'>'+tz+'</option>');
        });
        $('#select_time_zones').val(time_zone_local);
        $('#select_time_zones').selectpicker('refresh');
    };

    let handle_events = function(){
        $('#select_time_zones').on('changed.bs.select', select_time_zone_change);
    };

    let select_time_zone_change = function(){
      calendar.setOption('timeZone', this.value);
      $(this).blur();
    };

    let render_calendar = function () {
        calendar = new FullCalendar.Calendar(calendarEl, config_calendar);
        calendar.render();
    };

    let refetch_calendar = function () {
        calendar.refetchEvents()
    };

    return{
        init: function () {
            init_elements();
            handle_events();
        },
        refetch_calendar: refetch_calendar
    }
}();