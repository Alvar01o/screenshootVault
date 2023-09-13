export interface IUser {
    email: string,
    name: string
}
export interface ILoginUser {
    email: FormDataEntryValue,
    password: FormDataEntryValue
}
export interface ILoginFailed {
    token: boolean,    
}

export interface ILoginResponse {
    token: string,
    email: string,
    name: string,
    id: string
}