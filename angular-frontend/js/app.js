
(function(){
  var app = angular.module('exBook', ['ui.bootstrap', 'satellizer']);

    app.config(function($authProvider){
      $authProvider.google({
        clientId: '334346238965-oliggj0124b9r4nhbdf4nuboiiha7ov3.apps.googleusercontent.com',
        responseType: 'token',
        url: '/auth/google',
        authorizationEndpoint: 'https://accounts.google.com/o/oauth2/auth',
        redirectUri: window.location.origin,
        requiredUrlParams: ['scope'],
        optionalUrlParams: ['display'],
        scope: ['profile', 'email'],
        scopePrefix: 'openid',
        scopeDelimiter: ' ',
        display: 'popup',
        type: '2.0',
        popupOptions: { width: 452, height: 633}
      });
    });

    app.controller('login-controller', function($scope, $auth, $log, login){

      $auth.setStorageType('sessionStorage');
      $scope.data = {};

      $scope.loggedIn = function(){
        return login.getLoginStatus();
      }

      $scope.authenticate = function(provider){
        $auth.authenticate(provider)
          .then(function(response){
            console.log(response)
            console.log(response.access_token);
            $auth.setToken(response.access_token);
            login.setLoginStatus(true);
          })
          .catch(function(response) {
            console.log('something went wrong');
          });
      };

      $scope.logOut = function(){
        $auth.logout();
        login.setLoginStatus(false);
      };

    });//end of controller

    app.controller('question-controller', function($scope, login){

      var question = {
          question_text: 'This is question number 1',
          answer_1: 'This is answer number 1',
          answer_2: 'This is answer number 2',
          answer_3: 'This is answer number 3',
          answer_4: 'This is answer number 4',
          answer_5: 'This is answer number 5',
          answer_6: 'This is answer number 1',
        }


      this.question = question;


      $scope.loggedIn = function(){
        return login.getLoginStatus();
      };

      $scope.validateAnswer = function(){
        // do something
      };

      $scope.isCorrect = function(){

      };

      $scope.isIncorrect = function(){

      };
    });//end of controller

    app.controller('answer-controller', function($scope, $log, answer){
      var clicked = [0,0,0,0,0,0]

      $scope.isClicked = function(index){
        return answer.getClickedIndex() === index;
      };

      $scope.clickCount = function(index){
        return clicked[index]
      }

      $scope.addClick = function(index){
        clicked[index]++;
        for (i=0; i<clicked.length;i++){
          if (i != index ){
            clicked[index] = 0;
          };
        };
      };

      $scope.clickedOnce = function(index){
        return clicked[index] === 1;
      }

      $scope.clickedTwice = function(index){
        return clicked[index] === 2;
      }

    });

    app.factory('login', function($auth, $http, $q){
      var service = {};
      var _loggedIn = false;

      var makeUrl = function(){
        _hostname = '';
        _port = '';
        _version = '';
        _finalUrl = _hostname+_port+_version+'/googlesignin'
        return _finalUrl;
      };

      service.getLoginStatus = function(){
        return _loggedIn;
      };

      service.setLoginStatus = function(bool){
        _loggedIn = bool;
      };

      service.callBackend = function(){
        makeUrl();
        var deffered = $q.defer;
        $http({
          method: 'POST',
          url: _finalUrl
        }).success(function(data){
          deferred.resolve(data);
        }).error(function(){
          deferred.reject('There was an error')
        })
        return deferred.promise;
      };

        return service;
    });//end of service

    app.factory('answer', function(){
      var service = {};
      var _clicked;

      service.getClickedIndex = function(){
        return _clicked;
      };

      service.setClickedIndex = function(index){
        _clicked = index;
      };

      service.checkSend = function(index){
        if (_clicked === index){
        }
      };

      return service;

    });

    // app.factory('payLoad', function($auth, $http, $q){
    //   var service = {}
    //
    //   var makeUrl = function(url){
    //     _hostname = '';
    //     _port = '';
    //     _version = '';
    //     _finalUrl = _hostname+_port+_version+url
    //     return _finalUrl;
    //   };
    //
    //   var makePayload = function(contents){
    //     return payLoad;
    //   };
    //
    //   service.sendPayload = function(url, payload, function){
    //     makePayload(payload);
    //     var deffered = $q.defer;
    //     $http({
    //       method: 'POST',
    //       url: _finalUrl
    //     }).success(function(data){
    //       deferred.resolve(data);
    //     }).error(function(){
    //       deferred.reject('There was an error')
    //     })
    //     return deferred.promise;
    //   };
    // });//end of service

})();// end of wrapper
