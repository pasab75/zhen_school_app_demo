(function () {
  'use strict';
  angular
    .module('exBook')
    .config(config);

    function config($authProvider){
      $authProvider.google({
        clientId: '334346238965-oliggj0124b9r4nhbdf4nuboiiha7ov3.apps.googleusercontent.com',
        responseType: 'token',
        url: '/zhen_school_app_demo/angular-frontend/index.html',
        authorizationEndpoint: 'https://accounts.google.com/o/oauth2/auth',
        scope: ['https://www.googleapis.com/auth/plus.login', 'email'],
        scopePrefix: 'openid',
        scopeDelimiter: ' ',
        display: 'popup',
        type: '2.0',
        popupOptions: { width: 452, height: 633}
    });
  };
})();
