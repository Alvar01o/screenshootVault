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


    //    it('should return a 401 error for unauthenticated user', async () => {
    //        // Make a request to the /data endpoint without a JWT token
    //        const res = await request(app).get('/data');
    //    
    //        // Expect the response to have a 401 status code
    //        expect(res.status).toEqual(401);
    //      });
    //    
    //      it('should return a 404 error for non-existent user', async () => {
    //        // Sign a JWT token for a non-existent user
    //        const token = signToken({ user: { id: '456' } });
    //    
    //        // Make a request to the /data endpoint with the JWT token
    //        const res = await request(app)
    //          .get('/data')
    //          .set('Authorization', `Bearer ${token}`);
    //    
    //        // Expect the response to have a 404 status code
    //        expect(res.status).toEqual(404);
    //      });
    //    
    //      it('should return a 403 error for invalid token', async () => {
    //        // Make a request to the /data endpoint with an invalid JWT token
    //        const res = await request(app)
    //          .get('/data')
    //          .set('Authorization', 'Bearer invalid_token');
    //    
    //        // Expect the response to have a 403 status code
    //        expect(res.status).toEqual(403);
    //      });
});

describe('POST /api/files/add', () => {
    it('should upload a file', async () => {
        const res = await testAgent
            .post('/api/files/add')
            .attach('file', './__tests__/testFiles/test.txt')
            .set('Authorization', `Bearer ${token}`);
            console.log(res.error)
        expect(res.status).toEqual(200);
        expect(res.body).toHaveProperty('file');
        expect(res.body.file).toHaveProperty('filename', 'test.txt');
    });
});
// Similarmente, puedes escribir pruebas para otras rutas
