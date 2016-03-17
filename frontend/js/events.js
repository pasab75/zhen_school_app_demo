// methods for displaying things on the frontend

// show login

var show_login = function(){

    var $top_overlay = '<div id="overlay" class="overlay-top"></div>'
    var $bot_overlay = '<div id="overlay" class="overlay-bottom"></div>'
    $top_overlay.appendTo('body')
    $bot_overlay.appendTo('body')
    var $login_box = '<div id="login" class="login_box center-block"></div>'
    var $login_text = '<h2 id="login" class="center-block login_text">Please log in with your GOOGLE account.</h2>'
    var $login_button = '<a id="login" class="center-block login_btn g-signin2" data-theme="light" data-onsuccess="onSignIn"></a>'
        $('.jumbotron').append($login_box)
        $('.login-box').append($login_text)
        $('#mcContainer').append($login_button)
};

var clear_login = function(){
    $('.overlay-top').animateCss_out('slideOutUp');
    $('.overlay-bottom').animateCss_out('slideOutDown');
    $('#login').remove();
};

var show_activity_choices = function(){
    var $activity_btn = '<div  id="activity" class="btn btn-primary">Push to get a question</div>'
        $('#mcContainer').append($activity_btn);
};

var clear_activity = function(){
    $('#activity').remove();
};

// show activity table

// show correct answers

// show a question
