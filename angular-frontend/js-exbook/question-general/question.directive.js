(function() {
    'use strict';

    angular
        .module('exBook')
        .directive('exQuestion', exQuestion);

    /* @ngInject */
    function exQuestion() {
        var directive = {
            restrict: 'EA',
            templateUrl: 'js-exBook/question-general/question.template.html',
            scope: {
            },
            controller: QuestionController,
            controllerAs: 'questionCtrl',
            bindToController: true
        };

        return directive;
    }

    QuestionController.$inject = ['questionservice'];

    /* @ngInject */
    function QuestionController(questionservice) {
        var vm = this;

        activate();

        function activate() {
          vm.data = questionservice;
        }
    }
})();
