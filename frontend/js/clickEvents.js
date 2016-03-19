$(document).ready(function(){
    $(document).on("click", ".activated", function(){
	    console.log('Sending user answer = ' + $(this).attr('data-index'));
        var validation_request = new Request($(this).attr('data-question_id'), $(this).attr('data-index'), '0', '0')
        validation_request.send(urlsendANS, checkValid)

    });

    $(document).on("click", ".clickable", function(){
        $('.mcAnsBtn').each(function(){
            $(this).removeClass('btn-warning');
            $(this).removeClass('activated');
        });
	    $(this).addClass('btn-warning')
	    $(this).addClass('activated');
    });

    $(document).on("click", "#debug-btn", function(){
        debugURL = '';
        POST.debug(debugURL);
    });

    $(document).on('opening', '.remodal', function () {
        console.log('opening');
    });

    $(document).on('opened', '.remodal', function () {
        console.log('opened');
    });

    $(document).on('closing', '.remodal', function (e) {
        console.log('closing' + (e.reason ? ', reason: ' + e.reason : ''));
    });

    $(document).on('closed', '.remodal', function (e) {
        console.log('closed' + (e.reason ? ', reason: ' + e.reason : ''));
    });

    $(document).on('confirmation', '.remodal', function () {
        console.log('confirmation');
    });

    $(document).on('cancellation', '.remodal', function () {
        console.log('cancellation');
    });

});
