
var local = true; //determines whether you are testing locally or you are on the VPS

var hostname = ''; //which server you are routing to
var port = '5000'; //port that server is listening on

if (local == true){
    hostname = 'http://127.0.0.1'
}

else
    hostname = 'http://exbookapp.org'

hostroot = hostname + ':' + port + '/api/';

version = "v1/";

tokensignin = hostroot + version + 'tokensignin'
urlgetdef = hostroot + version + 'get/question/definition/by/topic';
urlgetrand = hostroot + version + 'get/question/random';
urlsendANS = hostroot + version + 'validate/question';


// request object that both holds the data that we will send to the server
// and also has a function that posts its own content to the server as JSON
// server will receive the data as in the JSON field
var Request = function(question_id, user_answer, activity_choice, topic){
    this.request_content = JSON.stringify({'question_id': question_id,
                            'user_answer': user_answer,
                            'user_identifier': sessionStorage.getItem("id_token"),
                            'activity_choice': activity_choice,
                            'topic': topic
                           });

    this.send = function(url, success_function){
        console.log(this.request_content)
        $.ajax({
              type: "POST",
              contentType: "application/json; charset=utf-8",
              url: url,
              data: this.request_content,
              success: success_function,
              dataType: "json",
              contentType: "application/json, charset=utf-8"
        });
    };
};


parseQuestion = function(data){

    // gets raw data from server response
    // parses it into a question_information
    // calls a function to display it on the frontend

};

displayQuestion = function(question_information){

    // displays a question on the screen
    // takes question object

};

parseAnswer = function(data){

    // takes raw data from server response
    // figure out what kind of response it is
    // display changes on the frontend

};

endActivity = function(){
    // ends the current activity

    // pushes user back to a selection screen
}

askServer = function(){
    // not sure what to do, ask the server to give you something
}



parse_multiple_choice = function(data) { //this is the on success function for parsing a multiple choice question
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

parse_free_response = function(data) { //this is the on success function for parsing a multiple choice question
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
                $(this).animateCss_in('pulse')
            }
        });

        setTimeout(function(){
           clearOldQuestion();
        },1500);

        setTimeout(function(){
        var randomPayload = new Request('0', '0', '0', 'topic index 4');
        randomPayload.send(urlgetdef, parse_multiple_choice)
        },2000);

    };
    if (data.validation == 'false'){
        console.log('you are not correct');

        $('.mcAnsBtn').each(function(){
            if ($(this).attr("data-index") == data.answer_index){
                $(this).addClass("btn-success")
                $(this).animateCss_in('pulse')
            }
            if ($(this).attr("data-index") == data.given_answer){
                $(this).addClass('btn-danger');
            }
        });
        setTimeout(function(){
           clearOldQuestion();
        },2000);

        setTimeout(function(){
        var randomPayload = new Request('0', '0', '0', 'topic index 4');
        randomPayload.send(urlgetdef, parse_multiple_choice)
        },2800);

    };
}