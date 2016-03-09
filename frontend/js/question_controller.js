$(document).ready(function(){
    var getQ = new backend();

    var success = function(data) {
        $('#questionText').text(data.question_text); //adds question text to page

        var $aProto = $('#a_proto'); //creates prototype question box
		var minWidth = 200; //this is the minimum width of an answer button to be displayed
		
        for (var i = 0; i < data.answers.length; i++) {
            var $thisClone = $aProto.clone() //clones a prototype question box
                .text(data.answers[i]) //inserts answer text into question boxes
                .appendTo($('#mcContainer')) //puts question boxes in the correct container
                .addClass('a'+i) //adds class identifiers to each question box
                .removeClass('hidden'); //shows the question box
            //console.log(minWidth);
            if ($thisClone.width() > minWidth){
            	//console.log(minWidth);
            	minWidth = $thisClone.width(); //checks for the maximum box width to standardize box widths
            if ($thisClone.text(data.answer_index)){
            	derp;
            };
         };
        };
        
        $('.mcAnsBtn').each(function(){
        	$(this).width(minWidth); //standardizes box widths
        });
        $('#mcContainer').randomize('a');
    };

    var error = function() {
        console.log("error");
    };
    
	var qID = ""; //question ID to get
    getQ.getData(success,qID); 
});

$('.mcAnsBtn').click(function(){
	
});
