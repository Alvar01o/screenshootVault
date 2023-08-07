export interface IUser {
    email: string,
    name: string
}
export interface ILoginUser {
    email: FormDataEntryValue,
    password: FormDataEntryValue
}
export interface ILoginResponse {
    token: string,
    email: string,
    name: string
}