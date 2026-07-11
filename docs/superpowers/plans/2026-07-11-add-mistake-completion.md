# 错题添加功能完整实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 完成错题添加功能：调整后端 `grade` 为可选字符串标签，前端添加页真实提交到后端，错题列表页拉取真实数据。

**Architecture:** 后端调整 Pydantic schema 和 model 的 `grade` 类型；前端 add 页增加孩子选择、年级标签、知识点标签输入，完成字段映射后调用 `mistakesAPI.createMistake`；列表页使用 `useEffect` 调用 `mistakesAPI.getMistakes` 渲染真实数据。

**Tech Stack:** Python 3.11 + FastAPI + Pydantic + MongoDB / Next.js 14 + React + TypeScript + Tailwind CSS

## Global Constraints

- 所有代码注释使用中文
- 提交信息使用中文，类型前缀小写
- 不引入新的依赖
- 复用现有 `frontend/src/lib/api.ts` 中的 `mistakesAPI`
- 通过 `feature/add-mistake-completion` 分支提交 PR 合并到 `main`
- 每个 TDD 循环必须看到测试失败后再写实现
- 后端 `grade` 从必填整数改为可选字符串标签

---

### Task 1: 调整后端错题 schema 和 model 的 grade 字段

**Files:**
- Modify: `backend/app/schemas/mistake.py`
- Modify: `backend/app/models/mistake.py`
- Test: `backend/tests/test_mistakes.py`

**Interfaces:**
- Consumes: 现有 `MistakeCreate`, `MistakeUpdate`, `MistakeResponse`, `MistakeModel`
- Produces: `grade` 字段类型从 `int` 调整为 `Optional[str]`/`str`

- [ ] **Step 1: 编写失败测试（验证 grade 可为字符串和 null）**

在 `backend/tests/test_mistakes.py` 中新增测试：

```python
async def test_create_mistake_with_string_grade(client, auth_headers, test_child):
    """测试使用字符串标签作为 grade 创建错题"""
    payload = {
        "child_id": test_child["id"],
        "subject": "数学",
        "grade": "高一",
        "chapter": "函数与导数",
        "question_text": "求函数 f(x)=x² 的导数",
        "answer": "f'(x)=2x",
        "explanation": "使用幂函数求导法则",
        "difficulty": 3,
        "source": "单元测试",
        "tags": ["求导"],
        "knowledge_points": [],
    }
    response = await client.post("/mistakes", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["grade"] == "高一"


async def test_create_mistake_without_grade(client, auth_headers, test_child):
    """测试不传 grade 创建错题"""
    payload = {
        "child_id": test_child["id"],
        "subject": "数学",
        "chapter": "函数与导数",
        "question_text": "求函数 f(x)=x² 的导数",
        "answer": "f'(x)=2x",
        "explanation": "使用幂函数求导法则",
        "difficulty": 3,
        "source": "单元测试",
        "tags": [],
        "knowledge_points": [],
    }
    response = await client.post("/mistakes", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data.get("grade") is None or data.get("grade") == ""
```

- [ ] **Step 2: 运行测试确认失败**

```bash
cd backend
pytest tests/test_mistakes.py::test_create_mistake_with_string_grade tests/test_mistakes.py::test_create_mistake_without_grade -v
```

预期：失败，原因是 `grade` 字段校验不通过（当前为 int）。

- [ ] **Step 3: 修改 schema 和 model**

修改 `backend/app/schemas/mistake.py`：

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MistakeCreate(BaseModel):
    child_id: str
    subject: str
    grade: Optional[str] = None
    chapter: str
    question_text: str = ""
    question_image_url: str = ""
    question_latex: str = ""
    answer: str = ""
    explanation: str = ""
    difficulty: int = Field(ge=1, le=5, default=3)
    source: str = ""
    tags: List[str] = []
    knowledge_points: List[str] = []


class MistakeUpdate(BaseModel):
    subject: Optional[str] = None
    grade: Optional[str] = None
    chapter: Optional[str] = None
    question_text: Optional[str] = None
    question_image_url: Optional[str] = None
    question_latex: Optional[str] = None
    answer: Optional[str] = None
    explanation: Optional[str] = None
    explanation_gif_url: Optional[str] = None
    difficulty: Optional[int] = Field(None, ge=1, le=5)
    source: Optional[str] = None
    tags: Optional[List[str]] = None
    knowledge_points: Optional[List[str]] = None


class MistakeResponse(BaseModel):
    id: str
    child_id: str
    subject: str
    grade: Optional[str] = None
    chapter: str
    knowledge_points: List[str] = []
    question_image_url: str = ""
    question_text: str = ""
    question_latex: str = ""
    answer: str = ""
    explanation: str = ""
    explanation_gif_url: str = ""
    difficulty: int = 3
    source: str = ""
    tags: List[str] = []
    created_at: datetime
    updated_at: datetime
```

修改 `backend/app/models/mistake.py`：

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MistakeModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    child_id: str
    subject: str
    grade: Optional[str] = None
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

- [ ] **Step 4: 运行测试确认通过**

```bash
cd backend
pytest tests/test_mistakes.py -v
```

预期：所有测试通过。

- [ ] **Step 5: 提交**

```bash
git add backend/app/schemas/mistake.py backend/app/models/mistake.py backend/tests/test_mistakes.py
git commit -m "refactor: 将错题 grade 字段从必填整数改为可选字符串标签"
```

---

### Task 2: 调整前端 Mistake 类型定义

**Files:**
- Modify: `frontend/src/types/index.ts`

**Interfaces:**
- Consumes: 后端 `MistakeResponse.grade` 现为 `Optional[str]`
- Produces: 前端 `Mistake.grade` 类型同步更新

- [ ] **Step 1: 修改类型定义**

修改 `frontend/src/types/index.ts` 中的 `Mistake` 接口：

```typescript
/**
 * 错题记录
 */
export interface Mistake {
  id: string;
  child_id: string;
  subject: string;
  grade?: string;
  chapter: string;
  knowledge_points: string[];
  question_image_url: string;
  question_text: string;
  question_latex: string;
  answer: string;
  explanation: string;
  explanation_gif_url: string;
  difficulty: number;
  source: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}
```

- [ ] **Step 2: 运行前端类型检查**

```bash
cd frontend
npx tsc --noEmit
```

预期：可能暴露其他文件中 `grade` 作为 number 使用的地方，记录并在后续任务修复。

- [ ] **Step 3: 提交**

```bash
git add frontend/src/types/index.ts
git commit -m "refactor: 调整前端 Mistake 类型 grade 为可选字符串"
```

---

### Task 3: 实现前端添加错题页面真实提交

**Files:**
- Modify: `frontend/src/app/mistakes/add/page.tsx`

**Interfaces:**
- Consumes: `useAuth().user`（含 `children` 列表）、`mistakesAPI.createMistake`
- Produces: 表单提交后调用 `POST /mistakes` 并跳转 `/mistakes`

- [ ] **Step 1: 验证当前状态（失败证据）**

启动前端开发服务器，访问 `http://localhost:3000/mistakes/add`，点击提交按钮，观察浏览器控制台仅输出 `console.log` 而未发起网络请求。

- [ ] **Step 2: 重写添加错题页面**

完整替换 `frontend/src/app/mistakes/add/page.tsx` 为：

```tsx
'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import MainLayout from '@/components/layout/MainLayout';
import { useAuth } from '@/hooks/useAuth';
import { mistakesAPI } from '@/lib/api';

const DIFFICULTY_MAP: Record<string, number> = {
  简单: 1,
  中等: 3,
  困难: 5,
};

const AddMistakePage: React.FC = () => {
  const router = useRouter();
  const { user, isLoading: isAuthLoading } = useAuth();

  const [formData, setFormData] = useState({
    child_id: '',
    subject: '',
    chapter: '',
    content: '',
    answer: '',
    analysis: '',
    difficulty: '中等',
    grade: '',
    source: '',
    tags: '',
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  // 默认选中第一个孩子
  useEffect(() => {
    if (user && user.children.length > 0 && !formData.child_id) {
      setFormData((prev) => ({ ...prev, child_id: user.children[0].id }));
    }
  }, [user, formData.child_id]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!formData.child_id) {
      setError('请先选择孩子');
      return;
    }

    setIsSubmitting(true);

    try {
      await mistakesAPI.createMistake({
        child_id: formData.child_id,
        subject: formData.subject,
        grade: formData.grade || undefined,
        chapter: formData.chapter,
        question_text: formData.content,
        answer: formData.answer,
        explanation: formData.analysis,
        difficulty: DIFFICULTY_MAP[formData.difficulty],
        source: formData.source,
        tags: formData.tags
          .split('，')
          .map((t) => t.trim())
          .filter(Boolean),
        knowledge_points: [],
        question_image_url: '',
        question_latex: '',
      });
      router.push('/mistakes');
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      setError(typeof detail === 'string' ? detail : '提交失败，请稍后重试');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isAuthLoading) {
    return (
      <MainLayout>
        <div className="flex justify-center items-center h-64">
          <span className="text-gray-500">加载中...</span>
        </div>
      </MainLayout>
    );
  }

  if (!user) {
    return (
      <MainLayout>
        <div className="text-center py-12 text-gray-500">
          请先登录后再添加错题
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">添加错题</h1>

        {error && (
          <div className="mb-4 p-3 bg-red-50 text-red-600 rounded-md text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                孩子 <span className="text-red-500">*</span>
              </label>
              <select
                name="child_id"
                value={formData.child_id}
                onChange={handleChange}
                className="w-full border rounded-lg px-3 py-2"
                required
              >
                <option value="">请选择孩子</option>
                {user.children.map((child) => (
                  <option key={child.id} value={child.id}>
                    {child.name}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">难度</label>
              <select
                name="difficulty"
                value={formData.difficulty}
                onChange={handleChange}
                className="w-full border rounded-lg px-3 py-2"
              >
                <option value="简单">简单</option>
                <option value="中等">中等</option>
                <option value="困难">困难</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                科目 <span className="text-red-500">*</span>
              </label>
              <select
                name="subject"
                value={formData.subject}
                onChange={handleChange}
                className="w-full border rounded-lg px-3 py-2"
                required
              >
                <option value="">请选择科目</option>
                <option value="数学">数学</option>
                <option value="物理">物理</option>
                <option value="化学">化学</option>
                <option value="英语">英语</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">年级标签</label>
              <input
                type="text"
                name="grade"
                value={formData.grade}
                onChange={handleChange}
                placeholder="例如：高一"
                className="w-full border rounded-lg px-3 py-2"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              章节 <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              name="chapter"
              value={formData.chapter}
              onChange={handleChange}
              placeholder="例如：函数与导数"
              className="w-full border rounded-lg px-3 py-2"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              题目内容 <span className="text-red-500">*</span>
            </label>
            <textarea
              name="content"
              value={formData.content}
              onChange={handleChange}
              rows={4}
              placeholder="请输入题目内容"
              className="w-full border rounded-lg px-3 py-2"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              正确答案 <span className="text-red-500">*</span>
            </label>
            <textarea
              name="answer"
              value={formData.answer}
              onChange={handleChange}
              rows={2}
              placeholder="请输入正确答案"
              className="w-full border rounded-lg px-3 py-2"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">解析</label>
            <textarea
              name="analysis"
              value={formData.analysis}
              onChange={handleChange}
              rows={3}
              placeholder="请输入解析"
              className="w-full border rounded-lg px-3 py-2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">标签</label>
            <input
              type="text"
              name="tags"
              value={formData.tags}
              onChange={handleChange}
              placeholder="用中文逗号分隔，例如：函数, 导数"
              className="w-full border rounded-lg px-3 py-2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">来源</label>
            <input
              type="text"
              name="source"
              value={formData.source}
              onChange={handleChange}
              placeholder="例如：2026年高考真题"
              className="w-full border rounded-lg px-3 py-2"
            />
          </div>

          <div className="flex gap-4 pt-4">
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? '提交中...' : '提交'}
            </button>
            <button
              type="button"
              onClick={() => router.back()}
              className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
            >
              取消
            </button>
          </div>
        </form>
      </div>
    </MainLayout>
  );
};

export default AddMistakePage;
```

- [ ] **Step 3: 验证提交行为**

启动前后端服务，访问 `http://localhost:3000/mistakes/add`，填写表单并提交。在浏览器开发者工具中确认：
- 请求 `POST http://localhost:8000/api/v1/mistakes` 返回 200
- 请求体中包含正确的字段映射
- 成功后跳转 `/mistakes`

- [ ] **Step 4: 运行前端构建检查**

```bash
cd frontend
npm run build
```

预期：构建成功，无 TypeScript 类型错误。

- [ ] **Step 5: 提交**

```bash
git add frontend/src/app/mistakes/add/page.tsx
git commit -m "feat: 实现添加错题页面的真实后端提交"
```

---

### Task 4: 实现错题列表页真实数据拉取

**Files:**
- Modify: `frontend/src/app/mistakes/page.tsx`

**Interfaces:**
- Consumes: `useAuth().user`、`mistakesAPI.getMistakes`
- Produces: 列表页渲染真实错题数据

- [ ] **Step 1: 验证当前状态（失败证据）**

访问 `http://localhost:3000/mistakes`，观察列表显示的是写死的 3 条模拟数据，不随添加错题变化。

- [ ] **Step 2: 重写列表页为真实数据**

完整替换 `frontend/src/app/mistakes/page.tsx` 为：

```tsx
'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import MainLayout from '@/components/layout/MainLayout';
import { useAuth } from '@/hooks/useAuth';
import { mistakesAPI } from '@/lib/api';
import { Mistake } from '@/types';

const DIFFICULTY_LABELS: Record<number, string> = {
  1: '简单',
  2: '简单',
  3: '中等',
  4: '困难',
  5: '困难',
};

const DIFFICULTY_COLORS: Record<string, string> = {
  简单: 'bg-green-100 text-green-800',
  中等: 'bg-yellow-100 text-yellow-800',
  困难: 'bg-red-100 text-red-800',
};

const MistakesPage: React.FC = () => {
  const { user, isLoading: isAuthLoading } = useAuth();
  const [selectedChildId, setSelectedChildId] = useState<string>('');
  const [mistakes, setMistakes] = useState<Mistake[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const [filterSubject, setFilterSubject] = useState('all');
  const [filterDifficulty, setFilterDifficulty] = useState('all');

  // 默认选中第一个孩子
  useEffect(() => {
    if (user && user.children.length > 0 && !selectedChildId) {
      setSelectedChildId(user.children[0].id);
    }
  }, [user, selectedChildId]);

  // 拉取错题列表
  useEffect(() => {
    if (!selectedChildId) return;

    setIsLoading(true);
    setError('');

    mistakesAPI
      .getMistakes({ child_id: selectedChildId })
      .then((response) => {
        setMistakes(response.data.items || []);
      })
      .catch((err) => {
        const detail = err.response?.data?.detail;
        setError(typeof detail === 'string' ? detail : '加载错题失败，请稍后重试');
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [selectedChildId]);

  const filteredMistakes = mistakes.filter((mistake) => {
    const difficultyLabel = DIFFICULTY_LABELS[mistake.difficulty] || '中等';
    const subjectMatch = filterSubject === 'all' || mistake.subject === filterSubject;
    const difficultyMatch = filterDifficulty === 'all' || difficultyLabel === filterDifficulty;
    return subjectMatch && difficultyMatch;
  });

  const formatDate = (dateString: string) => {
    if (!dateString) return '';
    return new Date(dateString).toLocaleDateString('zh-CN');
  };

  if (isAuthLoading) {
    return (
      <MainLayout>
        <div className="flex justify-center items-center h-64">
          <span className="text-gray-500">加载中...</span>
        </div>
      </MainLayout>
    );
  }

  if (!user) {
    return (
      <MainLayout>
        <div className="text-center py-12 text-gray-500">请先登录</div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-800">错题本</h1>
          <Link
            href="/mistakes/add"
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            添加错题
          </Link>
        </div>

        <div className="bg-white rounded-lg shadow p-4 flex flex-wrap gap-4 items-end">
          <div>
            <label className="block text-sm text-gray-600 mb-1">孩子</label>
            <select
              value={selectedChildId}
              onChange={(e) => setSelectedChildId(e.target.value)}
              className="border rounded px-3 py-2"
            >
              <option value="">请选择孩子</option>
              {user.children.map((child) => (
                <option key={child.id} value={child.id}>
                  {child.name}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm text-gray-600 mb-1">科目</label>
            <select
              value={filterSubject}
              onChange={(e) => setFilterSubject(e.target.value)}
              className="border rounded px-3 py-2"
            >
              <option value="all">全部科目</option>
              <option value="数学">数学</option>
              <option value="物理">物理</option>
              <option value="化学">化学</option>
              <option value="英语">英语</option>
            </select>
          </div>
          <div>
            <label className="block text-sm text-gray-600 mb-1">难度</label>
            <select
              value={filterDifficulty}
              onChange={(e) => setFilterDifficulty(e.target.value)}
              className="border rounded px-3 py-2"
            >
              <option value="all">全部难度</option>
              <option value="简单">简单</option>
              <option value="中等">中等</option>
              <option value="困难">困难</option>
            </select>
          </div>
        </div>

        {isLoading && (
          <div className="flex justify-center items-center h-64">
            <span className="text-gray-500">加载中...</span>
          </div>
        )}

        {error && !isLoading && (
          <div className="bg-red-50 text-red-600 p-4 rounded-lg text-sm">{error}</div>
        )}

        {!isLoading && !error && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredMistakes.map((mistake) => {
                const difficultyLabel = DIFFICULTY_LABELS[mistake.difficulty] || '中等';
                return (
                  <div
                    key={mistake.id}
                    className="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <span className="text-sm text-gray-500">{mistake.subject}</span>
                      <span
                        className={`text-xs px-2 py-1 rounded ${DIFFICULTY_COLORS[difficultyLabel]}`}
                      >
                        {difficultyLabel}
                      </span>
                    </div>
                    <p className="text-gray-800 mb-2 line-clamp-3">{mistake.question_text}</p>
                    <div className="flex justify-between items-center text-sm text-gray-400">
                      <span>{mistake.chapter}</span>
                      <span>{formatDate(mistake.created_at)}</span>
                    </div>
                  </div>
                );
              })}
            </div>

            {filteredMistakes.length === 0 && (
              <div className="text-center py-12 text-gray-500">暂无错题记录</div>
            )}
          </>
        )}
      </div>
    </MainLayout>
  );
};

export default MistakesPage;
```

- [ ] **Step 3: 验证列表页拉取真实数据**

添加一条新错题后跳转到 `/mistakes`，确认列表中显示刚添加的记录（包括科目、章节、内容、难度标签、日期）。

- [ ] **Step 4: 运行前端构建检查**

```bash
cd frontend
npm run build
```

预期：构建成功，无 TypeScript 类型错误。

- [ ] **Step 5: 提交**

```bash
git add frontend/src/app/mistakes/page.tsx
git commit -m "feat: 错题列表页改为从后端拉取真实数据"
```

---

### Task 5: 端到端验证与回归测试

**Files:**
- 无需修改文件

- [ ] **Step 1: 运行后端完整测试**

```bash
cd backend
pytest -v
```

预期：所有测试通过，包括新增的 grade 字符串/null 用例。

- [ ] **Step 2: 运行前端构建**

```bash
cd frontend
npm run build
```

预期：构建成功，exit 0。

- [ ] **Step 3: 手动端到端验证**

1. 登录账户
2. 访问 `/mistakes/add`
3. 选择孩子、填写表单、添加标签、填写年级标签
4. 提交后跳转到 `/mistakes`
5. 确认新错题出现在列表中
6. 切换科目/难度筛选，确认筛选正常
7. 切换孩子，确认列表按孩子刷新

- [ ] **Step 4: 提交（若仅有验证，无需单独提交）**

---

### Task 6: 推送分支并创建 Pull Request

**Files:**
- 无需修改文件

- [ ] **Step 1: 推送功能分支**

```bash
git push -u origin feature/add-mistake-completion
```

- [ ] **Step 2: 创建 Pull Request**

```bash
gh pr create --title "feat: 完成错题添加功能" --body "$(cat <<'EOF'
## 变更摘要
- 后端错题 grade 字段从必填整数改为可选字符串标签
- 前端添加错题页面接入真实后端提交，增加孩子选择、年级标签、知识点标签
- 前端错题列表页改为从后端拉取真实数据

## 测试计划
- [ ] 运行 `cd backend && pytest -v` 所有测试通过
- [ ] 运行 `cd frontend && npm run build` 构建成功
- [ ] 手动验证：添加错题后能在列表页看到新记录
- [ ] 验证切换孩子后列表刷新

## 设计文档
- docs/superpowers/specs/2026-07-11-add-mistake-completion-design.md

## 计划文档
- docs/superpowers/plans/2026-07-11-add-mistake-completion.md
EOF
)"
```

- [ ] **Step 3: 等待审查通过后合并**

```bash
gh pr merge <pr-number> --squash
```

---

## Self-Review

- **Spec coverage:**
  - grade 改为可选字符串标签 ✅（Task 1）
  - 前端 add 页真实提交 ✅（Task 3）
  - 孩子选择默认第一个、可切换 ✅（Task 3、Task 4）
  - 年级标签输入 ✅（Task 3）
  - 知识点标签输入 ✅（Task 3）
  - 列表页真实数据 ✅（Task 4）
  - 端到端验证 ✅（Task 5）

- **Placeholder scan:** 无 TBD/TODO/模糊描述；所有代码块为完整可运行代码。

- **Type consistency:**
  - 后端 `MistakeCreate/MistakeUpdate/MistakeResponse/MistakeModel.grade` 统一为 `Optional[str]`
  - 前端 `Mistake.grade` 同步为 `string?`
  - 难度映射：`简单→1`、`中等→3`、`困难→5` 前后端一致
  - API 调用参数与 `mistakesAPI.createMistake` 签名一致
