import request from 'supertest';
import app from '../src/index'; // Importa tu aplicación Express

let randomNumber = Math.floor(Math.random() * 10000) + 1;
let rand_email = 'test'+randomNumber+'@email.com';
let psw = 'testpassword';
describe('POST /api/users/register', () => {
    it('should create a new user and return 200 status code', async () => {
        const response = await request(app)
            .post('/api/users/register')
            .send({
                name: 'Test User',
                email: rand_email,
                password: psw,
            });
        expect(response.statusCode).toEqual(200);
        expect(response.body.email).toEqual(rand_email);
        // etc.
    });
});


describe('POST /api/users/login', () => {
    test('should return 200 status code and a token for valid login', async () => {
        const response = await request(app)
            .post('/api/users/login')
            .send({
                email: rand_email,
                password: psw,
            });
        expect(response.statusCode).toEqual(200);
        expect(response.body.token).toBeDefined();
    });
});

describe('GET /api/users/data', () => {
    test('should return 200 status code and user data for valid token', async () => {
        // Primero, obtén un token válido al iniciar sesión
        const loginResponse = await request(app)
            .post('/api/users/login')
            .send({
                email: rand_email,
                password: psw,
            });

        // Usa ese token para hacer una solicitud GET a /api/users/data
        const response = await request(app)
            .get('/api/users/data')
            .set('Authorization', `Bearer ${loginResponse.body.token}`);
        expect(response.statusCode).toEqual(200);
        expect(response.body.email).toEqual(rand_email);
    });
});


// Similarmente, puedes escribir pruebas para otras rutas
