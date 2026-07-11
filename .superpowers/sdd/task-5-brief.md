# Task 5: 前端登录注册页面

## 任务目标
实现前端登录注册页面，包含认证状态管理、登录表单、注册表单以及对应的页面。

## 工作目录
D:/Projects/shutong/.worktrees/feature-frontend-basic-framework/frontend

## 需要创建的文件
1. `src/hooks/useAuth.ts` - 认证状态管理 Hook
2. `src/components/auth/LoginForm.tsx` - 登录表单组件
3. `src/components/auth/RegisterForm.tsx` - 注册表单组件
4. `src/app/login/page.tsx` - 登录页面
5. `src/app/register/page.tsx` - 注册页面

## 技术要求
- 使用 TypeScript
- 使用 React Hook Form 或 useState 管理表单状态
- 使用 Tailwind CSS 进行样式设计
- 使用 Next.js App Router
- 集成已有的 `@/lib/api` 中的 authAPI

## 认证流程要求（用户已确认）
1. 登录/注册成功后立即跳转到 `/dashboard`
2. 未登录访问需要认证的页面应自动重定向到 `/login`
3. MVP 阶段暂不实现 token 刷新机制

## 接口依赖
- `POST /api/v1/auth/login` - 登录
- `POST /api/v1/auth/register` - 注册
- `GET /api/v1/users/me` - 获取当前用户信息

## 详细实现要求

### 1. hooks/useAuth.ts
- 创建 AuthProvider 上下文
- 提供 user, loading, login, register, logout 方法
- 使用 localStorage 存储 token
- 登录/注册成功后自动设置用户状态

### 2. components/auth/LoginForm.tsx
- 邮箱和密码输入框
- 表单验证（邮箱格式、密码不为空）
- 错误提示显示
- 加载状态处理
- 登录成功后跳转到 /dashboard

### 3. components/auth/RegisterForm.tsx
- 用户名、邮箱、密码、确认密码输入框
- 表单验证（用户名长度、邮箱格式、密码长度、密码一致性）
- 错误提示显示
- 加载状态处理
- 注册成功后跳转到 /dashboard

### 4. app/login/page.tsx
- 使用 AuthProvider 包裹
- 居中布局，卡片式设计
- 包含 Logo 和标题
- 底部有注册页面链接

### 5. app/register/page.tsx
- 使用 AuthProvider 包裹
- 居中布局，卡片式设计
- 包含 Logo 和标题
- 底部有登录页面链接

## 测试要求
- 创建 `src/__tests__/useAuth.test.ts` 测试认证 Hook
- 创建 `src/__tests__/LoginForm.test.tsx` 测试登录表单
- 创建 `src/__tests__/RegisterForm.test.tsx` 测试注册表单

## 验收标准
- [ ] 所有文件按要求创建
- [ ] 登录表单能正确提交并跳转
- [ ] 注册表单能正确提交并跳转
- [ ] 表单验证正常工作
- [ ] 错误提示正确显示
- [ ] 代码无 TypeScript 类型错误
- [ ] 所有测试通过
