$(document).ready(function(){
    var questInit = new postRequest();

    var success = function(data) {
        $('#questionText').text(data.question_text); //adds question text to page

        var $aProto = $('#a_proto'); //creates prototype question box

		var correctAns = data.answer_index;

		var minWidth = 200; //this is the minimum width of an answer button to be displayed

        for (var i = 0; i < data.answers.length; i++) {
            var $thisClone = $aProto.clone() //clones a prototype question box
                .text(data.answers[i]) //inserts answer text into question boxes
                .appendTo($('#mcContainer')) //puts question boxes in the correct container
                .addClass('a'+i) //adds class identifiers to each question box
                .removeClass('hidden'); //shows the question box
            //console.log(minWidth);
                console.log(i);
            if ($thisClone.width() > minWidth){
            	//console.log(minWidth);
            	minWidth = $thisClone.width(); //checks for the maximum box width to standardize box widths
            };
            if ((i+1) == correctAns){
            	$thisClone.addClass('correct');
            };
         };

        
        $('.mcAnsBtn').each(function(){
        	$(this).width(minWidth); //standardizes box widths
        });
        $('#mcContainer').randomize('a');

    var error = function() {
        console.log("error");
    };

    };
	var qID = {'id':'2'}; //question ID to get
	var url = 'http://exbookapp.org:5000/get/question'
    questInit.getData(success, qID, url);
});

$('.mcAnsBtn').click(function(){
	
});

