(function() {
  'use strict';

  angular
    .module('exBook')
    .directive('exNavbar', exNavbar);

  /* @ngInject */
  function exNavbar() {
    var directive = {
      restrict: 'EA',
      templateUrl: 'js-exbook/nav/nav.template.html',
      controller: NavController,
      controllerAs: 'navCtrl',
      bindToController: true
    };

    return directive;

  };

  NavController.$inject = ['loginservice'];

  function NavController(loginservice) {
    var vm = this;

    activate();

    function activate(){
      vm.isCollapsed = true;
      vm.login = loginservice;
    };

    // activate();
    //
    // function activate(){
    //   vm.isCollapsed = true;
    // };

  };

})();
