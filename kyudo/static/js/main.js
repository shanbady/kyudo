/*
 * Main entry point to the Kyudo application
 */

var KyodoApp = (function(Backbone, $) {

  var Question = Backbone.Model.extend({
    defaults: {
      text: null
    }
  });

  var QuestionCollection = Backbone.Collection.extend({
    url: "/api/questions/",
    model: Question,
  });

  var QuestionView = Backbone.View.extend({
    tagName: "li",
    template: _.template($('#question-template').html()),

    render: function() {
      this.$el.html(this.template(this.model.toJSON()));
      return this;
    }
  });

  var View = Backbone.View.extend({

    el: "#questionApp",

    initialize: function() {
      this.input = this.$('input#query');
      this.questions = new QuestionCollection;

      this.listenTo(this.questions, "add", this.addOne);
      this.listenTo(this.questions, "reset", this.addAll);
      this.listenTo(this.questions, "all", this.render);

      this.questions.fetch();
    },

    submitQuestion: function(event) {
      event.preventDefault();
      var query = this.input.val();

      if (!query) { return; }

      this.questions.create({text:query});
      this.input.val('');

      return false;
    },

    addOne: function(question) {
      var view = new QuestionView({model:question});
      this.$("#question-list").append(view.render().el);
    },

    addAll: function() {
      this.questions.each(this.addOne, this);
    },

    render: function() {

    },

    events: {
      "submit form": "submitQuestion"
    }

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

      // Do the CSRf AJAX Modification
      var csrfToken   = $('input[name="csrfmiddlewaretoken"]').val();
      $.ajaxSetup({headers: {"X-CSRFToken": csrfToken}});

      console.log("KyodoApp is started and ready");
    }
  }

})(Backbone, jQuery);

// On DOM Ready - initialize and execute the app.
$(function() {
  KyodoApp.init();
});
