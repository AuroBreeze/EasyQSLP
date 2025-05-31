import  request  from './http'

interface Token{
    //token: string,
    accessToken?: string,
    refreshToken?: string
    detail?: string,
    code?: string,
    verified?: boolean
}


async function GetToken(email: string, password: string): Promise<Token>{
    const valid = {email: email, password: password}
    try {
        const response = await request.post('/api/v1/user/token/', valid)
        return {
            accessToken: response.access,
            refreshToken: response.refresh
        }
    } catch (error: any) {
        return {
            detail: error.response?.data?.detail || 'Authentication failed',
            code: error.response?.data?.code || 'unknown_error'
        }
    }
}

async function RefreshToken(refreshToken: string): Promise<Token>{
    try {
        const response = await request.post('/api/v1/user/token/refresh/', {refresh: refreshToken})
        return {
            accessToken: response.access,
            refreshToken: response.refresh
        }
    } catch (error: any) {
        return {
            detail: error.response?.data?.detail || 'Token refresh failed',
            code: error.response?.data?.code || 'refresh_error'
        }
    }
}

async function VerifyToken(token: string): Promise<Token>{
    try {
        await request.post('/api/v1/user/token/verify/', {token: token})
        return {
            verified: true
        }
    } catch (error) {
        return {
            verified: false,
            detail: 'Token verification failed',
            code: 'token_invalid'
        }
    }
}

export default {
    GetToken(email: string, password: string){return GetToken(email, password)},
    RefreshToken(refreshToken: string){return RefreshToken(refreshToken)},
    VerifyToken(token: string){ return VerifyToken(token)}
}
