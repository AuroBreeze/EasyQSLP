import { Interface } from 'readline'
import request from './http'

interface LoginResponse {
    success: boolean
    message: string
    username?: string
    user_id?: number
    errors?: any

}
async function Login(email: string, password: string): Promise<LoginResponse> {
    const valid = { email, password }
    try{
        const response = await request.post('/api/v1/user/login/', valid)
        return {
            success: response.success,
            message: response.message,
            username: response.username,
            user_id: response.user_id
        }
    }catch(error: any){
        return {
            success: error.success,
            message: error.message,
            errors: error.errors,
        }
    }
}


interface RegisterResponse {
    success: boolean
    message: string
    errors?: any
    
}
async function Register(email: string, password: string, username: string ,code: string): Promise<RegisterResponse> {
    const valid = { email, password, username, code }
    try{
        const response = await request.post('/api/v1/user/register/', valid)
        return {
            success: response.success,
            message: response.message,
        }
    }catch(error: any){
        return {
            success: error.success,
            message: error.message,
            errors: error.errors,
        }
    }
}

interface ResetPasswordResponse {
    success: boolean
    message: string
    errors?: any
}
async function ResetPassword(email: string, code: string, password: string,password_confirm: string): Promise<ResetPasswordResponse> {
    const valid = { email, code, password, password_confirm }
    try{
        const response = await request.post('/api/v1/user/resetpassword/', valid)
        return {
            success: response.success,
            message: response.message,
        }
    }catch(error: any){
        return {
            success: error.success,
            message: error.message,
            errors: error.errors,
        }
    }
}

export default {
    Login(email: string, password: string){
        return Login(email, password)
    },
    Register(email: string, password: string, username: string, code: string){
        return Register(email, password, username, code)
    },
    ResetPassword(email: string, code: string, password: string, password_confirm: string){
        return ResetPassword(email, code, password,password_confirm)
    }
}

