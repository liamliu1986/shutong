# 错题添加功能完整实现设计文档

**日期：** 2026-07-11
**主题：** 完成错题添加功能（前端提交 + 列表真实数据 + grade 字段语义调整）

---

## 1. 背景与目标

当前 `frontend/src/app/mistakes/add/page.tsx` 的表单提交逻辑只有 TODO，未真正调用后端 API。同时错题列表页 `/mistakes` 仍使用写死的模拟数据，导致添加错题后用户无法在列表中看到新记录。

本次设计目标：
1. 补全前端添加错题页面的真实后端提交链路。
2. 将错题列表页改为从后端拉取真实数据。
3. 根据产品设计理念调整 `grade` 字段：从「必填学年整数」改为「可选的学年标签字符串」。
4. 增加孩子选择、年级标签输入、知识点标签输入，使表单与后端数据模型对齐。

---

## 2. 设计哲学

- **学科是核心维度**：知识图谱基于学科构建，学年仅为辅助标签。
- **默认简化，支持切换**：有多个孩子时默认选中第一个，允许用户切换。
- **真实数据优先**：添加完成后列表页应立即反映最新数据。
- **MVP 范围内不做过度设计**：标签使用简单逗号分隔输入，不接入复杂知识图谱选择器。

---

## 3. 后端变更

### 3.1 文件：`backend/app/schemas/mistake.py`

将 `grade` 从必填整数改为可选字符串标签：

- `MistakeCreate.grade`: `int = Field(ge=1, le=12)` → `Optional[str] = None`
- `MistakeUpdate.grade`: `Optional[int]` → `Optional[str]`
- `MistakeResponse.grade`: `int` → `str = ""`

其他字段保持不变。

### 3.2 文件：`backend/app/models/mistake.py`

- `MistakeModel.grade`: `int = Field(ge=1, le=12)` → `Optional[str] = None`

### 3.3 文件：`backend/app/api/mistakes.py`

无需修改。`child_id` 归属校验逻辑保持不变。

### 3.4 文件：`backend/app/services/mistake_service.py`

无需修改。`create_mistake` 直接使用 `data.model_dump()`，schema 调整后自然支持新的 grade 类型。

### 3.5 文件：`backend/tests/test_mistakes.py`

新增/更新测试用例：
- 创建错题时不传 `grade` 应成功。
- 创建错题时 `grade` 为字符串标签（如 "高一"）应成功。
- 创建错题时 `grade` 为 `null` 应成功。

---

## 4. 前端变更

### 4.1 文件：`frontend/src/types/index.ts`

调整 `Mistake` 接口：
- `grade: number` → `grade?: string`

新增辅助类型（如需要）：
- 难度映射常量：`{ 简单: 1, 中等: 3, 困难: 5 }`

### 4.2 文件：`frontend/src/app/mistakes/add/page.tsx`

表单字段扩展为：
- `child_id`：下拉选择，默认 `user.children[0].id`
- `subject`：科目下拉（数学/物理/化学/英语）
- `chapter`：章节文本输入
- `content`：题目内容文本域 → 映射为后端 `question_text`
- `answer`：正确答案文本域
- `analysis`：解析文本域 → 映射为后端 `explanation`
- `difficulty`：难度下拉（简单/中等/困难）→ 映射为后端数字 1/3/5
- `grade`：可选学年标签文本输入（如 "高一"）
- `source`：来源文本输入
- `tags`：标签文本输入，逗号分隔 → 映射为后端字符串数组

提交逻辑：
1. 校验 `child_id` 已选择。
2. 构造请求体，完成字段映射。
3. 调用 `mistakesAPI.createMistake`。
4. 显示加载态，禁用提交按钮。
5. 成功：跳转 `/mistakes`。
6. 失败：显示后端返回的错误信息或通用网络错误。

### 4.3 文件：`frontend/src/app/mistakes/page.tsx`

- 移除模拟数据数组。
- 增加 `child_id` 选择器，默认第一个孩子。
- 使用 `useEffect` 在 `child_id` 变化时调用 `mistakesAPI.getMistakes`。
- 难度数字映射回中文标签：1→简单，3→中等，5→困难。
- 显示加载态、错误态、空状态。
- 保持现有筛选 UI，在前端内存中过滤已加载数据。

### 4.4 文件：`frontend/src/lib/api.ts`

无需修改。`mistakesAPI.createMistake` 和 `mistakesAPI.getMistakes` 已存在。

---

## 5. 数据流

```
用户访问 /mistakes/add
  → useAuth 提供 user（含 children）
  → 默认选中 user.children[0].id
  → 用户填写表单
  → 点击提交
  → handleSubmit 构造 CreateMistakePayload
       child_id: 所选孩子 ID
       subject: 表单 subject
       grade: 表单 grade（可选字符串）
       chapter: 表单 chapter
       question_text: 表单 content
       answer: 表单 answer
       explanation: 表单 analysis
       difficulty: {简单:1, 中等:3, 困难:5}[表单 difficulty]
       source: 表单 source
       tags: 表单 tags 按逗号分割并 trim
       knowledge_points: []
  → POST /mistakes
  → 成功后 router.push('/mistakes')
  → /mistakes 页面 useEffect 拉取列表
  → 显示真实错题数据
```

---

## 6. 错误处理

| 场景 | 处理方式 |
|---|---|
| 未选择孩子 | 提交按钮禁用，显示提示 |
| 必填字段为空 | HTML5 `required` 拦截 |
| 后端返回 403 | 提示「无权访问该孩子数据」 |
| 后端返回 422 | 显示校验错误详情 |
| 网络错误 | 显示「网络异常，请稍后重试」 |
| 列表页加载失败 | 显示错误信息 + 重试按钮 |

---

## 7. 测试策略

### 后端测试

- 更新 `backend/tests/test_mistakes.py`：
  - 不传 `grade` 创建错题 → 200
  - `grade="高一"` 创建错题 → 200
  - `grade=null` 创建错题 → 200
  - 返回的 `grade` 类型为字符串或 null

### 前端验证

- `cd frontend && npm run build` 无 TypeScript 错误。
- 手动流程：登录 → 添加错题 → 列表页显示新记录。

---

## 8. 兼容性说明

- MongoDB 中已存在的 `grade` 整数字段不会导致异常：Pydantic 在响应时会按新 schema 序列化；旧整数在读取时若以字符串输出，FastAPI 会自动转换。
- 新创建的错题 `grade` 为字符串或 null，与旧数据共存。

---

## 9. 范围边界

**在本次范围内：**
- 后端 `grade` 类型调整
- 前端 add 页真实提交
- 前端列表页真实数据

**不在本次范围内：**
- 图片上传（`question_image_url`）
- 知识图谱知识点选择器（`knowledge_points` 传空数组）
- AI 解析真实接入（保持现有模拟实现）
- 分页无限滚动（列表页使用基础分页参数）

---

## 10. 待确认事项

无。所有关键决策已在 brainstorming 阶段确认：
- grade 改为可选字符串标签 ✅
- 孩子选择默认第一个、可切换 ✅
- 列表页改为真实数据 ✅
- 增加简单标签输入框 ✅
