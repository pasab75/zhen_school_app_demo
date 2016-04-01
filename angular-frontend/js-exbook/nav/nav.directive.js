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

  NavController.$inject = ['loginservice', 'debug'];

  function NavController(loginservice, debug) {
    var vm = this;

    activate();

    function activate(){
      vm.isCollapsed = true;
      vm.login = loginservice;
      vm.debug = debug;
    };

    // activate();
    //
    // function activate(){
    //   vm.isCollapsed = true;
    // };

  };

})();
