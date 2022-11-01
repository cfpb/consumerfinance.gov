const fileInput = document.getElementById('supporting_documentation');
const fileListWrapper = document.getElementById('file-list-wrapper');
const fileList = document.querySelector('#file-list-wrapper > ul');
const radioParent = document.getElementById('mail-radio');
const initialCheckedRadio = radioParent.querySelector('input[checked]');
const addressWrapper = document.getElementById('mail-target');
const form = document.getElementById('privacy-form');
const submitIcon = document.getElementById('submit-icon');

/**
 * @param {object} evt - change event fired on fileInput
 */
function fileSelected(evt) {
  clearSelectedFiles();
  addFiles(evt.target.files);
}

/**
 * Clears selected file names and hides file list header
 */
function clearSelectedFiles() {
  fileList.innerHTML = '';
  fileListWrapper.className = 'u-hidden';
}

/**
 * @param {Array} files - DOMList of files provided to the input component
 */
function addFiles(files) {
  if (files.length) fileListWrapper.className = '';
  for (const file of files) {
    addFile(file);
  }
}

/**
 * @param {object} file - File object passed through from the change event
 */
function addFile(file) {
  const li = document.createElement('li');
  li.innerText = file.name;
  fileList.appendChild(li);
}

/**
 * @param {object} evt - Bubbled change event on wrapper radio buttons
 */
function toggleMailingAddress(evt) {
  openWrapper(evt.target.id);
}

/**
 * @param {string} id - The id of the current checked toggle
 */
function openWrapper(id) {
  if (id === 'id_contact_channel_1') {
    addressWrapper.className = 'open';
  } else {
    addressWrapper.className = '';
  }
}

openWrapper(initialCheckedRadio.id);
addFiles(fileInput.files);

fileInput.addEventListener('change', fileSelected);
radioParent.addEventListener('change', toggleMailingAddress);
form.addEventListener('submit', function () {
  submitIcon.classList.add('submitting');
});
