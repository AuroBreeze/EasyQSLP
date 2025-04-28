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
        console.log("API123123"+response)
        if (!response.success) {
            return {
                success: false,
                message: response.message,
                errors: response.errors
            }
        }
        return {
            success: true,
            message: response.message,
            username: response.username,
            user_id: response.user_id
        }
    } catch (error: any) {
        return {
            success: false,
            message: error,
            errors: error
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
            return {
                success: false,
                message: response.message || '注册失败',
                errors: response.errors || {}
            }
        }
        return {
            success: true,
            message: response.message || '注册成功',
            errors: {}
        }
    } catch (error: any) {
        return {
            success: false,
            message: error.response?.data?.message || error.message || '网络错误',
            errors: error.response?.data?.errors || {}
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
            return {
                success: false,
                message: response.message || '密码重置失败',
                errors: response.errors || {}
            }
        }
        return {
            success: true,
            message: response.message || '密码重置成功',
            errors: {}
        }
    } catch (error: any) {
        return {
            success: false,
            message: error.response?.data?.message || error.message || '网络错误',
            errors: error.response?.data?.errors || {}
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
