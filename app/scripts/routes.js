/**
 * Created by felipe on 29/01/15.
 */

(function () {
  'use strict';
  function config($routeProvider) {
    $routeProvider
      .when('/', {
        redirectTo: '/home'

      })
      .when('/home', {
        templateUrl: 'views/home.tpl.html',
        controller: 'homeController',
        controllerAs: 'homeCtrl'
      })
      .when('/mega', {
        templateUrl: 'views/mega.tpl.html',
        controller: 'megaController',
        controllerAs: 'megaCtrl'
      })
      .when('/mega/login', {
        templateUrl: 'views/mega.login.tpl.html',
        controller: 'megaLoginController',
        controllerAs: 'megaLoginCtrl'
      })
      .when('/informacion', {
        templateUrl: 'views/informacion.tpl.html',
        controller: 'informacionController',
        controllerAs: 'informacionCtrl'
      });

  }

  angular.module('RPIWebAdmin').config(config);

})();
