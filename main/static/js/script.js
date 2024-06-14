const getAuthToken = () => {
    return localStorage.getItem('jwt_token');
}

const setAuthToken = (token) => {
    localStorage.setItem('jwt_token', token);
}

const apiGET = (url) => {
    const token = getAuthToken();
    return fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + token
        }
    }).then(response => {
        if (!response.ok) {
            throw new Error('Authorization failed');
        }
        // return response.json();
        return response;
    });
}

const apiPOST = (url, data) => {
    const token = getAuthToken();
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(data)
    }).then(response => {
        if (!response.ok) {
            throw new Error('Authorization failed');
        }
        return response.json();
    });
}
