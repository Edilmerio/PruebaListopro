let Core = function () {

    let show_notification = function (obj) {
        if (obj !== {}) {
            // type = success,error,info
            let config = {
                title: obj.title,
                text: obj.text,
                delay: 3000,
            };
            if (obj.type === 'success'){
                PNotify.success(config);
            }
            else if (obj.type === 'info'){
                PNotify.info(config);
            }
            else if (obj.type === 'error'){
                PNotify.error(config);
            }
        }
    };

    return{
        show_notification: show_notification,
    }

}();