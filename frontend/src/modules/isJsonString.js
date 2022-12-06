/**
 *
 * @param {string} str
 * @returns {boolean} whether string can be parsed into json
 */
const isJsonString = (str) => {
  try {
    JSON.parse(str);
  } catch (e) {
    return false;
  }
  return true;
};

export default isJsonString;
