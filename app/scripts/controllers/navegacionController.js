/**
 * Created by felipe on 30/07/16.
 */

(function () {
    'use strict';

    function navegacionController(navegacion, $mdSidenav) {

        var navegacionCtrl = this;

        navegacionCtrl.selected = null;
        navegacionCtrl.paginas = [];


        navegacion
            .loadAllPaginas()
            .then(function (paginas) {
                navegacionCtrl.paginas = [].concat(paginas);
                navegacionCtrl.selected = paginas[0];
            });


        navegacionCtrl.toggleList = function () {
            $mdSidenav('left').toggle();
        };

        navegacionCtrl.selectPagina = function (pagina) {
            navegacionCtrl.selected = pagina;
            window.location.href = pagina.ruta;
        };

    }

    angular
        .module('RPIWebAdmin.controllers')
        .controller('navegacionController', navegacionController);
})();
