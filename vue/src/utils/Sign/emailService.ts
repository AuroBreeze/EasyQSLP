import request from '../base/http'

interface EmailResponse {
  success: boolean
  message: string
  errors?: any
}

async function sendEmail(email:string,usage:string):Promise<EmailResponse>{
    const vaild = {email,usage}
    
    try{
        const response = await request.post('/api/v1/user/emailsendcode/',vaild)
        return {
            success:response.success,
            message:response.message,
        }

    }catch(error:any){
        return {
            success:error.success,
            message:error.message,
            errors:error.errors,
        }

    }
}

export default {
    sendEmail(email:string,usage:string){
        return sendEmail(email,usage)
    }
}