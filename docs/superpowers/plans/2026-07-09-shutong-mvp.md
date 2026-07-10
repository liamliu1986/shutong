# 书童 MVP 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建书童智能学习助手 MVP，包含用户认证、知识图谱、错题本、题库管理和自由组卷功能

**Architecture:** 前后端分离架构，Next.js 14 前端 + FastAPI 后端 + MongoDB 数据存储 + Neo4j 知识图谱

**Tech Stack:** Next.js 14, TypeScript, Tailwind CSS, shadcn/ui, Python 3.11, FastAPI, MongoDB, Neo4j, Docker

## Global Constraints

- Python 版本：3.11+
- Node.js 版本：20+
- 数据库：MongoDB 7.x + Neo4j 5.x
- API 格式：RESTful JSON
- 认证方式：JWT Bearer Token
- 测试框架：pytest（后端）、vitest（前端）
- 代码风格：Black（Python）、Prettier（TypeScript）

---

## 文件结构总览

```
shutong/
├── docker-compose.yml
├── .gitignore
├── .env.example
│
├── backend/
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── alembic.ini
│   ├── alembic/
│   │   └── versions/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── child.py
│   │   │   ├── mistake.py
│   │   │   ├── question_bank.py
│   │   │   ├── paper.py
│   │   │   └── study_plan.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── child.py
│   │   │   ├── mistake.py
│   │   │   ├── question_bank.py
│   │   │   ├── paper.py
│   │   │   └── study_plan.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── children.py
│   │   │   ├── knowledge_graph.py
│   │   │   ├── mistakes.py
│   │   │   ├── question_bank.py
│   │   │   ├── papers.py
│   │   │   └── generate_paper.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── user_service.py
│   │   │   ├── knowledge_graph_service.py
│   │   │   ├── mistake_service.py
│   │   │   ├── question_bank_service.py
│   │   │   ├── paper_service.py
│   │   │   └── ocr_service.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── security.py
│   │       └── validators.py
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_users.py
│       ├── test_mistakes.py
│       ├── test_question_bank.py
│       └── test_papers.py
│
├── frontend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── Dockerfile
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   ├── register/
│   │   │   │   └── page.tsx
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx
│   │   │   ├── knowledge-graph/
│   │   │   │   └── page.tsx
│   │   │   ├── mistakes/
│   │   │   │   ├── page.tsx
│   │   │   │   └── add/
│   │   │   │       └── page.tsx
│   │   │   ├── question-bank/
│   │   │   │   ├── page.tsx
│   │   │   │   └── upload/
│   │   │   │       └── page.tsx
│   │   │   └── generate-paper/
│   │   │       └── page.tsx
│   │   ├── components/
│   │   │   ├── ui/
│   │   │   ├── layout/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── MainLayout.tsx
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   └── RegisterForm.tsx
│   │   │   ├── mistakes/
│   │   │   │   ├── MistakeList.tsx
│   │   │   │   ├── MistakeCard.tsx
│   │   │   │   └── MistakeForm.tsx
│   │   │   └── question-bank/
│   │   │       ├── QuestionList.tsx
│   │   │       ├── QuestionCard.tsx
│   │   │       └── PaperUploadForm.tsx
│   │   ├── lib/
│   │   │   ├── api.ts
│   │   │   ├── auth.ts
│   │   │   └── utils.ts
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   └── useApi.ts
│   │   └── types/
│   │       └── index.ts
│   └── public/
│
└── docs/
    └── superpowers/
        ├── specs/
        │   └── 2026-07-09-shutong-design.md
        └── plans/
            └── 2026-07-09-shutong-mvp.md
```

---

## Phase 1: 项目初始化与基础设施

### Task 1: 初始化项目仓库与 Docker 配置

**Files:**
- Create: `docker-compose.yml`
- Create: `.gitignore`
- Create: `.env.example`
- Create: `backend/Dockerfile`
- Create: `frontend/Dockerfile`

**Interfaces:**
- Produces: Docker 服务配置，包含 MongoDB、Neo4j、Backend、Frontend

- [ ] **Step 1: 创建 .gitignore 文件**

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
*.egg-info/
dist/
build/

# Node
node_modules/
.next/
out/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Docker
docker-compose.override.yml

# MongoDB data
mongo-data/

# Neo4j data
neo4j-data/
neo4j-logs/
```

- [ ] **Step 2: 创建 .env.example 文件**

```env
# MongoDB
MONGODB_URI=mongodb://mongodb:27017/shutong
MONGODB_ROOT_USER=admin
MONGODB_ROOT_PASSWORD=password123

# Neo4j
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password123

# Backend
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OCR Service (Baidu)
BAIDU_OCR_API_KEY=
BAIDU_OCR_SECRET_KEY=

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

- [ ] **Step 3: 创建 docker-compose.yml**

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:7
    container_name: shutong-mongodb
    restart: unless-stopped
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGODB_ROOT_USER:-admin}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGODB_ROOT_PASSWORD:-password123}
      MONGO_INITDB_DATABASE: shutong
    volumes:
      - mongo-data:/data/db
      - ./scripts/mongo-init.js:/docker-entrypoint-initdb.d/init.js
    networks:
      - shutong-network

  neo4j:
    image: neo4j:5
    container_name: shutong-neo4j
    restart: unless-stopped
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      NEO4J_AUTH: ${NEO4J_USER:-neo4j}/${NEO4J_PASSWORD:-password123}
      NEO4J_PLUGINS: '["apoc"]'
    volumes:
      - neo4j-data:/data
      - neo4j-logs:/logs
    networks:
      - shutong-network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: shutong-backend
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/shutong
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=${NEO4J_USER:-neo4j}
      - NEO4J_PASSWORD=${NEO4J_PASSWORD:-password123}
      - SECRET_KEY=${SECRET_KEY:-change-me-in-production}
    depends_on:
      - mongodb
      - neo4j
    volumes:
      - ./backend:/app
      - upload-data:/app/uploads
    networks:
      - shutong-network

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: shutong-frontend
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
    depends_on:
      - backend
    volumes:
      - ./frontend/src:/app/src
    networks:
      - shutong-network

volumes:
  mongo-data:
  neo4j-data:
  neo4j-logs:
  upload-data:

networks:
  shutong-network:
    driver: bridge
```

- [ ] **Step 4: 创建 backend/Dockerfile**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p uploads/images uploads/gifs uploads/papers

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

- [ ] **Step 5: 创建 frontend/Dockerfile**

```dockerfile
FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy application code
COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
```

- [ ] **Step 6: 初始化 Git 仓库并提交**

```bash
git init
git add .
git commit -m "chore: 初始化项目仓库和 Docker 配置"
```

---

### Task 2: 后端基础框架搭建

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/app/__init__.py`
- Create: `backend/app/main.py`
- Create: `backend/app/config.py`
- Create: `backend/app/database.py`
- Create: `backend/tests/__init__.py`
- Create: `backend/tests/conftest.py`

**Interfaces:**
- Produces: FastAPI 应用实例，数据库连接

- [ ] **Step 1: 创建 requirements.txt**

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0
motor==3.3.2
pymongo==4.6.1
neo4j==5.17.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
aiofiles==23.2.1
httpx==0.26.0
python-dotenv==1.0.0
alembic==1.13.1
pytest==7.4.4
pytest-asyncio==0.23.3
pytest-mock==3.12.0
```

- [ ] **Step 2: 创建 app/config.py**

```python
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "书童"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # MongoDB
    MONGODB_URI: str = "mongodb://localhost:27017/shutong"
    
    # Neo4j
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password123"
    
    # JWT
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OCR
    BAIDU_OCR_API_KEY: str = ""
    BAIDU_OCR_SECRET_KEY: str = ""
    
    # 文件上传
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

- [ ] **Step 3: 创建 app/database.py**

```python
from motor.motor_asyncio import AsyncIOMotorClient
from neo4j import AsyncGraphDatabase
from app.config import get_settings

settings = get_settings()

# MongoDB
mongodb_client: AsyncIOMotorClient = None
mongodb = None

# Neo4j
neo4j_driver = None


async def connect_mongodb():
    global mongodb_client, mongodb
    mongodb_client = AsyncIOMotorClient(settings.MONGODB_URI)
    mongodb = mongodb_client.get_database()
    
    # 创建索引
    await mongodb.users.create_index("email", unique=True)
    await mongodb.users.create_index("username", unique=True)
    await mongodb.mistakes.create_index("child_id")
    await mongodb.mistakes.create_index("knowledge_points")
    await mongodb.question_bank.create_index("child_id")
    await mongodb.question_bank.create_index("subject")
    await mongodb.papers.create_index("child_id")
    
    print("✅ MongoDB 连接成功")


async def close_mongodb():
    global mongodb_client
    if mongodb_client:
        mongodb_client.close()
        print("❌ MongoDB 连接关闭")


async def connect_neo4j():
    global neo4j_driver
    neo4j_driver = AsyncGraphDatabase.driver(
        settings.NEO4J_URI,
        auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
    )
    print("✅ Neo4j 连接成功")


async def close_neo4j():
    global neo4j_driver
    if neo4j_driver:
        await neo4j_driver.close()
        print("❌ Neo4j 连接关闭")


def get_mongodb():
    return mongodb


def get_neo4j():
    return neo4j_driver
```

- [ ] **Step 4: 创建 app/main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.database import connect_mongodb, close_mongodb, connect_neo4j, close_neo4j
from app.api import auth, users, children, knowledge_graph, mistakes, question_bank, papers, generate_paper

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时连接数据库
    await connect_mongodb()
    await connect_neo4j()
    yield
    # 关闭时断开连接
    await close_mongodb()
    await close_neo4j()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/v1", tags=["认证"])
app.include_router(users.router, prefix="/api/v1", tags=["用户"])
app.include_router(children.router, prefix="/api/v1", tags=["孩子管理"])
app.include_router(knowledge_graph.router, prefix="/api/v1", tags=["知识图谱"])
app.include_router(mistakes.router, prefix="/api/v1", tags=["错题本"])
app.include_router(question_bank.router, prefix="/api/v1", tags=["题库"])
app.include_router(papers.router, prefix="/api/v1", tags=["试卷"])
app.include_router(generate_paper.router, prefix="/api/v1", tags=["组卷"])


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

- [ ] **Step 5: 创建 tests/conftest.py**

```python
import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database import connect_mongodb, close_mongodb, connect_neo4j, close_neo4j


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def setup_database():
    await connect_mongodb()
    await connect_neo4j()
    yield
    await close_mongodb()
    await close_neo4j()


@pytest.fixture
async def client(setup_database) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_user(client: AsyncClient):
    """创建测试用户并返回"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Test123456"
    }
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    return response.json()
```

- [ ] **Step 6: 运行基础测试验证框架**

```bash
cd backend
pytest tests/ -v
```

Expected: 测试通过或显示 "no tests ran"

- [ ] **Step 7: 提交代码**

```bash
git add backend/
git commit -m "feat: 搭建后端基础框架"
```

---

### Task 3: 前端基础框架搭建

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/next.config.js`
- Create: `frontend/tailwind.config.ts`
- Create: `frontend/src/app/layout.tsx`
- Create: `frontend/src/app/page.tsx`
- Create: `frontend/src/lib/api.ts`
- Create: `frontend/src/types/index.ts`

**Interfaces:**
- Produces: Next.js 应用，API 客户端

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

- [ ] **Step 3: 创建 tailwind.config.ts**

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

- [ ] **Step 4: 创建 src/app/layout.tsx**

```typescript
import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: '书童 - 智能学习助手',
  description: '帮助家长辅助孩子学习的智能学习助手',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  )
}
```

- [ ] **Step 5: 创建 src/app/globals.css**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 0, 0, 0;
  --background-start-rgb: 214, 219, 220;
  --background-end-rgb: 255, 255, 255;
}

body {
  color: rgb(var(--foreground-rgb));
  background: linear-gradient(
      to bottom,
      transparent,
      rgb(var(--background-end-rgb))
    )
    rgb(var(--background-start-rgb));
}
```

- [ ] **Step 6: 创建 src/app/page.tsx**

```typescript
export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold mb-4">📚 书童</h1>
      <p className="text-xl text-gray-600">智能学习助手</p>
      <div className="mt-8 flex gap-4">
        <a
          href="/login"
          className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
        >
          登录
        </a>
        <a
          href="/register"
          className="px-6 py-3 border border-primary-600 text-primary-600 rounded-lg hover:bg-primary-50"
        >
          注册
        </a>
      </div>
    </main>
  )
}
```

- [ ] **Step 7: 创建 src/lib/api.ts**

```typescript
import axios from 'axios'

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token')
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default api

// 认证 API
export const authAPI = {
  login: (data: { email: string; password: string }) =>
    api.post('/auth/login', data),
  register: (data: { username: string; email: string; password: string }) =>
    api.post('/auth/register', data),
  getProfile: () => api.get('/users/me'),
}

// 孩子 API
export const childrenAPI = {
  list: () => api.get('/users/me/children'),
  create: (data: { name: string; grade: number; subjects: string[] }) =>
    api.post('/users/me/children', data),
}

// 知识图谱 API
export const knowledgeGraphAPI = {
  getSubjects: () => api.get('/subjects'),
  getSubjectGraph: (id: string) => api.get(`/subjects/${id}/graph`),
}

// 错题本 API
export const mistakesAPI = {
  list: (params?: any) => api.get('/mistakes', { params }),
  create: (data: any) => api.post('/mistakes', data),
  get: (id: string) => api.get(`/mistakes/${id}`),
  update: (id: string, data: any) => api.put(`/mistakes/${id}`, data),
  delete: (id: string) => api.delete(`/mistakes/${id}`),
}

// 题库 API
export const questionBankAPI = {
  list: (params?: any) => api.get('/question-bank', { params }),
  get: (id: string) => api.get(`/question-bank/${id}`),
  update: (id: string, data: any) => api.put(`/question-bank/${id}`, data),
  delete: (id: string) => api.delete(`/question-bank/${id}`),
}

// 试卷 API
export const papersAPI = {
  list: () => api.get('/papers'),
  upload: (formData: FormData) =>
    api.post('/papers', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  get: (id: string) => api.get(`/papers/${id}`),
  recognize: (id: string) => api.post(`/papers/${id}/recognize`),
  getQuestions: (id: string) => api.get(`/papers/${id}/questions`),
  confirm: (id: string, data: any) => api.post(`/papers/${id}/confirm`, data),
}

// 组卷 API
export const generatePaperAPI = {
  preview: (data: any) => api.post('/generate-paper/preview', data),
  create: (data: any) => api.post('/generate-paper', data),
}
```

- [ ] **Step 8: 创建 src/types/index.ts**

```typescript
// 用户类型
export interface User {
  id: string
  username: string
  email: string
  children: Child[]
}

// 孩子类型
export interface Child {
  id: string
  name: string
  grade: number
  subjects: string[]
}

// 知识点类型
export interface KnowledgePoint {
  id: string
  name: string
  description: string
  mastery: number
}

// 错题类型
export interface Mistake {
  id: string
  child_id: string
  subject: string
  grade: number
  chapter: string
  knowledge_points: string[]
  question_image_url: string
  question_text: string
  question_latex: string
  answer: string
  explanation: string
  explanation_gif_url: string
  difficulty: number
  source: string
  tags: string[]
  created_at: string
  updated_at: string
}

// 题库题目类型
export interface Question {
  id: string
  child_id: string
  subject: string
  grade: number
  question_type: 'choice' | 'fill_blank' | 'solve'
  question_text: string
  question_latex: string
  question_image_url: string
  options?: { label: string; content: string; is_correct: boolean }[]
  answer: string
  explanation: string
  chapter: string
  knowledge_point_ids: string[]
  difficulty: number
  tags: string[]
  source_type: 'single' | 'paper'
  source_paper_id?: string
  source_paper_name?: string
  question_index?: number
  used_count: number
  correct_rate: number
}

// 试卷类型
export interface Paper {
  id: string
  child_id: string
  name: string
  subject: string
  grade: number
  images: { page: number; url: string }[]
  question_ids: string[]
  question_count: number
  source: string
  exam_date?: string
  total_score?: number
  status: 'uploaded' | 'processing' | 'completed' | 'failed'
  created_at: string
}

// 学习计划类型
export interface StudyPlan {
  id: string
  child_id: string
  subject: string
  title: string
  description: string
  start_date: string
  end_date: string
  daily_tasks: DailyTask[]
  status: 'active' | 'completed' | 'paused'
  progress: number
}

export interface DailyTask {
  date: string
  tasks: {
    type: 'review' | 'practice' | 'test'
    knowledge_point_id: string
    description: string
    completed: boolean
  }[]
}

// 组卷配置类型
export interface GeneratePaperConfig {
  child_id: string
  subject: string
  grade: number
  total_questions: number
  question_type_distribution: {
    choice: number
    fill_blank: number
    solve: number
  }
  difficulty_distribution: {
    easy: number
    medium: number
    hard: number
  }
  knowledge_point_ids: string[]
  exclude_recent_days?: number
  name?: string
}
```

- [ ] **Step 9: 安装依赖并验证**

```bash
cd frontend
npm install
npm run dev
```

Expected: 开发服务器在 http://localhost:3000 启动

- [ ] **Step 10: 提交代码**

```bash
git add frontend/
git commit -m "feat: 搭建前端基础框架"
```

---

## Phase 2: 用户认证模块

### Task 4: 后端用户认证

**Files:**
- Create: `backend/app/models/user.py`
- Create: `backend/app/schemas/user.py`
- Create: `backend/app/utils/security.py`
- Create: `backend/app/services/auth_service.py`
- Create: `backend/app/api/auth.py`
- Create: `backend/app/dependencies.py`
- Create: `backend/tests/test_auth.py`

**Interfaces:**
- Produces: `/api/v1/auth/register`, `/api/v1/auth/login`, `/api/v1/auth/refresh`

- [ ] **Step 1: 创建 models/user.py**

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


class ChildModel(BaseModel):
    id: str = Field(default_factory=lambda: str(datetime.now().timestamp()))
    name: str
    grade: int = Field(ge=7, le=12)
    subjects: List[str] = []


class UserModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    username: str
    email: str
    password_hash: str
    children: List[ChildModel] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True
```

- [ ] **Step 2: 创建 schemas/user.py**

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    email: str
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    children: List[dict] = []


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class ChildCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    grade: int = Field(..., ge=7, le=12)
    subjects: List[str] = []
```

- [ ] **Step 3: 创建 utils/security.py**

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
```

- [ ] **Step 4: 创建 services/auth_service.py**

```python
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status

from app.database import get_mongodb
from app.models.user import UserModel
from app.schemas.user import UserCreate, UserLogin, TokenResponse, UserResponse
from app.utils.security import verify_password, get_password_hash, create_access_token


class AuthService:
    @staticmethod
    async def register(user_data: UserCreate) -> TokenResponse:
        db = get_mongodb()
        
        # 检查用户是否已存在
        existing_user = await db.users.find_one({
            "$or": [
                {"email": user_data.email},
                {"username": user_data.username}
            ]
        })
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名或邮箱已存在"
            )
        
        # 创建用户
        user_dict = user_data.model_dump()
        user_dict["password_hash"] = get_password_hash(user_data.password)
        del user_dict["password"]
        user_dict["children"] = []
        user_dict["created_at"] = datetime.now()
        user_dict["updated_at"] = datetime.now()
        
        result = await db.users.insert_one(user_dict)
        user_id = str(result.inserted_id)
        
        # 生成 Token
        access_token = create_access_token(data={"sub": user_id})
        
        return TokenResponse(
            access_token=access_token,
            user=UserResponse(
                id=user_id,
                username=user_data.username,
                email=user_data.email,
                children=[]
            )
        )
    
    @staticmethod
    async def login(user_data: UserLogin) -> TokenResponse:
        db = get_mongodb()
        
        # 查找用户
        user = await db.users.find_one({"email": user_data.email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="邮箱或密码错误"
            )
        
        # 验证密码
        if not verify_password(user_data.password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="邮箱或密码错误"
            )
        
        # 生成 Token
        user_id = str(user["_id"])
        access_token = create_access_token(data={"sub": user_id})
        
        return TokenResponse(
            access_token=access_token,
            user=UserResponse(
                id=user_id,
                username=user["username"],
                email=user["email"],
                children=user.get("children", [])
            )
        )
    
    @staticmethod
    async def get_current_user(user_id: str) -> UserResponse:
        db = get_mongodb()
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        return UserResponse(
            id=str(user["_id"]),
            username=user["username"],
            email=user["email"],
            children=user.get("children", [])
        )
```

- [ ] **Step 5: 创建 dependencies.py**

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.security import decode_token
from app.database import get_mongodb
from bson import ObjectId

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证"
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证"
        )
    
    db = get_mongodb()
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    user["id"] = str(user.pop("_id"))
    return user
```

- [ ] **Step 6: 创建 api/auth.py**

```python
from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserLogin, TokenResponse, UserResponse
from app.services.auth_service import AuthService
from app.dependencies import get_current_user

router = APIRouter()


@router.post("/auth/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    """用户注册"""
    return await AuthService.register(user_data)


@router.post("/auth/login", response_model=TokenResponse)
async def login(user_data: UserLogin):
    """用户登录"""
    return await AuthService.login(user_data)


@router.get("/users/me", response_model=UserResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """获取当前用户信息"""
    return UserResponse(
        id=current_user["id"],
        username=current_user["username"],
        email=current_user["email"],
        children=current_user.get("children", [])
    )
```

- [ ] **Step 7: 创建 tests/test_auth.py**

```python
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register(client: AsyncClient):
    """测试用户注册"""
    user_data = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "Test123456"
    }
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["username"] == "newuser"
    assert data["user"]["email"] == "new@example.com"


@pytest.mark.asyncio
async def test_register_duplicate(client: AsyncClient):
    """测试重复注册"""
    user_data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "Test123456"
    }
    # 第一次注册
    await client.post("/api/v1/auth/register", json=user_data)
    
    # 第二次注册应失败
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    """测试用户登录"""
    # 先注册
    user_data = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "Test123456"
    }
    await client.post("/api/v1/auth/register", json=user_data)
    
    # 登录
    login_data = {
        "email": "login@example.com",
        "password": "Test123456"
    }
    response = await client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """测试错误密码登录"""
    login_data = {
        "email": "test@example.com",
        "password": "wrongpassword"
    }
    response = await client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_profile(client: AsyncClient, test_user):
    """测试获取用户信息"""
    token = test_user["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = await client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
```

- [ ] **Step 8: 运行测试验证**

```bash
cd backend
pytest tests/test_auth.py -v
```

Expected: 所有测试通过

- [ ] **Step 9: 提交代码**

```bash
git add backend/
git commit -m "feat: 实现用户认证模块"
```

---

### Task 5: 前端登录注册页面

**Files:**
- Create: `frontend/src/components/auth/LoginForm.tsx`
- Create: `frontend/src/components/auth/RegisterForm.tsx`
- Create: `frontend/src/app/login/page.tsx`
- Create: `frontend/src/app/register/page.tsx`
- Create: `frontend/src/hooks/useAuth.ts`

**Interfaces:**
- Consumes: `/api/v1/auth/register`, `/api/v1/auth/login`
- Produces: 登录/注册页面

- [ ] **Step 1: 创建 hooks/useAuth.ts**

```typescript
'use client'

import { useState, useEffect, createContext, useContext, ReactNode } from 'react'
import { authAPI } from '@/lib/api'
import { User } from '@/types'

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (username: string, email: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      loadUser()
    } else {
      setLoading(false)
    }
  }, [])

  const loadUser = async () => {
    try {
      const response = await authAPI.getProfile()
      setUser(response.data)
    } catch {
      localStorage.removeItem('token')
    } finally {
      setLoading(false)
    }
  }

  const login = async (email: string, password: string) => {
    const response = await authAPI.login({ email, password })
    localStorage.setItem('token', response.data.access_token)
    setUser(response.data.user)
  }

  const register = async (username: string, email: string, password: string) => {
    const response = await authAPI.register({ username, email, password })
    localStorage.setItem('token', response.data.access_token)
    setUser(response.data.user)
  }

  const logout = () => {
    localStorage.removeItem('token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
```

- [ ] **Step 2: 创建 components/auth/LoginForm.tsx**

```typescript
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'

export default function LoginForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await login(email, password)
      router.push('/dashboard')
    } catch (err: any) {
      setError(err.response?.data?.detail || '登录失败，请重试')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="p-3 bg-red-100 text-red-700 rounded-lg">
          {error}
        </div>
      )}
      
      <div>
        <label className="block text-sm font-medium mb-1">邮箱</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">密码</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          required
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
      >
        {loading ? '登录中...' : '登录'}
      </button>
    </form>
  )
}
```

- [ ] **Step 3: 创建 components/auth/RegisterForm.tsx**

```typescript
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'

export default function RegisterForm() {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { register } = useAuth()
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (password !== confirmPassword) {
      setError('两次密码输入不一致')
      return
    }

    if (password.length < 6) {
      setError('密码长度不能少于6位')
      return
    }

    setLoading(true)

    try {
      await register(username, email, password)
      router.push('/dashboard')
    } catch (err: any) {
      setError(err.response?.data?.detail || '注册失败，请重试')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="p-3 bg-red-100 text-red-700 rounded-lg">
          {error}
        </div>
      )}
      
      <div>
        <label className="block text-sm font-medium mb-1">用户名</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          required
          minLength={2}
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">邮箱</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">密码</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          required
          minLength={6}
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">确认密码</label>
        <input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          required
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
      >
        {loading ? '注册中...' : '注册'}
      </button>
    </form>
  )
}
```

- [ ] **Step 4: 创建 app/login/page.tsx**

```typescript
import Link from 'next/link'
import LoginForm from '@/components/auth/LoginForm'
import { AuthProvider } from '@/hooks/useAuth'

export default function LoginPage() {
  return (
    <AuthProvider>
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="w-full max-w-md p-8 bg-white rounded-lg shadow-lg">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold">📚 书童</h1>
            <p className="text-gray-600 mt-2">智能学习助手</p>
          </div>
          
          <h2 className="text-2xl font-bold text-center mb-6">登录</h2>
          
          <LoginForm />
          
          <p className="text-center mt-6 text-gray-600">
            还没有账号？
            <Link href="/register" className="text-primary-600 hover:underline ml-1">
              立即注册
            </Link>
          </p>
        </div>
      </div>
    </AuthProvider>
  )
}
```

- [ ] **Step 5: 创建 app/register/page.tsx**

```typescript
import Link from 'next/link'
import RegisterForm from '@/components/auth/RegisterForm'
import { AuthProvider } from '@/hooks/useAuth'

export default function RegisterPage() {
  return (
    <AuthProvider>
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="w-full max-w-md p-8 bg-white rounded-lg shadow-lg">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold">📚 书童</h1>
            <p className="text-gray-600 mt-2">智能学习助手</p>
          </div>
          
          <h2 className="text-2xl font-bold text-center mb-6">注册</h2>
          
          <RegisterForm />
          
          <p className="text-center mt-6 text-gray-600">
            已有账号？
            <Link href="/login" className="text-primary-600 hover:underline ml-1">
              立即登录
            </Link>
          </p>
        </div>
      </div>
    </AuthProvider>
  )
}
```

- [ ] **Step 6: 验证前端页面**

```bash
cd frontend
npm run dev
```

访问 http://localhost:3000/login 和 http://localhost:3000/register 验证页面

- [ ] **Step 7: 提交代码**

```bash
git add frontend/
git commit -m "feat: 实现登录注册页面"
```

---

## Phase 3: 知识图谱模块

### Task 6: 知识图谱数据初始化

**Files:**
- Create: `backend/app/services/knowledge_graph_service.py`
- Create: `backend/app/api/knowledge_graph.py`
- Create: `backend/scripts/init_math_graph.py`
- Create: `backend/tests/test_knowledge_graph.py`

**Interfaces:**
- Produces: Neo4j 知识图谱数据，`/api/v1/subjects`, `/api/v1/subjects/{id}/graph`

- [ ] **Step 1: 创建 knowledge_graph_service.py**

```python
from neo4j import AsyncSession
from typing import List, Optional
from app.database import get_neo4j


class KnowledgeGraphService:
    @staticmethod
    async def init_math_graph():
        """初始化数学知识图谱"""
        driver = get_neo4j()
        async with driver.session() as session:
            # 清空现有数据
            await session.run("MATCH (n) DETACH DELETE n")
            
            # 创建学科节点
            await session.run("""
                CREATE (s:Subject {
                    id: 'math',
                    name: '数学',
                    grade_level: '7-12'
                })
            """)
            
            # 创建章节节点
            chapters = [
                {"id": "ch1", "name": "二次函数", "order": 1},
                {"id": "ch2", "name": "一次函数", "order": 2},
                {"id": "ch3", "name": "方程与不等式", "order": 3},
                {"id": "ch4", "name": "几何图形", "order": 4},
            ]
            
            for ch in chapters:
                await session.run("""
                    MATCH (s:Subject {id: 'math'})
                    CREATE (c:Chapter {
                        id: $id,
                        name: $name,
                        order: $order
                    })
                    CREATE (s)-[:HAS_CHAPTER {order: $order}]->(c)
                """, **ch)
            
            # 创建知识点节点
            knowledge_points = [
                # 二次函数
                {"id": "kp1", "name": "二次函数的定义", "chapter": "ch1", "importance": 5},
                {"id": "kp2", "name": "二次函数的图像", "chapter": "ch1", "importance": 5},
                {"id": "kp3", "name": "二次函数的性质", "chapter": "ch1", "importance": 4},
                {"id": "kp4", "name": "二次函数的应用", "chapter": "ch1", "importance": 3},
                # 一次函数
                {"id": "kp5", "name": "一次函数的定义", "chapter": "ch2", "importance": 4},
                {"id": "kp6", "name": "一次函数的图像", "chapter": "ch2", "importance": 4},
                {"id": "kp7", "name": "一次函数的性质", "chapter": "ch2", "importance": 4},
                # 方程与不等式
                {"id": "kp8", "name": "一元二次方程", "chapter": "ch3", "importance": 5},
                {"id": "kp9", "name": "不等式", "chapter": "ch3", "importance": 4},
                # 几何图形
                {"id": "kp10", "name": "三角形", "chapter": "ch4", "importance": 4},
                {"id": "kp11", "name": "四边形", "chapter": "ch4", "importance": 4},
                {"id": "kp12", "name": "圆", "chapter": "ch4", "importance": 4},
            ]
            
            for kp in knowledge_points:
                await session.run("""
                    MATCH (c:Chapter {id: $chapter})
                    CREATE (kp:KnowledgePoint {
                        id: $id,
                        name: $name,
                        description: '',
                        importance: $importance
                    })
                    CREATE (c)-[:HAS_KNOWLEDGE_POINT]->(kp)
                """, **kp)
            
            # 创建知识点关联关系
            relations = [
                ("kp1", "kp2"),  # 二次函数定义 → 图像
                ("kp2", "kp3"),  # 图像 → 性质
                ("kp3", "kp4"),  # 性质 → 应用
                ("kp5", "kp6"),  # 一次函数定义 → 图像
                ("kp6", "kp7"),  # 图像 → 性质
                ("kp5", "kp1"),  # 一次函数 → 二次函数（前置）
                ("kp8", "kp1"),  # 方程 → 二次函数
            ]
            
            for from_id, to_id in relations:
                await session.run("""
                    MATCH (a:KnowledgePoint {id: $from_id})
                    MATCH (b:KnowledgePoint {id: $to_id})
                    CREATE (a)-[:RELATED_TO]->(b)
                """, from_id=from_id, to_id=to_id)
            
            print("✅ 数学知识图谱初始化完成")
    
    @staticmethod
    async def get_subjects() -> List[dict]:
        """获取所有学科"""
        driver = get_neo4j()
        async with driver.session() as session:
            result = await session.run("""
                MATCH (s:Subject)
                RETURN s.id as id, s.name as name, s.grade_level as grade_level
            """)
            subjects = []
            async for record in result:
                subjects.append({
                    "id": record["id"],
                    "name": record["name"],
                    "grade_level": record["grade_level"]
                })
            return subjects
    
    @staticmethod
    async def get_subject_graph(subject_id: str) -> dict:
        """获取学科知识图谱"""
        driver = get_neo4j()
        async with driver.session() as session:
            # 获取章节
            chapters_result = await session.run("""
                MATCH (s:Subject {id: $subject_id})-[:HAS_CHAPTER]->(c:Chapter)
                RETURN c.id as id, c.name as name, c.order as order
                ORDER BY c.order
            """, subject_id=subject_id)
            
            chapters = []
            async for record in chapters_result:
                # 获取每个章节的知识点
                kps_result = await session.run("""
                    MATCH (c:Chapter {id: $chapter_id})-[:HAS_KNOWLEDGE_POINT]->(kp:KnowledgePoint)
                    RETURN kp.id as id, kp.name as name, kp.importance as importance
                """, chapter_id=record["id"])
                
                kps = []
                async for kp_record in kps_result:
                    kps.append({
                        "id": kp_record["id"],
                        "name": kp_record["name"],
                        "importance": kp_record["importance"]
                    })
                
                chapters.append({
                    "id": record["id"],
                    "name": record["name"],
                    "order": record["order"],
                    "knowledge_points": kps
                })
            
            # 获取知识点关联关系
            relations_result = await session.run("""
                MATCH (a:KnowledgePoint)-[:RELATED_TO]->(b:KnowledgePoint)
                RETURN a.id as from_id, b.id as to_id
            """)
            
            relations = []
            async for record in relations_result:
                relations.append({
                    "from": record["from_id"],
                    "to": record["to_id"]
                })
            
            return {
                "subject_id": subject_id,
                "chapters": chapters,
                "relations": relations
            }
    
    @staticmethod
    async def get_child_mastery(child_id: str, subject_id: str) -> List[dict]:
        """获取孩子对某学科知识点的掌握度"""
        driver = get_neo4j()
        async with driver.session() as session:
            result = await session.run("""
                MATCH (c:Child {id: $child_id})-[g:Grades]->(kp:KnowledgePoint)
                WHERE kp.id IN (
                    MATCH (s:Subject {id: $subject_id})-[:HAS_CHAPTER]->(ch)-[:HAS_KNOWLEDGE_POINT]->(kp2)
                    RETURN kp2.id
                )
                RETURN kp.id as id, kp.name as name, g.mastery as mastery
            """, child_id=child_id, subject_id=subject_id)
            
            mastery_list = []
            async for record in result:
                mastery_list.append({
                    "id": record["id"],
                    "name": record["name"],
                    "mastery": record["mastery"]
                })
            return mastery_list
```

- [ ] **Step 2: 创建 api/knowledge_graph.py**

```python
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.dependencies import get_current_user
from app.services.knowledge_graph_service import KnowledgeGraphService

router = APIRouter()


@router.get("/subjects")
async def get_subjects(current_user: dict = Depends(get_current_user)):
    """获取所有学科"""
    return await KnowledgeGraphService.get_subjects()


@router.get("/subjects/{subject_id}/graph")
async def get_subject_graph(
    subject_id: str,
    current_user: dict = Depends(get_current_user)
):
    """获取学科知识图谱"""
    return await KnowledgeGraphService.get_subject_graph(subject_id)


@router.get("/children/{child_id}/mastery")
async def get_child_mastery(
    child_id: str,
    subject_id: str,
    current_user: dict = Depends(get_current_user)
):
    """获取孩子知识点掌握度"""
    # 验证孩子属于当前用户
    user_children = [c["id"] for c in current_user.get("children", [])]
    if child_id not in user_children:
        raise HTTPException(status_code=403, detail="无权访问该孩子的数据")
    
    return await KnowledgeGraphService.get_child_mastery(child_id, subject_id)
```

- [ ] **Step 3: 创建 scripts/init_math_graph.py**

```python
"""初始化数学知识图谱的脚本"""
import asyncio
from app.database import connect_neo4j, close_neo4j
from app.services.knowledge_graph_service import KnowledgeGraphService


async def main():
    await connect_neo4j()
    await KnowledgeGraphService.init_math_graph()
    await close_neo4j()
    print("初始化完成！")


if __name__ == "__main__":
    asyncio.run(main())
```

- [ ] **Step 4: 创建 tests/test_knowledge_graph.py**

```python
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_subjects(client: AsyncClient, test_user):
    """测试获取学科列表"""
    token = test_user["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = await client.get("/api/v1/subjects", headers=headers)
    assert response.status_code == 200
    subjects = response.json()
    assert isinstance(subjects, list)


@pytest.mark.asyncio
async def test_get_subject_graph(client: AsyncClient, test_user):
    """测试获取学科知识图谱"""
    token = test_user["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 先初始化知识图谱
    from app.services.knowledge_graph_service import KnowledgeGraphService
    await KnowledgeGraphService.init_math_graph()
    
    response = await client.get("/api/v1/subjects/math/graph", headers=headers)
    assert response.status_code == 200
    graph = response.json()
    assert "chapters" in graph
    assert "relations" in graph
```

- [ ] **Step 5: 运行测试验证**

```bash
cd backend
pytest tests/test_knowledge_graph.py -v
```

- [ ] **Step 6: 提交代码**

```bash
git add backend/
git commit -m "feat: 实现知识图谱模块"
```

---

## Phase 4: 错题本模块

### Task 7: 错题本后端实现

**Files:**
- Create: `backend/app/models/mistake.py`
- Create: `backend/app/schemas/mistake.py`
- Create: `backend/app/services/mistake_service.py`
- Create: `backend/app/services/ocr_service.py`
- Create: `backend/app/api/mistakes.py`
- Create: `backend/tests/test_mistakes.py`

**Interfaces:**
- Produces: `/api/v1/mistakes` CRUD API

- [ ] **Step 1: 创建 models/mistake.py**

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MistakeModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    child_id: str
    subject: str
    grade: int
    chapter: str
    knowledge_points: List[str] = []
    
    question_image_url: str = ""
    question_text: str = ""
    question_latex: str = ""
    
    answer: str = ""
    explanation: str = ""
    explanation_gif_url: str = ""
    
    difficulty: int = Field(ge=1, le=5, default=3)
    source: str = ""
    tags: List[str] = []
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True
```

- [ ] **Step 2: 创建 schemas/mistake.py**

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MistakeCreate(BaseModel):
    child_id: str
    subject: str
    grade: int = Field(ge=7, le=12)
    chapter: str
    knowledge_points: List[str] = []
    
    question_image_url: str = ""
    question_text: str
    question_latex: str = ""
    
    answer: str = ""
    explanation: str = ""
    
    difficulty: int = Field(ge=1, le=5, default=3)
    source: str = ""
    tags: List[str] = []


class MistakeUpdate(BaseModel):
    subject: Optional[str] = None
    chapter: Optional[str] = None
    knowledge_points: Optional[List[str]] = None
    question_text: Optional[str] = None
    answer: Optional[str] = None
    explanation: Optional[str] = None
    difficulty: Optional[int] = None
    tags: Optional[List[str]] = None


class MistakeResponse(BaseModel):
    id: str
    child_id: str
    subject: str
    grade: int
    chapter: str
    knowledge_points: List[str]
    question_image_url: str
    question_text: str
    question_latex: str
    answer: str
    explanation: str
    explanation_gif_url: str
    difficulty: int
    source: str
    tags: List[str]
    created_at: datetime
    updated_at: datetime


class MistakeListResponse(BaseModel):
    items: List[MistakeResponse]
    total: int
    page: int
    page_size: int
```

- [ ] **Step 3: 创建 services/ocr_service.py**

```python
import httpx
from typing import Optional
from app.config import get_settings

settings = get_settings()


class OCRService:
    @staticmethod
    async def recognize_image(image_url: str) -> dict:
        """识别图片中的文字"""
        # 这里使用简化的 OCR 逻辑
        # 实际应调用百度 OCR API
        
        # 模拟 OCR 结果
        return {
            "text": "已知函数f(x)=x²+2x+1，求f(2)的值。",
            "latex": "f(x)=x^2+2x+1",
            "confidence": 0.95,
            "detected_subject": "数学",
            "detected_chapter": "二次函数",
            "suggested_knowledge_points": [
                {"id": "kp1", "name": "二次函数的定义", "confidence": 0.9}
            ]
        }
    
    @staticmethod
    async def recognize_paper(image_url: str) -> dict:
        """识别试卷，返回切题结果"""
        # 模拟试卷识别
        return {
            "total_questions": 20,
            "questions": [
                {
                    "index": 1,
                    "type": "choice",
                    "text": "下列哪个是二次函数？",
                    "image_url": "/uploads/crops/q1.jpg"
                }
                # ... 更多题目
            ]
        }
```

- [ ] **Step 4: 创建 services/mistake_service.py**

```python
from datetime import datetime
from typing import Optional, List
from bson import ObjectId
from fastapi import HTTPException

from app.database import get_mongodb
from app.schemas.mistake import MistakeCreate, MistakeUpdate, MistakeResponse, MistakeListResponse


class MistakeService:
    @staticmethod
    async def create_mistake(data: MistakeCreate) -> MistakeResponse:
        db = get_mongodb()
        
        mistake_dict = data.model_dump()
        mistake_dict["created_at"] = datetime.now()
        mistake_dict["updated_at"] = datetime.now()
        
        result = await db.mistakes.insert_one(mistake_dict)
        mistake_id = str(result.inserted_id)
        
        return MistakeResponse(
            id=mistake_id,
            **mistake_dict
        )
    
    @staticmethod
    async def get_mistakes(
        child_id: str,
        subject: Optional[str] = None,
        chapter: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> MistakeListResponse:
        db = get_mongodb()
        
        query = {"child_id": child_id}
        if subject:
            query["subject"] = subject
        if chapter:
            query["chapter"] = chapter
        
        total = await db.mistakes.count_documents(query)
        
        cursor = db.mistakes.find(query) \
            .sort("created_at", -1) \
            .skip((page - 1) * page_size) \
            .limit(page_size)
        
        items = []
        async for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            items.append(MistakeResponse(**doc))
        
        return MistakeListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size
        )
    
    @staticmethod
    async def get_mistake(mistake_id: str) -> MistakeResponse:
        db = get_mongodb()
        
        doc = await db.mistakes.find_one({"_id": ObjectId(mistake_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="错题不存在")
        
        doc["id"] = str(doc.pop("_id"))
        return MistakeResponse(**doc)
    
    @staticmethod
    async def update_mistake(mistake_id: str, data: MistakeUpdate) -> MistakeResponse:
        db = get_mongodb()
        
        update_data = {k: v for k, v in data.model_dump().items() if v is not None}
        update_data["updated_at"] = datetime.now()
        
        result = await db.mistakes.update_one(
            {"_id": ObjectId(mistake_id)},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="错题不存在")
        
        return await MistakeService.get_mistake(mistake_id)
    
    @staticmethod
    async def delete_mistake(mistake_id: str):
        db = get_mongodb()
        
        result = await db.mistakes.delete_one({"_id": ObjectId(mistake_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="错题不存在")
        
        return {"message": "删除成功"}
```

- [ ] **Step 5: 创建 api/mistakes.py**

```python
from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.dependencies import get_current_user
from app.schemas.mistake import MistakeCreate, MistakeUpdate, MistakeResponse, MistakeListResponse
from app.services.mistake_service import MistakeService

router = APIRouter()


@router.post("/mistakes", response_model=MistakeResponse)
async def create_mistake(
    data: MistakeCreate,
    current_user: dict = Depends(get_current_user)
):
    """创建错题"""
    # 验证孩子属于当前用户
    user_children = [c["id"] for c in current_user.get("children", [])]
    if data.child_id not in user_children:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="无权操作该孩子的数据")
    
    return await MistakeService.create_mistake(data)


@router.get("/mistakes", response_model=MistakeListResponse)
async def get_mistakes(
    child_id: str,
    subject: Optional[str] = None,
    chapter: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """获取错题列表"""
    return await MistakeService.get_mistakes(
        child_id=child_id,
        subject=subject,
        chapter=chapter,
        page=page,
        page_size=page_size
    )


@router.get("/mistakes/{mistake_id}", response_model=MistakeResponse)
async def get_mistake(
    mistake_id: str,
    current_user: dict = Depends(get_current_user)
):
    """获取错题详情"""
    return await MistakeService.get_mistake(mistake_id)


@router.put("/mistakes/{mistake_id}", response_model=MistakeResponse)
async def update_mistake(
    mistake_id: str,
    data: MistakeUpdate,
    current_user: dict = Depends(get_current_user)
):
    """更新错题"""
    return await MistakeService.update_mistake(mistake_id, data)


@router.delete("/mistakes/{mistake_id}")
async def delete_mistake(
    mistake_id: str,
    current_user: dict = Depends(get_current_user)
):
    """删除错题"""
    return await MistakeService.delete_mistake(mistake_id)


@router.get("/mistakes/{mistake_id}/explanation")
async def get_explanation(
    mistake_id: str,
    current_user: dict = Depends(get_current_user)
):
    """获取 AI 解析（占位）"""
    mistake = await MistakeService.get_mistake(mistake_id)
    return {
        "answer": mistake.answer or "暂无答案",
        "explanation": mistake.explanation or "暂无解析",
        "explanation_gif_url": mistake.explanation_gif_url,
        "steps": []
    }
```

- [ ] **Step 6: 创建 tests/test_mistakes.py**

```python
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_mistake(client: AsyncClient, test_user):
    """测试创建错题"""
    token = test_user["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 先添加一个孩子
    child_data = {"name": "小明", "grade": 9, "subjects": ["数学"]}
    child_response = await client.post("/api/v1/users/me/children", json=child_data, headers=headers)
    child_id = child_response.json()["id"]
    
    # 创建错题
    mistake_data = {
        "child_id": child_id,
        "subject": "数学",
        "grade": 9,
        "chapter": "二次函数",
        "question_text": "已知函数f(x)=x²+2x+1，求f(2)的值。",
        "difficulty": 3
    }
    
    response = await client.post("/api/v1/mistakes", json=mistake_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["question_text"] == mistake_data["question_text"]
    assert "id" in data


@pytest.mark.asyncio
async def test_get_mistakes(client: AsyncClient, test_user):
    """测试获取错题列表"""
    token = test_user["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 获取当前用户的孩子
    user_response = await client.get("/api/v1/users/me", headers=headers)
    children = user_response.json().get("children", [])
    
    if children:
        child_id = children[0]["id"]
        response = await client.get(f"/api/v1/mistakes?child_id={child_id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
```

- [ ] **Step 7: 运行测试验证**

```bash
cd backend
pytest tests/test_mistakes.py -v
```

- [ ] **Step 8: 提交代码**

```bash
git add backend/
git commit -m "feat: 实现错题本模块"
```

---

## Phase 5: 题库管理模块

### Task 8: 题库管理后端实现

**Files:**
- Create: `backend/app/models/question_bank.py`
- Create: `backend/app/schemas/question_bank.py`
- Create: `backend/app/services/question_bank_service.py`
- Create: `backend/app/services/paper_service.py`
- Create: `backend/app/api/question_bank.py`
- Create: `backend/app/api/papers.py`

**Interfaces:**
- Produces: `/api/v1/question-bank`, `/api/v1/papers` API

- [ ] **Step 1: 创建 models/question_bank.py**

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class QuestionOption(BaseModel):
    label: str
    content: str
    is_correct: bool = False


class QuestionModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    child_id: str
    subject: str
    grade: int
    
    question_type: str  # "choice" | "fill_blank" | "solve"
    question_text: str
    question_latex: str = ""
    question_image_url: str = ""
    
    options: List[QuestionOption] = []
    answer: str = ""
    explanation: str = ""
    
    chapter: str = ""
    knowledge_point_ids: List[str] = []
    difficulty: int = Field(ge=1, le=5, default=3)
    tags: List[str] = []
    
    source_type: str = "single"  # "single" | "paper"
    source_paper_id: Optional[str] = None
    source_paper_name: Optional[str] = None
    question_index: Optional[int] = None
    
    used_count: int = 0
    correct_rate: float = 0.0
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True


class PaperModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    child_id: str
    name: str
    subject: str
    grade: int
    
    images: List[dict] = []
    question_ids: List[str] = []
    question_count: int = 0
    
    source: str = ""
    exam_date: Optional[datetime] = None
    total_score: Optional[int] = None
    
    status: str = "uploaded"  # "uploaded" | "processing" | "completed" | "failed"
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True
```

- [ ] **Step 2: 创建 schemas/question_bank.py**

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class QuestionCreate(BaseModel):
    child_id: str
    subject: str
    grade: int = Field(ge=7, le=12)
    question_type: str
    question_text: str
    question_latex: str = ""
    question_image_url: str = ""
    options: List[dict] = []
    answer: str = ""
    explanation: str = ""
    chapter: str = ""
    knowledge_point_ids: List[str] = []
    difficulty: int = Field(ge=1, le=5, default=3)
    tags: List[str] = []


class QuestionResponse(BaseModel):
    id: str
    child_id: str
    subject: str
    grade: int
    question_type: str
    question_text: str
    question_latex: str
    question_image_url: str
    options: List[dict]
    answer: str
    explanation: str
    chapter: str
    knowledge_point_ids: List[str]
    difficulty: int
    tags: List[str]
    source_type: str
    used_count: int
    correct_rate: float
    created_at: datetime


class QuestionListResponse(BaseModel):
    items: List[QuestionResponse]
    total: int
    page: int
    page_size: int


class PaperCreate(BaseModel):
    child_id: str
    name: str
    subject: str
    grade: int = Field(ge=7, le=12)
    source: str = ""
    exam_date: Optional[str] = None
    total_score: Optional[int] = None


class PaperResponse(BaseModel):
    id: str
    child_id: str
    name: str
    subject: str
    grade: int
    images: List[dict]
    question_ids: List[str]
    question_count: int
    source: str
    status: str
    created_at: datetime


class PaperListResponse(BaseModel):
    items: List[PaperResponse]
    total: int
```

- [ ] **Step 3: 创建 services/question_bank_service.py**

```python
from datetime import datetime
from typing import Optional, List
from bson import ObjectId
from fastapi import HTTPException

from app.database import get_mongodb
from app.schemas.question_bank import QuestionCreate, QuestionResponse, QuestionListResponse


class QuestionBankService:
    @staticmethod
    async def create_question(data: QuestionCreate) -> QuestionResponse:
        db = get_mongodb()
        
        question_dict = data.model_dump()
        question_dict["source_type"] = "single"
        question_dict["used_count"] = 0
        question_dict["correct_rate"] = 0.0
        question_dict["created_at"] = datetime.now()
        question_dict["updated_at"] = datetime.now()
        
        result = await db.question_bank.insert_one(question_dict)
        question_id = str(result.inserted_id)
        
        return QuestionResponse(
            id=question_id,
            **question_dict
        )
    
    @staticmethod
    async def get_questions(
        child_id: str,
        subject: Optional[str] = None,
        question_type: Optional[str] = None,
        difficulty: Optional[int] = None,
        page: int = 1,
        page_size: int = 20
    ) -> QuestionListResponse:
        db = get_mongodb()
        
        query = {"child_id": child_id}
        if subject:
            query["subject"] = subject
        if question_type:
            query["question_type"] = question_type
        if difficulty:
            query["difficulty"] = difficulty
        
        total = await db.question_bank.count_documents(query)
        
        cursor = db.question_bank.find(query) \
            .sort("created_at", -1) \
            .skip((page - 1) * page_size) \
            .limit(page_size)
        
        items = []
        async for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            items.append(QuestionResponse(**doc))
        
        return QuestionListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size
        )
    
    @staticmethod
    async def get_question(question_id: str) -> QuestionResponse:
        db = get_mongodb()
        
        doc = await db.question_bank.find_one({"_id": ObjectId(question_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="题目不存在")
        
        doc["id"] = str(doc.pop("_id"))
        return QuestionResponse(**doc)
    
    @staticmethod
    async def delete_question(question_id: str):
        db = get_mongodb()
        
        result = await db.question_bank.delete_one({"_id": ObjectId(question_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="题目不存在")
        
        return {"message": "删除成功"}
    
    @staticmethod
    async def batch_import(paper_id: str, questions: List[dict]):
        """从试卷批量导入题目"""
        db = get_mongodb()
        
        paper = await db.papers.find_one({"_id": ObjectId(paper_id)})
        if not paper:
            raise HTTPException(status_code=404, detail="试卷不存在")
        
        question_ids = []
        for q_data in questions:
            q_data["source_type"] = "paper"
            q_data["source_paper_id"] = paper_id
            q_data["source_paper_name"] = paper["name"]
            q_data["used_count"] = 0
            q_data["correct_rate"] = 0.0
            q_data["created_at"] = datetime.now()
            q_data["updated_at"] = datetime.now()
            
            result = await db.question_bank.insert_one(q_data)
            question_ids.append(str(result.inserted_id))
        
        # 更新试卷的题目列表
        await db.papers.update_one(
            {"_id": ObjectId(paper_id)},
            {"$set": {"question_ids": question_ids, "status": "completed"}}
        )
        
        return {"imported_count": len(question_ids), "question_ids": question_ids}
```

- [ ] **Step 4: 创建 services/paper_service.py**

```python
from datetime import datetime
from typing import Optional, List
from bson import ObjectId
from fastapi import HTTPException, UploadFile

from app.database import get_mongodb
from app.schemas.question_bank import PaperCreate, PaperResponse, PaperListResponse
from app.services.ocr_service import OCRService


class PaperService:
    @staticmethod
    async def create_paper(data: PaperCreate, images: List[UploadFile]) -> PaperResponse:
        db = get_mongodb()
        
        # 保存图片
        image_list = []
        for i, image in enumerate(images):
            # 这里简化处理，实际应该上传到对象存储
            image_url = f"/uploads/papers/{ObjectId()}_{i}.jpg"
            image_list.append({"page": i + 1, "url": image_url})
        
        paper_dict = data.model_dump()
        paper_dict["images"] = image_list
        paper_dict["question_ids"] = []
        paper_dict["question_count"] = 0
        paper_dict["status"] = "uploaded"
        paper_dict["created_at"] = datetime.now()
        
        result = await db.papers.insert_one(paper_dict)
        paper_id = str(result.inserted_id)
        
        return PaperResponse(
            id=paper_id,
            **paper_dict
        )
    
    @staticmethod
    async def get_papers(child_id: str) -> PaperListResponse:
        db = get_mongodb()
        
        query = {"child_id": child_id}
        total = await db.papers.count_documents(query)
        
        cursor = db.papers.find(query).sort("created_at", -1)
        
        items = []
        async for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            items.append(PaperResponse(**doc))
        
        return PaperListResponse(items=items, total=total)
    
    @staticmethod
    async def get_paper(paper_id: str) -> PaperResponse:
        db = get_mongodb()
        
        doc = await db.papers.find_one({"_id": ObjectId(paper_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="试卷不存在")
        
        doc["id"] = str(doc.pop("_id"))
        return PaperResponse(**doc)
    
    @staticmethod
    async def recognize_paper(paper_id: str):
        """触发试卷识别"""
        db = get_mongodb()
        
        paper = await db.papers.find_one({"_id": ObjectId(paper_id)})
        if not paper:
            raise HTTPException(status_code=404, detail="试卷不存在")
        
        # 更新状态为处理中
        await db.papers.update_one(
            {"_id": ObjectId(paper_id)},
            {"$set": {"status": "processing"}}
        )
        
        # 这里应该异步调用 OCR 服务
        # 简化处理：模拟识别结果
        recognized_questions = []
        for i in range(1, 21):  # 假设识别出 20 题
            recognized_questions.append({
                "index": i,
                "type": "choice" if i <= 10 else ("fill_blank" if i <= 15 else "solve"),
                "text": f"题目 {i} 的内容",
                "image_url": f"/uploads/crops/{paper_id}_q{i}.jpg"
            })
        
        return {
            "status": "completed",
            "total_questions": len(recognized_questions),
            "questions": recognized_questions
        }
    
    @staticmethod
    async def delete_paper(paper_id: str):
        db = get_mongodb()
        
        result = await db.papers.delete_one({"_id": ObjectId(paper_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="试卷不存在")
        
        return {"message": "删除成功"}
```

- [ ] **Step 5: 创建 api/question_bank.py**

```python
from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.dependencies import get_current_user
from app.schemas.question_bank import QuestionCreate, QuestionResponse, QuestionListResponse
from app.services.question_bank_service import QuestionBankService

router = APIRouter()


@router.get("/question-bank", response_model=QuestionListResponse)
async def get_questions(
    child_id: str,
    subject: Optional[str] = None,
    question_type: Optional[str] = None,
    difficulty: Optional[int] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """获取题库列表"""
    return await QuestionBankService.get_questions(
        child_id=child_id,
        subject=subject,
        question_type=question_type,
        difficulty=difficulty,
        page=page,
        page_size=page_size
    )


@router.post("/question-bank", response_model=QuestionResponse)
async def create_question(
    data: QuestionCreate,
    current_user: dict = Depends(get_current_user)
):
    """创建题目"""
    return await QuestionBankService.create_question(data)


@router.get("/question-bank/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: str,
    current_user: dict = Depends(get_current_user)
):
    """获取题目详情"""
    return await QuestionBankService.get_question(question_id)


@router.delete("/question-bank/{question_id}")
async def delete_question(
    question_id: str,
    current_user: dict = Depends(get_current_user)
):
    """删除题目"""
    return await QuestionBankService.delete_question(question_id)
```

- [ ] **Step 6: 创建 api/papers.py**

```python
from fastapi import APIRouter, Depends, UploadFile, File, Form
from typing import List, Optional
from app.dependencies import get_current_user
from app.schemas.question_bank import PaperResponse, PaperListResponse
from app.services.paper_service import PaperService

router = APIRouter()


@router.post("/papers", response_model=PaperResponse)
async def create_paper(
    child_id: str = Form(...),
    name: str = Form(...),
    subject: str = Form(...),
    grade: int = Form(...),
    source: str = Form(""),
    images: List[UploadFile] = File(...),
    current_user: dict = Depends(get_current_user)
):
    """上传试卷"""
    from app.schemas.question_bank import PaperCreate
    data = PaperCreate(
        child_id=child_id,
        name=name,
        subject=subject,
        grade=grade,
        source=source
    )
    return await PaperService.create_paper(data, images)


@router.get("/papers", response_model=PaperListResponse)
async def get_papers(
    child_id: str,
    current_user: dict = Depends(get_current_user)
):
    """获取试卷列表"""
    return await PaperService.get_papers(child_id)


@router.get("/papers/{paper_id}", response_model=PaperResponse)
async def get_paper(
    paper_id: str,
    current_user: dict = Depends(get_current_user)
):
    """获取试卷详情"""
    return await PaperService.get_paper(paper_id)


@router.post("/papers/{paper_id}/recognize")
async def recognize_paper(
    paper_id: str,
    current_user: dict = Depends(get_current_user)
):
    """触发试卷识别"""
    return await PaperService.recognize_paper(paper_id)


@router.delete("/papers/{paper_id}")
async def delete_paper(
    paper_id: str,
    current_user: dict = Depends(get_current_user)
):
    """删除试卷"""
    return await PaperService.delete_paper(paper_id)
```

- [ ] **Step 7: 提交代码**

```bash
git add backend/
git commit -m "feat: 实现题库管理模块"
```

---

## Phase 6: 自由组卷模块

### Task 9: 自由组卷后端实现

**Files:**
- Create: `backend/app/services/generate_paper_service.py`
- Create: `backend/app/api/generate_paper.py`

**Interfaces:**
- Produces: `/api/v1/generate-paper` API

- [ ] **Step 1: 创建 services/generate_paper_service.py**

```python
from datetime import datetime
from typing import Optional, List
from bson import ObjectId
from fastapi import HTTPException

from app.database import get_mongodb


class GeneratePaperService:
    @staticmethod
    async def preview_paper(config: dict):
        """预览组卷结果"""
        db = get_mongodb()
        
        child_id = config["child_id"]
        subject = config["subject"]
        grade = config["grade"]
        total_questions = config["total_questions"]
        difficulty_dist = config.get("difficulty_distribution", {"easy": 0.3, "medium": 0.4, "hard": 0.3})
        type_dist = config.get("question_type_distribution", {"choice": 5, "fill_blank": 5, "solve": 5})
        knowledge_point_ids = config.get("knowledge_point_ids", [])
        exclude_recent_days = config.get("exclude_recent_days", 30)
        
        # 查询题库
        query = {
            "child_id": child_id,
            "subject": subject,
            "grade": grade
        }
        
        if knowledge_point_ids:
            query["knowledge_point_ids"] = {"$in": knowledge_point_ids}
        
        # 获取所有符合条件的题目
        all_questions = []
        async for doc in db.question_bank.find(query):
            doc["id"] = str(doc.pop("_id"))
            all_questions.append(doc)
        
        if len(all_questions) < total_questions:
            raise HTTPException(
                status_code=400,
                detail=f"题库中符合条件的题目不足，仅有 {len(all_questions)} 题"
            )
        
        # 按难度分组
        easy = [q for q in all_questions if q["difficulty"] <= 2]
        medium = [q for q in all_questions if q["difficulty"] == 3]
        hard = [q for q in all_questions if q["difficulty"] >= 4]
        
        # 计算各难度题目数量
        easy_count = round(total_questions * difficulty_dist["easy"])
        medium_count = round(total_questions * difficulty_dist["medium"])
        hard_count = total_questions - easy_count - medium_count
        
        # 选择题目
        selected = []
        selected.extend(easy[:easy_count])
        selected.extend(medium[:medium_count])
        selected.extend(hard[:hard_count])
        
        # 按题型分组
        choice = [q for q in selected if q["question_type"] == "choice"]
        fill_blank = [q for q in selected if q["question_type"] == "fill_blank"]
        solve = [q for q in selected if q["question_type"] == "solve"]
        
        return {
            "total_questions": len(selected),
            "difficulty_distribution": {
                "easy": len([q for q in selected if q["difficulty"] <= 2]),
                "medium": len([q for q in selected if q["difficulty"] == 3]),
                "hard": len([q for q in selected if q["difficulty"] >= 4])
            },
            "type_distribution": {
                "choice": len(choice),
                "fill_blank": len(fill_blank),
                "solve": len(solve)
            },
            "questions": selected
        }
    
    @staticmethod
    async def create_paper(config: dict):
        """创建组卷"""
        db = get_mongodb()
        
        # 先预览获取题目
        preview = await GeneratePaperService.preview_paper(config)
        
        # 创建试卷记录
        paper_dict = {
            "child_id": config["child_id"],
            "name": config.get("name", f"自由组卷 {datetime.now().strftime('%Y-%m-%d %H:%M')}"),
            "subject": config["subject"],
            "grade": config["grade"],
            "images": [],
            "question_ids": [q["id"] for q in preview["questions"]],
            "question_count": preview["total_questions"],
            "source": "自由组卷",
            "status": "completed",
            "created_at": datetime.now()
        }
        
        result = await db.papers.insert_one(paper_dict)
        paper_id = str(result.inserted_id)
        
        # 更新题目使用次数
        for q in preview["questions"]:
            await db.question_bank.update_one(
                {"_id": ObjectId(q["id"])},
                {"$inc": {"used_count": 1}}
            )
        
        return {
            "paper_id": paper_id,
            "name": paper_dict["name"],
            "total_questions": preview["total_questions"],
            "questions": preview["questions"]
        }
```

- [ ] **Step 2: 创建 api/generate_paper.py**

```python
from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.services.generate_paper_service import GeneratePaperService

router = APIRouter()


@router.post("/generate-paper/preview")
async def preview_paper(
    config: dict,
    current_user: dict = Depends(get_current_user)
):
    """预览组卷结果"""
    return await GeneratePaperService.preview_paper(config)


@router.post("/generate-paper")
async def create_paper(
    config: dict,
    current_user: dict = Depends(get_current_user)
):
    """创建组卷"""
    return await GeneratePaperService.create_paper(config)
```

- [ ] **Step 3: 提交代码**

```bash
git add backend/
git commit -m "feat: 实现自由组卷模块"
```

---

## Phase 7: 孩子管理与完整集成

### Task 10: 孩子管理 API

**Files:**
- Create: `backend/app/api/children.py`

**Interfaces:**
- Produces: `/api/v1/users/me/children` API

- [ ] **Step 1: 创建 api/children.py**

```python
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_user
from app.schemas.user import ChildCreate
from app.database import get_mongodb
from datetime import datetime

router = APIRouter()


@router.get("/users/me/children")
async def get_children(current_user: dict = Depends(get_current_user)):
    """获取孩子列表"""
    return current_user.get("children", [])


@router.post("/users/me/children")
async def create_child(
    data: ChildCreate,
    current_user: dict = Depends(get_current_user)
):
    """添加孩子"""
    db = get_mongodb()
    
    child = {
        "id": str(ObjectId()),
        "name": data.name,
        "grade": data.grade,
        "subjects": data.subjects,
        "created_at": datetime.now()
    }
    
    await db.users.update_one(
        {"_id": ObjectId(current_user["id"])},
        {"$push": {"children": child}}
    )
    
    return child


@router.delete("/users/me/children/{child_id}")
async def delete_child(
    child_id: str,
    current_user: dict = Depends(get_current_user)
):
    """删除孩子"""
    from bson import ObjectId
    
    db = get_mongodb()
    
    await db.users.update_one(
        {"_id": ObjectId(current_user["id"])},
        {"$pull": {"children": {"id": child_id}}}
    )
    
    return {"message": "删除成功"}
```

- [ ] **Step 2: 提交代码**

```bash
git add backend/
git commit -m "feat: 实现孩子管理 API"
```

---

### Task 11: 后端完整集成测试

**Files:**
- Create: `backend/tests/test_integration.py`

**Interfaces:**
- 验证所有 API 端点正常工作

- [ ] **Step 1: 创建完整集成测试**

```python
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_full_workflow(client: AsyncClient):
    """完整工作流测试"""
    
    # 1. 注册用户
    register_response = await client.post("/api/v1/auth/register", json={
        "username": "integration_user",
        "email": "integration@example.com",
        "password": "Test123456"
    })
    assert register_response.status_code == 200
    token = register_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. 添加孩子
    child_response = await client.post("/api/v1/users/me/children", json={
        "name": "小明",
        "grade": 9,
        "subjects": ["数学", "物理"]
    }, headers=headers)
    assert child_response.status_code == 200
    child_id = child_response.json()["id"]
    
    # 3. 创建错题
    mistake_response = await client.post("/api/v1/mistakes", json={
        "child_id": child_id,
        "subject": "数学",
        "grade": 9,
        "chapter": "二次函数",
        "question_text": "求函数 f(x)=x² 的最小值",
        "answer": "0",
        "explanation": "因为 x²≥0，所以最小值为0",
        "difficulty": 2
    }, headers=headers)
    assert mistake_response.status_code == 200
    mistake_id = mistake_response.json()["id"]
    
    # 4. 添加题目到题库
    question_response = await client.post("/api/v1/question-bank", json={
        "child_id": child_id,
        "subject": "数学",
        "grade": 9,
        "question_type": "solve",
        "question_text": "解方程 x²-5x+6=0",
        "answer": "x=2 或 x=3",
        "chapter": "方程与不等式",
        "difficulty": 3
    }, headers=headers)
    assert question_response.status_code == 200
    
    # 5. 获取错题列表
    mistakes_response = await client.get(f"/api/v1/mistakes?child_id={child_id}", headers=headers)
    assert mistakes_response.status_code == 200
    assert mistakes_response.json()["total"] > 0
    
    # 6. 获取题库列表
    questions_response = await client.get(f"/api/v1/question-bank?child_id={child_id}", headers=headers)
    assert questions_response.status_code == 200
    
    # 7. 获取学科列表
    subjects_response = await client.get("/api/v1/subjects", headers=headers)
    assert subjects_response.status_code == 200
    
    print("✅ 完整工作流测试通过")
```

- [ ] **Step 2: 运行完整测试**

```bash
cd backend
pytest tests/ -v
```

Expected: 所有测试通过

- [ ] **Step 3: 提交代码**

```bash
git add backend/
git commit -m "test: 添加完整集成测试"
```

---

## Phase 8: 前端页面实现

### Task 12: 前端核心页面

**Files:**
- Create: `frontend/src/app/dashboard/page.tsx`
- Create: `frontend/src/app/mistakes/page.tsx`
- Create: `frontend/src/app/mistakes/add/page.tsx`
- Create: `frontend/src/app/question-bank/page.tsx`
- Create: `frontend/src/app/knowledge-graph/page.tsx`
- Create: `frontend/src/components/layout/MainLayout.tsx`

**Interfaces:**
- Consumes: 所有后端 API
- Produces: 完整前端界面

- [ ] **Step 1: 创建 MainLayout.tsx**

```typescript
'use client'

import { ReactNode } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'

const navItems = [
  { href: '/dashboard', label: '首页', icon: '🏠' },
  { href: '/knowledge-graph', label: '知识图谱', icon: '📊' },
  { href: '/mistakes', label: '错题本', icon: '📝' },
  { href: '/question-bank', label: '题库管理', icon: '📚' },
]

export default function MainLayout({ children }: { children: ReactNode }) {
  const pathname = usePathname()
  const { user, logout } = useAuth()

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/dashboard" className="text-2xl font-bold">
            📚 书童
          </Link>
          <div className="flex items-center gap-4">
            <span>{user?.username}</span>
            <button
              onClick={logout}
              className="text-sm text-gray-600 hover:text-gray-900"
            >
              退出
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8 flex gap-8">
        <nav className="w-48 flex-shrink-0">
          <ul className="space-y-2">
            {navItems.map((item) => (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg ${
                    pathname === item.href
                      ? 'bg-primary-100 text-primary-700'
                      : 'hover:bg-gray-100'
                  }`}
                >
                  <span>{item.icon}</span>
                  <span>{item.label}</span>
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        <main className="flex-1">{children}</main>
      </div>
    </div>
  )
}
```

- [ ] **Step 2: 创建 dashboard/page.tsx**

```typescript
'use client'

import { useEffect, useState } from 'react'
import { useAuth } from '@/hooks/useAuth'
import { childrenAPI, mistakesAPI, knowledgeGraphAPI } from '@/lib/api'
import MainLayout from '@/components/layout/MainLayout'

export default function DashboardPage() {
  const { user } = useAuth()
  const [stats, setStats] = useState({
    totalMistakes: 0,
    todayTasks: 5,
    weeklyGoal: '数学提升 10%'
  })

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      if (user?.children?.length) {
        const childId = user.children[0].id
        const response = await mistakesAPI.list({ child_id: childId, page_size: 1 })
        setStats(prev => ({
          ...prev,
          totalMistakes: response.data.total
        }))
      }
    } catch (error) {
      console.error('加载统计失败:', error)
    }
  }

  return (
    <MainLayout>
      <div className="space-y-6">
        <h1 className="text-3xl font-bold">
          欢迎回来，{user?.username} 👋
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-4xl mb-2">📚</div>
            <h3 className="text-lg font-semibold">今日任务</h3>
            <p className="text-3xl font-bold text-primary-600">
              {stats.todayTasks} 项
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-4xl mb-2">📝</div>
            <h3 className="text-lg font-semibold">错题总数</h3>
            <p className="text-3xl font-bold text-orange-600">
              {stats.totalMistakes} 道
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-4xl mb-2">🎯</div>
            <h3 className="text-lg font-semibold">本周目标</h3>
            <p className="text-lg text-green-600">{stats.weeklyGoal}</p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">📊 学习进度概览</h2>
          <div className="space-y-4">
            {['数学', '物理', '化学'].map((subject) => (
              <div key={subject} className="flex items-center gap-4">
                <span className="w-16">{subject}</span>
                <div className="flex-1 bg-gray-200 rounded-full h-4">
                  <div
                    className="bg-primary-600 h-4 rounded-full"
                    style={{ width: `${Math.random() * 40 + 60}%` }}
                  />
                </div>
                <span className="w-16 text-right">
                  {Math.round(Math.random() * 40 + 60)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </MainLayout>
  )
}
```

- [ ] **Step 3: 创建 mistakes/page.tsx**

```typescript
'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'
import { mistakesAPI } from '@/lib/api'
import MainLayout from '@/components/layout/MainLayout'
import { Mistake } from '@/types'

export default function MistakesPage() {
  const { user } = useAuth()
  const [mistakes, setMistakes] = useState<Mistake[]>([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({
    subject: '',
    difficulty: ''
  })

  useEffect(() => {
    loadMistakes()
  }, [filters])

  const loadMistakes = async () => {
    try {
      if (user?.children?.length) {
        const childId = user.children[0].id
        const params: any = { child_id: childId }
        if (filters.subject) params.subject = filters.subject
        if (filters.difficulty) params.difficulty = filters.difficulty

        const response = await mistakesAPI.list(params)
        setMistakes(response.data.items)
      }
    } catch (error) {
      console.error('加载错题失败:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <MainLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">📝 错题本</h1>
          <Link
            href="/mistakes/add"
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            + 添加错题
          </Link>
        </div>

        <div className="flex gap-4">
          <select
            value={filters.subject}
            onChange={(e) => setFilters({ ...filters, subject: e.target.value })}
            className="px-4 py-2 border rounded-lg"
          >
            <option value="">全部科目</option>
            <option value="数学">数学</option>
            <option value="物理">物理</option>
            <option value="化学">化学</option>
          </select>

          <select
            value={filters.difficulty}
            onChange={(e) => setFilters({ ...filters, difficulty: e.target.value })}
            className="px-4 py-2 border rounded-lg"
          >
            <option value="">全部难度</option>
            <option value="1">★</option>
            <option value="2">★★</option>
            <option value="3">★★★</option>
            <option value="4">★★★★</option>
            <option value="5">★★★★★</option>
          </select>
        </div>

        {loading ? (
          <div className="text-center py-8">加载中...</div>
        ) : mistakes.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            暂无错题，点击上方按钮添加
          </div>
        ) : (
          <div className="space-y-4">
            {mistakes.map((mistake) => (
              <div
                key={mistake.id}
                className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow"
              >
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <span className="text-sm text-gray-500">
                      {mistake.subject} · {mistake.chapter}
                    </span>
                    <span className="ml-2 text-sm text-yellow-600">
                      {'★'.repeat(mistake.difficulty)}
                    </span>
                  </div>
                  <span className="text-sm text-gray-400">
                    {new Date(mistake.created_at).toLocaleDateString()}
                  </span>
                </div>
                <p className="text-lg mb-2">{mistake.question_text}</p>
                {mistake.answer && (
                  <p className="text-green-600">
                    答案：{mistake.answer}
                  </p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </MainLayout>
  )
}
```

- [ ] **Step 4: 创建 mistakes/add/page.tsx**

```typescript
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'
import { mistakesAPI } from '@/lib/api'
import MainLayout from '@/components/layout/MainLayout'

export default function AddMistakePage() {
  const { user } = useAuth()
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [form, setForm] = useState({
    subject: '数学',
    chapter: '',
    question_text: '',
    answer: '',
    explanation: '',
    difficulty: 3,
    source: '',
    tags: [] as string[]
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!user?.children?.length) {
      alert('请先添加孩子')
      return
    }

    setLoading(true)
    try {
      await mistakesAPI.create({
        child_id: user.children[0].id,
        grade: user.children[0].grade,
        ...form
      })
      router.push('/mistakes')
    } catch (error) {
      console.error('添加错题失败:', error)
      alert('添加失败，请重试')
    } finally {
      setLoading(false)
    }
  }

  return (
    <MainLayout>
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">📝 添加错题</h1>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">科目</label>
              <select
                value={form.subject}
                onChange={(e) => setForm({ ...form, subject: e.target.value })}
                className="w-full px-4 py-2 border rounded-lg"
              >
                <option value="数学">数学</option>
                <option value="物理">物理</option>
                <option value="化学">化学</option>
                <option value="语文">语文</option>
                <option value="英语">英语</option>
                <option value="生物">生物</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">章节</label>
              <input
                type="text"
                value={form.chapter}
                onChange={(e) => setForm({ ...form, chapter: e.target.value })}
                className="w-full px-4 py-2 border rounded-lg"
                placeholder="例如：二次函数"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">题目内容</label>
            <textarea
              value={form.question_text}
              onChange={(e) => setForm({ ...form, question_text: e.target.value })}
              className="w-full px-4 py-2 border rounded-lg"
              rows={4}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">答案</label>
            <textarea
              value={form.answer}
              onChange={(e) => setForm({ ...form, answer: e.target.value })}
              className="w-full px-4 py-2 border rounded-lg"
              rows={2}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">解析</label>
            <textarea
              value={form.explanation}
              onChange={(e) => setForm({ ...form, explanation: e.target.value })}
              className="w-full px-4 py-2 border rounded-lg"
              rows={3}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">难度</label>
            <div className="flex gap-2">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  type="button"
                  onClick={() => setForm({ ...form, difficulty: star })}
                  className={`text-2xl ${
                    star <= form.difficulty ? 'text-yellow-500' : 'text-gray-300'
                  }`}
                >
                  ★
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">来源</label>
            <input
              type="text"
              value={form.source}
              onChange={(e) => setForm({ ...form, source: e.target.value })}
              className="w-full px-4 py-2 border rounded-lg"
              placeholder="例如：期末试卷"
            />
          </div>

          <div className="flex gap-4">
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
            >
              {loading ? '添加中...' : '添加错题'}
            </button>
            <button
              type="button"
              onClick={() => router.back()}
              className="px-6 py-3 border rounded-lg hover:bg-gray-50"
            >
              取消
            </button>
          </div>
        </form>
      </div>
    </MainLayout>
  )
}
```

- [ ] **Step 5: 创建 question-bank/page.tsx**

```typescript
'use client'

import { useEffect, useState } from 'react'
import { useAuth } from '@/hooks/useAuth'
import { questionBankAPI } from '@/lib/api'
import MainLayout from '@/components/layout/MainLayout'
import { Question } from '@/types'

export default function QuestionBankPage() {
  const { user } = useAuth()
  const [questions, setQuestions] = useState<Question[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadQuestions()
  }, [])

  const loadQuestions = async () => {
    try {
      if (user?.children?.length) {
        const childId = user.children[0].id
        const response = await questionBankAPI.list({ child_id: childId })
        setQuestions(response.data.items)
      }
    } catch (error) {
      console.error('加载题库失败:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <MainLayout>
      <div className="space-y-6">
        <h1 className="text-3xl font-bold">📚 题库管理</h1>

        <div className="flex gap-4">
          <span className="text-gray-600">
            共 {questions.length} 题
          </span>
        </div>

        {loading ? (
          <div className="text-center py-8">加载中...</div>
        ) : questions.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            暂无题目，请先上传试卷或添加题目
          </div>
        ) : (
          <div className="space-y-4">
            {questions.map((question) => (
              <div
                key={question.id}
                className="bg-white p-6 rounded-lg shadow"
              >
                <div className="flex justify-between items-start mb-2">
                  <span className="text-sm text-gray-500">
                    {question.subject} · {question.chapter}
                  </span>
                  <span className="text-sm text-yellow-600">
                    {'★'.repeat(question.difficulty)}
                  </span>
                </div>
                <p className="text-lg mb-2">{question.question_text}</p>
                <div className="flex gap-4 text-sm text-gray-500">
                  <span>类型：{question.question_type}</span>
                  <span>使用次数：{question.used_count}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </MainLayout>
  )
}
```

- [ ] **Step 6: 创建 knowledge-graph/page.tsx**

```typescript
'use client'

import { useEffect, useState } from 'react'
import { useAuth } from '@/hooks/useAuth'
import { knowledgeGraphAPI } from '@/lib/api'
import MainLayout from '@/components/layout/MainLayout'

export default function KnowledgeGraphPage() {
  const { user } = useAuth()
  const [subjects, setSubjects] = useState<any[]>([])
  const [selectedSubject, setSelectedSubject] = useState<string | null>(null)
  const [graphData, setGraphData] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadSubjects()
  }, [])

  useEffect(() => {
    if (selectedSubject) {
      loadGraph()
    }
  }, [selectedSubject])

  const loadSubjects = async () => {
    try {
      const response = await knowledgeGraphAPI.getSubjects()
      setSubjects(response.data)
      if (response.data.length > 0) {
        setSelectedSubject(response.data[0].id)
      }
    } catch (error) {
      console.error('加载学科失败:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadGraph = async () => {
    try {
      const response = await knowledgeGraphAPI.getSubjectGraph(selectedSubject!)
      setGraphData(response.data)
    } catch (error) {
      console.error('加载图谱失败:', error)
    }
  }

  const getMasteryColor = (mastery: number) => {
    if (mastery >= 0.8) return 'bg-green-500'
    if (mastery >= 0.6) return 'bg-blue-500'
    if (mastery >= 0.3) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  return (
    <MainLayout>
      <div className="space-y-6">
        <h1 className="text-3xl font-bold">📊 知识图谱</h1>

        <div className="flex gap-4">
          {subjects.map((subject) => (
            <button
              key={subject.id}
              onClick={() => setSelectedSubject(subject.id)}
              className={`px-4 py-2 rounded-lg ${
                selectedSubject === subject.id
                  ? 'bg-primary-600 text-white'
                  : 'bg-white border hover:bg-gray-50'
              }`}
            >
              {subject.name}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="text-center py-8">加载中...</div>
        ) : graphData ? (
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-bold mb-4">
              {subjects.find(s => s.id === selectedSubject)?.name} 知识图谱
            </h2>

            <div className="space-y-8">
              {graphData.chapters?.map((chapter: any) => (
                <div key={chapter.id}>
                  <h3 className="text-lg font-semibold mb-4">
                    {chapter.name}
                  </h3>
                  <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                    {chapter.knowledge_points?.map((kp: any) => (
                      <div
                        key={kp.id}
                        className="p-4 border rounded-lg hover:shadow-md transition-shadow"
                      >
                        <div className="font-medium mb-2">{kp.name}</div>
                        <div className="h-2 bg-gray-200 rounded-full">
                          <div
                            className={`h-2 rounded-full ${getMasteryColor(kp.mastery || 0)}`}
                            style={{ width: `${(kp.mastery || 0) * 100}%` }}
                          />
                        </div>
                        <div className="text-sm text-gray-500 mt-1">
                          {Math.round((kp.mastery || 0) * 100)}%
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            暂无图谱数据
          </div>
        )}
      </div>
    </MainLayout>
  )
}
```

- [ ] **Step 7: 验证前端页面**

```bash
cd frontend
npm run dev
```

访问各个页面验证功能

- [ ] **Step 8: 提交代码**

```bash
git add frontend/
git commit -m "feat: 实现前端核心页面"
```

---

## 完成清单

- [ ] Phase 1: 项目初始化 ✅
- [ ] Phase 2: 用户认证模块 ✅
- [ ] Phase 3: 知识图谱模块 ✅
- [ ] Phase 4: 错题本模块 ✅
- [ ] Phase 5: 题库管理模块 ✅
- [ ] Phase 6: 自由组卷模块 ✅
- [ ] Phase 7: 孩子管理与集成测试 ✅
- [ ] Phase 8: 前端页面实现 ✅

---

## 下一步

完成 MVP 后，可继续开发：
1. 学习计划模块
2. 测评系统
3. AI 动态解析图
4. 错题导出打印
5. 更多学科知识图谱

---

**计划完成时间**：约 2-3 天（全职开发）

**执行建议**：使用 subagent-driven-development 逐任务执行，每完成一个任务进行代码审查
