(function () {
    'use strict';

    angular.module('RPIWebAdmin', ['RPIWebAdmin.controllers','ngRoute','ngMaterial','ngMessages']);

    angular.module('RPIWebAdmin.controllers', ['RPIWebAdmin.services']);
    angular.module('RPIWebAdmin.controllers').constant('ServerUrl', 'ws://localhost:8888');
    //angular.module('RPIWebAdmin.controllers').var
    //angular.module('RPIWebAdmin.controllers', ['RPIWebAdmin.services', 'RPIWebAdmin.utils']);

    //angular.module('RPIWebAdmin.services', ['ngResource']);
    angular.module('RPIWebAdmin.services', []);

    //angular.module('RPIWebAdmin.services').constant('BaseUrl', 'http://localhost:8000');

    //angular.module('RPIWebAdmin.utils', []);


})();
