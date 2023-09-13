import { startTestServer } from '../src/testServer';

let randomNumber = Math.floor(Math.random() * 10000) + 1;
let rand_email = 'test' + randomNumber + '@email.com';
let psw = 'testpassword';
let token = '';

export const testAgent = startTestServer();
describe('POST /api/users/register', () => {
    it('should create a new user and return 200 status code', async () => {
        const response = await testAgent
            .post('/api/users/register')
            .send({
                name: 'Test User',
                email: rand_email,
                password: psw,
            });
        expect(response.statusCode).toEqual(200);
        expect(response.body.email).toEqual(rand_email);
    });
});


describe('POST /api/users/login', () => {
    test('should return 200 status code and a token for valid login', async () => {
        const response = await testAgent
            .post('/api/users/login')
            .send({
                email: rand_email,
                password: psw,
            });
        expect(response.statusCode).toEqual(200);
        token = response.body.token;
        expect(response.body.token).toBeDefined();
    });
});

describe('GET /api/users/data', () => {
    test('should return 200 status code and user data for valid token', async () => {
        // Primero, obtén un token válido al iniciar sesión
        const user: any = {
            email: rand_email,
            password: psw
        };

        // Usa ese token para hacer una solicitud GET a /api/users/data
        const response = await testAgent
            .get('/api/users/data')
            .set('Authorization', `Bearer ${token}`);
        expect(response.statusCode).toEqual(200);
        expect(response.body.email).toEqual(rand_email);
    });
});

describe('POST /api/files/add', () => {
    it('should upload a file', async () => {
        const res = await testAgent
            .post('/api/files/add')
            .attach('file', './__tests__/testFiles/test.txt')
            .set('Authorization', `Bearer ${token}`);
        expect(res.status).toEqual(200);
        expect(res.body).toHaveProperty('file');
        expect(res.body.file).toHaveProperty('filename', 'test.txt');
    });
});
