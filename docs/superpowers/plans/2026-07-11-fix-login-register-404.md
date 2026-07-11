# 修复登录注册页面 404 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (inline execution) for this small bugfix.

**Goal:** 补全缺失的 `/login` 和 `/register` 前端页面，使首页的登录/注册链接能正常访问，登录/注册成功后跳转 `/dashboard`。

**Architecture:** 使用 Next.js 14 App Router 的页面组件，复用已有的 `useAuth` Hook（它封装了 axios 调用、token 存储和路由跳转），两个页面均为 Client Component。

**Tech Stack:** Next.js 14 + React + TypeScript + Tailwind CSS + shadcn/ui 风格手写表单

## Global Constraints

- 所有代码注释使用中文
- 提交信息使用中文，类型前缀小写
- 不引入新的依赖
- 复用现有 `frontend/src/hooks/useAuth.tsx` 和 `frontend/src/lib/api.ts`
- 修复通过 `bugfix/` 分支提交 PR 合并到 `main`

---

### Task 1: 创建登录页面

**Files:**
- Create: `frontend/src/app/login/page.tsx`

**Interfaces:**
- Consumes: `useAuth().login(email, password)` from `frontend/src/hooks/useAuth.tsx`
- Produces: `/login` 路由可渲染登录表单

- [ ] **Step 1: 验证当前状态（失败证据）**

访问 http://localhost:3000/login，预期看到 Next.js 404 页面。

- [ ] **Step 2: 创建登录页面**

```tsx
'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await login(email, password);
    } catch (err: any) {
      setError(err.response?.data?.detail || '登录失败，请检查邮箱和密码');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-2xl font-bold text-center text-gray-800 mb-2">书童</h1>
        <p className="text-center text-gray-500 mb-8">登录您的账户</p>

        {error && (
          <div className="mb-4 p-3 bg-red-50 text-red-600 rounded-md text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              邮箱
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
              placeholder="请输入邮箱"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              密码
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
              placeholder="请输入密码"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-2.5 px-4 bg-primary-600 text-white rounded-md font-medium hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? '登录中...' : '登录'}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-600">
          还没有账户？{' '}
          <Link href="/register" className="text-primary-600 hover:underline">
            立即注册
          </Link>
        </p>
      </div>
    </main>
  );
}
```

- [ ] **Step 3: 验证登录页面可访问**

访问 http://localhost:3000/login，预期看到登录表单，不再 404。

- [ ] **Step 4: 提交**

```bash
git add frontend/src/app/login/page.tsx
git commit -m "fix: 添加登录页面"
```

---

### Task 2: 创建注册页面

**Files:**
- Create: `frontend/src/app/register/page.tsx`

**Interfaces:**
- Consumes: `useAuth().register(username, email, password)` from `frontend/src/hooks/useAuth.tsx`
- Produces: `/register` 路由可渲染注册表单

- [ ] **Step 1: 验证当前状态（失败证据）**

访问 http://localhost:3000/register，预期看到 Next.js 404 页面。

- [ ] **Step 2: 创建注册页面**

```tsx
'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';

export default function RegisterPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { register } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('两次输入的密码不一致');
      return;
    }

    setIsLoading(true);

    try {
      await register(username, email, password);
    } catch (err: any) {
      setError(err.response?.data?.detail || '注册失败，请检查输入信息');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-2xl font-bold text-center text-gray-800 mb-2">书童</h1>
        <p className="text-center text-gray-500 mb-8">创建新账户</p>

        {error && (
          <div className="mb-4 p-3 bg-red-50 text-red-600 rounded-md text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
              用户名
            </label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
              placeholder="请输入用户名"
            />
          </div>

          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              邮箱
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
              placeholder="请输入邮箱"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              密码
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
              placeholder="请输入密码"
            />
          </div>

          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
              确认密码
            </label>
            <input
              id="confirmPassword"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
              placeholder="请再次输入密码"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-2.5 px-4 bg-primary-600 text-white rounded-md font-medium hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? '注册中...' : '注册'}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-600">
          已有账户？{' '}
          <Link href="/login" className="text-primary-600 hover:underline">
            立即登录
          </Link>
        </p>
      </div>
    </main>
  );
}
```

- [ ] **Step 3: 验证注册页面可访问**

访问 http://localhost:3000/register，预期看到注册表单，不再 404。

- [ ] **Step 4: 提交**

```bash
git add frontend/src/app/register/page.tsx
git commit -m "fix: 添加注册页面"
```

---

### Task 3: 端到端验证

**Files:**
- 无需修改文件

- [ ] **Step 1: 确认后端服务可正常注册/登录**

打开浏览器开发者工具，访问 http://localhost:3000/register，填写信息注册，观察网络请求：
- 请求 `POST http://localhost:8000/api/v1/auth/register` 应返回 200
- 注册成功后页面应跳转至 `/dashboard`

- [ ] **Step 2: 验证登录流程**

访问 http://localhost:3000/login，使用刚注册的账户登录：
- 请求 `POST http://localhost:8000/api/v1/auth/login` 应返回 200
- 登录成功后页面应跳转至 `/dashboard`

- [ ] **Step 3: 运行前端构建检查**

```bash
cd frontend
npm run build
```

预期：构建成功，无 TypeScript 类型错误。

- [ ] **Step 4: 提交（若仅有验证，无需单独提交）**

---

## Self-Review

- Spec coverage: 两个缺失页面各一个任务，验证一个任务。覆盖完整。
- Placeholder scan: 无 TBD/TODO/模糊描述，代码完整。
- Type consistency: `useAuth` 中的 `login(email, password)` 和 `register(username, email, password)` 签名与页面表单一致。
