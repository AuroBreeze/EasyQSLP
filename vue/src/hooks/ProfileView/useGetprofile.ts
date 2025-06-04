import { ref, reactive } from 'vue'
import requests from '@/utils/base/http'

const base_url = "/api/v1/user/profile/"

interface ProfileResponse {
    success: boolean,
    message: string,
    data: any
}
async function getProfile(id: string): Promise<ProfileResponse> {
    try {
        const response = await requests.get(base_url + id)
        return response
    } catch (error: any) {
        console.log("useGetProfile error: " + error)
        return {
            success: false,
            message: error.message,
            data: error.errors
        }
    }
}

export default{
    getProfile(id: string){
        return getProfile(id)
    }
}


