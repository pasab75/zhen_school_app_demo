(function() {
    'use strict';

    angular
        .module('exBook')
        .service('questionservice', questionservice);

    /* @ngInject */
    function questionservice() {
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
    }

})();
