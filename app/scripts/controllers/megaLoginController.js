/**
 * Created by felipe on 30/07/16.
 */

(function () {
    'use strict';

    function megaLoginController($scope) {


        $scope.project = {
    description: 'Nuclear Missile Defense System',
    rate: 500
  };

        var megaLoginCtrl = this;
        megaLoginCtrl.inLogin = false;

        megaLoginCtrl.email = '';
        megaLoginCtrl.contrasenna = '';

        var mysocket = new WebSocket('ws://localhost:8888/mega');

        $scope.$on('$destroy', function onDestroy() {
            mysocket.close();
        });


        mysocket.onopen = function (evt) {
            var cmd = {
                cmd: 'isLogged'
            };
            mysocket.send(JSON.stringify(cmd));
        };

        mysocket.onmessage = function (evt) {
            var data = JSON.parse(evt.data);
            switch (data.cmd) {
                case 'isLogged':
                    if (data.status === true) {
                        window.location.href = '#mega';
                    }
                    break;

                case 'login':
                    if (data.errorCode === 0) {
                        window.location.href = '#mega';
                    } else {
                        megaLoginCtrl.inLogin = false;
                        $scope.$apply();
                        alert(evt.data);
                    }
                    break;
            }
        };

        mysocket.onclose = function (evt) {
            //alert("Websocket cerrado");
        };

        mysocket.onerror = function (evt) {
            //alert("ERROR: " + evt.data);
        };

        megaLoginCtrl.enviar = function () {
            megaLoginCtrl.inLogin = true;
            var data = {
                cmd: 'login',
                email: megaLoginCtrl.email,
                contrasenna: megaLoginCtrl.contrasenna
            };
            mysocket.send(JSON.stringify(data));
        };
    }

    angular
        .module('RPIWebAdmin.controllers')
        .controller('megaLoginController', megaLoginController);
})();
