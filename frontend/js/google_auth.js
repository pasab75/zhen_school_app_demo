function onSignIn(googleUser) {
    sessionStorage.setItem("id_token", googleUser.getAuthResponse().id_token);
    console.log(googleUser.getAuthResponse());
    var response_function = function(data){
        if (data.user_exists == 'true'){
            //clear_login();
            //$('.login-page').animateCss_out('fadeOutUp')
        }
        else{
            console.log('suck a dick')
            // redirect to buy page
        }
    };

    var authentication_payload = new Request('0','0','0','0');

    authentication_payload.send(tokensignin ,response_function)
};

function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();

    auth2.signOut().then(function () {
        console.log('User signed out.');
});
}