const getCookieValue = (cookie, key) => {
    const cookies = cookie.split(';');
    for(let cookie of cookies){
        const cookieKeyVal = cookie.split('=');
        if (cookieKeyVal[0].trim() === key){
            return cookieKeyVal[1];
        }
    }
    return null;
}

export default getCookieValue;
