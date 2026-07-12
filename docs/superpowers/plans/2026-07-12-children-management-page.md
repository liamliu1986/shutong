# 前端孩子管理功能实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现前端孩子管理页面 `/children`，支持查看、添加、删除孩子，并在主导航栏增加入口。

**Architecture:** 新建 Next.js 14 App Router Client Component 页面，使用现有 `useAuth` 进行登录态校验，调用 `childrenAPI` 完成数据交互；页面顶部为添加表单，下方为孩子卡片列表。

**Tech Stack:** Next.js 14 + React + TypeScript + Tailwind CSS + Axios

## Global Constraints

- 所有代码注释使用中文
- 提交信息使用中文，类型前缀小写
- 不引入新的依赖
- 复用现有 `frontend/src/lib/api.ts` 中的 `childrenAPI`
- 复用现有 `frontend/src/components/layout/MainLayout.tsx` 布局
- 复用现有 `frontend/src/hooks/useAuth.tsx` 进行登录态校验
- 孩子年级范围固定为 7-12，对应「初一」到「高三」
- 科目选项固定为：数学、物理、化学、英语
- 所有输入错误和接口错误均需在页面上显示中文提示
- 通过 `feature/children-management-page` 分支提交 PR 合并到 `main`

---

### Task 1: 创建 `/children` 页面组件

**Files:**
- Create: `frontend/src/app/children/page.tsx`

**Interfaces:**
- Consumes: `useAuth()` 的 `user` 与 `isLoading`、`childrenAPI.getChildren/createChild/deleteChild`、`Child` 类型
- Produces: 默认导出的 `ChildrenPage` 组件，渲染在 `/children` 路由

- [ ] **Step 1: 验证当前状态（失败证据）**

启动前端开发服务器：

```bash
cd frontend
npm run dev
```

在浏览器访问 `http://localhost:3000/children`，预期看到 Next.js 404 页面，因为孩子管理页面尚未创建。

- [ ] **Step 2: 编写 `/children` 页面**

创建 `frontend/src/app/children/page.tsx`，完整内容如下：

```tsx
'use client';

import React, { useCallback, useEffect, useState } from 'react';
import MainLayout from '@/components/layout/MainLayout';
import { useAuth } from '@/hooks/useAuth';
import { childrenAPI } from '@/lib/api';
import { Child } from '@/types';
import axios from 'axios';

/**
 * 年级选项（7-12 对应初一至高三）
 */
const GRADE_OPTIONS: { value: number; label: string }[] = [
  { value: 7, label: '初一' },
  { value: 8, label: '初二' },
  { value: 9, label: '初三' },
  { value: 10, label: '高一' },
  { value: 11, label: '高二' },
  { value: 12, label: '高三' },
];

/**
 * 科目选项
 */
const SUBJECT_OPTIONS = ['数学', '物理', '化学', '英语'];

/**
 * 将年级数值转换为中文标签
 */
const getGradeLabel = (grade: number): string => {
  const option = GRADE_OPTIONS.find((item) => item.value === grade);
  return option ? option.label : `年级 ${grade}`;
};

/**
 * 格式化日期字符串
 */
const formatDate = (dateString?: string): string => {
  if (!dateString) return '';
  return new Date(dateString).toLocaleDateString('zh-CN');
};

const ChildrenPage: React.FC = () => {
  const { user, isLoading: isAuthLoading } = useAuth();

  const [children, setChildren] = useState<Child[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [listError, setListError] = useState('');
  const [formError, setFormError] = useState('');

  const [name, setName] = useState('');
  const [grade, setGrade] = useState<number>(7);
  const [subjects, setSubjects] = useState<string[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);

  /**
   * 拉取孩子列表
   */
  const fetchChildren = useCallback(() => {
    setIsLoading(true);
    setListError('');

    childrenAPI
      .getChildren()
      .then((response) => {
        setChildren(response.data || []);
      })
      .catch((err: unknown) => {
        let message = '加载孩子列表失败，请稍后重试';
        if (axios.isAxiosError(err)) {
          const detail = err.response?.data?.detail;
          if (typeof detail === 'string') {
            message = detail;
          }
        }
        setListError(message);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, []);

  useEffect(() => {
    if (user) {
      fetchChildren();
    }
  }, [user, fetchChildren]);

  /**
   * 切换科目选中状态
   */
  const toggleSubject = (subject: string) => {
    setSubjects((prev) =>
      prev.includes(subject) ? prev.filter((s) => s !== subject) : [...prev, subject]
    );
  };

  /**
   * 重置表单
   */
  const resetForm = () => {
    setName('');
    setGrade(7);
    setSubjects([]);
    setFormError('');
  };

  /**
   * 提交添加孩子表单
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError('');

    if (!name.trim()) {
      setFormError('请输入孩子姓名');
      return;
    }

    setIsSubmitting(true);

    try {
      await childrenAPI.createChild({
        name: name.trim(),
        grade,
        subjects,
      });
      resetForm();
      fetchChildren();
    } catch (err: unknown) {
      let message = '添加失败，请稍后重试';
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail;
        if (typeof detail === 'string') {
          message = detail;
        } else if (Array.isArray(detail)) {
          message = detail.map((item: { msg?: string }) => item.msg || JSON.stringify(item)).join('；');
        }
      }
      setFormError(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  /**
   * 删除孩子
   */
  const handleDelete = async (childId: string) => {
    if (!window.confirm('确定删除该孩子吗？相关错题和试卷数据可能受到影响。')) {
      return;
    }

    try {
      await childrenAPI.deleteChild(childId);
      fetchChildren();
    } catch (err: unknown) {
      let message = '删除失败，请稍后重试';
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail;
        if (typeof detail === 'string') {
          message = detail;
        }
      }
      setListError(message);
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
        <div className="text-center py-12 text-gray-500">请先登录</div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-gray-800">孩子管理</h1>

        {/* 添加孩子表单 */}
        <section className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">添加孩子</h2>

          {formError && (
            <div className="mb-4 p-3 bg-red-50 text-red-600 rounded-md text-sm">{formError}</div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  姓名 <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="请输入孩子姓名"
                  maxLength={50}
                  className="w-full border rounded-lg px-3 py-2"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  年级 <span className="text-red-500">*</span>
                </label>
                <select
                  value={grade}
                  onChange={(e) => setGrade(Number(e.target.value))}
                  className="w-full border rounded-lg px-3 py-2"
                >
                  {GRADE_OPTIONS.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">科目</label>
                <div className="flex flex-wrap gap-3 pt-2">
                  {SUBJECT_OPTIONS.map((subject) => (
                    <label key={subject} className="flex items-center space-x-1 text-sm text-gray-700">
                      <input
                        type="checkbox"
                        checked={subjects.includes(subject)}
                        onChange={() => toggleSubject(subject)}
                        className="rounded border-gray-300"
                      />
                      <span>{subject}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>

            <div className="pt-2">
              <button
                type="submit"
                disabled={isSubmitting}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSubmitting ? '添加中...' : '添加'}
              </button>
            </div>
          </form>
        </section>

        {/* 孩子列表 */}
        <section>
          <h2 className="text-lg font-semibold text-gray-800 mb-4">孩子列表</h2>

          {isLoading && (
            <div className="flex justify-center items-center h-64">
              <span className="text-gray-500">加载中...</span>
            </div>
          )}

          {listError && !isLoading && (
            <div className="bg-red-50 text-red-600 p-4 rounded-lg text-sm flex justify-between items-center">
              <span>{listError}</span>
              <button
                type="button"
                onClick={fetchChildren}
                className="px-3 py-1 border border-red-300 rounded hover:bg-red-100 transition-colors"
              >
                重试
              </button>
            </div>
          )}

          {!isLoading && !listError && children.length === 0 && (
            <div className="text-center py-12 text-gray-500 bg-white rounded-lg shadow">
              暂无孩子，请添加一个孩子
            </div>
          )}

          {!isLoading && !listError && children.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {children.map((child) => (
                <div
                  key={child.id}
                  className="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow"
                >
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h3 className="font-semibold text-gray-800">{child.name}</h3>
                      <span className="text-xs px-2 py-0.5 rounded bg-blue-100 text-blue-800">
                        {getGradeLabel(child.grade)}
                      </span>
                    </div>
                    <button
                      type="button"
                      onClick={() => handleDelete(child.id)}
                      className="text-red-500 hover:text-red-700 text-sm"
                    >
                      删除
                    </button>
                  </div>

                  {child.subjects && child.subjects.length > 0 && (
                    <div className="flex flex-wrap gap-2 mb-3">
                      {child.subjects.map((subject) => (
                        <span
                          key={subject}
                          className="text-xs px-2 py-0.5 rounded bg-gray-100 text-gray-700"
                        >
                          {subject}
                        </span>
                      ))}
                    </div>
                  )}

                  <div className="text-xs text-gray-400">
                    创建时间：{formatDate(child.created_at)}
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </MainLayout>
  );
};

export default ChildrenPage;
```

- [ ] **Step 3: 运行前端类型检查**

```bash
cd frontend
npx tsc --noEmit
```

预期：无 TypeScript 类型错误。若出现 `childrenAPI` 返回类型相关报错，检查 `frontend/src/lib/api.ts` 中的 `getChildren` 是否已正确定义。

- [ ] **Step 4: 手动验证页面可访问**

刷新浏览器 `http://localhost:3000/children`，预期：
- 页面正常加载，显示「孩子管理」标题
- 显示「添加孩子」表单（姓名、年级下拉、科目复选框、添加按钮）
- 显示「孩子列表」区域（初次为空时提示「暂无孩子，请添加一个孩子」）

- [ ] **Step 5: 提交**

```bash
git add frontend/src/app/children/page.tsx
git commit -m "feat: 添加孩子管理页面"
```

---

### Task 2: 在主导航栏增加「孩子管理」入口

**Files:**
- Modify: `frontend/src/components/layout/MainLayout.tsx`

**Interfaces:**
- Consumes: 无新增依赖
- Produces: `navItems` 数组增加 `/children` 导航项，页面左侧菜单显示「孩子管理」

- [ ] **Step 1: 修改导航栏配置**

修改 `frontend/src/components/layout/MainLayout.tsx` 中的 `navItems` 数组，在「首页」之后插入「孩子管理」：

```tsx
const navItems = [
  { href: '/dashboard', label: '首页', icon: '📊' },
  { href: '/children', label: '孩子管理', icon: '👶' },
  { href: '/knowledge-graph', label: '知识图谱', icon: '📚' },
  { href: '/mistakes', label: '错题本', icon: '📝' },
  { href: '/question-bank', label: '题库管理', icon: '❓' },
];
```

- [ ] **Step 2: 运行前端类型检查与构建**

```bash
cd frontend
npx tsc --noEmit
npm run build
```

预期：类型检查通过，Next.js 构建成功，exit 0。

- [ ] **Step 3: 手动验证导航入口**

启动开发服务器后访问任意已登录页面，预期左侧导航栏从上至下依次为：首页、孩子管理、知识图谱、错题本、题库管理。点击「孩子管理」跳转到 `/children`。

- [ ] **Step 4: 提交**

```bash
git add frontend/src/components/layout/MainLayout.tsx
git commit -m "feat: 在主导航栏添加孩子管理入口"
```

---

### Task 3: 端到端验证

**Files:**
- 无需修改文件

- [ ] **Step 1: 启动后端服务**

确认后端服务已启动并监听 `http://localhost:8000`：

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- [ ] **Step 2: 启动前端开发服务器**

```bash
cd frontend
npm run dev
```

- [ ] **Step 3: 完整手动验证**

1. 访问 `http://localhost:3000/login`，使用已有账户登录。
2. 在左侧导航栏点击「孩子管理」，进入 `/children`。
3. 填写姓名「测试孩子」，选择年级「高一」，勾选「数学」「物理」，点击「添加」。
4. 确认列表中出现新添加的孩子卡片，显示姓名、「高一」标签、「数学」「物理」标签、创建时间。
5. 切换到 `/mistakes/add`，确认「孩子」选择器中包含刚添加的「测试孩子」。
6. 返回 `/children`，点击孩子卡片上的「删除」，在 `window.confirm` 确认框中点击「确定」。
7. 确认列表中该孩子卡片消失。
8. 刷新页面，确认列表保持为空或仅显示剩余孩子。

- [ ] **Step 4: 运行前端构建**

```bash
cd frontend
npm run build
```

预期：构建成功，exit 0，无 TypeScript 类型错误。

- [ ] **Step 5: 提交（若仅有验证，无需单独提交）**

---

### Task 4: 推送分支并创建 Pull Request

**Files:**
- 无需修改文件

- [ ] **Step 1: 推送功能分支**

```bash
git push -u origin feature/children-management-page
```

- [ ] **Step 2: 创建 Pull Request**

```bash
gh pr create --title "feat: 实现前端孩子管理页面" --body "$(cat <<'EOF'
## 变更摘要
- 新增 `/children` 页面，支持查看、添加、删除孩子
- 添加表单包含姓名、年级（初一至高三）、科目（数学/物理/化学/英语）
- 在 `MainLayout` 主导航栏增加「孩子管理」入口

## 测试计划
- [ ] 运行 `cd frontend && npm run build` 构建成功
- [ ] 登录后访问 `/children`，能正常加载页面和表单
- [ ] 添加孩子后列表中显示新卡片
- [ ] 删除孩子后列表同步更新
- [ ] 在 `/mistakes/add` 的孩子选择器中能看到新增孩子

## 设计文档
- docs/superpowers/specs/2026-07-12-children-management-design.md

## 计划文档
- docs/superpowers/plans/2026-07-12-children-management-page.md
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
  - `/children` 独立页面 ✅（Task 1）
  - 查看孩子列表 ✅（Task 1）
  - 添加孩子表单（姓名、年级、科目）✅（Task 1）
  - 删除孩子并确认 ✅（Task 1）
  - 加载/空状态/错误处理 ✅（Task 1）
  - 主导航栏增加入口 ✅（Task 2）
  - 端到端验证 ✅（Task 3）

- **Placeholder scan:** 无 TBD/TODO/模糊描述；所有代码块为完整可运行代码。

- **Type consistency:**
  - `Child` 类型已存在，`grade` 为 `number`，`subjects` 为 `string[]`，与后端 `ChildCreate` 一致
  - `childrenAPI.createChild` 参数为 `{ name: string; grade: number; subjects: string[] }`，页面调用时类型匹配
  - `childrenAPI.getChildren` 返回数组直接赋值给 `Child[]`
