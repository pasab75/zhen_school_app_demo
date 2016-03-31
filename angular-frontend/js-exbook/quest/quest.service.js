(function() {
    'use strict';

    angular
        .module('exBook')
        .service('questservice', questservice);

    /* @ngInject */
    function questservice() {
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

    }
})();
