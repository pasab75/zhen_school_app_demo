(function() {
    'use strict';

    angular
        .module('exBook')
        .controller('ViewController', ViewController);

    ViewController.$inject = ['viewservice'];

    /* @ngInject */
    function ViewController(viewservice) {
        var vm = this;

        activate();

        function activate() {
          vm.view = viewservice;
        }
    }
})();
