import request from './http'

interface BaseResponse {
    success: boolean
    message: string
    errors?: any
}

interface LoginResponse extends BaseResponse {
    username: string
    user_id: number
}

interface Error extends BaseResponse {}
async function Login(email: string, password: string): Promise<LoginResponse | Error> {
    const valid = { email, password }
    try {
        const response = await request.post('/api/v1/user/login/', valid)
        if (!response.success) {
            return response
        }
        return response
    } catch (error: any) {
        if(error.response.status === 400){
        return error
    }
        return {
            success: false,
            message: "未知错误",
            errors: {ValidationError: "未知错误"}
    }
}
}


interface RegisterResponse {
    success: boolean
    message: string
}
async function Register(email: string, password: string, username: string, code: string): Promise<RegisterResponse | Error> {
    const valid = { email, password, username, code }
    try {
        const response = await request.post('/api/v1/user/register/', valid)
        if (!response.success) {
            return response
        }
        return response
    } catch (error: any) {
        if(error.response.status === 400){
        return error
    }
        return {
            success: false,
            message: "未知错误",
            errors: {ValidationError: "未知错误"}
    }
}
}

interface ResetPasswordResponse {
    success: boolean
    message: string
}
async function ResetPassword(email: string, code: string, password: string, password_confirm: string): Promise<ResetPasswordResponse | Error> {
    const valid = { email, code, password, password_confirm }
    try {
        const response = await request.post('/api/v1/user/resetpassword/', valid)
        if (!response.success) {
            return response}
        return response
    } catch (error: any) {
        if(error.response.status === 400){
        return error
    }
        return {
            success: false,
            message: "未知错误",
            errors: {ValidationError: "未知错误"}
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
