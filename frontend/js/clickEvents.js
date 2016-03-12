$(document).ready(function(){
    $(document).on("click", ".questionClicked", function(){
	    console.log($(this).attr('data-index'));
	    var indexes = {'qID':$(this).attr('data-qID'), 'aID':$(this).attr('data-index')};
        POST.validateAns(indexes);
    });

    $(document).on("click", "#a_proto", function(){
        $('.mcAnsBtn').each(function(){
            $(this).removeClass('questionClicked'); //standardizes box widths
        });
	    $(this).addClass('questionClicked')
    });

    $(document).on("click", "#debug-btn", function(){
        debugURL = '';
        POST.debug(debugURL);
    });

    $(document).on("click", "#questionText", function(){
        POST.addQuestions();
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
