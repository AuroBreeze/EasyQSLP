import profile from '@/utils/ProfileView/getProfile'
import {ref,reactive} from 'vue'

const userProfile = reactive({
    'avatar': '', 
    'userprofile_md': '', 
    'userprofile_html': '', 
    'content_hash': '', 
    'create_time': '', 
    'update_time': '', 
    'user_Login': '', 
    'toc': '', 
    'word_count': '', 
    'username': '', 
    'email': '', 
    'join_date': ''
})

const data = (id:string) => {
    profile.getProfile(id).then((response) => {
        if (response.success) {
            Object.assign(userProfile, response.data)
        }
    })
    return userProfile
}

export default {
    userProfile,
    data
}
