$(document).ready(function(){
    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings){
            xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
        }
    });
});