
var local = true; //determines whether you are testing locally or you are on the VPS

var hostname = ''; //which server you are routing to
var port = '5000'; //port that server is listening on

if (local == true){
    hostname = 'http://127.0.0.1'
}

else
    hostname = 'http://exbookapp.org'

hostroot = hostname + ':' + port + '/api/'

version = "v1/"

tokensignin = hostroot + version + 'tokensignin'
urlgetdef = hostroot + version + 'get/question/definition/by/topic';
urlgetrand = hostroot + version + 'get/question/random';
urlsendANS = hostroot + version + 'validate/question';

// This is POST object that contains all the various types of POSTS we will do


parseQuestion = function(data){
    // get the data

    // figure out what kind of data it is

    // display the data on the page
};

parseAnswer = function(data){
    // get server response

    // figure out what kind of response it is

    // display data on the page

};

endActivity = function(){
    // ends the current activity

    // pushes user back to a selection screen
}

askServer = function(){
    // not sure what to do, ask the server to give you something
}



parseMCQuestion = function(data) { //this is the on success function for parsing a multiple choice question
    $('#question_text').text(data.question_text)
    $('#question_text').animateCss_in('fadeIn')
    var minWidth = 200; //this is the minimum width of an answer button to be displayed

    for (var i = 0; i < data.answer_text.length; i++) {
        var $answer_button = '<div data-index="'+i+'" data-question_id="'+data.question_id+'" class="btn btn-primary clickable mcAnsBtn">'+data.answer_text[i]+'</div>'
        $('#mcContainer').append($answer_button)

         };

    $('#mcContainer').randomize('a'); //randomize answer boxes
    $('.mcAnsBtn').animateCss_in('flipInX')
    var error = function() {
        console.log("error");
    };
};

clearOldQuestion = function(){
    $('.mcAnsBtn').animateCss_out('flipOutX')
    $('#question_text').animateCss_in('fadeOut')
};

// request contains all the information required to make POST calls

checkValid = function(data){
    console.log(data);

    $('.mcAnsBtn').each(function(){
            $(this).removeClass("clickable")
            $(this).removeClass("activated")
    });

    if (data.validation == 'true'){
        console.log('you are correct');

        $('.mcAnsBtn').each(function(){
            if ($(this).attr("data-index") == data.answer_index){
                $(this).removeClass("btn-warning")
                $(this).addClass("btn-success")
            }
        });

        setTimeout(function(){
           clearOldQuestion();
        },1500);

        setTimeout(function(){
            POST.getranddef();
        },2000);


        //$('[data-remodal-id=modal]').remodal().open();
    };
    if (data.validation == 'false'){
        console.log('you are not correct');

        $('.mcAnsBtn').each(function(){
            if ($(this).attr("data-index") == data.answer_index){
                $(this).addClass("btn-success")
            }
            if ($(this).attr("data-index") == data.given_answer){
                $(this).addClass('btn-warning');
            }
        });
        setTimeout(function(){
           clearOldQuestion();
        },2000);

        setTimeout(function(){
            POST.getranddef();
        },2800);

    };
}

// payload to send to the server

make_payload = function(user_identifier, question_id, user_answer, activity_choice){
    var payload = {'question_id': question_id,
                   'user_answer': user_answer,
                   'user_identifier': user_identifier,
                   'activity_choice': activity_choice
                  };
    return payload
};

var request = function() {

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
        var user_id = sessionStorage.getItem("id_token")
        var qtype = {'user_identifier':user_id, 'question_type' : '0', 'topic': 'topic index 1' };
        this.postData(parseMCQuestion, qtype ,urlgetdef);
    }

    this.getrandmc = function(){
        var user_id = sessionStorage.getItem("id_token")
        var qtype = {'user_identifier':user_id, 'question_type' : '1'};
        this.postData(parseMCQuestion, qtype ,urlgetrand);
    };

    this.getrandfr = function(){
        var user_id = sessionStorage.getItem("id_token")
        var qtype = {'question_type' : '2'};
        this.postData(parseMCQuestion, qtype ,urlgetrand);
    };

    this.validateAns = function(validation) {
        var user_id = sessionStorage.getItem("id_token")
        this.postData(checkValid, validation, urlsendANS );
    };

};