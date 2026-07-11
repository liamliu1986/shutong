# 书童（ShuTong）

> 智能学习助手 - 帮助家长辅助孩子学习

书童是一款面向家长的教育辅助 Web 应用，通过知识图谱、错题本、题库管理、学习计划和测评系统，帮助家长科学管理孩子的学习过程，精准定位薄弱环节，提升学习效率。

---

## 核心功能

1. **知识图谱构建**
   - 初高中语数英物化生六科知识图谱
   - 可视化展示知识点层级与关联
   - 掌握度评估与追踪

2. **错题本功能**
   - 拍照/上传图片记录错题
   - OCR 识别题目内容
   - AI 生成答案与解析
   - 按科目、章节、知识点分类管理

3. **题库管理**
   - 上传整张试卷，自动切题识别
   - 按题型、知识点归类
   - 自由组卷练习
   - 原卷复现测试

4. **学习计划**（开发中）
   - 基于薄弱知识点制定计划
   - 根据测评结果动态调整

5. **测评系统**（开发中）
   - 根据知识图谱生成测试题
   - 评估掌握程度并更新图谱

---

## 技术栈

### 前端
- [Next.js 14](https://nextjs.org/) - React 全栈框架
- [TypeScript](https://www.typescriptlang.org/) - 类型安全
- [Tailwind CSS](https://tailwindcss.com/) - 原子化 CSS
- [Axios](https://axios-http.com/) - HTTP 客户端

### 后端
- [FastAPI](https://fastapi.tiangolo.com/) - 高性能 Python Web 框架
- [Pydantic](https://docs.pydantic.dev/) - 数据验证
- [Motor](https://motor.readthedocs.io/) - 异步 MongoDB 驱动
- [Neo4j Python Driver](https://neo4j.com/docs/python-manual/current/) - 图数据库驱动

### 数据库
- [MongoDB](https://www.mongodb.com/) - 文档数据库（用户、错题、题库、计划）
- [Neo4j](https://neo4j.com/) - 图数据库（知识图谱）

### 部署
- [Docker](https://www.docker.com/) - 容器化
- [Docker Compose](https://docs.docker.com/compose/) - 多服务编排

---

## 快速开始

### 环境要求

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) 或 Docker Engine + Docker Compose
- Git

### 1. 克隆项目

```bash
git clone https://github.com/liamliu1986/shutong.git
cd shutong
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，至少修改 `SECRET_KEY`：

```env
# JWT 密钥（必须设置，建议使用随机字符串）
SECRET_KEY=your-random-secret-key-here
```

### 3. 启动服务

```bash
# 使用 Make（推荐）
make up

# 或直接使用 Docker Compose
docker-compose up -d
```

启动后访问：

| 服务 | 地址 |
|------|------|
| 前端页面 | http://localhost:3000 |
| 后端 API | http://localhost:8000 |
| API 文档 | http://localhost:8000/docs |
| Neo4j Browser | http://localhost:7474 |

### 4. 运行测试

```bash
# 使用 Make
make test

# 或直接使用 Docker Compose
docker-compose run --rm backend-test
```

---

## 常用命令

```bash
# 构建镜像
make build

# 启动服务
make up

# 停止服务
make down

# 查看日志
make logs

# 运行测试
make test

# 进入后端容器
make shell

# 只启动后端和数据库
make backend

# 清理所有容器、卷和镜像
make clean
```

---

## 项目结构

```
shutong/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic 模式
│   │   ├── services/       # 业务逻辑
│   │   ├── utils/          # 工具函数
│   │   ├── main.py         # 应用入口
│   │   ├── config.py       # 配置管理
│   │   ├── database.py     # 数据库连接
│   │   └── dependencies.py # 依赖注入
│   ├── tests/              # 测试文件
│   ├── scripts/            # 工具脚本
│   ├── requirements.txt    # Python 依赖
│   └── Dockerfile          # 后端镜像
│
├── frontend/                # Next.js 前端
│   ├── src/
│   │   ├── app/           # 页面路由
│   │   ├── components/    # 组件
│   │   ├── hooks/         # 自定义 Hooks
│   │   ├── lib/           # API 客户端
│   │   └── types/         # TypeScript 类型
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   └── Dockerfile         # 前端镜像
│
├── docs/                    # 文档
│   └── superpowers/
│       ├── specs/         # 设计文档
│       └── plans/         # 实施计划
│
├── docker-compose.yml       # Docker 编排
├── Makefile                # 常用命令
├── .env.example            # 环境变量示例
├── .gitignore
└── README.md               # 本文件
```

---

## API 接口概览

### 认证
- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `GET /api/v1/users/me` - 获取当前用户信息

### 孩子管理
- `GET /api/v1/users/me/children` - 获取孩子列表
- `POST /api/v1/users/me/children` - 添加孩子
- `DELETE /api/v1/users/me/children/{child_id}` - 删除孩子

### 知识图谱
- `GET /api/v1/subjects` - 获取学科列表
- `GET /api/v1/subjects/{subject_id}/graph` - 获取学科知识图谱
- `GET /api/v1/children/{child_id}/mastery` - 获取知识点掌握度

### 错题本
- `POST /api/v1/mistakes` - 创建错题
- `GET /api/v1/mistakes` - 获取错题列表
- `GET /api/v1/mistakes/{id}` - 获取错题详情
- `PUT /api/v1/mistakes/{id}` - 更新错题
- `DELETE /api/v1/mistakes/{id}` - 删除错题

### 题库管理
- `GET /api/v1/question-bank` - 获取题库列表
- `POST /api/v1/question-bank` - 创建题目
- `GET /api/v1/question-bank/{id}` - 获取题目详情
- `DELETE /api/v1/question-bank/{id}` - 删除题目

### 试卷
- `POST /api/v1/papers` - 上传试卷
- `GET /api/v1/papers` - 获取试卷列表
- `POST /api/v1/papers/{id}/recognize` - 触发试卷识别

### 组卷
- `POST /api/v1/generate-paper/preview` - 预览组卷结果
- `POST /api/v1/generate-paper` - 创建组卷

完整的 API 文档可在服务启动后访问：http://localhost:8000/docs

---

## 初始化知识图谱

```bash
# 进入后端容器
make shell

# 运行初始化脚本
python -m scripts.init_math_graph
```

---

## 测试

项目使用 pytest 进行后端测试。

```bash
# 运行所有测试
make test

# 预期输出
# =========================== 26 passed, 7 warnings ============================
```

---

## 开发计划

### 已实现（MVP）
- [x] 用户认证
- [x] 孩子管理
- [x] 数学知识图谱
- [x] 错题本核心功能
- [x] 题库管理 + 自由组卷
- [x] 前端核心页面
- [x] Docker all-in-one 部署

### 待实现
- [ ] 学习计划模块
- [ ] 测评系统
- [ ] AI 动态解析图
- [ ] OCR 真实服务接入
- [ ] 更多学科知识图谱
- [ ] 错题导出打印
- [ ] 移动端适配优化

---

## 设计文档

- [设计文档](docs/superpowers/specs/2026-07-09-shutong-design.md)
- [MVP 实施计划](docs/superpowers/plans/2026-07-09-shutong-mvp.md)

---

## 贡献指南

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/your-feature-name`
3. 提交变更：`git commit -m "feat: 你的功能描述"`
4. 推送分支：`git push origin feature/your-feature-name`
5. 创建 Pull Request

---

## 许可证

[MIT](LICENSE)

---

## 联系方式

如有问题或建议，欢迎提交 Issue 或 Pull Request。
