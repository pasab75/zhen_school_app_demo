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

    $(document).on("click", "#questionText", function(){
        POST.addQuestions();
    });

});
