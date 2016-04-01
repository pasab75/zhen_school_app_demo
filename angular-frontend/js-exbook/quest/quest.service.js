(function() {
    'use strict';

    angular
        .module('exBook')
        .service('questservice', questservice);

    questservice.$inject = ['$log', '$auth', 'httpwrapper'];

    /* @ngInject */
    function questservice($log, $auth, httpwrapper) {
      var vm = this;

      vm.quests = [];

      vm.getQuests = getQuests;

      function getQuests(){
        httpwrapper.genericApiCall('get/quests/daily', {user_identifier: $auth.getToken()}, success, failure);
      };

      function success(response){
        $log.log('Succeeded getting quests')
        $log.log(response)
        vm.quests = response.data;
      };

      function failure(response){
        $log.log('Failed getting quests')
      };

    }
})();
