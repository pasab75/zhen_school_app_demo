function onSignIn(googleUser) {
    var id_token = googleUser.getAuthResponse().id_token;
//    var profile = googleUser.getBasicProfile();
//    console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
//    console.log('Name: ' + profile.getName());
//    console.log('Image URL: ' + profile.getImageUrl());
//    console.log('Email: ' + profile.getEmail());

    var response_function = function(data){
        if (data.user_exists == 'true'){
            clear_login();
        }
        else{
            console.log('suck a dick')
        }
    };

    var authentication_payload = make_payload(id_token, '0','0','0');

    $.post(tokensignin, authentication_payload, response_function);

    sessionStorage.setItem("id_token", id_token);
    localStorage.setItem("id_token", id_token);

    //console.log(sessionStorage.getItem('id_token'));

}

function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();

    auth2.signOut().then(function () {
        console.log('User signed out.');
});
}
