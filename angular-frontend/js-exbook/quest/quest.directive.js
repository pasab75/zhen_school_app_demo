(function() {
    'use strict';

    angular
        .module('exBook')
        .directive('exQuestSelect', exQuestSelect);

    /* @ngInject */
    function exQuestSelect() {
        var directive = {
            restrict: 'EA',
            templateUrl: 'js-exbook/quest/quest.template.html',
            scope: {
            },
            controller: QuestController,
            controllerAs: 'questCtrl',
            bindToController: true
        };

        return directive;

    }

    QuestController.$inject = ['questservice'];

    /* @ngInject */
    function QuestController(questservice) {
        var vm = this;
        
        activate();

        function activate() {
          vm.data = questservice;
        }
    }
})();
