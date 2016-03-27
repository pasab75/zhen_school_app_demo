
(function(){
  var app = angular.module('exBook', ['services', 'ui.bootstrap', 'satellizer']);

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

    app.controller('debug-controller', function($scope, $auth, apiCall, urlList, ViewState){
      $scope.status = "I haven't done anything yet";
      $scope.statusCount = 0;
      $scope.string_to_send = JSON.stringify({'user_identifier':$auth.getToken() ,'user_id':'12345'})
      $scope.barf = "nothing to barf yet";
      $scope.topic = '';
      $scope.quest = '';
      $scope.answer = '';

      $scope.exists = ViewState.data;

      $scope.displayQuestionType = function(index){
        ViewState.displayQuestionType(index);
      };

      $scope.displayQuestSelect = function(){
        ViewState.displayQuestSelect();
      };

      $scope.initializeDatabase = function(){
        apiCall.debug(urlList.makeUrl('database/initialize'), 'DO IT NOW', function(data){
          $scope.status = 'I did something ' + data.data.response_type;
          $scope.barf = data.data;}, function(data){
            $scope.status = 'I failed ' +  data['response_type'];
            $scope.barf = data.data;});
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


    });//end of controller

    app.controller('NavController', function ($scope, $location, $auth, ViewState) {
        $scope.isCollapsed = true;

        $scope.exists = ViewState.data;

        $scope.logOut = function(){
          $auth.logout();
          ViewState.setLoggedOut();
        };

        // $scope.$on('$routeChangeSuccess', function () {
        //     $scope.isCollapsed = true;
        // });

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

    app.controller('login-controller', function($scope, $auth, $log, ViewState, apiCall){

      $auth.setStorageType('sessionStorage');
      $scope.data = {};

      $scope.exists = ViewState.data;

      $scope.authenticate = function(provider){
        $auth.authenticate(provider)
          .then(function(response){
            console.log(response)
            console.log(response.access_token);
            $auth.setToken(response.access_token);
            $log.log('finished setting access token')
            ViewState.setLoggedIn();
            ViewState.displayQuestSelect();
            apiCall.getDailies();
            $log.log('finished getting dailies')
          })
          .catch(function(response) {
            console.log('something went wrong');
          });
      };

      $scope.logOut = function(){
        $auth.logout();
        ViewState.setLoggedOut()
      };

    });//end of controller

    app.controller('activity-controller', function($scope, ViewState){
      var activities = [
        {
          title: 'This is activity number 1',
          number_questions: '30',
          number_points: '400',
          topics:[
            'topic 1'
          ]
        },
        {
          title: 'This is activity number 2',
          number_questions: '30',
          number_points: '400',
          topics:[
            'topic 1'
          ]
        },
        {
          title: 'This is activity number 3',
          number_questions: '30',
          number_points: '400',
          topics:[
            'topic 1'
          ]
        },
        {
          title: 'This is activity number 4',
          number_questions: '30',
          number_points: '400',
          topics:[
            'topic 1'
          ]
        },
      ];

      $scope.exists = ViewState.data;

      $scope.viewAccess = ViewState.data;

      $scope.getQuestion = function(){
        ViewState.displayQuestionType(0);
      }

    });//end of activity-controller

    app.controller('question-controller', function($scope, ViewState){
      var question1 = {
          question_text: 'This is question number 1',
          answers:[
                    'Q1 This is answer number 1',
                    'Q1 This is answer number 2',
                    'Q1 This is answer number 3',
                    'Q1 This is answer number 4',
                    'Q1 This is answer number 5',
                    'Q1 This is answer number 6'
                  ]
        }

      var question2 = {
          question_text: 'This is question number 2',
          answers:[
                    'Q2 This is answer number 1',
                    'Q2 This is answer number 2',
                    'Q2 This is answer number 3',
                    'Q2 This is answer number 4',
                    'Q2 This is answer number 5',
                    'Q2 This is answer number 6'
                  ]
        }

        var question0 = {
            question_text: '',
            answers:[
                    ]
          }

      var question = question1;

      $scope.exists = ViewState.data;

      $scope.question = question1;

      $scope.changeQuestion = function(){
        if($scope.question == question0){
          $scope.question = question1;
        }
        else if($scope.question == question1){
          $scope.question = question2;
        }
        else{
          $scope.question = question0;
        }
      };

    });//end of controller

    app.controller('answer-controller', function($scope, $log){
      $scope.clickArray = [0,0,0,0,0,0];
      var clickable = true;

      $scope.clickUpdate = function(index){
        if (clickable){
          for (i = 0; i < 6; i++){
            if (i == index){
              $scope.clickArray[i]++;
            }
            else{
              $scope.clickArray[i] = 0;
            }
          }
          if ($scope.clickArray[index] >= 2){
            $log.log('sending api call');
            clickable = false;
          }
        };
      };
    });

})();// end of wrapper
