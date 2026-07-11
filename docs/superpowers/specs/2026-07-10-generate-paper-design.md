# 自由组卷功能设计文档

## 概述

自由组卷功能允许用户根据指定的学科、年级、题型分布、难度分布、知识点范围等条件，从题库中智能筛选题目并组合成试卷。

## 架构

### 模块划分

```
app/
├── api/
│   └── generate_paper.py       # 组卷 API 路由
├── services/
│   └── generate_paper_service.py  # 组卷服务逻辑
```

### 数据流

```
用户请求 → API 路由 → GeneratePaperService → MongoDB（题库查询）
                                            → MongoDB（试卷存储）
                                            → 返回结果
```

## 组件设计

### 1. API 路由 (`app/api/generate_paper.py`)

提供两个端点：

- `POST /generate-paper/preview` - 预览组卷结果（不持久化）
- `POST /generate-paper` - 创建组卷（持久化到数据库）

两个端点都需要用户认证（通过 `get_current_user` 依赖）。

### 2. 组卷服务 (`app/services/generate_paper_service.py`)

#### 配置参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `child_id` | string | 是 | - | 孩子 ID |
| `subject` | string | 是 | - | 学科（如"数学"） |
| `grade` | int | 是 | - | 年级 |
| `total_questions` | int | 是 | - | 总题数 |
| `question_type_distribution` | object | 否 | `{"choice": 5, "fill_blank": 5, "solve": 5}` | 题型分布 |
| `difficulty_distribution` | object | 否 | `{"easy": 0.3, "medium": 0.4, "hard": 0.3}` | 难度分布 |
| `knowledge_point_ids` | array | 否 | `[]` | 知识点 ID 列表 |
| `exclude_recent_days` | int | 否 | `30` | 排除最近 N 天做过的题 |
| `name` | string | 否 | 自动生成 | 试卷名称 |

#### 预览流程（`preview_paper`）

1. 根据 `child_id`、`subject`、`grade` 和 `knowledge_point_ids` 查询题库
2. 验证题目数量是否满足 `total_questions` 要求
3. 按难度分组：easy（difficulty <= 2）、medium（difficulty == 3）、hard（difficulty >= 4）
4. 根据 `difficulty_distribution` 计算各难度题目数量
5. 从各难度组中选择题目
6. 返回预览结果（题目列表、难度分布、题型分布）

#### 创建流程（`create_paper`）

1. 调用 `preview_paper` 获取题目
2. 创建试卷记录到 `papers` 集合
3. 更新题目使用次数（`used_count` 字段）
4. 返回创建结果

### 3. 数据模型

#### 试卷记录（papers 集合）

```json
{
  "child_id": "string",
  "name": "string",
  "subject": "string",
  "grade": "int",
  "images": [],
  "question_ids": ["string"],
  "question_count": "int",
  "source": "自由组卷",
  "status": "completed",
  "created_at": "datetime"
}
```

#### 题目记录（question_bank 集合）

```json
{
  "child_id": "string",
  "subject": "string",
  "grade": "int",
  "difficulty": "int (1-5)",
  "question_type": "string (choice|fill_blank|solve)",
  "knowledge_point_ids": ["string"],
  "used_count": "int"
}
```

## 错误处理

- 题目不足时返回 400 错误，包含实际可用题目数
- 未认证用户返回 401 错误

## 测试策略

- 单元测试：验证难度分组逻辑、题目选择算法
- 集成测试：验证完整的预览和创建流程
- 边界测试：题目恰好足够、题目不足、空题库等场景
