(function() {
    'use strict';

    angular
        .module('exBook')
        .controller('ViewController', ViewController);

    ViewController.$inject = ['viewservice'];

    /* @ngInject */
    function ViewController(viewservice) {
        var vm = this;

        vm.view = viewservice;

        activate();

        function activate() {

        }
    }
})();
