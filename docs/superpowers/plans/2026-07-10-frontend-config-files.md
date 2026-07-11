# 前端基础配置文件创建计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为书童项目前端补齐缺失的基础配置文件和入口文件，使项目可安装依赖、可构建、可运行。

**Architecture:** 基于 Next.js 14 App Router + TypeScript + Tailwind CSS 的前端基础配置；通过 package.json 锁定依赖版本，通过 tsconfig/next.config/tailwind/postcss 配置构建与样式，通过 layout.tsx/page.tsx 提供根布局和首页入口。

**Tech Stack:** Next.js 14.1.0, React 18.2.0, TypeScript 5.3.3, Tailwind CSS 3.4.1, PostCSS 8.4.33, Autoprefixer 10.4.17

## Global Constraints

- 工作目录：`D:/Projects/shutong/frontend`
- 不要修改现有的 `src/components` 和 `src/app` 下的页面文件
- package.json 中的依赖版本必须与现有代码兼容
- 创建 `.gitignore` 文件（如果还没有）
- 所有新文件内容严格采用用户提供的规格

---

## Task 1: 创建 package.json 与 .gitignore

**Files:**
- Create: `D:/Projects/shutong/frontend/package.json`
- Create: `D:/Projects/shutong/frontend/.gitignore`（如缺失）

**Interfaces:**
- Produces: `package.json` 定义项目元数据、scripts、dependencies、devDependencies
- Produces: `.gitignore` 忽略 node_modules、.next、out、.env 等

- [ ] **Step 1: 创建 package.json**

```json
{
  "name": "shutong-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.1.0",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "axios": "1.6.5",
    "tailwind-merge": "2.2.0",
    "clsx": "2.1.0",
    "lucide-react": "0.312.0"
  },
  "devDependencies": {
    "@types/node": "20.11.5",
    "@types/react": "18.2.48",
    "@types/react-dom": "18.2.18",
    "autoprefixer": "10.4.17",
    "postcss": "8.4.33",
    "tailwindcss": "3.4.1",
    "typescript": "5.3.3"
  }
}
```

- [ ] **Step 2: 创建 .gitignore**

```gitignore
# Dependencies
node_modules/

# Next.js
.next/
out/

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
```

- [ ] **Step 3: 提交**

```bash
cd D:/Projects/shutong/frontend
git add package.json .gitignore
git commit -m "chore: 添加前端 package.json 与 .gitignore"
```

---

## Task 2: 创建 TypeScript 与 Next.js 配置文件

**Files:**
- Create: `D:/Projects/shutong/frontend/tsconfig.json`
- Create: `D:/Projects/shutong/frontend/next.config.js`

**Interfaces:**
- Produces: `tsconfig.json` 标准 Next.js TypeScript 配置
- Produces: `next.config.js` Next.js 运行时配置（允许 localhost 图片域名）

- [ ] **Step 1: 创建 tsconfig.json**

```json
{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

- [ ] **Step 2: 创建 next.config.js**

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ['localhost'],
  },
}

module.exports = nextConfig
```

- [ ] **Step 3: 提交**

```bash
cd D:/Projects/shutong/frontend
git add tsconfig.json next.config.js
git commit -m "chore: 添加前端 TypeScript 与 Next.js 配置"
```

---

## Task 3: 创建 Tailwind CSS 与 PostCSS 配置

**Files:**
- Create: `D:/Projects/shutong/frontend/tailwind.config.ts`
- Create: `D:/Projects/shutong/frontend/postcss.config.js`

**Interfaces:**
- Produces: `tailwind.config.ts` 样式主题配置（content 路径、自定义 primary 色阶）
- Produces: `postcss.config.js` PostCSS 插件配置

- [ ] **Step 1: 创建 tailwind.config.ts**

```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
      },
    },
  },
  plugins: [],
}

export default config
```

- [ ] **Step 2: 创建 postcss.config.js**

```javascript
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

- [ ] **Step 3: 提交**

```bash
cd D:/Projects/shutong/frontend
git add tailwind.config.ts postcss.config.js
git commit -m "chore: 添加前端 Tailwind CSS 与 PostCSS 配置"
```

---

## Task 4: 创建全局样式、根布局与首页

**Files:**
- Create: `D:/Projects/shutong/frontend/src/app/globals.css`
- Create: `D:/Projects/shutong/frontend/src/app/layout.tsx`
- Create: `D:/Projects/shutong/frontend/src/app/page.tsx`

**Interfaces:**
- Produces: `globals.css` 注入 Tailwind 指令
- Produces: `layout.tsx` 中文语言、标题"书童 - 智能学习助手"、根布局
- Produces: `page.tsx` 首页，显示书童标题和登录/注册按钮

- [ ] **Step 1: 创建 globals.css**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

- [ ] **Step 2: 创建 layout.tsx**

```tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

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
      <body className={inter.className}>{children}</body>
    </html>
  )
}
```

- [ ] **Step 3: 创建 page.tsx**

```tsx
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
```

- [ ] **Step 4: 提交**

```bash
cd D:/Projects/shutong/frontend
git add src/app/globals.css src/app/layout.tsx src/app/page.tsx
git commit -m "feat: 添加前端全局样式、根布局与首页"
```

---

## Task 5: 安装依赖并验证构建

**Files:**
- Modify: `D:/Projects/shutong/frontend/package-lock.json`（由 npm install 自动生成）

**Interfaces:**
- Consumes: `package.json` 中声明的依赖
- Produces: `node_modules/` 和 `package-lock.json`

- [ ] **Step 1: 安装依赖**

```bash
cd D:/Projects/shutong/frontend
npm install
```

- [ ] **Step 2: 验证构建**

```bash
cd D:/Projects/shutong/frontend
npm run build
```

Expected: 构建成功退出（exit 0），无 TypeScript/Next.js 配置相关错误。

- [ ] **Step 3: 提交 package-lock.json**

```bash
cd D:/Projects/shutong/frontend
git add package-lock.json
git commit -m "chore: 锁定前端依赖版本"
```

---

## Self-Review

1. **Spec coverage:** 用户要求创建的 8 个文件均已覆盖；.gitignore 检查逻辑已包含。
2. **Placeholder scan:** 无 TBD/TODO/implement later；所有代码块均为完整内容。
3. **Type consistency:** `layout.tsx` 使用 React.ReactNode 类型；`page.tsx` 为默认导出的 React 组件；与现有代码风格一致。
