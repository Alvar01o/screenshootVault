import request from 'supertest';
import app from '../src/index'; // Importa tu aplicación Express

describe('POST /api/users/register', () => {
    it('should create a new user and return 200 status code', async () => {
        let randomNumber = Math.floor(Math.random() * 10000) + 1;
        const response = await request(app)
            .post('/api/users/register')
            .send({
                name: 'Test User',
                email: 'test'+randomNumber+'@email.com',
                password: 'testpassword',
            });
        expect(response.statusCode).toEqual(200);
        expect(response.body.email).toEqual('test'+randomNumber+'@email.com');
        // etc.
    });
});

// Similarmente, puedes escribir pruebas para otras rutas
