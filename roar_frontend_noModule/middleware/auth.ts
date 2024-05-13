import { useSessionStorage } from "@vueuse/core"

export default defineNuxtRouteMiddleware(async(to, from) => {
    const token = useSessionStorage('token', { access: '', refresh: '' })
    await validateToken()
    if (token.value.access === '') {
        return navigateTo('/Auth')
    }

})
