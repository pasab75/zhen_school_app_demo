(function() {
  'use strict';

  angular
    .module('exBook')
    .directive('exLoginBox', exLoginBox);

  /* @ngInject */
  function exLoginBox() {
    var directive = {
      restrict: 'EA',
      templateUrl: 'js-exbook/login/login.template.html',
      controller: LoginController,
      controllerAs: 'loginCtrl',
      bindToController: true
    };

    return directive;

  };

  LoginController.$inject = ['$log', 'loginservice'];

  function LoginController($log, loginservice) {
    var vm = this;

    vm.loginserv = loginservice;
    vm.logIn = logIn;

    function logIn(){
      loginservice.googleLogin();
    };

  };

})();
