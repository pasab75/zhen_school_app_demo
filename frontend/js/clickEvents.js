$(document).ready(function(){
    $(document).on("click", ".activated", function(){
	    console.log($(this).attr('data-index'));
	    var indexes = {'qID':$(this).attr('data-qID'), 'aID':$(this).attr('data-index')};
        POST.validateAns(indexes);

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
