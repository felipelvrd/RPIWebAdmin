/**
 * Created by felipe on 28/07/16.
 */

(function () {
    'use strict';

    function megaController($scope, $mdDialog, ServerUrl) {
        var megaCtrl = this;
        megaCtrl.salida = '';
        megaCtrl.nodos = [];
        megaCtrl.cargandoNodos = true;
        megaCtrl.isLoged = true;
        megaCtrl.email = '';
        megaCtrl.contrasenna = '';
        megaCtrl.inLogin = false;

        var MegaServer = new WebSocket(ServerUrl + '/mega');

        function enviarServer(data) {
            MegaServer.send(JSON.stringify(data));
        }

        function noLogueado() {
            megaCtrl.isLoged = false;
        }

        function listarNodos(data) {
            megaCtrl.nodos = data.nodos;
            megaCtrl.path = data.path;
            megaCtrl.cargandoNodos = false;
        }

        function actualizarDescarga(data) {
            megaCtrl.descarga = data;
            megaCtrl.descarga.porcentaje = megaCtrl.descarga.bytesTransferidos * 100 / megaCtrl.descarga.totalBytes;
        }

        function cargarNodos() {
            var data = {
                cmd: 'recargarNodos'
            };
            enviarServer(data);
            megaCtrl.cargandoNodos = true;
        }

        function login(data) {
            if (data.errorCode === 0) {
                megaCtrl.isLoged = true;
                cargarNodos();
            } else {
                megaCtrl.inLogin = false;
                $mdDialog.show(
                    $mdDialog.alert()
                        .parent(angular.element(document.querySelector('#popupContainer')))
                        .clickOutsideToClose(true)
                        .title('Código de error: ' + data.errorCode)
                        .textContent('Ocurrio un error al intentar iniciar sesión, descripción del error: ' +
                            data.errorString)
                        .ariaLabel('Error inicio de sesión')
                        .ok('OK')
                );
            }
        }


        // Cuando se sale de la página se cierra el socket
        $scope.$on('$destroy', function onDestroy() {
            MegaServer.close();
        });


        /*MegaServer.onopen = function (evt) {

         };*/

        MegaServer.onmessage = function (evt) {
            var data = JSON.parse(evt.data);

            switch (data.cmd) {
                case 'noLogueado':
                    noLogueado();
                    break;
                case 'listaNodos':
                    listarNodos(data);
                    break;
                case 'downloadUpdate':
                    actualizarDescarga(data);
                    break;
                case 'login':
                    login(data);
                    break;
            }
            $scope.$apply();
        };


        megaCtrl.enviar = function () {
            megaCtrl.inLogin = true;
            var data = {
                cmd: 'login',
                email: megaCtrl.email,
                contrasenna: megaCtrl.contrasenna
            };
            MegaServer.send(JSON.stringify(data));
        };

        /*MegaServer.onclose = function (evt) {
            //alert("Websocket cerrado");
        };*/

        /*MegaServer.onerror = function (evt) {
            //alert("ERROR: " + evt.data);
        };*/

        megaCtrl.recargarNodos = function () {
            cargarNodos();
        };

        megaCtrl.clkNodo = function (nodo) {
            var data = {};
            if (nodo.tipo === 'F') {
                data = {
                    cmd: 'cd',
                    carpeta: nodo.nombre
                };
                MegaServer.send(JSON.stringify(data));
            }
            else if (nodo.tipo === 'A') {
                data = {
                    cmd: 'descargar',
                    nombre: nodo.nombre
                };
                MegaServer.send(JSON.stringify(data));
            }
        };
    }

    angular
        .module('RPIWebAdmin.controllers')
        .controller('megaController', megaController);
})();
