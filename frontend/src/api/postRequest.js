import address from '../config/address.json';
import getCookieValue from '../modules/getCookieValue';
import errorReport from '../modules/errorReport';

export default function postRequest(e, destination, callback) {
  return new Promise((resolve, _) => {
    e.preventDefault();
    let formElement = e.target;
    let data = new FormData(formElement);
    let request_url = address.back + destination;
    const xhr = new XMLHttpRequest();
    xhr.open('POST', request_url);
    xhr.withCredentials = true;
    const csrfToken = getCookieValue(document.cookie, 'csrftoken');
    xhr.setRequestHeader('X-CSRFToken', csrfToken);
    xhr.onreadystatechange = () => {
      if (xhr.readyState === 4 && xhr.status === 201) {
        callback();
        resolve(true);
      }
      if (xhr.readyState === 4 && xhr.status >= 400) {
        errorReport(xhr.statusText, 'freeNtoe-upload');
        resolve(false);
      }
    };
    xhr.send(data);
  });
}
