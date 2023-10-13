import axios from 'axios';
import slugify from 'slugify';
const API_URL = 'http://localhost:3001'

const receiveLoginResponse = (response) => {
    if (response.status === 200) {
        let user = {
            token: response.data.token,
            email: response.data.user.email,
            name: response.data.user.name,
            id: response.data.user.id
        };
        localStorage.setItem('user', JSON.stringify(user));
        return true;
    }
    if (response.status === 400) {
        let user = {
            msg: response.data.msg
        };
        localStorage.setItem('user', JSON.stringify(user));
    }
    return false;
};

export const login = async (user) => {
    try {
        const response = await axios.post(API_URL + '/api/users/login', {
            email: user.email,
            password: user.password
        });
        let loginResponse = receiveLoginResponse(response);
        return loginResponse;
    } catch (error) {
        return false;
    }
}

export const register = async (user) => {
    let friendlDomain = slugify(user.domain, {
        replacement: "-", // replace spaces with replacement character, defaults to `-`
        remove: undefined, // remove characters that match regex, defaults to `undefined`
        lower: true, // convert to lower case, defaults to `false`
        strict: true, // strip special characters except replacement, defaults to `false`
        locale: "en", // language code of the locale to use
        trim: true, // trim leading and trailing replacement chars, defaults to `true`
      });
    try {
        const response = await axios.post(API_URL + '/api/users/register', {
            email: user.email,
            password: user.password,
            name: user.username,
            domain: friendlDomain
        });
        let loginResponse = receiveLoginResponse(response);
        return loginResponse;
    } catch (error) {
        return false;
    }
}