
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
          baseClass = "answer-module",
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
            var node = sel.baseNode;
            var parent = node.parentElement;
            // Walk up the parents of the selected node up to 
            // the rich text input element. If an element with
            // the tip class is found, remove the containing
            // tip element and return.
            while ( parent ) {
              if ( parent.classList.contains( baseClass ) ) {
                var docFrag = document.createDocumentFragment();
                while (parent.firstChild) {
                    var child = parent.removeChild(parent.firstChild);
                    docFrag.appendChild(child);
                }
                parent.parentNode.replaceChild(docFrag, parent);
                return;
              } else if ( parent.classList.contains('richtext') ) {
                parent = null;
              } else {
                parent = parent.parentNode;
              }
            }

            // Otherwise, check that the selection is not empty.
            // If it has contents, clone them, insert them in a
            // new tip element, and replace the selection with
            // the new element.
            var range = sel.getRangeAt(0).cloneRange();

            if (range.endOffset > range.startOffset) {
              var contents = range.cloneContents();
              var elem = document.createElement("aside");
              elem.className = baseClass;
              elem.appendChild(contents);
              range.deleteContents();
              range.insertNode(elem);

              // Update selection's value to encompass
              // the contents of new element. this makes
              // it possible to immediately remove the new tip
              // wrapper by clicking the tip button again.
              var newRange = document.createRange();
              newRange.setStart(elem, 0);
              newRange.setEnd(elem, elem.childNodes.length); 
              sel.removeAllRanges();
              sel.addRange(newRange);

              // Clear any empty elements created by this process.
              $(range.commonAncestorContainer).find('*').each(function() {
                if ($(this).is(':empty') || $(this).text() === '') {
                  $(this).remove();
                }
              });
            }

            return _this.options.editable.element.trigger('change');
          });
          
          buttonset.hallobuttonset();
          return toolbar.append(buttonset);
        }
      }
    });
})(jQuery);
}).call(this);