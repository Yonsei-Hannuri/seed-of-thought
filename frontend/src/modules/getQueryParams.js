/**
 *
 * @returns {{[key:string]: string }} query params key, value set as object
 */
const getQueryParams = () => {
  const urlSearchParams = new URLSearchParams(window.location.search);
  return Object.fromEntries(urlSearchParams.entries());
};

export default getQueryParams;
