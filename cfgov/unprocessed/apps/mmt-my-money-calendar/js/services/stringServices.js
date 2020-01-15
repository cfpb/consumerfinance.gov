/**
 * Joins a list of class names, filtering out any null/empty values.
 * @param {Array[String]} classList list of class names
 */
export const joinClasses = classList => classList.filter(x => x).join(" ");
