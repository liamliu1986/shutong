# 自由组卷功能实施计划

## 任务概览

创建自由组卷后端服务，包括 API 路由和业务逻辑服务。

## 前置条件

- [x] 项目目录 `D:/Projects/shutong/backend` 存在
- [x] `app/database.py` 已实现 `get_mongodb()` 函数
- [x] `app/dependencies.py` 已实现 `get_current_user` 依赖
- [x] `app/main.py` 已注册路由

## 任务列表

### 任务 1：创建组卷服务文件

**文件路径**: `backend/app/services/generate_paper_service.py`

**操作**: 创建新文件

**TDD 步骤**:

#### RED - 编写失败测试

在 `backend/tests/test_generate_paper.py` 中编写测试：

```python
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.generate_paper_service import GeneratePaperService

@pytest.mark.asyncio
async def test_preview_paper_returns_correct_structure():
    """测试预览组卷返回正确的结构"""
    mock_db = MagicMock()
    mock_cursor = AsyncMock()
    mock_cursor.__aiter__ = MagicMock(return_value=iter([
        {"_id": "id1", "difficulty": 1, "question_type": "choice", "child_id": "c1", "subject": "数学", "grade": 9},
        {"_id": "id2", "difficulty": 2, "question_type": "fill_blank", "child_id": "c1", "subject": "数学", "grade": 9},
        {"_id": "id3", "difficulty": 3, "question_type": "solve", "child_id": "c1", "subject": "数学", "grade": 9},
        {"_id": "id4", "difficulty": 4, "question_type": "choice", "child_id": "c1", "subject": "数学", "grade": 9},
        {"_id": "id5", "difficulty": 5, "question_type": "solve", "child_id": "c1", "subject": "数学", "grade": 9},
    ]))
    mock_db.question_bank.find.return_value = mock_cursor

    with patch("app.services.generate_paper_service.get_mongodb", return_value=mock_db):
        result = await GeneratePaperService.preview_paper({
            "child_id": "c1",
            "subject": "数学",
            "grade": 9,
            "total_questions": 3
        })

    assert "total_questions" in result
    assert "difficulty_distribution" in result
    assert "type_distribution" in result
    assert "questions" in result
```

#### Verify RED - 确认测试失败

运行测试，确认因模块不存在而失败。

#### GREEN - 编写最小实现

创建 `backend/app/services/generate_paper_service.py`，实现 `GeneratePaperService` 类。

#### Verify GREEN - 确认测试通过

运行测试，确认所有测试通过。

---

### 任务 2：创建组卷 API 路由

**文件路径**: `backend/app/api/generate_paper.py`

**操作**: 创建新文件

**内容**:

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

---

### 任务 3：注册路由到主应用

**文件路径**: `backend/app/main.py`

**操作**: 修改现有文件

**变更**:

1. 添加导入：`from app.api import generate_paper`
2. 注册路由：`app.include_router(generate_paper.router, prefix="/api/v1", tags=["自由组卷"])`

---

## 验证清单

- [ ] `generate_paper_service.py` 文件已创建
- [ ] `generate_paper.py` 路由文件已创建
- [ ] 路由已在 `main.py` 中注册
- [ ] 所有测试通过
- [ ] 代码无语法错误
