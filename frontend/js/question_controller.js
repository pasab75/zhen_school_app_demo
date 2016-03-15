$(document).ready(function(){


    POST = new request();

    console.log(urlgetrand);

    console.log(hostroot);

    addquestionsURL = hostname + ':5000/api/v1/add/dummy/questions';

    // POST.debug(addquestionsURL);

    POST.getranddef();

});
