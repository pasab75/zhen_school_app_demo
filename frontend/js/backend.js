
var local = true; //determines whether you are testing locally or you are on the VPS

var hostname = ''; //which server you are routing to
var port = '5000'; //port that server is listening on

if (local == true){
    hostname = 'http://127.0.0.1'
}

else
    hostname = 'http://exbookapp.org'

hostroot = hostname + ':' + port + '/'

urlgetdef = hostroot + 'get/defquestion/topic';
urlgetrand = hostroot + 'get/question/random';
urlsendANS = hostroot + 'validate/question';



// This is POST object that contains all the various types of POSTS we will do


    parseMCQuestion = function(data) { //this is the on success function for parsing a multiple choice question
        $('#questionText').text(data.question_text); //adds question text to page

        var $aProto = $('#a_proto'); //creates prototype question box

        //var correctAns = data.answer_index;

        var minWidth = 200; //this is the minimum width of an answer button to be displayed

        for (var i = 0; i < data.answers.length; i++) {
            var $thisClone = $aProto.clone() //clones a prototype question box
                .text(data.answers[i]) //inserts answer text into question boxes
                .appendTo($('#mcContainer')) //puts question boxes in the correct container
                .attr('data-index', i) //adds class identifiers to each question box
                .attr('data-qID', data.questionID) //adds question identifier to each question box
                .hide()
                .fadeIn('slow') //shows the question box
                .removeClass('hidden');

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

    var clearOldQuestion = function(){
        $("#mcContainer").empty();
        $('#questionText').text(''); //adds question text to page
    };

    // request contains all the information required to make POST calls

    checkValid = function(data){
        console.log(data);
        if (data.validation == 'true'){
            console.log('you are correct');
            clearOldQuestion();
            //POST.getrandmc();
            POST.getranddef();
            //$('[data-remodal-id=modal]').remodal().open();

        };
        if (data.validation == 'false'){
            console.log('you are not correct');
            clearOldQuestion();
            //POST.getrandmc();
            POST.getranddef();
        };
    }

var request = function() {

/* success functions to pass POST object */


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

    this.getranddef = function(){
        var qtype = {'question_type' : '0', 'topic': 'topic index 1' };
        this.postData(parseMCQuestion, qtype ,urlgetdef);
    }

    this.getrandmc = function(){
        var qtype = {'question_type' : '1'};
        this.postData(parseMCQuestion, qtype ,urlgetrand);
    };

    this.getrandfr = function(){
        var qtype = {'question_type' : '2'};
        this.postData(parseMCQuestion, qtype ,urlgetrand);
    };

    this.validateAns = function(validation) {
        this.postData(checkValid, validation, urlsendANS );
    }; //checks whether an answer to a question is correct or not; validation should be an object that contains question ID, chosen answer, user data (points, time, username etc)

    this.addQuestions = function() {
        var nothing = {'nothing' : '0'};
        this.postData(console.log('added questions successfully'), nothing, 'http://127.0.0.1:5000/add/dummy/questions' );
    };

    this.debug = function(url){
        var nothing = {'nothing' : '0'};
        this.postData(console.log('successful post at ' + url), nothing, url);
    };

};