# 添加子代理交付物核查流程到 CLAUDE.md

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (inline execution) for this documentation update.

**Goal:** 在 CLAUDE.md 中新增「子代理交付物核查」流程章节，防止任务标记完成但代码文件未真实进入仓库的问题复发。

**Architecture:** 在 CLAUDE.md 的 Phase 4（实施阶段）末尾和 Phase 10（最终核查清单）中分别补充交付物核查流程与红旗警示，形成实施中自查 + 最终兜底的双重保障。

**Tech Stack:** Markdown / Git

## Global Constraints

- 所有新增内容使用中文
- 提交信息使用中文，类型前缀小写
- 不修改无关章节，保持 CLAUDE.md 原有结构
- 通过 `docs/` 分支提交 PR 合并到 `main`

---

### Task 1: 在 Phase 4 实施阶段末尾增加交付物核查流程

**Files:**
- Modify: `C:\Users\liuzh\.claude\CLAUDE.md`（在 Phase 4 末尾REFACTOR之后）

**Interfaces:**
- Consumes: 现有 CLAUDE.md Phase 4 结构
- Produces: 新增「子代理交付物核查」子章节

- [ ] **Step 1: 定位插入位置**

在 CLAUDE.md 中找到「Phase 4: Implementation（实施 - TDD 强制模式）」章节，定位到 REFACTOR 步骤之后、「实施方式选择」之前的位置。

- [ ] **Step 2: 插入新增内容**

插入以下内容（保持与周围章节一致的 Markdown 标题层级和列表风格）：

```markdown
### 4.4 子代理交付物核查（强制）

**触发条件：** 任何任务由子代理、脚本或自动化工具完成，或任务涉及多个文件的创建/修改。

**核心铁律：**
```
任务标记完成 ≠ 文件真实进入仓库
```

**必须在标记任务完成前执行以下核查：**

1. **文件存在性检查**
   - 对照计划/设计文档，逐一确认每个声明创建/修改的文件真实存在
   - 命令：
     ```bash
     ls -la <file-path>
     ```
   - 不允许仅依赖子代理的口头报告或任务状态标记

2. **Git 跟踪状态检查**
   - 确认文件已被 git 跟踪，不是未跟踪状态（`??`）
   - 命令：
     ```bash
     git status --short
     ```
   - 未跟踪文件必须 `git add` 后才能继续

3. **内容完整性检查**
   - 抽查关键文件，确认：
     - 无占位符（TBD / TODO / implement later）
     - 无语法错误
     - 文件内容与任务规格一致
   - 命令：
     ```bash
     git diff --cached -- <file-path>
     ```

4. **提交记录检查**
   - 确认相关变更有对应的 git 提交
   - 命令：
     ```bash
     git log --oneline -- <file-path>
     ```
   - 提交信息符合规范（类型前缀 + 中文描述）

5. **基线环境复现验证（关键任务）**
   - 在干净的 worktree 或新的 Docker 环境中重新运行完整测试
   - 确认功能可复现，不依赖本地未提交的临时文件

**禁止：**
- 仅因子代理报告"完成"就标记任务完成
- 不检查 git status 就进入下一任务
- 在 worktree 中积累大量未提交文件
- 假设"文件肯定提交了"
```

- [ ] **Step 3: 自检新增章节**

确认：
- 插入位置正确，不破坏原有章节编号
- 所有命令可直接复制执行
- 无英文注释，无占位符

- [ ] **Step 4: 提交**

```bash
git add C:\Users\liuzh\.claude\CLAUDE.md
git commit -m "docs: 在 Phase 4 增加子代理交付物核查流程"
```

---

### Task 2: 在最终核查清单中增加交付物核查项

**Files:**
- Modify: `C:\Users\liuzh\.claude\CLAUDE.md`（在「十、最终核查清单」中）

**Interfaces:**
- Consumes: 现有「十、最终核查清单」结构
- Produces: 新增「子代理交付物核查」核查项

- [ ] **Step 1: 定位插入位置**

在「十、最终核查清单」中找到「流程合规」小节，在「隔离 worktree 已创建且基线测试通过」之后增加新的核查项。

- [ ] **Step 2: 插入新增内容**

在「流程合规」小节的 checklist 中增加：

```markdown
- [ ] 子代理/自动化任务的交付物已逐一核查（文件存在、git 跟踪、内容完整、提交记录）
```

- [ ] **Step 3: 在红旗章节增加对应警示**

在「六、Red Flags（立即停止并回归流程）」中新增一条：

```markdown
### 6.5 子代理交付专用红旗

- 子代理报告完成但未独立验证文件是否存在
- 任务标记完成但 `git status` 显示文件未跟踪
- "这个文件应该已经提交了"
- 计划中的文件路径与实际文件路径不一致
- 合并前未在干净环境中复现功能
```

- [ ] **Step 4: 自检**

确认：
- 清单项格式与其他项一致
- 红旗章节编号连续（如已有 6.5 则改为 6.6）

- [ ] **Step 5: 提交**

```bash
git add C:\Users\liuzh\.claude\CLAUDE.md
git commit -m "docs: 在最终核查清单和红旗中补充交付物核查"
```

---

### Task 3: 验证文档更新

**Files:**
- 无需修改文件

- [ ] **Step 1: 检查 CLAUDE.md 整体结构**

运行：
```bash
grep -n "子代理交付物核查" C:\Users\liuzh\.claude\CLAUDE.md
```

预期输出两处匹配：Phase 4 章节和最终核查清单章节。

- [ ] **Step 2: 确认无语法问题**

快速浏览新增章节，确认 Markdown 标题层级正确，列表无断裂。

- [ ] **Step 3: 推送并创建 PR**

```bash
git checkout main
git pull origin main
git checkout -b docs/add-agent-delivery-check
git push -u origin docs/add-agent-delivery-check
gh pr create --title "docs: 添加子代理交付物核查流程" --body "..."
gh pr merge <pr-number> --squash
```

---

## Self-Review

- Spec coverage: Phase 4 实施中自查、最终核查清单兜底、红旗警示三处均已覆盖。
- Placeholder scan: 无 TBD/TODO/模糊描述，命令具体可执行。
- Type consistency: 不涉及代码类型。
