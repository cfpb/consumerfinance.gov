(function() {
  (function($) {
    return $.widget('IKS.editHtmlButton', {
      options: {
        uuid: '',
        editable: null
      },
      populateToolbar: function(toolbar) {
        var button, widget;

        var getEnclosing = function(tag) {
          var node;
          node = widget.options.editable.getSelection().commonAncestorContainer;
          return $(node).parents(tag).get(0);
        };

        widget = this;

        button = $('<span></span>');
        button.hallobutton({
          uuid: this.options.uuid,
          editable: this.options.editable,
          label: 'Edit HTML',
          icon: 'icon-code',
          command: null
        });

        toolbar.append(button);

        button.on('click', function(event) {
          $('body > .modal').remove();
          var contents = '<div class="modal fade" tabindex="-1" role="dialog" aria-hidden="true">' + 
                            '<div class="modal-dialog">' +
                              '<div class="modal-content">'+
                                '<button type="button" class="close icon text-replace icon-cross" '+
                                         'data-dismiss="modal" aria-hidden="true">' +
                                    '&times;' + 
                                '</button>' +         
                                '<div class="modal-body">' +
                                  '<header class="nice-padding hasform">' +
                                    '<div class="row">' +
                                      '<div class="left">' +
                                        '<div class="col">' + 
                                          '<h1><i class="fa fa-file-code-o"></i>Edit HTML Code</h1>' +
                                        '</div>' +
                                      '</div>' +
                                    '</div>' +
                                  '</header>' +
                                  '<div class="modal-body-body" style="padding:15px;"></div>' +
                                '</div> <!-- /.modal-body -->' +         
                              '</div><!-- /.modal-content -->' +    
                            '</div><!-- /.modal-dialog -->' +
                          '</div>';
          var container = $(contents);

          // add container to body and hide it, so content can be added to it before display                                                                             
          $('body').append(container);
          container.modal('hide');
          var modalBody = container.find('.modal-body-body');
          var bodyContents =  '<textarea style="height: 400px; border: 1px solid black" id="wagtail-edit-html-content">' +
                                widget.options.editable.element.html() +
                              '</textarea>' +
                              '<button id="wagtail-edit-html-save" type="button" class="button" style="margin-top:15px;">' +
                                'Save' + 
                              '</button>';
          modalBody.html(bodyContents);
          $("#wagtail-edit-html-save").on("click", function() {
              widget.options.editable.setContents($("#wagtail-edit-html-content").val());
              widget.options.editable.setModified();
              container.modal('hide');
          });
          container.modal('show');
        });
      }
    });
  })(jQuery);
}).call(this);