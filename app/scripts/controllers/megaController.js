/**
 * Created by felipe on 28/07/16.
 */

(function () {
    'use strict';

    function megaController($scope) {
        var megaCtrl = this;
        megaCtrl.nodos = [];
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
            if (data.cmd === 'isLogged'){
                if (data.status === false){
                    window.location.href = '#mega/login';
                } else{
                    var cmd = {
                        cmd: 'listaNodos'
                    };
                    mysocket.send(JSON.stringify(cmd));
                }
            } if (data.cmd === 'listaNodos'){

                megaCtrl.nodos = data.nodos;
                //megaCtrl.nodos = [{nombre: 'primero'}];
                $scope.$apply();
            }
        };

        mysocket.onclose = function (evt) {
            //alert("Websocket cerrado");
        };

        mysocket.onerror = function (evt) {
            //alert("ERROR: " + evt.data);
        }

        megaCtrl.enviar = function () {

            var data = {
                cmd: 'login',
                email: megaCtrl.email,
                contrasenna: megaCtrl.contrasenna
            };
            mysocket.send(JSON.stringify(data));

        }
    }

    angular
        .module('RPIWebAdmin.controllers')
        .controller('megaController', megaController);
})();
