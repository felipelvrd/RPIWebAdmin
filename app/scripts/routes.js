/**
 * Created by felipe on 29/01/15.
 */

(function () {
    'use strict';
    function config($routeProvider) {
        $routeProvider

            .when('/', {
                templateUrl: 'views/home.tpl.html',
                controller: 'HomeController',
                controllerAs: 'HomeCtrl'
            })
            .when('/mega',{
                templateUrl: 'views/mega.tpl.html',
                controller: 'MegaController',
                controllerAs: 'MegaCtrl'
            })
            .when('/home', {
                templateUrl: 'views/home.tpl.html',
                controller: 'HomeController',
                controllerAs: 'HomeCtrl'
            });

    }

    angular.module('RPIWebAdmin').config(config);

})();
