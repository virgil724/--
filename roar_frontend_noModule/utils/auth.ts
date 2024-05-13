import { useSessionStorage } from "@vueuse/core"


const token = useSessionStorage('token', {
    refresh: '', access: ''
})
export const save_token = (access, refresh) => {
    token.value.access = access
    token.value.refresh = refresh
}
const token_clear = () => {
    token.value.refresh = ''
    token.value.access = ''
}
const token_refresh = async () => {
    try {
        const { access, refresh } = await $fetch("/operation/api/dj-rest-auth/token/refresh/", {
            method: "post", body: {
                refresh: token.value.refresh
            }
        })
        save_token(access, refresh)
    } catch {
        token_clear()
    }

}


export const validateToken = async () => {
    if (token.value.access !== "") {
        try {
            await $fetch("/operation/api/dj-rest-auth/token/verify/", {
                method: "POST",
                body: { token: token.value.access }
            })
        } catch (error) {
            await token_refresh()
        }
    }
}