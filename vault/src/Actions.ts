import axios from 'axios';
import { ILoginUser } from './interfaces'

const API_URL = 'http://localhost:3001'

export const logIng = async (user: ILoginUser) => {
    try {
        const response = await axios.post(API_URL + '/api/users/login', {
            email: user.email,
            password: user.password
        });
        console.log(response)
        // Suponiendo que el endpoint devuelve un token cuando el login es exitoso
        const token = response.data.token;
        return token;
    } catch (error) {
        console.log(error)
    }
}