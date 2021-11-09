const fileInput = document.getElementById( 'upload-file' );
const fileCount = document.querySelector( '#upload-file-list > h4' );
const fileList = document.querySelector( '#upload-file-list > ul' );

/**
 * @param {object} evt - change event fired on fileInput
 */
function fileSelected( evt ) {
  clearSelectedFiles();
  addFiles( evt.target.files );
}

/**
 * Clears selected file names and hides file list header
 */
function clearSelectedFiles() {
  fileList.innerHTML = '';
  fileCount.className = 'u-hidden';
}

/**
 * @param {array} files - DOMList of files provided to the input component
 */
function addFiles( files ) {
  if ( files.length ) fileCount.className = '';
  for ( const file of files ) {
    addFile( file );
  }
}

/**
 * @param {object} file - File object passed through from the change event
 */
function addFile( file ) {
  const li = document.createElement( 'li' );
  li.innerText = file.name;
  fileList.appendChild( li );
}

addFiles( fileInput.files );
fileInput.addEventListener( 'change', fileSelected );
