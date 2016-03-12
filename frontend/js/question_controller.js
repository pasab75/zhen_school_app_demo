$(document).ready(function(){


    POST = new request();

    console.log(urlgetrand);

    console.log(hostroot);

    //POST.getMC(qID);

    addquestionsURL = hostname + ':5000/add/dummy/questions';


    POST.debug(addquestionsURL);
    //POST.getrandmc();
    POST.getranddef();

});
