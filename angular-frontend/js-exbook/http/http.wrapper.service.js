(function() {
    'use strict';

    angular
        .module('exBook')
        .service('httpwrapper', httpwrapper);

    httpwrapper.$inject = ['$http'];

    /* @ngInject */
    function httpwrapper($http) {
      var vm = this;

      vm.hostroot = 'http://127.0.0.1';
      vm.portnumber = '5000';
      vm.apiversion = 'v1';

      vm.buildUrl = buildUrl;
      vm.genericApiCall = genericApiCall;

      function buildUrl(route) {
        return vm.hostroot + ":" + vm.portnumber + '/api/' + vm.apiversion + '/' + route;
      };

      function genericApiCall(route, data, success, error){
        $http.post(vm.buildUrl(route), data)
          .then(success, error);
      };

    }
})();
