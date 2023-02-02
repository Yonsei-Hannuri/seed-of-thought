import axios from 'axios';
import getCookieValue from './getCookieValue';

function errorReport(e, from) {
  const csrfToken = getCookieValue(document.cookie, 'csrftoken');
  axios({
    method: 'POST',
    url: process.env.REACT_APP_API_DOMAIN + 'frontError/',
    withCredentials: true,
    data: {
      errorMessage: e,
      from: from,
    },
    headers: {
      'Content-Type': 'Application/json',
      'X-CSRFToken': csrfToken,
    },
  });
}

export default errorReport;
