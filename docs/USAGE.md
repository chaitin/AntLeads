# AntLeads 使用文档

## 项目简介

**AntLeads** 是一个基于 AI 的智能营销与商机管理系统，帮助企业在线生成、管理和转化商品销售线索。

### 核心功能

1. **商机来源追踪** - 支持多渠道线索收集（广告、表单、活动、导入等）
2. **AI 智能打分** - 自动评估线索质量并分配优先级
3. **自动打标签** - 基于线索属性智能分类
4. **商机漏斗可视化** - 实时展示销售管道状态
5. **自动任务提醒** - 阶段变化时自动创建跟进任务
6. **数据分析** - 多维度统计与转化分析

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- uv (Python 包管理工具)
- pnpm (可选，推荐用于前端)

### 安装步骤

1. **克隆项目**

```bash
git clone <repository-url>
cd antleads
```

2. **后端安装**

```bash
# 安装 Python 依赖
make bootstrap
# 或
uv sync

# 复制环境变量配置
cp .env.example .env
```

3. **前端安装**

```bash
cd apps/web
pnpm install
# 或
npm install
```

### 启动服务

#### 后端 API

```bash
# 启动 FastAPI 服务器 (http://localhost:8000)
make api
# 或
uv run uvicorn apps.api.main:app --reload
```

#### 前端

```bash
cd apps/web
pnpm dev
# 或
npm run dev
# 访问 http://localhost:5173
```

### 生成示例数据

```bash
make sample-data
# 或
uv run python data/sample/generate_sample_data.py
```

## API 文档

启动后端服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 主要 API 端点

#### 商机管理

- `POST /api/v1/leads/` - 创建新商机（自动 AI 评分和打标签）
- `GET /api/v1/leads/` - 获取商机列表（支持分页、搜索、筛选）
- `GET /api/v1/leads/{id}` - 获取单个商机详情
- `PATCH /api/v1/leads/{id}` - 更新商机（阶段变化时自动创建任务）
- `DELETE /api/v1/leads/{id}` - 删除商机
- `POST /api/v1/leads/import` - 批量导入商机
- `GET /api/v1/leads/stats/overview` - 获取商机统计数据

#### 任务管理

- `POST /api/v1/tasks/` - 创建新任务
- `GET /api/v1/tasks/` - 获取任务列表
- `GET /api/v1/tasks/{id}` - 获取任务详情
- `PATCH /api/v1/tasks/{id}` - 更新任务状态
- `DELETE /api/v1/tasks/{id}` - 删除任务

#### 销售漏斗

- `GET /api/v1/funnel/` - 获取销售漏斗数据（支持日期筛选）

#### 自动化

- `GET /api/v1/automation/overdue` - 获取逾期任务
- `GET /api/v1/automation/reminders` - 获取需要提醒的任务
- `POST /api/v1/automation/stale-leads` - 为不活跃商机创建任务

## AI 评分规则

系统会根据以下因素自动计算商机分数（0-100分）：

### 评分维度

1. **来源质量（0-30分）**
   - 转介绍: 30分
   - 活动: 25分
   - 网站表单: 20分
   - 落地页: 18分
   - Google Ads: 15分
   - 其他付费渠道: 10-12分
   - 导入: 5分

2. **联系信息完整度（0-25分）**
   - 邮箱: 10分
   - 电话: 8分
   - 公司: 5分
   - 职位: 2分

3. **预估价值（0-20分）**
   - ≥ $100,000: 20分
   - ≥ $50,000: 15分
   - ≥ $10,000: 10分
   - < $10,000: 5分

4. **产品兴趣（0-10分）**
   - 有明确产品兴趣: 10分

5. **UTM 追踪（0-10分）**
   - Campaign: 5分
   - Source: 3分
   - Medium: 2分

6. **企业信息（0-5分）**
   - 有公司名称: 5分

### 自动标签

系统会根据商机属性自动打标签：

- **价值级别**: `enterprise`（≥$100K）、`mid-market`（≥$50K）、`smb`（<$50K）
- **质量等级**: `hot-lead`（分数≥75）、`warm-lead`（分数≥50）、`cold-lead`（分数<50）
- **来源类型**: `high-quality`（转介绍/活动）、`paid-traffic`（广告渠道）
- **信息完整度**: `complete-profile`（所有联系信息齐全）
- **兴趣类型**: `enterprise-interest`、`demo-request` 等

### 优先级建议

- **Urgent**: 分数 ≥ 80
- **High**: 分数 ≥ 60
- **Medium**: 分数 ≥ 40
- **Low**: 分数 < 40

## 自动化规则

### 阶段转换自动任务

当商机状态变更时，系统会自动创建对应的跟进任务：

| 阶段 | 自动任务 | 优先级 | 截止时间 |
|------|---------|--------|---------|
| NEW | 初次联系 | High | 1天后 |
| CONTACTED | 跟进联系 | Medium | 3天后 |
| QUALIFIED | 安排 Demo | High | 2天后 |
| PROPOSAL | 发送方案 + 跟进方案 | Urgent | 1天后 + 5天后 |
| NEGOTIATION | 商务谈判会议 | Urgent | 2天后 |

### 不活跃商机提醒

可通过 API 手动触发为不活跃商机创建任务：

```bash
curl -X POST "http://localhost:8000/api/v1/automation/stale-leads?days_inactive=7"
```

## 前端页面

### Dashboard（仪表盘）

- 关键指标卡片：总商机数、平均分数、预估价值、待办任务
- 商机阶段分布
- 商机来源分析
- 最近待办任务

### Leads（商机管理）

- 商机列表展示
- 搜索和筛选
- 查看商机详情
- 创建/编辑商机

### Tasks（任务管理）

- 任务列表
- 按状态筛选
- 任务详情查看
- 创建/更新任务

### Funnel（销售漏斗）

- 可视化漏斗图表
- 各阶段转化率
- 阶段价值统计
- 数据趋势分析

## 开发命令

```bash
# 后端
make bootstrap      # 安装依赖
make api           # 启动 API 服务器
make lint          # 代码格式化和检查
make test          # 运行测试
make test-cov      # 运行测试并生成覆盖率报告
make sample-data   # 生成示例数据
make clean         # 清理临时文件

# 前端
cd apps/web
pnpm dev           # 开发模式
pnpm build         # 生产构建
pnpm preview       # 预览构建结果
pnpm lint          # ESLint 检查
```

## 项目结构

```
antleads/
├── apps/
│   ├── api/              # FastAPI 后端
│   │   ├── main.py       # 应用入口
│   │   ├── config.py     # 配置管理
│   │   ├── database.py   # 数据库连接
│   │   ├── models.py     # SQLAlchemy ORM 模型
│   │   ├── routes/       # API 路由
│   │   └── services/     # 业务逻辑服务
│   └── web/              # React 前端
│       ├── src/
│       │   ├── components/  # UI 组件
│       │   ├── pages/       # 页面组件
│       │   ├── services/    # API 调用
│       │   ├── types/       # TypeScript 类型
│       │   └── hooks/       # React Hooks
│       └── package.json
├── packages/
│   ├── core/             # 共享业务逻辑
│   │   ├── models/       # Pydantic 数据模型
│   │   └── schemas/      # API Schemas
│   └── ml/               # AI/ML 功能
│       └── lead_scoring.py  # 商机评分引擎
├── data/
│   ├── sample/           # 示例数据
│   └── raw/              # 原始数据集
├── tests/                # 测试文件
├── docs/                 # 文档和 ADR
├── Makefile              # 开发命令
├── pyproject.toml        # Python 项目配置
└── requirements.txt      # Python 依赖
```

## 环境变量说明

参考 `.env.example` 文件：

```bash
# 应用配置
APP_NAME=AntLeads
DEBUG=true

# CORS 设置
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# 数据库
DATABASE_URL=sqlite+aiosqlite:///./antleads.db

# AI 功能
AI_SCORING_ENABLED=true
AI_MODEL_NAME=gpt-4
OPENAI_API_KEY=your-api-key-here  # 可选，当前评分引擎为规则引擎

# 任务自动化
AUTO_TASK_ENABLED=true
DEFAULT_FOLLOW_UP_DAYS=3
```

## 常见问题

### 如何修改 AI 评分规则？

编辑 `packages/ml/lead_scoring.py` 中的 `LeadScorer` 类，调整各维度权重。

### 如何添加新的商机来源？

1. 在 `packages/core/models/lead.py` 的 `LeadSource` 枚举中添加新值
2. 在 `packages/ml/lead_scoring.py` 的 `source_weights` 字典中设置权重

### 如何自定义自动任务规则？

编辑 `apps/api/services/task_automation.py` 中的 `create_stage_transition_tasks` 方法。

### 数据库迁移

当前使用 SQLite，生产环境建议切换到 PostgreSQL：

```bash
# 修改 .env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/antleads
```

## 技术栈

### 后端
- FastAPI - 现代 Python Web 框架
- SQLAlchemy - ORM
- Pydantic - 数据验证
- aiosqlite - 异步 SQLite

### 前端
- React 18 - UI 框架
- TypeScript - 类型安全
- Vite - 构建工具
- React Query - 数据获取
- Recharts - 图表可视化
- Axios - HTTP 客户端

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feat/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feat/amazing-feature`)
5. 开启 Pull Request

遵循 Conventional Commits 规范：
- `feat:` - 新功能
- `fix:` - Bug 修复
- `chore:` - 日常维护
- `docs:` - 文档更新
- `test:` - 测试相关

## 许可证

MIT License
