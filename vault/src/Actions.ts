import axios from 'axios';
import { ILoginUser, ILoginResponse, ILoginFailed } from './interfaces'

const API_URL = 'http://localhost:3001'

const receiveLoginResponse = (response: any) : boolean => {
    if (response.status === 200) {
        let user:ILoginResponse = {
            token: response.data.token,
            email: response.data.user.email,
            name: response.data.user.name,
            id: response.data.user.id
        };
        localStorage.setItem('user', JSON.stringify(user));
        return true;
    }
    if (response.status === 400) {
        let user:ILoginFailed = {
            msg: response.data.msg
        };
        localStorage.setItem('user', JSON.stringify(user));
    }
    return false;
};

export const login = async (user: ILoginUser) => {
    try {
        const response = await axios.post(API_URL + '/api/users/login', {
            email: user.email,
            password: user.password
        });
        let loginResponse: boolean = receiveLoginResponse(response);
        return loginResponse;
    } catch (error) {
        return false;
    }
}