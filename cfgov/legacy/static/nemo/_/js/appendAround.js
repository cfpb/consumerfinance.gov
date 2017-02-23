/*! appendAround markup pattern. [c]2012, @scottjehl, Filament Group, Inc. MIT/GPL 
how-to:
    1. Insert potential element containers throughout the DOM
    2. give each container a data-set attribute with a value that matches all other containers' values
    3. Place your appendAround content in one of the potential containers
    4. Call appendAround() on that element when the DOM is ready
*/
(function( $ ){
    $.fn.appendAround = function(){

      return this.each(function(){

        var $self = $( this ),
            att = "data-set",
            $parent = $self.parent(),
            currentParent = $parent[ 0 ], // changed to currentParent because parent is a reserved keyword
            attval = $parent.attr( att ),
            $set = $( "["+ att +"='" + attval + "']" );

        function isHidden( elem ){
            // getComputedStyle not supported in IE8
            return $( elem ).is( ":hidden" );
            //return window.getComputedStyle( elem, null ).getPropertyValue( "display" ) === "none";
        }

        function appendToVisibleContainer(){
            if( isHidden( currentParent ) ){
                var found = 0;
                $set.each(function(){
                    if( !isHidden( this ) && !found ){
                        $self.appendTo( this );
                        found++;
                        currentParent = this;
                    }
                });
            }
        }

        appendToVisibleContainer();

        $(window).bind( "resize", appendToVisibleContainer );

      });
    };
}( jQuery ));