// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  ssr: false,

  vite: {
    server: {
      proxy: {
        '/operation/api/': 'http://127.0.0.1:8000/',
      }
    }
  },

  modules: ["@nuxtjs/tailwindcss", "shadcn-nuxt", 
  ],
  shadcn: {
    /**
     * Prefix for all the imported component
     */
    prefix: '',
    /**
     * Directory that the component lives in.
     * @default "./components/ui"
     */
    componentDir: './components/ui'
  }

})