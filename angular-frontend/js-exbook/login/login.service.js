(function() {
    'use strict';

    angular
        .module('exBook')
        .service('loginservice', loginservice);

    loginservice.$inject = ['$auth','$log', 'viewservice'];

    /* @ngInject */
    function loginservice($auth, $log, viewservice) {
      this.activetoken = false;
      this.storageType = 'sessionStorage';

      this.googleLogin = googleLogin;
      this.checkToken = checkToken;
      this.logOut = logOut;

      // makes sure that the JWT token is still valid
      function checkToken(){
        return $auth.isAuthenticated();
      };

      // first login function
      // this is what happens when the user clicks the google login button
      function googleLogin(){
        $auth.authenticate('google')
          .then(function(response){
            viewservice.toggleLogin();
            $log.log(response)
            $auth.setToken(response.access_token)
          })
          .catch(function(response){
            $log.log('something wrong has happened')
          });
      };

      function logOut(){
        viewservice.toggleLogin();
      }


    }
})();
