/**
 * getNewHash - Convert an old eRegs hash into a Regs3K hash.
 *
 * @param {string} hash - Old eRegs URL hash.
 * @returns {string} New Regs3K hash.
 */
const getNewHash = (hash) => {
  if (/(\w+-)+Interp-/.test(hash)) {
    // Trim off DDDD- e.g. 1003-2-f-Interp-3 becomes 2-f-Interp-3
    return hash.replace(/^#?\d\d\d\d-/, '');
  }
  // Trim off DDDD-D- e.g. 1003-4-a-9-ii-C becomes a-9-ii-C
  return hash.replace(/^#?\d\d\d\d-\w+-/, '');
};

/**
 * isOldHash - Check if provided hash is from the old eRegs site
 * All the former eRegs paragraph markers start with their four-digit reg.
 *
 * @param {string} hash - URL hash.
 * @returns {boolean} true/false.
 */
const isOldHash = (hash) => /^#?\d\d\d\d/.test(hash);

export { getNewHash, isOldHash };
