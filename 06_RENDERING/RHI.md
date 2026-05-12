# RHI 抽象层详解

## 摘要

RHI (Render Hardware Interface) 是 UE5.7.4 对不同 GPU API 的抽象层。它提供了与平台无关的 GPU 资源管理和命令提交接口，后端支持 D3D12、Vulkan 和 Metal。RHI 层是引擎渲染系统的基石，所有 GPU 操作最终都通过 RHI 完成。

**核心源码位置**:
- `Engine/Source/Runtime/RHI/Public/RHI.h` — RHI 基础定义
- `Engine/Source/Runtime/RHI/Public/DynamicRHI.h` — FDynamicRHI 动态接口（约 1522 行）
- `Engine/Source/Runtime/D3D12RHI/` — D3D12 后端实现

---

## 1. 架构概览

### 1.1 RHI 在渲染管线中的位置

```
Engine 层 (材质/渲染器/场景)
    ↓
RenderCore 层 (RDG / Shader / RenderResource)
    ↓
RHI 层 (FDynamicRHI / FRHICommandList)
    ↓ ↙       ↓          ↓
D3D12RHI   VulkanRHI   MetalRHI
    ↓         ↓          ↓
D3D12 API  Vulkan API  Metal API
    ↓         ↓          ↓
  GPU 硬件驱动
```

### 1.2 模块组织

| 目录 | 模块 | 职责 |
|------|------|------|
| `Runtime/RHI/` | RHI | 抽象接口定义、资源基类、公共工具 |
| `Runtime/RenderCore/` | RenderCore | 渲染核心（依赖 RHI，提供更高层抽象） |
| `Runtime/D3D12RHI/` | D3D12RHI | D3D12 后端实现 |
| `Runtime/VulkanRHI/` | VulkanRHI | Vulkan 后端实现 |
| `Runtime/Apple/` | MetalRHI | Metal 后端实现（macOS/iOS） |

---

## 2. FDynamicRHI — 动态 RHI 实现

### 2.1 类声明

源码: `DynamicRHI.h:98`

```cpp
class FDynamicRHI;
```

`FDynamicRHI` 是一个纯虚接口类，包含约 1522 行定义，提供所有 GPU 操作的抽象方法。每个平台实现一个子类（如 `FD3D12DynamicRHI`、`FVulkanDynamicRHI`）。

### 2.2 创建类方法分类

根据 `DynamicRHI.h` 源码中的虚方法签名，FDynamicRHI 的方法可分为以下类别：

#### 状态对象创建

```cpp
// 源码: DynamicRHI.h:252-264
virtual FSamplerStateRHIRef RHICreateSamplerState(const FSamplerStateInitializerRHI& Initializer) = 0;
virtual FRasterizerStateRHIRef RHICreateRasterizerState(const FRasterizerStateInitializerRHI& Initializer) = 0;
virtual FDepthStencilStateRHIRef RHICreateDepthStencilState(const FDepthStencilStateInitializerRHI& Initializer) = 0;
virtual FBlendStateRHIRef RHICreateBlendState(const FBlendStateInitializerRHI& Initializer) = 0;
virtual FVertexDeclarationRHIRef RHICreateVertexDeclaration(const FVertexDeclarationElementList& Elements) = 0;
```

#### Shader 创建

```cpp
// 源码: DynamicRHI.h:267-294
virtual FPixelShaderRHIRef RHICreatePixelShader(TArrayView<const uint8> Code, const FSHAHash& Hash) = 0;
virtual FVertexShaderRHIRef RHICreateVertexShader(TArrayView<const uint8> Code, const FSHAHash& Hash) = 0;
virtual FGeometryShaderRHIRef RHICreateGeometryShader(TArrayView<const uint8> Code, const FSHAHash& Hash) = 0;
virtual FMeshShaderRHIRef RHICreateMeshShader(TArrayView<const uint8> Code, const FSHAHash& Hash);
virtual FAmplificationShaderRHIRef RHICreateAmplificationShader(TArrayView<const uint8> Code, const FSHAHash& Hash);
virtual FComputeShaderRHIRef RHICreateComputeShader(TArrayView<const uint8> Code, const FSHAHash& Hash) = 0;
virtual FWorkGraphShaderRHIRef RHICreateWorkGraphShader(TArrayView<const uint8> Code, const FSHAHash& Hash, EShaderFrequency ShaderFrequency);
```

#### 管线状态创建

```cpp
// 源码: DynamicRHI.h:390-420
virtual FBoundShaderStateRHIRef RHICreateBoundShaderState(...) = 0;
virtual FGraphicsPipelineStateRHIRef RHICreateGraphicsPipelineState(const FGraphicsPipelineStateInitializer& Initializer) = 0;
virtual FComputePipelineStateRHIRef RHICreateComputePipelineState(const FComputePipelineStateInitializer& Initializer) = 0;
virtual FWorkGraphPipelineStateRHIRef RHICreateWorkGraphPipelineState(const FWorkGraphPipelineStateInitializer& Initializer);
```

#### Buffer 与 Texture 创建

```cpp
// 源码: DynamicRHI.h:434-518
virtual FUniformBufferRHIRef RHICreateUniformBuffer(const void* Contents, const FRHIUniformBufferLayout* Layout, EUniformBufferUsage Usage, EUniformBufferValidation Validation) = 0;
[[nodiscard]] virtual FRHIBufferInitializer RHICreateBufferInitializer(FRHICommandListBase& RHICmdList, const FRHIBufferCreateDesc& CreateDesc) = 0;
virtual FRHITextureInitializer RHICreateTextureInitializer(FRHICommandListBase& RHICmdList, const FRHITextureCreateDesc& CreateDesc) = 0;
```

#### 视图创建

```cpp
// 源码: DynamicRHI.h:526-527
virtual FShaderResourceViewRHIRef RHICreateShaderResourceView(FRHICommandListBase& RHICmdList, FRHIViewableResource* Resource, FRHIViewDesc const& ViewDesc) = 0;
virtual FUnorderedAccessViewRHIRef RHICreateUnorderedAccessView(FRHICommandListBase& RHICmdList, FRHIViewableResource* Resource, FRHIViewDesc const& ViewDesc) = 0;
```

#### Ray Tracing 相关

```cpp
// 源码: DynamicRHI.h:1010-1047
virtual FRayTracingGeometryRHIRef RHICreateRayTracingGeometry(FRHICommandListBase& RHICmdList, const FRayTracingGeometryInitializer& Initializer);
virtual FRayTracingSceneRHIRef RHICreateRayTracingScene(FRayTracingSceneInitializer Initializer);
virtual FRayTracingShaderRHIRef RHICreateRayTracingShader(TArrayView<const uint8> Code, const FSHAHash& Hash, EShaderFrequency ShaderFrequency);
virtual FRayTracingPipelineStateRHIRef RHICreateRayTracingPipelineState(const FRayTracingPipelineStateInitializer& Initializer);
virtual FShaderBindingTableRHIRef RHICreateShaderBindingTable(FRHICommandListBase& RHICmdList, const FRayTracingShaderBindingTableInitializer& Initializer);
virtual FShaderBundleRHIRef RHICreateShaderBundle(const FShaderBundleCreateInfo& CreateInfo);
```

#### 同步与查询

```cpp
// 源码: DynamicRHI.h:312-339
virtual void RHICreateTransition(FRHITransition* Transition, const FRHITransitionCreateInfo& CreateInfo);
virtual IRHITransientResourceAllocator* RHICreateTransientResourceAllocator();
virtual FGPUFenceRHIRef RHICreateGPUFence(const FName &Name) = 0;
virtual FRenderQueryRHIRef RHICreateRenderQuery(ERenderQueryType QueryType) = 0;
```

---

## 3. FRHICommandList — RHI 命令列表

### 3.1 命令列表层次

```
FRHIComputeCommandList         -- 计算命令列表（基础）
├── FRHICommandList            -- 图形命令列表（添加光栅化命令）
└── FRHICommandListImmediate   -- 立即模式命令列表（直接提交）
```

### 3.2 命令提交模型

RDG 通过 `FRHICommandList` 提交 GPU 命令。在 RDG 中：

- `ERDGPassFlags::Compute` / `AsyncCompute` -> 使用 `FRHIComputeCommandList&`
- `ERDGPassFlags::Raster` -> 使用 `FRHICommandList&`
- 需要立即执行的操作 -> 使用 `FRHICommandListImmediate&`

---

## 4. 核心资源类型

### 4.1 纹理资源

```
FRHITexture (基类)
├── FRHITexture2D        -- 2D 纹理
├── FRHITexture2DArray   -- 2D 纹理数组
├── FRHITexture3D        -- 3D 体积纹理
├── FRHITextureCube      -- 立方体贴图
└── FRHITextureReference -- 纹理引用（间接访问）
```

纹理创建通过 `FRHITextureCreateDesc` 描述符完成，由 `FDynamicRHI::RHICreateTextureInitializer` 创建。

### 4.2 缓冲区资源

```
FRHIBuffer (基类)
├── EBufferUsageFlags::VertexBuffer         -- 顶点缓冲区
├── EBufferUsageFlags::IndexBuffer          -- 索引缓冲区
├── EBufferUsageFlags::StructuredBuffer     -- 结构化缓冲区
├── EBufferUsageFlags::ByteAddressBuffer    -- 字节地址缓冲区
├── EBufferUsageFlags::DrawIndirect         -- 间接绘制缓冲区
├── EBufferUsageFlags::ShaderResource       -- SRV 可读
├── EBufferUsageFlags::UnorderedAccess      -- UAV 可写
└── EBufferUsageFlags::ReservedResource     -- 预留资源（虚拟地址）
```

缓冲区创建使用 `FRHIBufferCreateDesc` 描述符，由 `FDynamicRHI::RHICreateBufferInitializer` 创建。

### 4.3 Shader 资源

```
FRHIShader (基类)
├── FRHIVertexShader       -- 顶点着色器
├── FRHIPixelShader        -- 像素着色器
├── FRHIGeometryShader     -- 几何着色器
├── FRHIComputeShader      -- 计算着色器
├── FRHIMeshShader         -- Mesh Shader
├── FRHIAmplificationShader -- Amplification Shader
├── FRHIRayTracingShader   -- 光线追踪着色器
└── FRHIWorkGraphShader    -- Work Graph Shader
```

### 4.4 管线状态

```
FRHIPipelineState (基类)
├── FGraphicsPipelineState  -- 图形管线状态
├── FComputePipelineState   -- 计算管线状态
└── FWorkGraphPipelineState -- Work Graph 管线状态
```

图形管线状态由 `FGraphicsPipelineStateInitializer` 描述，包含：
- 绑定的 Shader
- 混合状态、光栅化状态、深度模板状态
- 顶点声明
- 渲染目标格式
- 采样数

### 4.5 视图类型

```
FRHIView (基类)
├── FRHIShaderResourceView  -- SRV（只读）
├── FRHIShaderResourceViewCombined -- 组合 SRV
├── FRHIUnorderedAccessView -- UAV（读写）
└── FRHIRayTracingAccelStructView -- RT 加速结构视图
```

### 4.6 Uniform Buffer

```cpp
// 源码: DynamicRHI.h:434
virtual FUniformBufferRHIRef RHICreateUniformBuffer(
    const void* Contents,
    const FRHIUniformBufferLayout* Layout,
    EUniformBufferUsage Usage,
    EUniformBufferValidation Validation) = 0;
```

---

## 5. 资源状态与转换

### 5.1 ERHIAccess

```cpp
enum class ERHIAccess : uint32 {
    Unknown     = 0,
    CPURead     = ...,
    Present     = ...,
    SRVMask     = ...,
    CopySrc     = ...,
    CopyDst     = ...,
    VRAMColor   = ...,
    RTV         = ...,
    DepthStencil= ...,
    UAVMask     = ...,
    // ... 等等
};
```

### 5.2 屏障转换

```cpp
// 源码: DynamicRHI.h:321-331
virtual void RHICreateTransition(FRHITransition* Transition,
    const FRHITransitionCreateInfo& CreateInfo);
```

RDG 通过 `FRDGBarrierBatchBegin`/`FRDGBarrierBatchEnd` 管理屏障，在 Pass 边界自动插入资源状态转换。

### 5.3 瞬时资源分配器

```cpp
// 源码: DynamicRHI.h:332
virtual IRHITransientResourceAllocator* RHICreateTransientResourceAllocator();
```

D3D12 后端使用 D3D12 瞬时资源（Placed Resources in Reserved Heaps）实现高效的帧内内存复用。

---

## 6. RHI 辅助功能

### 6.1 GPU 厂商检测

源码: `RHI.h:46-60`

```cpp
RHI_API bool IsRHIDeviceAMD();
RHI_API bool IsRHIDeviceIntel();
RHI_API bool IsRHIDeviceNVIDIA();
RHI_API bool IsRHIDeviceQualcomm();
RHI_API bool IsRHIDeviceApple();
```

### 6.2 GPU 崩溃调试

源码: `RHI.h:62-71`

```cpp
namespace UE::RHI {
    RHI_API bool UseGPUCrashDebugging();
    RHI_API bool UseGPUCrashBreadcrumbs();
    RHI_API bool ShouldEnableGPUCrashFeature(IConsoleVariable& CVar, TCHAR const* CommandLineSwitch);
}
```

### 6.3 投影矩阵修正

源码: `RHI.h:171-176`

```cpp
inline FMatrix AdjustProjectionMatrixForRHI(const FMatrix& InProjectionMatrix) {
    FScaleMatrix ClipSpaceFixScale(FVector(1.0f, GProjectionSignY, 1.0f - GMinClipZ));
    FTranslationMatrix ClipSpaceFixTranslate(FVector(0.0f, 0.0f, GMinClipZ));
    return InProjectionMatrix * ClipSpaceFixScale * ClipSpaceFixTranslate;
}
```

根据不同 API 的裁剪空间约定调整投影矩阵（Vulkan 的 Y 轴方向、Z 范围等差异）。

### 6.4 像素格式能力查询

源码: `RHI.h:143-156`

```cpp
inline bool RHIPixelFormatHasCapabilities(EPixelFormat InFormat, EPixelFormatCapabilities InCapabilities);
inline bool RHIIsTypedUAVLoadSupported(EPixelFormat InFormat);
inline bool RHIIsTypedUAVStoreSupported(EPixelFormat InFormat);
```

### 6.5 资源统计

源码: `RHI.h:91-127`

```cpp
struct FRHIResourceStats {
    FName Name;
    FName OwnerName;
    FString Type;
    FString Flags;
    uint64 SizeInBytes;
    bool bResident, bMarkedForDelete, bTransient, bStreaming;
    bool bRenderTarget, bDepthStencil, bUnorderedAccessView;
    bool bRayTracingAccelerationStructure;
};

RHI_API void RHIGetTrackedResourceStats(TArray<TSharedPtr<FRHIResourceStats>>& OutResourceStats);
```

---

## 7. D3D12 后端实现

### 7.1 关键文件

| 文件 | 路径 | 职责 |
|------|------|------|
| `D3D12RHI.h` | `D3D12RHI/Public/` | D3D12 RHI 公共接口 |
| `ID3D12DynamicRHI.h` | `D3D12RHI/Public/` | D3D12 动态 RHI 接口 |
| `D3D12ShaderResources.h` | `D3D12RHI/Public/` | Shader 资源绑定 |

### 7.2 D3D12 核心映射

| RHI 类型 | D3D12 对应 |
|----------|-----------|
| `FD3D12DynamicRHI` | 继承 `FDynamicRHI`，管理 D3D12 设备 |
| `FD3D12CommandContext` | 封装 `ID3D12GraphicsCommandList` |
| `FD3D12Resource` | 封装 `ID3D12Resource` |
| `FD3D12DescriptorCache` | 管理 CPU/GPU 描述符堆 |
| `FRHITexture -> FD3D12Texture` | `ID3D12Resource` + RTV/DSV/SRV/UAV 描述符 |
| `FRHIBuffer -> FD3D12Buffer` | `ID3D12Resource` + VB/IB/CB/SRV/UAV 描述符 |

### 7.3 命令提交流程

```
FRHICommandList::Dispatch()
  → FD3D12CommandContext::DispatchComputeShader()
    → ID3D12GraphicsCommandList::Dispatch()
      → ID3D12CommandQueue::ExecuteCommandLists()
```

---

## 8. RHI 命令列表基础设施

### 8.1 ENQUEUE_RENDER_COMMAND

引擎使用 `ENQUEUE_RENDER_COMMAND` 宏将操作从游戏线程调度到渲染线程：

```cpp
ENQUEUE_RENDER_COMMAND(MyCommand)(
    [Param1, Param2](FRHICommandListImmediate& RHICmdList) {
        // 在渲染线程执行
    });
```

### 8.2 渲染线程模型

```
游戏线程                    渲染线程                   RHI 线程
   |                          |                         |
   |-- ENQUEUE_RENDER_CMD --> |                         |
   |                          |-- RHICmdList.Dispatch ->|
   |                          |                         |-- D3D12 API 调用
   |                          |                         |-- GPU 提交
   |                          | <-- 完成 ---------------|
```

在非线程化渲染模式下（如 `-NoThreadedRendering`），渲染命令直接在游戏线程执行。

---

## 9. 多 GPU 支持

源码: `RHI.h:129`

```cpp
#include "MultiGPU.h"
```

RHI 层通过 `FRHIGPUMask` 支持多 GPU 配置，每个命令可指定目标 GPU 掩码。RDG 中通过 `RDG_GPU_MASK_SCOPE` 宏控制：

```cpp
// 源码: RenderGraphBuilder.h:1202-1206
#if WITH_MGPU
    #define RDG_GPU_MASK_SCOPE(GraphBuilder, GPUMask) SCOPED_GPU_MASK(GraphBuilder.RHICmdList, GPUMask)
#else
    #define RDG_GPU_MASK_SCOPE(GraphBuilder, GPUMask)
#endif
```

---

## 10. 纹理锁定 API

源码: `DynamicRHI.h:128-200`

```cpp
struct FRHILockedTextureDesc {
    FRHITexture* Texture;
    uint32 FaceIndex, ArrayIndex, MipIndex;
};

struct FRHILockTextureArgs : public FRHILockedTextureDesc {
    EResourceLockMode LockMode;
    bool bLockWithinMiptail;
    bool bNeedsDefaultRHIFlush;

    static FRHILockTextureArgs Lock2D(...);
    static FRHILockTextureArgs Lock2DArray(...);
    static FRHILockTextureArgs LockCubeFace(...);
};

struct FRHILockTextureResult {
    void* Data;
    uint64 ByteCount;
};
```

---

## 11. 渲染查询

```cpp
// 源码: DynamicRHI.h:647
virtual FRenderQueryRHIRef RHICreateRenderQuery(ERenderQueryType QueryType) = 0;
```

渲染查询类型包括：
- `RQT_Occlusion` — 遮挡查询
- `RQT_AbsoluteTime` — GPU 时间戳

---

## 12. Swap Chain 与 Present

```cpp
// 源码: DynamicRHI.h:725
virtual FViewportRHIRef RHICreateViewport(void* WindowHandle, uint32 SizeX, uint32 SizeY,
    bool bIsFullscreen, EPixelFormat PreferredPixelFormat) = 0;
```

Viewport 封装了平台相关的 Swap Chain：
- D3D12: `IDXGISwapChain`
- Vulkan: `VkSwapchainKHR`
- Metal: `CAMetalLayer`

---

## 13. Shader Library

```cpp
// 源码: DynamicRHI.h:294-307
virtual FRHIShaderLibraryRef RHICreateShaderLibrary(EShaderPlatform Platform,
    FString const& FilePath, FString const& Name);
```

支持预编译的 Shader Library（如 DXIL Library、Metal Library），用于 Pipeline State Cache 和 Ray Tracing。

---

## 14. 帧翻转追踪

源码: `DynamicRHI.h:47-68`

```cpp
struct FRHIFlipDetails {
    uint64 PresentIndex;
    double FlipTimeInSeconds;
    double VBlankTimeInSeconds;
    uint64 VBlankTimeInCycles;
};
```

用于精确追踪帧呈现时序，支持可变刷新率 (VRR) 和延迟分析。

---

## 15. 源码证据索引

| 源文件 | 行数 | 关键内容 |
|--------|------|----------|
| `RHI/Public/RHI.h` | ~200+ | RHI 基础定义、厂商检测、像素格式、投影修正 |
| `RHI/Public/DynamicRHI.h` | ~1522 | FDynamicRHI 纯虚接口（所有 GPU 操作） |
| `RHI/Public/RHIDefinitions.h` | - | RHI 枚举、标志、平台定义 |
| `RHI/Public/RHIResources.h` | - | FRHI 资源基类 |
| `RHI/Public/RHIContext.h` | - | RHI 命令上下文 |
| `RHI/Public/RHICommandList.h` | - | 命令列表定义 |
| `RHI/Public/RHIAccess.h` | - | ERHIAccess 资源访问状态 |
| `RHI/Public/RHITransientResourceAllocator.h` | - | 瞬时资源分配器接口 |
| `D3D12RHI/Public/D3D12RHI.h` | - | D3D12 后端公共接口 |
| `D3D12RHI/Public/ID3D12DynamicRHI.h` | - | D3D12 动态 RHI 接口 |
| `D3D12RHI/Public/D3D12ShaderResources.h` | - | D3D12 Shader 资源绑定 |
