/**
 * @param {number} totalSeconds - The time in seconds.
 * @returns {string} Time in the HH:MM:SS format.
 */
function formatTimestamp(totalSeconds) {
  let hours = Math.floor(totalSeconds / 3600);
  let minutes = Math.floor((totalSeconds - hours * 3600) / 60);
  let seconds = totalSeconds - hours * 3600 - minutes * 60;

  let timestamp = '';
  if (hours < 10) {
    hours = '0' + hours;
  }

  if (String(hours) !== '00') {
    timestamp = hours + ':';
  }

  if (minutes < 10) {
    minutes = '0' + minutes;
  }

  if (seconds < 10) {
    seconds = '0' + seconds;
  }

  timestamp += minutes + ':' + seconds;

  return timestamp;
}

export { formatTimestamp };
