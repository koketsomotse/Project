import NextAuth from "next-auth"
import CredentialsProvider from "next-auth/providers/credentials"
import axios from 'axios'

const handler = NextAuth({
  providers: [
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        username: { label: "Username", type: "text" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        try {
          // Replace with your Django backend URL
          const response = await axios.post('http://localhost:8000/api/auth/login/', {
            username: credentials?.username,
            password: credentials?.password,
          })

          if (response.data.token) {
            return {
              id: response.data.user.id,
              name: response.data.user.username,
              email: response.data.user.email,
              token: response.data.token,
            }
          }
          return null
        } catch (error) {
          return null
        }
      }
    })
  ],
  session: {
    strategy: "jwt",
  },
  pages: {
    signIn: '/login',
  },
  callbacks: {
    async jwt({ token, user }) {
      return { ...token, ...user }
    },
    async session({ session, token }) {
      session.user = token as any
      return session
    }
  }
})

export { handler as GET, handler as POST }
