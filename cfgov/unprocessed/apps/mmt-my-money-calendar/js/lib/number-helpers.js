/* Maps a number in a range, to a number in a different range.
 *
 * @param {number} num The number to map
 * @param {number} min The minimum value in the input range
 * @param {number} max The maximum value in the input range
 * @param {number} outMin The minimum value in the output range
 * @param {number} outMax The maximum value in the output range
 * @returns {number}
 * @see {@link https://stackoverflow.com/questions/345187/math-mapping-numbers}
 */
export const mapRange = ( num, min, max, outMin, outMax ) => ( num - min ) / ( max - min ) * ( outMax - outMin ) + outMin;


/* Clamps the value of a number between a minimum and a maximum
 *
 * @param {number} num The number to clamp
 * @param {number} min The minimum allowable value
 * @param {number} max The maximum allowable value
 * @see {@link https://stackoverflow.com/questions/11409895/whats-the-most-elegant-way-to-cap-a-number-to-a-segment}
 */
export const clamp = ( num, min, max ) => Math.min( Math.max( num, min ), max );
