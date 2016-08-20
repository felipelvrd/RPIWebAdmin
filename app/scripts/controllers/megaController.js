/**
 * Created by felipe on 28/07/16.
 */

(function () {
    'use strict';

    function megaController($scope, $mdDialog) {
        var megaCtrl = this;
        megaCtrl.salida = '';
        megaCtrl.nodos = [];
        var mysocket = new WebSocket('ws://localhost:8888/mega');
        megaCtrl.cargandoNodos = true;
        megaCtrl.isLoged = true;
        megaCtrl.email = '';
        megaCtrl.contrasenna = '';
        megaCtrl.inLogin = false;


        $scope.$on('$destroy', function onDestroy() {
            mysocket.close();
        });


        mysocket.onopen = function (evt) {

        };

        mysocket.onmessage = function (evt) {
            var data = JSON.parse(evt.data);

            switch (data.cmd) {

                case 'no_logueado':
                    megaCtrl.isLoged = false;
                    break;
                case 'listaNodos':

                    megaCtrl.nodos = data.nodos;
                    megaCtrl.path = data.path
                    megaCtrl.cargandoNodos = false;
                    //megaCtrl.nodos = [{nombre: 'primero'}];
                    $scope.$apply();
                    break;
                case 'downloadUpdate':
                    megaCtrl.descarga = data;
                    megaCtrl.descarga.porcentaje = megaCtrl.descarga.bytesTransferidos * 100 / megaCtrl.descarga.totalBytes;
                    $scope.$apply();
                    break;
                case 'login':
                    if (data.errorCode === 0) {
                        window.location.href = '#mega';
                    } else {
                        megaCtrl.inLogin = false;

                        $scope.$apply();
                        $mdDialog.show(
                            $mdDialog.alert()
                                .parent(angular.element(document.querySelector('#popupContainer')))
                                .clickOutsideToClose(true)
                                .title('Código de error: ' + data.errorCode)
                                .textContent('Ocurrio un error al intentar iniciar sesión, descripción del error: ' +
                                    data.errorString)
                                .ariaLabel('Error inicio de sesion')
                                .ok('OK')
                            //.targetEvent(evt)
                        );


                    }
                    break;
            }
        };

        megaCtrl.enviar = function () {
            megaCtrl.inLogin = true;
            var data = {
                cmd: 'login',
                email: megaCtrl.email,
                contrasenna: megaCtrl.contrasenna
            };
            mysocket.send(JSON.stringify(data));
        };

        mysocket.onclose = function (evt) {
            //alert("Websocket cerrado");
        };

        mysocket.onerror = function (evt) {
            //alert("ERROR: " + evt.data);
        }

        megaCtrl.clkNodo = function (nodo) {
            if (nodo.tipo === 'F') {
                var data = {
                    cmd: 'cd',
                    carpeta: nodo.nombre
                };
                mysocket.send(JSON.stringify(data));
            }
            else if (nodo.tipo === 'A') {
                var data = {
                    cmd: 'descargar',
                    nombre: nodo.nombre
                };
                mysocket.send(JSON.stringify(data));
            }
        }

    }

    angular
        .module('RPIWebAdmin.controllers')
        .controller('megaController', megaController);
})();
