(function() {
    'use strict';

    angular
        .module('exBook')
        .service('debug', debug);

    debug.$inject = ['$auth', 'httpwrapper'];

    /* @ngInject */
    function debug($auth, httpwrapper) {
        var vm = this;

        vm.createAccount = createAccount;
        vm.submitQuestion = submitQuestion;
        vm.startQuest = startQuest;
        vm.resumeQuest = resumeQuest;
        vm.dropQuest = dropQuest;
        vm.getUser = getUser;

        function createAccount(){
          httpwrapper.genericApiCall('account/create', {user_identifier: $auth.getToken(), first_name: 'Zhen', last_name: 'Lu'}, success, failure);
        }

        function success(){
            return true;
        };

        function failure(){
            return false;
        };

        function getUser(){
            httpwrapper.genericApiCall('user/get', {user_identifier: $auth.getToken()}, getUserSuccess, getUserFailure);
        }

        function getUserSuccess(){
          // store the user information in local storage
          // display information like current level on the user's gui
            return true;
        };

        function getUserFailure(){
          // display an error message popup
            return false;
        };

        function startQuest(){
            httpwrapper.genericApiCall('quest/start', {user_identifier: $auth.getToken(),
                chapter_index: 5, number_of_questions: 10, cumulative: false, seconds_per_question: 0}, startQuestSuccess, startQuestFailure);
        }

        function startQuestSuccess(){
          // display a question
            return true;
        };

        function startQuestFailure(){
          // display an error message
            return false;
        };

        function submitQuestion(){
            httpwrapper.genericApiCall('question/submit', {user_identifier: $auth.getToken(), user_answer:0}, success, failure);
        }

        function submitQuestionSuccess(){
          // update the buttons on screen to reflect the correct answer
          // update user points level etc
          // 
            return true;
        };

        function submitQuestionFailure(){
            return false;
        };

        function submitQuestionSuccess(){
            return true;
        };

        function submitQuestionFailure(){
            return false;
        };

        function resumeQuest(){
            httpwrapper.genericApiCall('quest/resume', {user_identifier: $auth.getToken()}, success, failure);
        }

        function dropQuest(){
            httpwrapper.genericApiCall('quest/drop', {user_identifier: $auth.getToken()}, success, failure);
        }




    }
})();
