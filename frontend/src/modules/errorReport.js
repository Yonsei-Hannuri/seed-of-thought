import axios from 'axios';
import address from '../config/address.json';
import getCookieValue from './getCookieValue'

function errorReport(e, from) {
  const csrfToken = getCookieValue(document.cookie, 'csrftoken')
  axios({
    method: 'POST',
    url: address.back + 'frontError/',
    withCredentials: true,
    data: {
      errorMessage: e,
      from: from,
    },
    headers: { 
      'Content-Type': 'Application/json',
      'X-CSRFToken': csrfToken 
    },
  });
}

export default errorReport;
