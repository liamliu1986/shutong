# 书童 - 智能学习助手 设计文档

> **项目名称**：书童（ShuTong）
> **版本**：v1.0
> **创建日期**：2026-07-09
> **状态**：设计完成，待审核

---

## 一、项目概述

### 1.1 项目背景

书童是一款面向家长辅助孩子学习的智能学习助手 Web 应用。通过知识图谱、错题本、学习计划、测评系统和题库管理五大核心模块，帮助家长科学管理孩子的学习过程，精准定位薄弱环节，提升学习效率。

### 1.2 目标用户

- **主要用户**：家长（辅助孩子学习）
- **使用场景**：家长帮助孩子记录错题、查看学习进度、制定学习计划

### 1.3 核心能力

1. **知识图谱构建**：初高中语数英物化生六科知识图谱，掌握度评估
2. **错题本功能**：提交错题（图片），识别题目，入库题目，生成答案与动态解析图，错题本整理打印，根据错题调整知识图谱掌握度
3. **学习计划**：制定学习计划，根据测评结果动态调整
4. **测评系统**：根据知识图谱生成题目测试，评估掌握程度
5. **题库管理**：上传试卷，自动切题归类，自由组卷，原卷复现测试

---

## 二、技术架构

### 2.1 技术选型

| 层级 | 技术栈 | 说明 |
|------|--------|------|
| 前端 | Next.js 14 + TypeScript + Tailwind CSS + shadcn/ui | SSR、组件化、响应式 |
| 后端 | Python 3.11 + FastAPI + SQLAlchemy + Pydantic | 异步高性能、类型安全 |
| 数据库 | MongoDB 7 + Neo4j 5 | 文档存储 + 图数据库 |
| AI 服务 | 百度 OCR + 本地 Qwen/Llama | 混合方案，平衡成本与质量 |
| 部署 | Docker Compose | 单机部署，简单维护 |

### 2.2 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                      用户浏览器                               │
│                   (家长/孩子)                                 │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTPS
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   Next.js 前端                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐    │
│  │ 知识图谱页面 │ │  错题本页面  │ │    学习计划页面      │    │
│  └─────────────┘ └─────────────┘ └─────────────────────┘    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐    │
│  │ 题库管理页面 │ │  测评中心    │ │    用户中心          │    │
│  └─────────────┘ └─────────────┘ └─────────────────────┘    │
└─────────────────────────┬───────────────────────────────────┘
                          │ API 调用
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI 后端                                │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐    │
│  │ 知识图谱模块 │ │  错题本模块  │ │    AI 服务模块       │    │
│  └─────────────┘ └─────────────┘ └─────────────────────┘    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐    │
│  │ 用户认证模块 │ │ 学习计划模块 │ │    题库管理模块      │    │
│  └─────────────┘ └─────────────┘ └─────────────────────┘    │
│  ┌─────────────┐                                             │
│  │ 测评模块    │                                             │
│  └─────────────┘                                             │
└─────────────────────────┬───────────────────────────────────┘
                          │
            ┌─────────────┴─────────────┐
            ▼                           ▼
┌───────────────────┐       ┌───────────────────┐
│    MongoDB        │       │      Neo4j        │
│ (用户/错题/计划)   │       │   (知识图谱)       │
└───────────────────┘       └───────────────────┘
            │
            ▼
┌───────────────────┐
│   云端 AI 服务    │
│ (OCR/题目生成)    │
└───────────────────┘
```

### 2.3 架构特点

1. **前后端分离**：Next.js 前端 + FastAPI 后端，通过 RESTful API 通信
2. **数据分层存储**：MongoDB 存储结构化数据，Neo4j 存储知识图谱关系
3. **AI 模块独立**：OCR 和题目生成可灵活替换服务提供商
4. **单体部署**：Docker Compose 一键部署，适合个人项目

---

## 三、数据模型

### 3.1 MongoDB 数据模型

#### 用户集合 (users)

```javascript
{
  _id: ObjectId,
  username: String,        // 家长用户名
  email: String,
  password_hash: String,
  children: [{             // 孩子列表
    id: String,
    name: String,
    grade: Number,         // 年级 (7-12)
    subjects: [String]     // 学习科目
  }],
  created_at: DateTime,
  updated_at: DateTime
}
```

#### 错题集合 (mistakes)

```javascript
{
  _id: ObjectId,
  child_id: String,        // 关联孩子
  subject: String,         // 科目
  grade: Number,
  chapter: String,         // 章节
  knowledge_points: [String], // 关联知识点ID列表

  // 题目内容
  question_image_url: String,  // 原始题目图片
  question_text: String,       // OCR识别的文字
  question_latex: String,      // LaTeX格式（数学公式）

  // 答案与解析
  answer: String,
  explanation: String,         // 文字解析
  explanation_gif_url: String, // 动态解析图URL

  // 元数据
  difficulty: Number,          // 难度 1-5
  source: String,              // 来源（课本/试卷/练习册）
  tags: [String],

  created_at: DateTime,
  updated_at: DateTime
}
```

#### 题库集合 (question_bank)

```javascript
{
  _id: ObjectId,
  child_id: String,           // 关联孩子
  subject: String,            // 科目
  grade: Number,

  // 题目内容
  question_type: String,      // "choice" | "fill_blank" | "solve"
  question_text: String,      // 题目文字
  question_latex: String,     // LaTeX 格式
  question_image_url: String, // 原始图片

  // 选项（选择题）
  options: [{
    label: String,            // "A" | "B" | "C" | "D"
    content: String,
    is_correct: Boolean
  }],

  // 答案与解析
  answer: String,
  explanation: String,

  // 分类信息
  chapter: String,
  knowledge_point_ids: [String],
  difficulty: Number,         // 1-5
  tags: [String],

  // 来源
  source_type: String,        // "single" | "paper"
  source_paper_id: ObjectId,  // 来源试卷ID
  source_paper_name: String,
  question_index: Number,     // 在原卷中的题号

  // 使用统计
  used_count: Number,         // 被组卷次数
  correct_rate: Number,       // 正确率

  created_at: DateTime,
  updated_at: DateTime
}
```

#### 试卷集合 (papers)

```javascript
{
  _id: ObjectId,
  child_id: String,
  name: String,               // 试卷名称
  subject: String,
  grade: Number,

  // 试卷图片
  images: [{
    page: Number,
    url: String
  }],

  // 题目列表
  question_ids: [ObjectId],   // 关联的题目ID
  question_count: Number,

  // 元数据
  source: String,             // 来源（学校/教辅/网络）
  exam_date: Date,            // 考试日期
  total_score: Number,        // 总分

  created_at: DateTime
}
```

#### 学习计划集合 (study_plans)

```javascript
{
  _id: ObjectId,
  child_id: String,
  subject: String,

  // 计划内容
  title: String,
  description: String,
  start_date: Date,
  end_date: Date,

  // 每日任务
  daily_tasks: [{
    date: Date,
    tasks: [{
      type: String,       // "review" | "practice" | "test"
      knowledge_point_id: String,
      description: String,
      completed: Boolean,
      completed_at: DateTime
    }]
  }],

  // 状态
  status: String,         // "active" | "completed" | "paused"
  progress: Number,       // 完成百分比

  created_at: DateTime,
  updated_at: DateTime
}
```

#### 测评记录集合 (assessments)

```javascript
{
  _id: ObjectId,
  child_id: String,
  subject: String,

  // 测试内容
  questions: [{
    question_id: String,
    knowledge_point_id: String,
    question_text: String,
    options: [String],
    correct_answer: String,
    child_answer: String,
    is_correct: Boolean,
    time_spent: Number     // 秒
  }],

  // 结果
  score: Number,
  total_questions: Number,
  correct_count: Number,

  // 知识点掌握度更新
  knowledge_mastery_updates: [{
    knowledge_point_id: String,
    old_mastery: Number,
    new_mastery: Number
  }],

  created_at: DateTime
}
```

### 3.2 Neo4j 知识图谱模型

```cypher
// 节点类型
(:Subject {id, name, grade_level})           // 学科
(:Chapter {id, name, order})                  // 章节
(:KnowledgePoint {id, name, description, importance}) // 知识点
(:Question {id, difficulty})                  // 题目（仅ID，详情在MongoDB）

// 关系类型
(:Subject)-[:HAS_CHAPTER {order}]->(:Chapter)
(:Chapter)-[:HAS_KNOWLEDGE_POINT {order}]->(:KnowledgePoint)
(:KnowledgePoint)-[:RELATED_TO {strength}]->(:KnowledgePoint)
(:Question)-[:TESTS]->(:KnowledgePoint)
(:KnowledgePoint)-[:PREREQUISITE_OF]->(:KnowledgePoint)

// 学生掌握度（关系属性）
(:Child)-[:Grades {mastery: Float, last_assessed: DateTime}]->(:KnowledgePoint)
```

---

## 四、核心功能模块

### 4.1 知识图谱模块

#### 功能清单

- 学科知识图谱初始化（预置初高中语数英物化生）
- 知识点关系管理（前置、关联、层级）
- 学生掌握度评估与更新
- 知识图谱可视化展示

#### 掌握度计算公式

```
新掌握度 = 旧掌握度 × 衰减系数 + 测试得分 × 权重

其中：
- 衰减系数 = 0.95（时间衰减，每过一周未复习）
- 权重 = 0.3（单次测试影响）
- 掌握度范围：0.0 ~ 1.0
```

#### 掌握度等级划分

| 掌握度 | 等级 | 颜色 | 说明 |
|--------|------|------|------|
| 0.0-0.3 | 未掌握 | 🔴 红色 | 需要重点学习 |
| 0.3-0.6 | 初步掌握 | 🟡 黄色 | 需要巩固练习 |
| 0.6-0.8 | 基本掌握 | 🔵 蓝色 | 可以适当复习 |
| 0.8-1.0 | 熟练掌握 | 🟢 绿色 | 已经掌握 |

---

### 4.2 错题本模块

#### 错题录入流程

```
上传图片 → OCR识别 → 信息确认 → 知识点标注 → 入库保存
    │           │           │           │
    ▼           ▼           ▼           ▼
  拍照/相册   提取文字    家长确认    自动+手动
            识别公式    编辑修正    标注知识点
```

#### 功能清单

- 图片上传（拍照/相册）
- OCR 题目识别（文字 + 公式）
- 题目信息编辑与确认
- 知识点自动标注 + 手动修正
- AI 生成答案与解析
- 动态解析图生成（数学/物理）
- 错题按科目/章节/知识点分类
- 错题本导出打印

#### 动态解析图生成

- 数学：几何图形变换、函数图像绘制
- 物理：力学分析图、电路图、运动轨迹
- 化学：分子结构、反应流程图

---

### 4.3 题库管理模块

#### 功能清单

- 上传整张试卷图片
- OCR 自动切题（识别每道题目边界）
- 自动识别题型（选择/填空/解答）
- 自动标注知识点
- 题目入库（单题/批量）
- 题库浏览与筛选
- 自由组卷（从题库选题）
- 原卷复现测试（按原试卷出题）

#### 试卷上传流程

```
上传试卷图片 → 图像预处理 → 自动切题 → 逐题识别
      │              │            │           │
      ▼              ▼            ▼           ▼
   支持多页      去噪/纠偏    识别题目边界   OCR+知识点
                                    │
                                    ▼
                              人工确认/修正
                                    │
                                    ▼
                              批量入库保存
```

#### 自由组卷规则

- 题型分布：选择题、填空题、解答题可配置
- 难度分布：简单:中等:困难 = 3:4:3（可调整）
- 知识点范围：可选择特定知识点
- 排除规则：可排除近期做过的题目
- 优先规则：可优先选择薄弱知识点题目

#### 原卷复现测试

- 支持按原卷顺序出题
- 支持随机打乱题目顺序
- 支持计时模式（模拟真实考试）
- 提交后显示答案与解析
- 自动更新知识点掌握度

---

### 4.4 学习计划模块

#### 计划生成逻辑

```
输入：薄弱知识点列表 + 学习时间 + 科目
      │
      ▼
┌─────────────────────────────────────┐
│         计划生成算法                 │
│  1. 按掌握度排序（低→高）           │
│  2. 计算每个知识点所需时间          │
│  3. 分配到每日学习任务              │
│  4. 插入复习节点（间隔重复）        │
│  5. 预留弹性时间                    │
└─────────────────────────────────────┘
      │
      ▼
输出：每日学习计划表
```

#### 计划调整规则

- 测评成绩提升 → 减少该知识点复习频率
- 测评成绩下降 → 增加该知识点复习频率
- 连续未完成 → 降低每日任务量
- 提前完成 → 增加新知识点或提高难度

---

### 4.5 测评模块

#### 测评类型

| 类型 | 说明 | 题目数 | 时间 |
|------|------|--------|------|
| 日常练习 | 针对单个知识点 | 5-10题 | 15分钟 |
| 章节测试 | 覆盖整个章节 | 15-20题 | 30分钟 |
| 综合测评 | 多个章节混合 | 20-30题 | 45分钟 |
| 原卷测试 | 按原试卷出题 | 原卷题数 | 原卷时间 |

#### 题目生成策略

1. 根据知识点从题库检索
2. 按难度分布选题（易:中:难 = 3:4:3）
3. 确保题型多样（选择/填空/解答）
4. 避免近期做过的原题
5. 优先选择薄弱知识点相关题目

---

## 五、API 设计

### 5.1 API 总览

**Base URL：** `http://localhost:8000/api/v1`

**认证方式：** JWT Token（Bearer Token）

| 模块 | 端点 | 方法 | 说明 |
|------|------|------|------|
| 用户 | /auth/register | POST | 注册 |
| 用户 | /auth/login | POST | 登录 |
| 用户 | /auth/refresh | POST | 刷新Token |
| 用户 | /users/me | GET | 获取当前用户信息 |
| 用户 | /users/me/children | GET/POST | 获取/添加孩子 |
| 知识图谱 | /subjects | GET | 获取学科列表 |
| 知识图谱 | /subjects/{id}/graph | GET | 获取学科知识图谱 |
| 知识图谱 | /knowledge-points/{id} | GET | 获取知识点详情 |
| 知识图谱 | /children/{id}/mastery | GET | 获取孩子掌握度 |
| 错题本 | /mistakes | POST | 创建错题 |
| 错题本 | /mistakes | GET | 获取错题列表 |
| 错题本 | /mistakes/{id} | GET/PUT/DELETE | 错题详情/更新/删除 |
| 错题本 | /mistakes/{id}/explanation | GET | 获取AI解析 |
| 错题本 | /mistakes/export | POST | 导出错题本 |
| 题库 | /question-bank | GET | 获取题库列表 |
| 题库 | /question-bank/{id} | GET/PUT/DELETE | 题目详情/更新/删除 |
| 题库 | /question-bank/batch | POST | 批量导入题目 |
| 试卷 | /papers | POST | 上传试卷 |
| 试卷 | /papers | GET | 获取试卷列表 |
| 试卷 | /papers/{id} | GET/DELETE | 试卷详情/删除 |
| 试卷 | /papers/{id}/recognize | POST | 触发试卷识别 |
| 试卷 | /papers/{id}/questions | GET | 获取试卷题目 |
| 组卷 | /generate-paper | POST | 自由组卷 |
| 组卷 | /generate-paper/preview | POST | 预览组卷结果 |
| 学习计划 | /study-plans | POST | 创建学习计划 |
| 学习计划 | /study-plans | GET | 获取计划列表 |
| 学习计划 | /study-plans/{id} | GET/PUT/DELETE | 计划详情/更新/删除 |
| 学习计划 | /study-plans/{id}/tasks | GET | 获取每日任务 |
| 学习计划 | /study-plans/{id}/tasks/{taskId} | PUT | 更新任务状态 |
| 测评 | /assessments | POST | 创建测评 |
| 测评 | /assessments/{id} | GET | 获取测评详情 |
| 测评 | /assessments/{id}/submit | POST | 提交测评答案 |
| 测评 | /assessments/paper | POST | 原卷测试 |
| AI服务 | /ocr/recognize | POST | OCR识别题目 |
| AI服务 | /ai/generate-explanation | POST | 生成答案解析 |
| AI服务 | /ai/generate-questions | POST | 生成测试题目 |

---

## 六、前端页面设计

### 6.1 页面结构

```
┌─────────────────────────────────────────────────────────────┐
│                      书童 - 智能学习助手                      │
├─────────────────────────────────────────────────────────────┤
│ 首页 │ 知识图谱 │ 错题本 │ 题库管理 │ 学习计划 │ 测评中心 │ 我的 │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 核心页面

1. **首页（仪表盘）**：学习进度概览、今日任务、最近动态
2. **知识图谱页面**：图谱可视化、知识点列表、掌握度展示
3. **错题本页面**：错题列表、筛选、错题详情
4. **错题添加流程**：上传图片 → OCR识别 → 知识点标注 → AI生成解析
5. **题库管理页面**：题库列表、筛选、批量操作
6. **试卷上传页面**：试卷信息填写、图片上传
7. **试卷识别确认页面**：识别结果确认、修正、批量入库
8. **自由组卷页面**：组卷参数配置、难度分布
9. **组卷预览页面**：题目预览、更换题目、确认开始
10. **原卷测试页面**：试卷信息、测试选项、题目预览
11. **测试答题页面**：题目展示、答题、计时、快速跳转
12. **测试结果页面**：得分统计、题目分析、知识点变化、错题回顾

---

## 七、项目结构

```
shutong/
├── frontend/                  # Next.js 前端
│   ├── src/
│   │   ├── app/              # App Router 页面
│   │   ├── components/       # 组件
│   │   ├── lib/              # 工具函数
│   │   ├── hooks/            # 自定义 Hooks
│   │   └── styles/           # 样式
│   ├── public/               # 静态资源
│   ├── package.json
│   └── tsconfig.json
│
├── backend/                   # FastAPI 后端
│   ├── app/
│   │   ├── api/              # API 路由
│   │   ├── models/           # 数据模型
│   │   ├── services/         # 业务逻辑
│   │   ├── core/             # 核心配置
│   │   └── utils/            # 工具函数
│   ├── requirements.txt
│   └── main.py
│
├── docs/                      # 文档
│   └── superpowers/
│       ├── specs/            # 设计文档
│       └── plans/            # 实施计划
│
├── docker-compose.yml         # Docker 编排
├── .gitignore
└── README.md
```

---

## 八、MVP 范围（第一阶段）

### 8.1 功能范围

- ✅ 用户注册/登录
- ✅ 孩子管理
- ✅ 知识图谱初始化（数学单科）
- ✅ 错题本核心功能（录入、查看、分类）
- ✅ 题库管理（上传试卷、题库浏览）
- ✅ 自由组卷
- ⏳ 学习计划（第二阶段）
- ⏳ 测评系统（第二阶段）
- ⏳ AI 动态解析图（第二阶段）

### 8.2 技术范围

- ✅ 前端基础框架搭建
- ✅ 后端基础框架搭建
- ✅ MongoDB 数据模型实现
- ✅ Neo4j 知识图谱初始化
- ✅ 基础 API 实现
- ✅ OCR 识别集成
- ⏳ 题目生成 AI 模型（第二阶段）
- ⏳ 动态解析图生成（第二阶段）

---

## 九、成功标准

1. **功能完整性**：MVP 范围内所有功能可正常使用
2. **用户体验**：家长可在 5 分钟内完成首次错题录入
3. **识别准确率**：OCR 题目识别准确率 ≥ 90%
4. **系统稳定性**：核心功能无阻塞性 Bug
5. **性能指标**：页面加载时间 < 3 秒，API 响应时间 < 500ms

---

## 十、风险与约束

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| OCR 识别准确率不足 | 用户体验差 | 支持手动修正，持续优化模型 |
| 知识图谱数据量大 | 初始化工作量大 | 分阶段初始化，先数学单科 |
| AI 模型成本高 | 运营成本增加 | 混合方案，核心功能用云端 |
| 单机部署性能有限 | 并发能力不足 | MVP 阶段足够，后续可扩展 |

---

## 附录

### A. 术语表

| 术语 | 说明 |
|------|------|
| 知识图谱 | 学科知识点及其关系的图结构表示 |
| 掌握度 | 学生对某个知识点的掌握程度 (0-1) |
| OCR | 光学字符识别，用于识别图片中的文字 |
| 组卷 | 从题库中选择题目组成试卷 |

### B. 参考资料

- Next.js 官方文档：https://nextjs.org/docs
- FastAPI 官方文档：https://fastapi.tiangolo.com
- MongoDB 官方文档：https://www.mongodb.com/docs
- Neo4j 官方文档：https://neo4j.com/docs

---

**文档维护者**：书童开发团队
**最后更新**：2026-07-09
