/*
 * Main entry point to the Kyudo application
 */

var KyodoApp = (function(Backbone, $) {

  var View = Backbone.View.extend({

  });

  var hotkeys = function(e) {
    if (e.keyCode == 27) {
      e.preventDefault();
      window.location = "/admin/";
    }
  };

  return {
    init: function() {
      var view = new View();
      $(document).keyup(hotkeys);
      console.log("KyodoApp is started and ready");
    }
  }

})(Backbone, jQuery);

// On DOM Ready - initialize and execute the app.
$(function() {
  KyodoApp.init();
});
