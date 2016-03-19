$(document).ready(function(){

//    show_login();
    addquestionsURL = hostname + ':5000/api/v1/add/dummy/questions';

    if (sessionStorage.getItem("id_token") || localStorage.getItem("id_token")){
        var randomPayload = new Request('0', '0', '0', 'topic index 4');
        console.log(randomPayload)
        randomPayload.send(urlgetdef, parse_multiple_choice)
    }

    else{
        var $login_page =

        $('body').appendTO()
    }

    // POST.debug(addquestionsURL);

    // console.log(randomPayload)

    //randomPayload.send(urlgetdef, parse_multiple_choice)

});
