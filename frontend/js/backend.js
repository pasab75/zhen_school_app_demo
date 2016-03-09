var backend = function() {
    this.getData = function(success,qID) {
		$.ajax({
		  type: "POST",
		  url: 'http://127.0.0.1:5000/get/question',
		  data: '{"id":"1"}',
		  success: success,
		  dataType: 'json'
		});
    };
};