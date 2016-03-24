
(function(){
  var app = angular.module('exBook', ['ui.bootstrap', 'satellizer']);

    app.config(function($authProvider){
      $authProvider.google({
        clientId: '334346238965-oliggj0124b9r4nhbdf4nuboiiha7ov3.apps.googleusercontent.com',
        responseType: 'token',
        url: '/zhen_school_app_demo/angular-frontend/index.html',
        authorizationEndpoint: 'https://accounts.google.com/o/oauth2/auth',
        scope: ['profile', 'email'],
        scopePrefix: 'openid',
        scopeDelimiter: ' ',
        display: 'popup',
        type: '2.0',
        popupOptions: { width: 452, height: 633}
      });
    });

    app.controller('debug-controller', function($scope, $auth, apiCall, urlList){
      $scope.status = "I haven't done anything yet";
      $scope.statusCount = 0;
      $scope.string_to_send = JSON.stringify({'user_identifier':$auth.getToken() ,'user_id':'12345'})
      $scope.barf = "nothing to barf yet";

      $scope.doSomething = function(){
        apiCall.debug(urlList.makeUrl('get/next/prompt/by/student'), $scope.string_to_send, function(data){
          $scope.status = 'I did something ' + data.data.response_type;
          $scope.barf = data.data;}, function(data){
            $scope.status = 'I failed ' +  data['response_type'];
            $scope.barf = data.data;});
      };

      $scope.initializeDatabase = function(){
        apiCall.debug(urlList.makeUrl('database/initialize'), 'DO IT NOW', function(data){
          $scope.status = 'I did something ' + data.data.response_type;
          $scope.barf = data.data;}, function(data){
            $scope.status = 'I failed ' +  data['response_type'];
            $scope.barf = data.data;});
      };

      $scope.getQuestion = function(){
        apiCall.debug(urlList.makeUrl('get/question/definition/by/topic'), JSON.stringify({'user_identifier': $auth.getToken(),'topic':'3'}),
          function(data){
            $scope.barf = data.data;
            $scope.status = 'I succeeded';
          },
          function(data){
            $scope.status = 'I failed ';
          }
        );
      };

      $scope.getDailies = function(){
        apiCall.debug(urlList.makeUrl('get/quests/daily'), JSON.stringify({'user_identifier': $auth.getToken(),'topic':'3'}),
          function(data){
            $scope.barf = data.data;
            $scope.status = 'I succeeded';
          },
          function(data){
            $scope.status = 'I failed ';
          }
        );
      };

      $scope.getQuestQuestion = function(){
        apiCall.debug(urlList.makeUrl('get/question/by/quest'), JSON.stringify({'user_identifier': $auth.getToken(),'quest_index':'3'}),
          function(data){
            $scope.barf = data.data;
            $scope.status = 'I succeeded';
          },
          function(data){
            $scope.status = 'I failed ';
          }
        );
      };

      $scope.getValidation = function(){
        apiCall.debug(urlList.makeUrl('get/validation/'), JSON.stringify({'user_identifier': $auth.getToken(),'user_answer':'3'}),
          function(data){
            $scope.barf = data.data;
            $scope.status = 'I succeeded';
          },
          function(data){
            $scope.status = 'I failed ';
          }
        );
      };

      $scope.getUser = function(){
        apiCall.debug(urlList.makeUrl('get/user'), JSON.stringify({'user_identifier': $auth.getToken()}),
          function(data){
            $scope.barf = data.data;
            $scope.status = 'I succeeded';
          },
          function(data){
            $scope.status = 'I failed ';
          }
        );
      };

      $scope.startQuest = function(){
        apiCall.debug(urlList.makeUrl('start/quest'), JSON.stringify({'user_identifier': $auth.getToken(), 'quest_index': '46'}),
          function(data){
            $scope.barf = data.data;
            $scope.status = 'I succeeded';
          },
          function(data){
            $scope.status = 'I failed ';
          }
        );
      };

      $scope.resumeQuest = function(){
        apiCall.debug(urlList.makeUrl('get/user'), JSON.stringify({'user_identifier': $auth.getToken()}),
          function(data){
            $scope.barf = data.data;
            $scope.status = 'I succeeded';
          },
          function(data){
            $scope.status = 'I failed ';
          }
        );
      };

      $scope.createAccount = function(){
        apiCall.debug(urlList.makeUrl('create/account'), JSON.stringify({'user_identifier': $auth.getToken()}),
          function(data){
            $scope.barf = data.data;
            $scope.status = 'I succeeded';
          },
          function(data){
            $scope.status = 'I failed ';
          }
        );
      };

      $scope.clearQuestions = function(){

      };

      $scope.successFunction = function(data){
        $scope.status = 'I did something ' + data;
        $scope.statusCount ++;
      };

      $scope.failureFunction = function(data){
        $scope.status = 'I failed ' + data;
        $scope.statusCount = 0;
      };
    });//end of controller

    app.controller('NavController', function ($scope, $location, $auth, login) {
        $scope.isCollapsed = true;

        $scope.loggedIn = function(){
          return login.getLoginStatus();
        }

        $scope.logOut = function(){
          $auth.logout();
          login.setLoginStatus(false);
        };

        $scope.$on('$routeChangeSuccess', function () {
            $scope.isCollapsed = true;
        });

        $scope.getClass = function (path) {
          if(path === '/') {
              if($location.path() === '/') {
                  return "active";
              } else {
                  return "";
              }
          }

          if ($location.path().substr(0, path.length) === path) {
              return "active";
          } else {
              return "";
          }
      }
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

    app.controller('activity-controller', function($scope, login){
      var activities = [
        {
          title: 'This is activity number 1',
          number_questions: '30',
          number_points: '400',
          topics:[
            'topic 1',
            'topic 2',
            'topic 3'
          ]
        },
        {
          title: 'This is activity number 2',
          number_questions: '30',
          number_points: '400',
          topics:[
            'topic 1',
            'topic 2',
            'topic 3'
          ]
        },
        {
          title: 'This is activity number 3',
          number_questions: '30',
          number_points: '400',
          topics:[
            'topic 1',
            'topic 2',
            'topic 3'
          ]
        },
        {
          title: 'This is activity number 4',
          number_questions: '30',
          number_points: '400',
          topics:[
            'topic 1',
            'topic 2',
            'topic 3'
          ]
        },
      ];

      $scope.activities = activities;

      $scope.loggedIn = function(){
        return login.getLoginStatus();
      }

      $scope.getQuestion = function(){

      }

    });//end of activity-controller

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


      $scope.question = question;

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
      var clicked = [0,0,0,0,0,0];
      $scope.clicked = clicked;
      $scope.user_answer = "";

      $scope.clickCount = function(index){
        return $scope.clicked[index];
      }

      $scope.addClick = function(index){
        $scope.clicked[index]++;
        for (i=0; i<$scope.clicked.length;i++){
          if (i != index ){
            $scope.clicked[i] = 0;
          };
        };
      };

      $scope.clickedNone = function(index){
        return clicked[index] === 0;
      }

      $scope.clickedOnce = function(index){
        return clicked[index] === 1;
      }

      $scope.clickedTwice = function(index){
        return clicked[index] >= 2;
      }

    });

    app.factory('login', function($auth, $http, $q){
      var login = {};
      var _loggedIn = false;

      var makeUrl = function(){
        _hostname = '';
        _port = '';
        _version = '';
        _finalUrl = _hostname+_port+_version+'/googlesignin'
        return _finalUrl;
      };

      login.getLoginStatus = function(){
        return _loggedIn;
      };

      login.setLoginStatus = function(bool){
        _loggedIn = bool;
      };

        return login;
    });//end of service

    app.factory('urlList', function(){
      var urlList = {
        protocol: 'http://',
        hostroot: 'localhost:',
        port: '5000/',
        prefix: 'api/',
        version: 'v1/',
        route: ''
      };

      urlList.studentLogin = function(){
        urlList.makeUrl('tokensignin');
      };

      urlList.studentDailyActivities = function(){
        urlList.makeUrl('get/daily/activities');
      };

      urlList.studentNext = function(){
        urlList.makeUrl('get/next/prompt/by/student');
      };

      urlList.makeUrl = function(route){
        return urlList.protocol + urlList.hostroot + urlList.port + urlList.prefix + urlList.version + route;
      };

      return urlList;

    });//end of service

    app.factory('answer', function(){
      var answer = {};
      var _clicked;

      answer.getClickedIndex = function(){
        return _clicked;
      };

      answer.setClickedIndex = function(index){
        _clicked = index;
      };

      answer.checkSend = function(index){
        if (_clicked === index){
        }
      };

      return answer;

    });

    app.factory('apiCall', function($auth, $http, $q, urlList){
      var apiCall = {};

      apiCall.makeQuestionObject = function(){
        console.log('I should make a question object.');
      };

      apiCall.makeActivityObject = function(){
        console.log('I should make an activity object.');
      };

      apiCall.makeMenuListObject = function(){
        console.log('I should make a men list object, whatever that means.')
      };

      apiCall.makeModalObject = function(){
        console.log('I should make a modal object.')
      }

      apiCall.decodeServerResponseType = function(data){
        switch (data.response_type) {
          case '0':
            service.makeActivityObject(data);
            break;
          case '1':
            service.makeQuestionObject(data);
            break;
          case '2':
            service.makeModalObject(data);
            break;
          default:
            console.log('Something went wrong while processing server response.');
        }
      };

      apiCall.getActivity = function(){

      };

      apiCall.getQuestion = function(){

      };

      apiCall.sendPayload = function(url, payload, success, error){
        return $http.post(url, payload).then(success, failure);
      };

      apiCall.backendLogIn = function(urlList, $auth){
        return $http.post(urlList.studentLogin(), $auth.getToken()).then();
      };

      apiCall.debug = function(url, payload, success, failure){
        return $http.post(url, payload).then(success, failure);
      };

      return apiCall;
    });//end of service

    app.factory('clientModel', function($window){
      var clientModel = {};

      clientModel.setLocalModel = function(activity_index, number_of_questions, current_question){
          $window.localStorage.model = {'activity_index':activity_index, 'number_of_questions':number_of_questions, 'current_question':current_question};
      };

      clientModel.getLocalModel = function(){
        return $window.localStorage.model;
      };

      clientModel.getServerModel = function(){
        //get user activity information from server
      };

      return clientModel;
    });//end of service

})();// end of wrapper
