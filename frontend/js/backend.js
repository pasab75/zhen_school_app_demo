// This is POST object that contains all the various types of POSTS we will do

var parseMCQuestion = function(data) { //this is the on success function for parsing a multiple choice question
    $('#questionText').text(data.question_text); //adds question text to page

    var $aProto = $('#a_proto'); //creates prototype question box

    //var correctAns = data.answer_index;

    var minWidth = 200; //this is the minimum width of an answer button to be displayed

    for (var i = 0; i < data.answers.length; i++) {
        var $thisClone = $aProto.clone() //clones a prototype question box
            .text(data.answers[i]) //inserts answer text into question boxes
            .appendTo($('#mcContainer')) //puts question boxes in the correct container
            .attr('data-index', i) //adds class identifiers to each question box
            .removeClass('hidden'); //shows the question box

            if ($thisClone.width() > minWidth){

            	minWidth = $thisClone.width(); //checks for the maximum box width to standardize box widths
            };
            //if ((i+1) == correctAns){
            //	$thisClone.addClass('correct');
            //};
         };


    $('.mcAnsBtn').each(function(){
        $(this).width(minWidth); //standardizes box widths
    });

    $('#mcContainer').randomize('a'); //randomize answer boxes

    var error = function() {
        console.log("error");
    };
};

// request contains all the information required to make POST calls

var request = function() {

    var url = new API();//get access to API addresses

    //Generic POST function

    this.postData = function(onSuccess, outgoingData, url) {
		$.ajax({
		  type: "POST",
		  url: url,
		  data: JSON.stringify(outgoingData, null, '\t'),
		  contentType: 'application/json;charset=UTF-8',
		  success: onSuccess,
		  dataType: 'json'
		});
    };

    this.requestData = function(onSuccess, url) {
		$.ajax({
		  type: "POST",
		  url: url,
		  contentType: 'application/json;charset=UTF-8',
		  success: onSuccess,
		  dataType: 'json'
		});
    };

    this.getRNDMC = function(){
        this.requestData(parseMCQuestion, url.getRNDMC)
    }

    this.getRNDFR = function(){
        this.requestData(parseMCQuestion, url.getRNDFR)
    }

    this.getRNDDEF = function(){
        this.requestData(parseMCQuestion, url.getRNDDEF)
    }

    this.getMCQuestion = function(questID) {
        this.postData(parseMCQuestion, questID, url.getMC);
    }; //gets a multiple choice question with ID questID

    this.getWORD = function(questID) {
        this.postData
    }; //gets a word from database with ID questID

    this.getDefinition = function(questID) {

    }; //gets a definition with ID questID

    this.getFreeResponse = function(questID) {

    }; //gets a free response question with ID questID

    this.validateAns = function(validation) {
        this.postData()
    }; //checks whether an answer to a question is correct or not; validation should be an object that contains question ID, chosen answer, user data (points, time, username etc)
};

//store the API addresses in this
var API = function(){
    var hostroot = 'http://exbookapp.org:5000/'

    this.getRNDMC = hostroot + 'get/random/MC';
    this.getRNDFR = hostroot + 'get/random/FR';
    this.getRNDDEF = hostroot + 'get/random/DEF';

    this.getMC = hostroot + 'get/MC';
    this.getWORD = hostroot + 'get/WORD';
    this.getDEF = hostroot + 'get/DEF';
    this.getFR = hostroot + 'get/FR';

    this.sendANS = hostroot + '';
}