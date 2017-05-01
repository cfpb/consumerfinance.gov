
(function () {
  (function (jQuery) {
    return jQuery.widget("IKS.answermodule", {
      options: {
        editable: null,
        toolbar: null,
        uuid: '',
        buttonCssClass: null
      },
      populateToolbar: function (toolbar) {
        if (window.location.href.indexOf('ask_cfpb') > -1) {
          var buttonset,
          _this = this;
          buttonset = jQuery("<span class=\"" + this.widgetName + "\"></span>");
          var buttonElement;
          buttonElement = jQuery('<span></span>');
          buttonElement.hallobutton({
            uuid: _this.options.uuid,
            editable: _this.options.editable,
            label: "Apply Ask CFPB tip style to selection",
            icon: 'icon-edit',
            command: null
          });

          buttonset.append(buttonElement);
          
          buttonElement.on('click', function (event) {
            var sel = window.getSelection();
            var range = sel.getRangeAt(0).cloneRange();
            var contents = range.cloneContents();
            var elem = document.createElement("aside");
            elem.className = "answer-module";
            elem.appendChild(contents);
            range.deleteContents();
            range.insertNode(elem);

            $(range.commonAncestorContainer).find('*').each(function() {
              if ($(this).is(':empty') || $(this).text() === '') {
                $(this).remove();
              }
            });

            return _this.options.editable.element.trigger('change');
          });
          
          buttonset.hallobuttonset();
          return toolbar.append(buttonset);
        }
      }
    });
})(jQuery);
}).call(this);