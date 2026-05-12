# Render Dependency Graph (RDG) 详解

## 摘要

RDG (Render Dependency Graph) 是 UE5.7.4 的渲染图系统，负责自动管理渲染 Pass 之间的资源依赖关系、生命周期和屏障转换。开发者通过声明式 API 构建渲染图，RDG 在执行阶段自动完成资源分配、依赖排序、Pass 裁剪和 GPU 屏障插入。

**核心源码位置**: `Engine/Source/Runtime/RenderCore/Public/RenderGraph.h` (仅作为统一包含入口，65 行)

---

## 1. 核心架构概览

### 1.1 文件组织

RDG 系统的源码分布在 `Engine/Source/Runtime/RenderCore/Public/` 下，由以下头文件组成：

| 文件 | 职责 |
|------|------|
| `RenderGraph.h` | 统一包含入口，包含 57 行框架设计文档注释 |
| `RenderGraphDefinitions.h` | 所有枚举、Handle、注册表类型定义 |
| `RenderGraphResources.h` | FRDGTexture、FRDGBuffer、FRDGView 等资源类 |
| `RenderGraphPass.h` | FRDGPass 基类、TRDGLambdaPass 模板类 |
| `RenderGraphBuilder.h` | FRDGBuilder 主构建器类（核心，约 1217 行） |
| `RenderGraphAllocator.h` | RDG 专用内存分配器 |
| `RenderGraphBlackboard.h` | Blackboard 数据共享机制 |
| `RenderGraphEvent.h` | GPU 事件名称管理 |
| `RenderGraphUtils.h` | 工具函数 |
| `RenderGraphValidation.h` | 调试验证 |
| `RenderGraphTrace.h` | UE Trace 追踪集成 |

### 1.2 核心类层次

```
FRDGResource (基类, 所有RDG资源)
├── FRDGUniformBuffer           -- Uniform Buffer
├── FRDGViewableResource        -- 可被视图引用的资源基类
│   ├── FRDGTexture             -- 纹理资源
│   └── FRDGBuffer              -- 缓冲区资源
└── FRDGView                    -- 视图资源（引用可查看资源）
    ├── FRDGShaderResourceView  -- SRV 基类
    │   ├── FRDGTextureSRV      -- 纹理 SRV
    │   └── FRDGBufferSRV       -- 缓冲区 SRV
    └── FRDGUnorderedAccessView -- UAV 基类
        ├── FRDGTextureUAV      -- 纹理 UAV
        └── FRDGBufferUAV       -- 缓冲区 UAV

FRDGPass (基类, 所有渲染 Pass)
├── TRDGLambdaPass<Params, Lambda>  -- Lambda Pass（最常用）
├── TRDGEmptyLambdaPass<Lambda>     -- 无参数 Lambda Pass
├── FRDGDispatchPass                -- 并行分发 Pass
├── TRDGDispatchPass<Params, Lambda>-- 带参数的并行分发 Pass
└── FRDGSentinelPass                -- 哨兵 Pass（序幕/尾声）

FRDGBuilder -- 渲染图构建器（主入口，约 1217 行头文件）
```

---

## 2. FRDGBuilder — 渲染图构建器

### 2.1 构建与执行

`FRDGBuilder` 是 RDG 系统的主入口。源码定义在 `RenderGraphBuilder.h` 第 47 行。

```cpp
// 源码: RenderGraphBuilder.h:63
RENDERCORE_API FRDGBuilder(
    FRHICommandListImmediate& RHICmdList,
    FRDGEventName Name = {},
    ERDGBuilderFlags Flags = ERDGBuilderFlags::None,
    EShaderPlatform ShaderPlatform = GMaxRHIShaderPlatform);
```

**关键方法**:

| 方法 | 行号 (RenderGraphBuilder.h) | 功能 |
|------|------|------|
| `CreateTexture()` | 101 | 创建 RDG 跟踪纹理 |
| `CreateBuffer()` | 107/113 | 创建 RDG 跟踪缓冲区 |
| `CreateSRV()` | 116-124 | 创建着色器资源视图 |
| `CreateUAV()` | 127-140 | 创建无序访问视图 |
| `CreateUniformBuffer()` | 147 | 创建 Uniform Buffer |
| `AllocParameters()` | 177 | 分配 Pass 参数结构 |
| `AddPass()` | 218/222/230 | 添加渲染 Pass |
| `AddDispatchPass()` | 237 | 添加并行分发 Pass |
| `QueueTextureExtraction()` | 346-347 | 队列纹理提取 |
| `QueueBufferExtraction()` | 353-354 | 队列缓冲区提取 |
| `QueueBufferUpload()` | 310-334 | 队列缓冲区上传 |
| `Execute()` | 413 | 执行整个渲染图 |
| `AddSetupTask()` | 257-286 | 添加异步设置任务 |

### 2.2 构建器标志

源码: `RenderGraphDefinitions.h:107-124`

```cpp
enum class ERDGBuilderFlags
{
    None = 0,
    ParallelSetup = 1 << 0,    // 允许并行化 AddSetupPass 调用
    ParallelCompile = 1 << 1,  // 允许并行化图编译
    ParallelExecute = 1 << 2,  // 允许并行化 Pass 执行
    Parallel = ParallelSetup | ParallelCompile | ParallelExecute,
};
```

### 2.3 内部注册表

`FRDGBuilder` 维护多个内部注册表来跟踪所有资源（源码: RenderGraphBuilder.h:545-549）：

```cpp
FRDGPassRegistry Passes;
FRDGTextureRegistry Textures;
FRDGBufferRegistry Buffers;
FRDGViewRegistry Views;
FRDGUniformBufferRegistry UniformBuffers;
```

每个注册表都是 `TRDGHandleRegistry<HandleType>` 的实例，通过 Handle 索引进行高效查找。

---

## 3. ERDGPassFlags — Pass 类型系统

源码: `RenderGraphDefinitions.h:127-158`

```cpp
enum class ERDGPassFlags : uint16
{
    None        = 0,
    Raster      = 1 << 0,   // 光栅化 Pass（图形管线）
    Compute     = 1 << 1,   // 计算 Pass（图形管线）
    AsyncCompute = 1 << 2,  // 异步计算 Pass（独立计算管线）
    Copy        = 1 << 3,   // 复制 Pass（图形管线）
    NeverCull   = 1 << 4,   // 永不裁剪
    SkipRenderPass = 1 << 5,// 跳过 RenderPass 开始/结束
    NeverMerge  = 1 << 6,   // 永不合并渲染 Pass
    NeverParallel = 1 << 7, // 永不并行执行
    Readback    = Copy | NeverCull,  // 回读
};
```

**Pass 标志决定三件事**:
1. 使用哪个 GPU 管线（Graphics / AsyncCompute）
2. 是否需要 RHI RenderPass（仅 Raster）
3. 裁剪和合并策略

### 3.1 Pass 任务模式

源码: `RenderGraphDefinitions.h:172-182`

```cpp
enum class ERDGPassTaskMode : uint8
{
    Inline,  // 必须在渲染线程内联执行
    Await,   // 可在任务中执行，Execute 结束时等待
    Async,   // 可在任务中执行，需手动等待
};
```

任务模式由 Lambda 签名自动推导（见 `TRDGLambdaPass::ExecuteLambdaTraits`，RenderGraphPass.h:570-651）：
- 使用 `FRHICommandListImmediate&` -> `Inline`
- 使用 `FRHICommandList&` + 无 `FRDGAsyncTask` -> `Await`
- 使用 `FRHICommandList&` + `FRDGAsyncTask` 前缀 -> `Async`

---

## 4. FRDGPass — Pass 基类详解

源码: `RenderGraphDefinitions.h:216-563`

### 4.1 核心成员

```cpp
class FRDGPass {
    const FRDGEventName Name;           // Pass 名称（用于 GPU Profiler）
    const FRDGParameterStruct ParameterStruct; // 参数结构
    const ERDGPassFlags Flags;          // Pass 类型标志
    const ERDGPassTaskMode TaskMode;    // 任务模式
    const ERHIPipeline Pipeline;        // GPU 管线
    FRDGPassHandle Handle;              // 注册表 Handle
    uint32 Workload = 1;                // 工作负载估算

    // 状态位（使用位域压缩，RenderGraphDefinitions.h:396-459）
    uint16 bSkipRenderPassBegin : 1;
    uint16 bSkipRenderPassEnd : 1;
    uint16 bAsyncComputeBegin : 1;
    uint16 bAsyncComputeEnd : 1;
    uint16 bGraphicsFork : 1;
    uint16 bGraphicsJoin : 1;
    uint16 bRenderPassOnlyWrites : 1;
    uint16 bSentinel : 1;
    uint16 bDispatchAfterExecute : 1;
    uint16 bDispatchPass : 1;

    // Pass 内资源状态追踪（RenderGraphDefinitions.h:479-515）
    TArray<FTextureState, FRDGArrayAllocator> TextureStates;
    TArray<FBufferState, FRDGArrayAllocator> BufferStates;
    TArray<FRDGViewHandle, FRDGArrayAllocator> Views;
    TArray<FRDGUniformBufferHandle, FRDGArrayAllocator> UniformBuffers;

    // 屏障批次管理（RenderGraphDefinitions.h:537-543）
    FRDGBarrierBatchBegin* PrologueBarriersToBegin;
    FRDGBarrierBatchEnd* PrologueBarriersToEnd;
    FRDGBarrierBatchBegin* EpilogueBarriersToBeginForGraphics;
    FRDGBarrierBatchBegin* EpilogueBarriersToBeginForAsyncCompute;
    FRDGBarrierBatchBegin* EpilogueBarriersToBeginForAll;
    FRDGBarrierBatchEnd* EpilogueBarriersToEnd;

    // 依赖追踪
    TArray<FRDGPassHandle, FRDGArrayAllocator> CrossPipelineConsumers;
    TArray<FRDGPass*, FRDGArrayAllocator> Producers;
};
```

### 4.2 TRDGLambdaPass 模板

源码: `RenderGraphDefinitions.h:566-710`

```cpp
template <typename ParameterStructType, typename ExecuteLambdaType>
class TRDGLambdaPass : public FRDGPass
{
    // Lambda 捕获大小限制为 1024 字节
    static constexpr int32 kMaximumLambdaCaptureSize = 1024;

    void Execute(FRHIComputeCommandList& RHICmdList) override {
        RHICmdList.SetStaticUniformBuffers(ParameterStruct.GetStaticUniformBuffers());
        ExecuteLambdaFunc(RHICmdList);
    }

    ExecuteLambdaType ExecuteLambda;
};
```

---

## 5. 资源类型详解

### 5.1 FRDGTexture

源码: `RenderGraphResources.h:569-693`

```cpp
class FRDGTexture final : public FRDGViewableResource {
    const FRDGTextureDesc Desc;         // 纹理描述符
    const ERDGTextureFlags Flags;       // 纹理标志
    FRDGTextureHandle Handle;           // 注册 Handle
    FRDGTextureHandle PreviousOwner;    // 别名链前驱
    FRDGTextureHandle NextOwner;        // 别名链后继
    FRDGTextureSubresourceLayout Layout;
    FRDGTextureSubresourceState State;      // 子资源状态追踪
    FRDGTextureSubresourceState FirstState; // 首次使用状态
    FRDGTextureSubresourceState MergeState; // 合并状态

    IPooledRenderTarget* RenderTarget;       // 池化渲染目标
    FRHITransientTexture* TransientTexture;  // 瞬时纹理
    FRHITextureViewCache* ViewCache;         // 视图缓存
};
```

### 5.2 FRDGTextureDesc

源码: `RenderGraphDefinitions.h:626-740`

提供静态工厂方法创建不同维度的纹理描述：

```cpp
struct FRDGTextureDesc : public FRHITextureDesc {
    static FRDGTextureDesc Create2D(FIntPoint, EPixelFormat, FClearValueBinding, ETextureCreateFlags, ...);
    static FRDGTextureDesc Create2DArray(FIntPoint, EPixelFormat, FClearValueBinding, ETextureCreateFlags, uint16 ArraySize, ...);
    static FRDGTextureDesc Create3D(FIntVector, EPixelFormat, FClearValueBinding, ETextureCreateFlags, ...);
    static FRDGTextureDesc CreateCube(uint32, EPixelFormat, FClearValueBinding, ETextureCreateFlags, ...);
    static FRDGTextureDesc CreateCubeArray(uint32, EPixelFormat, FClearValueBinding, ETextureCreateFlags, uint16 ArraySize, ...);
};
```

### 5.3 FRDGBuffer

源码: `RenderGraphResources.h:1319-1421`

```cpp
class FRDGBuffer final : public FRDGViewableResource {
    FRDGBufferDesc Desc;
    const ERDGBufferFlags Flags;
    FRDGBufferHandle Handle;
    FRDGPooledBuffer* PooledBuffer;
    FRHITransientBuffer* TransientBuffer;
    FRDGProducerStatesByPipeline LastProducer;
    FRDGBufferNumElementsCallback* NumElementsCallback;
    uint64 PendingCommitSize;
};
```

### 5.4 FRDGBufferDesc

源码: `RenderGraphResources.h:939-1118`

提供丰富的工厂方法：

| 方法 | 用途 |
|------|------|
| `CreateByteAddressDesc()` | Byte Address Buffer |
| `CreateStructuredDesc()` | Structured Buffer |
| `CreateBufferDesc()` | 通用 Vertex/Index Buffer |
| `CreateIndirectDesc()` | Indirect Draw/Dispatch Buffer |
| `CreateUploadDesc()` | 上传缓冲区 |
| `CreateStructuredUploadDesc()` | 结构化上传缓冲区 |

### 5.5 资源标志

```cpp
// 源码: RenderGraphDefinitions.h:162-181
enum class ERDGBufferFlags : uint8 {
    None = 0,
    MultiFrame = 1 << 0,               // 跨帧存活
    SkipTracking = 1 << 1,             // 跳过追踪（只读优化）
    ForceImmediateFirstBarrier = 1 << 2, // 首次屏障不分割
};

// 源码: RenderGraphDefinitions.h:183-206
enum class ERDGTextureFlags : uint8 {
    None = 0,
    MultiFrame = 1 << 0,
    SkipTracking = 1 << 1,
    ForceImmediateFirstBarrier = 1 << 2,
    MaintainCompression = 1 << 3,      // 阻止元数据解压
};
```

---

## 6. Handle 与注册表系统

### 6.1 TRDGHandle

源码: `RenderGraphDefinitions.h:341-433`

```cpp
template <typename LocalObjectType, typename LocalIndexType>
class TRDGHandle {
    static const IndexType kNullIndex = TNumericLimits<IndexType>::Max();
    IndexType Index = kNullIndex;

    // 支持比较、递增、Min/Max 操作
    inline static TRDGHandle Min(TRDGHandle A, TRDGHandle B);
    inline static TRDGHandle Max(TRDGHandle A, TRDGHandle B);
};
```

### 6.2 TRDGHandleRegistry

源码: `RenderGraphDefinitions.h:444-558`

```cpp
template <typename LocalHandleType, ERDGHandleRegistryDestructPolicy DestructPolicy = ...>
class TRDGHandleRegistry {
    void Insert(ObjectType* Object);
    template<typename DerivedType, class ...TArgs>
    DerivedType* Allocate(FRDGAllocator& Allocator, TArgs&&... Args);
    void Clear();
    inline ObjectType* Get(HandleType Handle);
    inline HandleType Begin() const;
    inline HandleType End() const;
    inline int32 Num() const;
};
```

**析构策略**:
- `Registry` -- 由注册表调用析构函数
- `Allocator` -- 由分配器管理生命周期
- `Never` -- 不自动析构（用于 View 等轻量资源）

---

## 7. 依赖追踪与屏障系统

### 7.1 FRDGProducerState

源码: `RenderGraphResources.h:42-49`

```cpp
struct FRDGProducerState {
    FRDGPass* Pass = nullptr;
    FRDGPass* PassIfSkipUAVBarrier = nullptr;
    FRDGPass* PassIfReadAccess = nullptr;
    ERHIAccess Access = ERHIAccess::Unknown;
    FRDGViewHandle NoUAVBarrierHandle;
};
```

### 7.2 FRDGSubresourceState

源码: `RenderGraphResources.h:68-125`

```cpp
struct FRDGSubresourceState {
    ERHIAccess Access = ERHIAccess::Unknown;
    FRDGPassHandlesByPipeline FirstPass;   // 首次使用的 Pass
    FRDGPassHandlesByPipeline LastPass;    // 最后使用的 Pass
    FRDGViewUniqueFilter NoUAVBarrierFilter;
    ERDGBufferReservedCommitHandle ReservedCommitHandle;
    EResourceTransitionFlags Flags;
    ERDGBarrierLocation BarrierLocation;   // Prologue 或 Epilogue
};
```

### 7.3 屏障批次

源码: `RenderGraphDefinitions.h:107-213`

```
FRDGBarrierBatchBegin -- 屏障开始批次
  └── 管理资源转换的 Begin 端
  └── 可被多个 FRDGBarrierBatchEnd 依赖
FRDGBarrierBatchEnd -- 屏障结束批次
  └── 依赖一个或多个 FRDGBarrierBatchBegin
  └── 在 Pass 的 Prologue/Epilogue 提交
```

屏障位置 `ERDGBarrierLocation`（RenderGraphResources.h:56-63）：
- `Prologue` -- 在 Pass 执行之前
- `Epilogue` -- 在 Pass 执行之后

### 7.4 Pass 合并机制

RDG 支持将相邻的 Raster Pass 合并为单个 RHI RenderPass。当一个 Pass 的 RenderTarget 与下一个相同且没有中间屏障需求时，RDG 会合并它们（通过 `bSkipRenderPassBegin`/`bSkipRenderPassEnd` 标志）。

---

## 8. 资源生命周期管理

### 8.1 自动分配与回收

RDG 资源的生命周期完全由图控制：

1. **创建阶段** (`CreateTexture`/`CreateBuffer`): 仅记录描述符，不分配 GPU 资源
2. **编译阶段**: 根据依赖分析确定每个资源的首次和末次使用 Pass
3. **分配阶段**: 在首次使用 Pass 之前分配，在末次使用 Pass 之后回收
4. **执行阶段**: 分配的 RHI 资源仅在注册使用它们的 Pass 中有效

### 8.2 瞬时资源分配器

源码: `RenderGraphBuilder.h:592-598`

```cpp
IRHITransientResourceAllocator* TransientResourceAllocator = nullptr;
bool bSupportsTransientTextures = false;
bool bSupportsTransientBuffers = false;
```

RDG 支持通过 `IRHITransientResourceAllocator` 进行瞬时资源分配，允许在同一帧内重用 GPU 内存。

### 8.3 资源提取

通过 `QueueTextureExtraction`/`QueueBufferExtraction` 将资源生存期延伸到图执行完毕后：

```cpp
// 源码: RenderGraphBuilder.h:346-354
void QueueTextureExtraction(FRDGTextureRef Texture,
    TRefCountPtr<IPooledRenderTarget>* OutPooledTexturePtr,
    ERDGResourceExtractionFlags Flags = ...);
void QueueBufferExtraction(FRDGBufferRef Buffer,
    TRefCountPtr<FRDGPooledBuffer>* OutPooledBufferPtr);
```

### 8.4 资源上传

```cpp
// 源码: RenderGraphBuilder.h:310-334
void QueueBufferUpload(FRDGBufferRef Buffer, const void* InitialData, uint64 InitialDataSize, ...);
```

支持多种上传模式：直接数据、回调填充、延迟大小确定。

---

## 9. Pass 裁剪 (Culling)

RDG 会自动裁剪不被任何外部输出需要的 Pass。裁剪过程（RenderGraphBuilder.h:983-990）：

```cpp
TArray<FRDGPass*, FRDGArrayAllocator> CullPassStack;

bool AddCullingDependency(...);
void AddCullRootBuffer(FRDGBuffer* Buffer);    // 外部/提取的 Buffer 是裁剪根
void AddCullRootTexture(FRDGTexture* Texture); // 外部/提取的 Texture 是裁剪根
void FlushCullStack();
```

标记 `NeverCull` 的 Pass 及其所有生产者永远不会被裁剪。

---

## 10. 并行执行

### 10.1 构建器并行标志

```cpp
// 源码: RenderGraphBuilder.h:994-1007
struct {
    TStaticArray<TArray<UE::Tasks::FTask>, ...> Tasks;
    bool bEnabled = false;
    int8 TaskPriorityBias = 0;
} ParallelSetup;
```

### 10.2 并行 Pass 执行

```cpp
// 源码: RenderGraphBuilder.h:1017-1030
struct FParallelExecute {
    TArray<FParallelPassSet> ParallelPassSets;
    TOptional<UE::Tasks::FTaskEvent> TasksAwait;
    TOptional<UE::Tasks::FTaskEvent> TasksAsync;
    ERDGPassTaskMode TaskMode = ERDGPassTaskMode::Inline;
    static UE::Tasks::FTask LastAsyncExecuteTask;
} ParallelExecute;
```

---

## 11. Blackboard — 图内数据共享

```cpp
// 源码: RenderGraphBuilder.h:434
FRDGBlackboard Blackboard;
```

Blackboard 允许在图的 Pass 之间共享任意数据，无需通过资源依赖传递。

---

## 12. 外部资源访问模式

源码: `RenderGraphBuilder.h:385-407`

```cpp
void UseExternalAccessMode(FRDGViewableResource* Resource,
    ERHIAccess ReadOnlyAccess, ERHIPipeline Pipelines = ...);
void UseInternalAccessMode(FRDGViewableResource* Resource);
```

允许在 RDG Pass 中直接访问底层 RHI 资源，RDG 自动管理状态转换。

---

## 13. 调试与诊断

### 13.1 即时模式

```cpp
// 命令行: -rdgimmediate
// CVar: r.RDG.ImmediateMode=1
static RENDERCORE_API bool IsImmediateMode();
```

即时模式下，`AddPass` 中的 Lambda 立即执行，保留完整调用栈便于调试。

### 13.2 调试宏

```cpp
// 源码: RenderGraphDefinitions.h:13-14
#define RDG_ENABLE_DEBUG (!UE_BUILD_SHIPPING && !UE_BUILD_TEST)
#define RDG_ENABLE_TRACE UE_TRACE_ENABLED && !IS_PROGRAM && !UE_BUILD_SHIPPING
```

- `RDG_ENABLE_DEBUG` -- 启用资源访问验证、未使用资源警告
- `RDG_ENABLE_TRACE` -- 启用 UE Insight 追踪
- `RDG_DUMP_RESOURCES` -- 启用帧资源转储（WITH_DUMPGPU）

### 13.3 GPU 事件

```cpp
// 源码: RenderGraphDefinitions.h:42-57
#define RDG_EVENTS_NONE 0       // 无字符串处理
#define RDG_EVENTS_STRING_REF 1 // 存储格式字符串指针
#define RDG_EVENTS_STRING_COPY 2 // 求值并存储格式化字符串
```

---

## 14. 典型使用模式

```cpp
// 1. 创建构建器
FRDGBuilder GraphBuilder(RHICmdList, RDG_EVENT_NAME("MyRenderer"));

// 2. 创建资源
FRDGTextureRef SceneColor = GraphBuilder.CreateTexture(
    FRDGTextureDesc::Create2D(ViewRect.Size(), PF_B8G8R8A8,
        FClearValueBinding::Black, TexCreate_RenderTargetable | TexCreate_ShaderResource),
    TEXT("SceneColor"));

FRDGBufferRef DataBuffer = GraphBuilder.CreateBuffer(
    FRDGBufferDesc::CreateStructuredDesc(sizeof(FMyData), NumElements),
    TEXT("DataBuffer"));

// 3. 创建视图
FRDGBufferSRVRef DataSRV = GraphBuilder.CreateSRV(DataBuffer, PF_R32_FLOAT);
FRDGTextureUAVRef ColorUAV = GraphBuilder.CreateUAV(SceneColor);

// 4. 分配参数并添加 Pass
auto* PassParams = GraphBuilder.AllocParameters<FMyPassParameters>();
PassParams->SceneColor = ColorUAV;
PassParams->Data = DataSRV;

GraphBuilder.AddPass(
    RDG_EVENT_NAME("MyComputePass"),
    PassParams,
    ERDGPassFlags::Compute,
    [PassParams](FRHIComputeCommandList& RHICmdList) {
        // GPU 命令录制
        RHICmdList.Dispatch(...);
    });

// 5. 提取输出
GraphBuilder.QueueTextureExtraction(SceneColor, &OutTexture);

// 6. 执行
GraphBuilder.Execute();
```

---

## 15. 源码证据索引

| 源文件 | 行数 | 关键内容 |
|--------|------|----------|
| `RenderCore/Public/RenderGraph.h` | 65 | 框架设计文档注释 |
| `RenderCore/Public/RenderGraphDefinitions.h` | ~800 | 枚举、Handle、注册表、Pass 基类 |
| `RenderCore/Public/RenderGraphResources.h` | ~1520 | 资源类（Texture/Buffer/View） |
| `RenderCore/Public/RenderGraphPass.h` | ~830 | Pass 实现（Lambda/Dispatch/Sentinel） |
| `RenderCore/Public/RenderGraphBuilder.h` | ~1217 | FRDGBuilder 主类 |
| `RenderCore/Private/RenderGraph.cpp` | - | 实现文件 |
| `RenderCore/Public/RenderGraphAllocator.h` | - | 内存分配器 |
| `RenderCore/Public/RenderGraphBlackboard.h` | - | Blackboard 数据共享 |
| `RenderCore/Public/RenderGraphEvent.h` | - | GPU 事件管理 |
| `RenderCore/Public/RenderGraphUtils.h` | - | 工具函数 |
