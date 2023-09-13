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
            email: response.data.user.email,
            name: response.data.user.name,
            id: response.data.user.id
        }
        localStorage.setItem('user', JSON.stringify(loginResponse));
        return true;
    } catch (error) {
        console.log(error)
        return false;
    }
}