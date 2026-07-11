import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { AuthProvider } from '@/hooks/useAuth'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: '书童 - 智能学习助手',
  description: '书童智能学习助手，帮助孩子高效学习',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN">
      <body className={inter.className}>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  )
}
