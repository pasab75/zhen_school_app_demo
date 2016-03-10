$(document).ready(function(){

    var POST = new request();

	var qID = {'id':'2'}; //question ID to get

    POST.getMCQuestion(qID);

});
