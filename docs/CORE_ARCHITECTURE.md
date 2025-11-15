# 核心架构文档

## 概述

本文档详细说明了 AntLeads 项目的核心架构设计，特别是 `packages/core` 目录下的 `models` 和 `schemas` 模块的设计理念和用途。

## 架构分层

```
┌─────────────────────────────────────────────────────────┐
│                   API Layer                             │
│  ┌─────────────────┐    ┌─────────────────────────────┐ │
│  │   HTTP Routes   │    │      Request/Response       │ │
│  │   (FastAPI)     │    │       Schemas              │ │
│  └─────────────────┘    └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│                Business Logic Layer                     │
│  ┌─────────────────┐    ┌─────────────────────────────┐ │
│  │   Services      │    │      Business Models        │ │
│  │  (AI Scoring,   │    │   (Domain Logic, Enums)     │ │
│  │   Automation)   │    │                             │ │
│  └─────────────────┘    └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│                  Data Access Layer                      │
│  ┌─────────────────┐    ┌─────────────────────────────┐ │
│  │   ORM Models    │    │      Database               │ │
│  │  (SQLAlchemy)   │    │    (PostgreSQL)             │ │
│  └─────────────────┘    └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## packages/core 模块详解

### models - 业务模型层

**位置：** `packages/core/models/`

**设计理念：**
- 定义核心业务实体和业务规则
- 包含领域特定的枚举和常量
- 支持AI驱动业务逻辑（评分、分类、推荐）
- 提供业务验证和计算方法

**主要组件：**

#### Lead 相关模型 (`lead.py`)
```python
# 联系信息模型
class ContactInfo(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    # ...

# 线索来源枚举
class LeadSource(str, Enum):
    WEB_FORM = "web_form"
    GOOGLE_ADS = "google_ads"
    REFERRAL = "referral"
    # ...

# 线索阶段枚举
class LeadStage(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"

# 线索优先级枚举
class LeadPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

# 线索业务模型
class Lead(BaseModel):
    id: Optional[UUID] = None
    name: str
    source: LeadSource
    stage: Optional[LeadStage] = LeadStage.NEW
    priority: Optional[LeadPriority] = LeadPriority.MEDIUM
    score: Optional[int] = 0
    contact_info: ContactInfo
    # ...
```

#### Task 相关模型 (`task.py`)
```python
# 任务类型枚举
class TaskType(str, Enum):
    CALL = "call"
    EMAIL = "email"
    MEETING = "meeting"
    FOLLOW_UP = "follow_up"
    PROPOSAL = "proposal"
    DEMO = "demo"
    NOTE = "note"
    OTHER = "other"

# 任务状态枚举
class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    OVERDUE = "overdue"

# 任务业务模型
class Task(BaseModel):
    id: Optional[UUID] = None
    lead_id: UUID
    title: str
    task_type: TaskType
    status: Optional[TaskStatus] = TaskStatus.PENDING
    priority: Optional[TaskPriority] = TaskPriority.MEDIUM
    # ...
```

**使用场景：**
- AI评分引擎处理线索
- 自动任务创建和分配
- 业务规则验证
- 数据分析和报告生成

### schemas - API模式层

**位置：** `packages/core/schemas/`

**设计理念：**
- 定义API输入输出的数据结构
- 提供HTTP请求验证和响应序列化
- 支持分页、筛选、排序等API特性
- 隔离内部业务模型和外部API接口

**主要组件：**

#### Lead API模式 (`lead.py`)
```python
# 创建线索请求
class LeadCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    source: LeadSource
    contact_info: ContactInfo = Field(default_factory=ContactInfo)
    tags: list[str] = Field(default_factory=list)
    product_interest: Optional[str] = None
    estimated_value: Optional[float] = Field(default=None, ge=0)
    # UTM跟踪参数
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    referrer_url: Optional[str] = None

# 更新线索请求
class LeadUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    stage: Optional[LeadStage] = None
    priority: Optional[LeadPriority] = None
    contact_info: Optional[ContactInfo] = None
    # ...

# 线索响应
class LeadResponse(BaseModel):
    id: UUID
    name: str
    source: LeadSource
    stage: LeadStage
    priority: LeadPriority
    score: int
    contact_info: ContactInfo
    tags: list[str]
    # ...

# 分页列表响应
class LeadListResponse(BaseModel):
    leads: list[LeadResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

# 批量导入请求
class LeadImportRequest(BaseModel):
    leads: list[LeadCreateRequest] = Field(..., min_length=1, max_length=1000)
    source: LeadSource = LeadSource.IMPORT
```

#### Task API模式 (`task.py`)
```python
# 创建任务请求
class TaskCreateRequest(BaseModel):
    lead_id: UUID
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    task_type: TaskType
    priority: TaskPriority = TaskPriority.MEDIUM
    assigned_to: Optional[UUID] = None
    due_date: Optional[datetime] = None
    reminder_at: Optional[datetime] = None

# 任务响应
class TaskResponse(BaseModel):
    id: UUID
    lead_id: UUID
    title: str
    description: Optional[str]
    task_type: TaskType
    status: TaskStatus
    priority: TaskPriority
    # ...
```

#### Funnel API模式 (`funnel.py`)
```python
# 漏斗阶段数据
class FunnelStageData(BaseModel):
    stage: LeadStage
    count: int
    total_value: float
    conversion_rate: Optional[float] = None
    average_days: Optional[float] = None

# 漏斗分析响应
class FunnelResponse(BaseModel):
    stages: list[FunnelStageData]
    total_leads: int
    total_value: float
    overall_conversion_rate: float
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
```

## 数据流转示例

### 1. 创建新线索

```
HTTP POST /api/leads
{
  "name": "John Smith",
  "source": "web_form",
  "contact_info": {
    "email": "john@example.com",
    "company": "Acme Corp"
  }
}
         │
         ▼
LeadCreateRequest (验证格式)
         │
         ▼
Lead (业务模型，用于AI评分)
         │
         ▼
AI Scoring Engine
         │
         ▼
LeadORM (数据库模型)
         │
         ▼
Database
```

**代码示例：**
```python
# 1. API Route
@router.post("/", response_model=LeadResponse)
async def create_lead(request: LeadCreateRequest, db: AsyncSession):
    # 2. 转换为业务模型用于AI处理
    temp_lead = Lead(
        name=request.name,
        source=request.source,
        contact_info=request.contact_info,
        # ...
    )

    # 3. AI评分和自动标签
    score = score_lead(temp_lead)
    suggested_tags = auto_tag_lead(temp_lead)

    # 4. 创建ORM模型保存到数据库
    lead_orm = LeadORM(
        name=request.name,
        source=request.source,
        score=score,
        # ...
    )

    # 5. 保存并返回响应
    await db.commit()
    return LeadResponse.from_orm(lead_orm)
```

### 2. 获取漏斗分析

```
HTTP GET /api/funnel?start_date=2024-01-01&end_date=2024-01-31
         │
         ▼
Query Parameters (验证)
         │
         ▼
Database Query (ORM Models)
         │
         ▼
Business Calculation (Models)
         │
         ▼
FunnelResponse (API Schema)
         │
         ▼
JSON Response
```

## 设计优势

### 1. 关注点分离
- **API层**：只关心HTTP接口和数据格式
- **业务层**：只关心业务逻辑和AI处理
- **数据层**：只关心数据持久化

### 2. 可测试性
```python
# 业务逻辑测试（不依赖HTTP）
def test_lead_scoring():
    lead = Lead(
        name="Test Lead",
        source=LeadSource.REFERRAL,
        contact_info=ContactInfo(email="test@example.com")
    )
    score = score_lead(lead)
    assert score > 20  # Referral leads get higher scores

# API接口测试
def test_create_lead_api(client):
    response = client.post("/api/leads", json={
        "name": "Test Lead",
        "source": "web_form"
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Test Lead"
```

### 3. 可扩展性
- 新增AI功能只需修改业务模型
- 新增API端点只需创建新的Schema
- 数据库结构变更只影响ORM模型

### 4. 类型安全
- 使用Pydantic进行运行时类型检查
- 枚举类型确保数据一致性
- IDE自动补全和类型提示

## 最佳实践

### 1. Schema设计原则
- 请求Schema：最小化必需字段，提供合理默认值
- 响应Schema：包含完整业务数据
- 使用Field进行详细验证规则
- 提供清晰的文档字符串

### 2. Model设计原则
- 业务字段有合理默认值
- 枚举类型使用str,Enum支持JSON序列化
- 可选字段使用Optional标注
- 包含业务验证方法

### 3. 数据转换
```python
# ORM -> Business Model
def orm_to_business(lead_orm: LeadORM) -> Lead:
    return Lead(
        id=lead_orm.id,
        name=lead_orm.name,
        source=lead_orm.source,
        # ...
    )

# Business Model -> Response
def business_to_response(lead: Lead) -> LeadResponse:
    return LeadResponse(
        id=lead.id,
        name=lead.name,
        source=lead.source,
        # ...
    )
```

## 总结

这种分层架构设计实现了：

1. **清晰的职责划分** - 每层只关心自己的职责
2. **良好的可测试性** - 各层可以独立测试
3. **灵活的扩展能力** - 新功能可以增量添加
4. **类型安全保障** - 减少运行时错误
5. **AI驱动业务** - 业务模型层支持复杂的AI逻辑

通过这种设计，项目能够支持复杂的AI驱动线索管理系统，同时保持代码的可维护性和可扩展性。