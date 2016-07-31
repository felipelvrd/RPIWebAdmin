/**
 * Created by felipe on 30/07/16.
 */

(function () {
    'use strict';

    function navegacionController(navegacion, $mdSidenav) {
      var self = this;

      self.selected     = null;
      self.paginas        = [ ];
      self.selectPagina   = selectPagina;
      self.toggleList   = toggleUsersList;

      // Load all registered users

      navegacion
      .loadAllPaginas()
      .then( function( paginas ) {
        self.paginas    = [].concat(paginas);
        self.selected = paginas[0];
      });


      function toggleUsersList() {
      $mdSidenav('left').toggle();
    }

  /**
    * Select the current avatars
    * @param menuId
    */
     function selectPagina (pagina) {
       self.selected =  pagina;
        window.location.href = pagina.ruta;
     }
    }

    angular
        .module('RPIWebAdmin.controllers')
        .controller('navegacionController', navegacionController);
})();
