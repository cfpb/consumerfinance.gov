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
          var buttonset,
        baseClass = "answer-module",
        textInputClass = 'richtext',
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
          var node = sel.baseNode || sel.anchorNode;
          var tip = $(node).closest( '.' + baseClass )[0];

          // If selection is currently styled as a tip,
          // remove the tip wrapper element.
          if ( tip ) {
            var docFrag = document.createDocumentFragment();
            while ( tip.firstChild ) {
              var child = tip.removeChild( tip.firstChild );
              docFrag.appendChild(child);
            }
            tip.parentNode.replaceChild(docFrag, tip);
            _this.options.editable.setModified();
            return;
          }

          // Otherwise, get the selected range. If it starts or ends
          // with a text node or inline element (a, strong, i), 
          // expand the selection either to that node's 
          // start or end bound, or the start or end bound of its parent
          // if it's not a direct child of the text input div.
          var range = rangy.getSelection().getRangeAt(0);
          
          function expandSelection( node, start ) {
            while ( node.nodeType === 3 
                    || ['A', 'I', 'Strong'].indexOf( node.nodeName ) > -1 ) {
              var parent = node.parentNode;
              if ( parent && !parent.classList.contains( textInputClass ) ) {
                range[start ? 'setStartBefore' : 'setEndAfter']( parent );
                node = parent;
              } else {
                range[start ? 'setStartBefore' : 'setEndAfter']( node );
                break;
              }
            }
          }

          expandSelection( range.startContainer, true );
          expandSelection( range.endContainer );


          // Check if range can be surrounded with a wrapper element.
          // If not, try to find the least common ancestor of the 
          // start and end containers and expand the start/end of the
          // range to encompas it so the range can be surrounded.
          function getDepth( ancestor, node ) {
            return node === ancestor 
                        ? 0 : 
                        $( node ).parentsUntil( common ).length + 1;
          }

          if ( !range.canSurroundContents() ) {
            var common = range.commonAncestorContainer;
            var start_depth = getDepth( common, range.startContainer );
            var end_depth = getDepth( common, range.endContainer );
            
            while ( !range.canSurroundContents() ) {
              if ( start_depth > end_depth ) {
                if ( range.startContainer.classList.contains( textInputClass ) ) {
                  break;
                } else {
                  range.setStartBefore( range.startContainer );
                  start_depth = getDepth( common, range.startContainer );
                }
              } else {
                if ( range.endContainer.classList.contains( textInputClass ) ) {
                  break;
                } else {
                  range.setEndAfter( range.endContainer );
                  end_depth = getDepth( common, range.endContainer );
                }
              }
            }
          }
          
          // If range can be surrounded, wrap it in an element 
          // that applies the tip class.
          if ( range.canSurroundContents() ) {
            var newNode = document.createElement( 'aside' );
            newNode.className = baseClass;
            range.surroundContents( newNode );
            return _this.options.editable.element.trigger( 'change' );
          }

        });
        
        buttonset.hallobuttonset();
        return toolbar.append(buttonset);
      }
    });
})(jQuery);
}).call(this);