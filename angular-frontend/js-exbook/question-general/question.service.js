(function() {
    'use strict';

    angular
        .module('exBook')
        .service('questionservice', questionservice);

    questionservice.$inject = ['$log', '$auth', 'httpwrapper'];

    /* @ngInject */
    function questionservice($log, $auth, httpwrapper) {
      var vm = this;

      vm.question = {
            question_text: 'This is question number 1',
            answers: [
              'answer 1',
              'answer 2',
              'answer 3',
              'answer 4',
              'answer 5',
              'answer 6'
            ]
        };

      vm.getQuestion = getQuestion;

      function getQuestion(){
        httpwrapper.genericApiCall('start/quest', {quest_index: 7225, user_identifier: $auth.getToken()}, success, failure);
      }

      function success(response){
        $log.log(response);
      };

      function failure(response){
        $log.log('Failed to get question')
      };

    }

})();
