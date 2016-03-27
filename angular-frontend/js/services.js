(function(){

  var services = angular.module('services',[]);

    services.factory('ViewState', function($log){
      var ViewState = {};

      ViewState.data = {
                        views: {
                          'loggedOut': true,
                          'sectionSelect': false,
                          'questSelect': false,
                          'question_type': [
                            false,
                            false,
                            false
                          ],
                          'debug': true,

                          quests:[

                          ],

                          questions:[

                          ]
                        }
                      }

      ViewState.setLoggedIn = function(){
        ViewState.data.views.loggedOut = false;
      }

      ViewState.setLoggedOut = function(){
        ViewState.data.views.loggedOut = true;
        ViewState.data.views.sectionSelect = false;
        ViewState.data.views.questSelect = false;
        for (i = 0; i < 3; i++){
          ViewState.data.views.question_type[i] = false;
        }
      }

      ViewState.displaySectionSelect = function(){
        ViewState.data.views.login_page = false;
        ViewState.data.views.sectionSelect = true;
        ViewState.data.views.questSelect = false;
        for (i = 0; i < 3; i++){
          ViewState.data.views.question_type[i] = false;
        }
      };

      ViewState.displayQuestSelect = function(){
        ViewState.data.views.login_page = false;
        ViewState.data.views.sectionSelect = false;
        ViewState.data.views.questSelect = true;
        for (i = 0; i < 3; i++){
          ViewState.data.views.question_type[i] = false;
        }
      };

      ViewState.displayQuestionType = function(index){
        ViewState.data.views.login_page = false;
        ViewState.data.views.sectionSelect = false;
        ViewState.data.views.questSelect = false;
        for (i = 0; i < 3; i++){
          if (i == index){
            ViewState.data.views.question_type[i] = true;
          }
          else{
            ViewState.data.views.question_type[i] = false;
          }
        }
      };

      ViewState.setQuestions = function(questions){
        ViewState.data.views.questions = questions;
        $log.log(ViewState.data.views.questions);
      }

      ViewState.setQuests = function(quests){
        ViewState.data.views.quests = quests;
        $log.log(ViewState.data.views.quests);
      }

      return ViewState;
    });//end of service

    services.factory('urlList', function(){
      var urlList = {
        protocol: 'http://',
        hostroot: 'localhost:',
        port: '5000/',
        prefix: 'api/',
        version: 'v1/',
        route: ''
      };


      urlList.makeUrl = function(route){
        return urlList.protocol + urlList.hostroot + urlList.port + urlList.prefix + urlList.version + route;
      };

      urlList.studentLogin = function(){
        return urlList.makeUrl('paidsignin');
      }

      urlList.getDailies = function(){
        return urlList.makeUrl('get/quests/daily');
      }

      return urlList;

    });//end of service

    services.factory('apiCall', function($auth, $http, $q, urlList, ViewState, $log){
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

      apiCall.sendPayload = function(url, payload, success, error){
        return $http.post(url, payload).then(success, failure);
      };

      apiCall.backendLogIn = function(){
        return $http.post(urlList.studentLogin(), {'user_identifier': $auth.getToken()}).then(
          function(){
          },
          function(){
            $log.log('failure to log in to backend')
          }
        );
      };

      apiCall.debug = function(url, payload, success, failure){
        return $http.post(url, payload).then(success, failure);
      };

      apiCall.getDailies = function(){
        apiCall.debug(urlList.makeUrl('get/quests/daily'), JSON.stringify({'user_identifier': $auth.getToken(),'topic': 3}),
          function(data){
            ViewState.setQuests(data.data);
            $log.log(data.data[0])
          },
          function(data){
            $log.log('I failed');
          }
        );
      };

      //
      // $scope.startQuest = function(){
      //   apiCall.debug(urlList.makeUrl('start/quest'), JSON.stringify({'user_identifier': $auth.getToken(), 'quest_index': $scope.quest}),
      //     function(data){
      //       $scope.barf = data.data;
      //       $scope.status = 'I succeeded';
      //     },
      //     function(data){
      //       $scope.status = 'I failed ';
      //     }
      //   );
      // };
      //
      // $scope.resumeQuest = function(){
      //   apiCall.debug(urlList.makeUrl('resume/quest'), JSON.stringify({'user_identifier': $auth.getToken()}),
      //     function(data){
      //       $scope.barf = data.data;
      //       $scope.status = 'I succeeded';
      //     },
      //     function(data){
      //       $scope.status = 'I failed ';
      //     }
      //   );
      // };
      //
      // $scope.stopQuest = function(){
      //   apiCall.debug(urlList.makeUrl('stop/quest'), JSON.stringify({'user_identifier': $auth.getToken()}),
      //     function(data){
      //       $scope.barf = data.data;
      //       $scope.status = 'I succeeded';
      //     },
      //     function(data){
      //       $scope.status = 'I failed ';
      //     }
      //   );
      // };
      //
      // $scope.getValidation = function(){
      //   apiCall.debug(urlList.makeUrl('get/validation'), JSON.stringify({'user_identifier': $auth.getToken(),'user_answer': $scope.answer}),
      //     function(data){
      //       $scope.barf = data.data;
      //       $scope.status = 'I succeeded';
      //     },
      //     function(data){
      //       $scope.status = 'I failed ';
      //     }
      //   );
      // };
      //
      // $scope.createAccount = function(){
      //   apiCall.debug(urlList.makeUrl('create/account'), JSON.stringify({'user_identifier': $auth.getToken()}),
      //     function(data){
      //       $scope.barf = data.data;
      //       $scope.status = 'I succeeded';
      //     },
      //     function(data){
      //       $scope.status = 'I failed ';
      //     }
      //   );
      // };

      return apiCall;
    });//end of service

    services.factory('clientModel', function($window){
      var clientModel = {};

      clientModel.setLocalModel = function(activity_index, number_of_questions, current_question){
          $window.localStorage.model = {activity_index:activity_index, number_of_questions:number_of_questions, current_question:current_question};
      };

      clientModel.getLocalModel = function(){
        return $window.localStorage.model;
      };

      clientModel.getServerModel = function(){
        //get user activity information from server
      };

      return clientModel;
    });//end of service
})();
