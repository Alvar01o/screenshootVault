import axios from 'axios';
import { ILoginUser, ILoginResponse, ILoginFailed } from './interfaces'

const API_URL = 'http://localhost:3001'

export const logIng = async (user: ILoginUser) => {
    try {
        const response = await axios.post(API_URL + '/api/users/login', {
            email: user.email,
            password: user.password
        });
        let loginResponse: ILoginResponse = {
            token: response.data.token,
            email: response.data.email,
            name: response.data.name
        }
        return loginResponse;
    } catch (error) {
        let loginResponse: ILoginFailed = {
            token: false
        }
        return loginResponse;
    }
}