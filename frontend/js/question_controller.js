$(document).ready(function(){


    POST = new request();

    //var qID = {'id':'2'}; //question ID to get
    console.log(urlgetrand);

    console.log(hostroot);

    //POST.getMC(qID);

    addquestionsURL = 'http://127.0.0.1:5000/add/dummy/questions';


    POST.debug(addquestionsURL);
    //POST.getrandmc();
    POST.getranddef();

});
