(function() {
    'use strict';

    angular
        .module('exBook')
        .service('questservice', questservice);

    questservice.$inject = ['httpwrapper'];

    /* @ngInject */
    function questservice(httpwrapper) {
      var vm = this;

      vm.quests = [
          {
            name: 'quest 1'
          },
          {
            name: 'quest 2'
          },
          {
            name: 'quest 3'
          }
      ]

      vm.getQuests = getQuests;
      vm.getQuestSuccess = getQuestSuccess;
      vm.getQuestError = getQuestError;

      function getQuests(){
        httpwrapper.genericApiCall('get/quests/daily', )
      };

      function getQuestSuccess(){

      };

      function getQuestError(){

      };

    }
})();
