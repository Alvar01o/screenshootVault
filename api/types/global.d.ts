declare namespace NodeJS {
    interface ProcessEnv {
        MONGO_URI: string;
        // y cualquier otra variable de entorno que quieras tipar
    }
}