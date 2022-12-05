/**
 * @param {HTMLElment} el
 * @returns {{left: number, top: number, height:number, width:number}}
 */
const getGlobalRect = (el) => {
  const rect = el.getBoundingClientRect();
  return {
    left: rect.left + window.scrollX,
    top: rect.top + window.scrollY,
    height: rect.height,
    width: rect.width,
  };
};
export default getGlobalRect;
