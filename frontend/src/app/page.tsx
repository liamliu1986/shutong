import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="text-center space-y-8 max-w-2xl">
        <h1 className="text-5xl font-bold text-primary-700">书童</h1>
        <p className="text-xl text-gray-600">智能学习助手，陪伴每一次成长</p>
        <div className="flex justify-center gap-4">
          <Link
            href="/login"
            className="px-8 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition-colors"
          >
            登录
          </Link>
          <Link
            href="/register"
            className="px-8 py-3 bg-white text-primary-600 border border-primary-600 rounded-lg font-medium hover:bg-primary-50 transition-colors"
          >
            注册
          </Link>
        </div>
      </div>
    </main>
  )
}
