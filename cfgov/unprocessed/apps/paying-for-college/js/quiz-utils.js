function elemContainsElem( parent, child ) {
   let node = child.parentNode;
   while ( node !== null ) {
     if ( node === parent ) {
       return true;
     }
     node = node.parentNode;
   }
   return false;
}

module.exports = {
	elemContainsElem
};