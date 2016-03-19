$(document).ready(function(){

//    show_login();
    addquestionsURL = hostname + ':5000/api/v1/add/dummy/questions';



    // POST.debug(addquestionsURL);
    var randomPayload = new Request('0', '0', '0', 'topic index 4');

    console.log(randomPayload)

    randomPayload.send(urlgetdef, parse_multiple_choice)

});
