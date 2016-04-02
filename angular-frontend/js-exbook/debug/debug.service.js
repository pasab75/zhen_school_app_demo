(function() {
    'use strict';

    angular
        .module('exBook')
        .service('debug', debug);

    debug.$inject = ['$auth', 'httpwrapper'];

    /* @ngInject */
    function debug($auth, httpwrapper) {
        var vm = this;

        vm.initializeDatabase = initializeDatabase;
        vm.addUser = addUser;

        function initializeDatabase(){
          httpwrapper.genericApiCall('database/initialize', {user_identifier: $auth.getToken()}, success, failure);
        }

        function addUser(){
          httpwrapper.genericApiCall('create/account', {user_identifier: $auth.getToken()}, success, failure);
        }

        function success(){
          return true;
        };

        function failure(){
          return false;
        };
    }
})();
