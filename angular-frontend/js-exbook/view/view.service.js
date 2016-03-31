(function() {
    'use strict';

    angular
        .module('exBook')
        .service('viewservice', viewservice);

    /* @ngInject */
    function viewservice() {
      var vm = this;

      vm.login = true;
      vm.quest = true;
      vm.question = false;

      vm.questModal = false;
      vm.completeModal = false;
      vm.resumeModal = false;

      vm.toggleLogin = toggleLogin;
      vm.toggleQuest = toggleQuest;
      vm.toggleQuestion = toggleQuestion;

        function toggleLogin(){
          vm.login = !vm.login;
        }

        function toggleQuest(){
          vm.quest = !vm.quest;
        }

        function toggleQuestion(){
          vm.question = !vm.question;
        }

    }
})();
