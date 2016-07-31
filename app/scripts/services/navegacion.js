/**
 * Created by felipe on 30/07/16.
 */

(function () {

    'use strict';

    function navegacion($q) {
      var paginas = [
        {
          titulo: 'Inicio',
          icono: 'res/ic_home_black_24px.svg',
          ruta: '#home'
        },
        {
          titulo: 'Mega',
          icono: 'res/mega-icon.svg',
          ruta: '#mega'
        },
        {
          titulo: 'Información',
          icono: '',
          ruta: '#informacion'
        }
      ];

      // Promise-based API
      return {
        loadAllPaginas: function () {
          // Simulate async nature of real remote calls
          return $q.when(paginas);
        }
      }
    }

    angular
        .module('RPIWebAdmin.services')
        .factory('navegacion', navegacion);
})();
