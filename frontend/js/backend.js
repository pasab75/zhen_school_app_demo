// This is a POST function that gets question by question ID
// Will most likely need to diversify this function to cover more cases

var postRequest = function() {
    this.getData = function(success,qID,url) {
		$.ajax({
		  type: "POST",
		  url: url,
		  data: JSON.stringify(qID, null, '\t'),
		  contentType: 'application/json;charset=UTF-8',
		  success: success,
		  dataType: 'json'
		});
    };
};