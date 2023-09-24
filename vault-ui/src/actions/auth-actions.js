import axios from 'axios';
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