function httpsfy(url, environment){
    if (environment === 'development'){
        return url;
    } else {
        return url.replace('http://', 'https://');
    }
}

export default httpsfy;