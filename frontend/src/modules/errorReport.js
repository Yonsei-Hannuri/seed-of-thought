import axios from 'axios';
import address from '../config/address.json';

function errorReport(e, from) {
  let csrfToken_ = document.cookie;
  let csrfToken = csrfToken_.split('=')[1];
  axios({
    method: 'POST',
    url: address.back + 'frontError/',
    withCredentials: true,
    data: {
      errorMessage: e,
      from: from,
    },
    headers: { 'X-CSRFToken': csrfToken },
  });
}

export default errorReport;
