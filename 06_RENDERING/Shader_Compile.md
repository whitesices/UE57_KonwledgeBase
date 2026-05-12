# Shader 编译详解

## 摘要

UE5.7.4 的 Shader 编译系统将 HLSL 着色器代码编译为各目标平台可执行的 GPU 指令。编译过程由独立进程 ShaderCompileWorker 执行，支持 HLSL 到 D3D12 DXIL、Vulkan SPIR-V、Metal MSL 的交叉编译，并通过 DDC (Derived Data Cache) 缓存编译结果。

**核心源码位置**:
- `Engine/Source/Runtime/RenderCore/Public/Shader.h` — Shader 基类与类型系统
- `Engine/Source/Runtime/RenderCore/Private/Shader.cpp` — Shader 编译实现
- `Engine/Source/Programs/ShaderCompileWorker/` — 独立编译进程
- `Engine/Shaders/Private/` — 引擎 HLSL 源码
- `Engine/Shaders/Shared/` — 跨平台共享头文件

---

## 1. 编译流程概览

### 1.1 端到端流程

```
UMaterial (材质节点图)
  → FMaterial::Compile()
    → FHLSLMaterialTranslator (节点图 → HLSL 源码)
      → FMaterialShaderMap::Compile()
        → FShaderType::CompileShader() (为每个 Shader Type)
          → FShaderCompiler::Compile() (调度到编译队列)
            → ShaderCompileWorker (独立进程)
              → DXC / FXC (HLSL → DXIL/DXBC)
              → CrossCompiler (HLSL → GLSL/SPIR-V)
              → Metal Compiler (HLSL → Metal MSL)
            → 缓存到 DDC (Derived Data Cache)
```

### 1.2 编译触发时机

| 触发场景 | 说明 |
|----------|------|
| 材质修改 | 编辑器中修改材质参数或节点连接 |
| Shader Permutation | 开启/关闭功能导致新的排列组合 |
| 平台切换 | 切换目标平台需要重新编译 |
| 首次加载 | 新项目首次加载或 DDC 缺失 |
| 引擎改动 | 修改 Engine/Shaders 下的 .usf/.ush 文件 |

---

## 2. Shader 类型系统

### 2.1 FShader — Shader 基类

源码: `Shader.h:828`

```cpp
class FShader {
    // 核心成员
    FShaderType* Type;                        // Shader 类型
    FShaderPipelineType* Pipeline;            // 所属管线
    FVertexFactoryType* VertexFactoryType;    // 关联的顶点工厂类型
    FShaderResourceParameterInfo ParameterMap; // 参数映射信息

    // 编译结果
    FShaderCodeData CodeData;                 // 编译后的字节码
    TArray<uint8> ParameterBufferData;        // 参数缓冲数据

    // 序列化
    friend FArchive& operator<<(FArchive& Ar, FShader*& Shader);
};
```

### 2.2 Shader 类型层次

```
FShaderType (类型注册系统)
├── FGlobalShaderType     -- 全局 Shader 类型
├── FMaterialShaderType   -- 材质 Shader 类型
├── FMeshMaterialShaderType -- Mesh 材质 Shader 类型
├── FNiagaraShaderType    -- Niagara 特效 Shader 类型
├── FComputeKernelShaderType -- Compute Kernel Shader 类型
└── FOpenColorIOShaderType -- OCIO Shader 类型
```

### 2.3 Shader 分类

| 类别 | 基类 | 说明 |
|------|------|------|
| FGlobalShader | `Shader.h` | 不依赖 Material，全局唯一。如后处理、Clear、Copy |
| FMaterialShader | `MaterialShader.h` | 依赖 Material 参数但不依赖 Mesh |
| FMeshMaterialShader | `MeshMaterialShader.h` | 同时依赖 Material 和 Mesh (VertexFactory) |

### 2.4 FShaderType 注册

源码: `Shader.h:90-93` (前向声明)

```cpp
class FGlobalShaderType;
class FMaterialShaderType;
class FMeshMaterialShaderType;
class FShaderType;
class FShaderPipelineType;
```

每个 Shader 类型在引擎启动时通过全局静态构造自动注册到 `FShaderType` 的类型列表中。注册宏示例：

```cpp
// 全局 Shader 注册
IMPLEMENT_GLOBAL_SHADER(TShader, "/Path/Shader.usf", "MainCS", SF_Compute);

// 材质 Shader 注册
IMPLEMENT_MATERIAL_SHADER_TYPE(TShader, ...);

// Mesh 材质 Shader 注册
IMPLEMENT_MESH_MATERIAL_SHADER_TYPE(TShader, ...);
```

---

## 3. Shader 参数系统

### 3.1 参数信息类型

源码: `Shader.h:145-313`

| 类 | 用途 |
|-----|------|
| `FShaderUniformBufferParameterInfo` | Uniform Buffer 参数绑定信息 (uint16 BaseIndex) |
| `FShaderResourceParameterInfo` | 资源参数绑定信息 (BaseIndex + BufferIndex + Type) |
| `FShaderLooseParameterInfo` | 松散参数绑定信息 (BaseIndex + Size) |
| `FShaderLooseParameterBufferInfo` | 松散参数缓冲信息 (BaseIndex + Size + Parameters[]) |
| `FShaderParameterMapInfo` | 参数映射汇总 (所有参数绑定信息的集合) |

### 3.2 参数映射信息

```cpp
// 源码: Shader.h:289-313
class FShaderParameterMapInfo {
    TMemoryImageArray<FShaderUniformBufferParameterInfo> UniformBuffers;
    TMemoryImageArray<FShaderResourceParameterInfo> TextureSamplers;
    TMemoryImageArray<FShaderResourceParameterInfo> SRVs;
    TMemoryImageArray<FShaderLooseParameterBufferInfo> LooseParameterBuffers;
    uint64 Hash;
};
```

### 3.3 参数绑定宏

UE 使用宏系统声明 Shader 参数：

```cpp
BEGIN_SHADER_PARAMETER_STRUCT(FMyPassParameters, )
    SHADER_PARAMETER(FMatrix, ViewProjection)
    SHADER_PARAMETER(FVector4f, ViewInfo)
    SHADER_PARAMETER_SRV(Texture2D, DepthTexture)
    SHADER_PARAMETER_UAV(RWTexture2D<float4>, OutputTexture)
    SHADER_PARAMETER_SAMPLER(SamplerState, LinearSampler)
    SHADER_PARAMETER_STRUCT(FSceneUniforms, Scene)
    RENDER_TARGET_BINDING_SLOTS()
END_SHADER_PARAMETER_STRUCT()
```

这些宏在编译期展开为 `FShaderParametersMetadata` 描述的反射信息。

---

## 4. Shader Permutation (排列组合)

### 4.1 排列组合系统

源码: `Shader.h:91-122`

```cpp
template<typename MetaShaderType>
struct TShaderTypePermutation {
    MetaShaderType* const Type;
    const int32 PermutationId;
};

using FShaderPermutation = TShaderTypePermutation<FShaderType>;
inline const int32 kUniqueShaderPermutationId = 0;
```

### 4.2 排列组合比较器

```cpp
// 源码: Shader.h:124-143
template<typename MetaShaderType>
class TCompareShaderTypePermutation {
    bool operator()(const TShaderTypePermutation& A, const TShaderTypePermutation& B) const {
        // 按类型名称长度、字典序、PermutationId 排序
    }
};
```

### 4.3 Permutation 维度

典型的 Shader 排列组合维度：
- **光照类型**: 点光/方向光/聚光灯
- **材质域**: Surface/DeferredDecal/Translucent
- **着色模型**: DefaultLit/Subsurface/ClearCoat/...
- **材质特性**: 双面/遮罩/半透明
- **平台特性**: SM5/ES3.1/Vulkan/Metal
- **功能开关**: 每个静态开关产生 2 个排列

一个复杂的材质 Shader 可能有数千甚至数万种排列组合。

---

## 5. FShaderMapResource 与 Shader 缓存

### 5.1 FShaderMapResource

源码: `Shader.h:335-349`

```cpp
class FShaderMapResource : public FRenderResource, public FDeferredCleanupInterface {
    EShaderPlatform GetPlatform() const { return Platform; }

    void AddRef();
    void Release();
    inline int32 GetNumRefs() const;
    virtual void ReleaseRHI() override;
    inline int32 GetNumShaders() const;
};
```

### 5.2 FMaterialShaderMap

`FMaterialShaderMap` 是材质到 Shader 集合的映射。它管理一个材质在特定 Shader Platform 下的所有编译后的 Shader。

```
UMaterial → FMaterialResource → FMaterialShaderMap
                                    ├── FMeshMaterialShader (BasePass VS/PS)
                                    ├── FMeshMaterialShader (DepthPass VS/PS)
                                    ├── FMeshMaterialShader (ShadowPass VS/PS)
                                    └── FMaterialShader (SSS, Decal, etc.)
```

---

## 6. ShaderCompileWorker — 独立编译进程

### 6.1 模块结构

源码: `Engine/Source/Programs/ShaderCompileWorker/ShaderCompileWorker.Build.cs`

ShaderCompileWorker 是一个独立进程程序，职责是：
1. 接收引擎主进程的编译任务
2. 调用编译器后端（DXC/FXC/Glslang/Metal）
3. 返回编译结果（字节码 + 反射信息）

### 6.2 为什么使用独立进程

- **稳定性**: 编译器崩溃不会影响主引擎进程
- **并行性**: 可启动多个 Worker 进程并行编译
- **内存隔离**: 编译器内存泄漏不影响引擎
- **跨平台**: Worker 可在远程机器上运行

### 6.3 编译后端映射

| 目标平台 | 编译后端 | 输出格式 |
|----------|----------|----------|
| D3D12 SM5.0+ | DXC (DirectX Shader Compiler) | DXIL |
| D3D11 SM5.0 | FXC (fxc.exe) | DXBC |
| Vulkan | DXC → SPIR-V (通过 -spirv 参数) | SPIR-V |
| OpenGL | HLSL → GLSL (CrossCompiler) | GLSL |
| Metal (macOS/iOS) | HLSL → Metal MSL | MSL |

---

## 7. Shader 文件组织

### 7.1 文件扩展名

| 扩展名 | 含义 | 示例位置 |
|--------|------|----------|
| `.usf` | Unreal Shader File (Shader 源码) | `Engine/Shaders/Private/` |
| `.ush` | Unreal Shader Header (头文件) | `Engine/Shaders/Shared/` |
| `.hlsl` | 标准 HLSL 文件 | 部分第三方代码 |

### 7.2 关键 Shader 目录

```
Engine/Shaders/
├── Private/                      -- 引擎内部 Shader 源码
│   ├── BasePassPixelShader.usf   -- Base Pass 像素着色器
│   ├── BasePassVertexShader.usf  -- Base Pass 顶点着色器
│   ├── DeferredShadingRenderer.usf -- 延迟渲染器
│   ├── Lumen/                    -- Lumen GI 相关
│   ├── Nanite/                   -- Nanite 虚拟几何
│   ├── PathTracing/              -- 路径追踪
│   ├── PostProcess/              -- 后处理效果
│   ├── RayTracing/               -- 光线追踪
│   ├── VirtualShadowMap/         -- 虚拟阴影图
│   └── ...
├── Shared/                       -- 跨平台共享头文件
│   ├── WaveIntrinsics.hlsl       -- Wave 操作
│   ├── RayTracingPayloadType.h   -- RT Payload 定义
│   └── ...
└── Public/                       -- 可被插件引用的公共头文件
```

---

## 8. Shader 编译优化

### 8.1 DDC 缓存

编译结果存储在 Derived Data Cache (DDC) 中，避免重复编译。DDC 键由以下因素决定：
- Shader 源码哈希
- 编译参数
- 目标平台
- Permutation ID
- 引擎版本

### 8.2 Shader Pipeline Cache

运行时的 PSO (Pipeline State Object) 缓存进一步减少卡顿：
- 首次运行时记录所有使用的 PSO
- 后续加载时预编译缓存的 PSO
- 存储在项目的 `DerivedDataCache/` 中

### 8.3 异步编译

Shader 编译默认异步进行：
- 编辑器修改材质时触发后台编译
- 使用半透明/棋盘格占位材质在编译期间显示
- 编译完成后自动替换

### 8.4 Shader 瘦身

UE 自动清理未使用的 Shader 参数：

```cpp
// RDG 框架提供的优化
ClearUnusedGraphResources(Shader, PassParameters);
```

---

## 9. 光线追踪 Payload 类型系统

源码: `Shader.h:315-333`

```cpp
enum class ERayTracingPayloadType : uint32;
typedef uint32(*TRayTracingPayloadSizeFunction)();

RENDERCORE_API uint32 GetRayTracingPayloadTypeMaxSize(ERayTracingPayloadType PayloadType);
RENDERCORE_API void RegisterRayTracingPayloadType(ERayTracingPayloadType, uint32 PayloadSize, ...);

#define IMPLEMENT_RT_PAYLOAD_TYPE(PayloadType, PayloadSize)
#define IMPLEMENT_RT_PAYLOAD_TYPE_FUNCTION(PayloadType, PayloadSizeFunction)
```

光线追踪 Shader 需要声明其 Payload 大小，用于 RT 管线优化。

---

## 10. 编译调试与诊断

### 10.1 编译日志

```
[ShaderCompileWorker] Compiling TBasePassPSFNoLightMapPolicy...
  → Source: Engine/Shaders/Private/BasePassPixelShader.usf
  → Entry: Main
  → Profile: ps_5_0
  → Defines: ...
  → Time: 1.23s
  → Output: 12345 bytes
```

### 10.2 控制台命令

| 命令 | 功能 |
|------|------|
| `r.ShaderDevelopmentMode 1` | 启用 Shader 开发模式（详细日志） |
| `r.DumpShaderDebugInfo 1` | 导出编译中间文件 |
| `r.Shaders.Optimize 0` | 禁用 Shader 优化（便于调试） |
| `r.Shaders.SkipCompilation 1` | 跳过编译（用于快速迭代） |
| `recompileshaders changed` | 重新编译修改过的 Shader |
| `recompileshaders all` | 重新编译所有 Shader |

### 10.3 Shader 编译错误处理

编译失败时引擎会：
1. 在 Output Log 中显示完整错误信息（含行号）
2. 使用默认的粉红色 Error Material 替代
3. 在 Shader Complexity 视图中标记错误 Shader
4. 将错误写入 ShaderCompileWorker 日志文件

---

## 11. Shader 平台抽象

### 11.1 EShaderPlatform

`EShaderPlatform` 是一个 uint16 枚举，标识编译目标平台：

```cpp
// 源码: RHIShaderPlatform.h (被 Shader.h 间接包含)
enum EShaderPlatform : uint16;
```

常见的平台值：
- `SP_PCD3D_SM5` — D3D11 Shader Model 5.0
- `SP_PCD3D_SM6` — D3D12 Shader Model 6.0+
- `SP_VULKAN_SM5` — Vulkan SM5
- `SP_VULKAN_ES31` — Vulkan ES3.1
- `SP_METAL` — Metal (macOS)
- `SP_METAL_MRT` — Metal MRT (iOS)

### 11.2 Feature Level 与 Shader Platform 的关系

```
ERHIFeatureLevel::ES3.1 → SM5 / Vulkan ES3.1 / Metal
ERHIFeatureLevel::SM5   → SM5 / Vulkan SM5 / Metal
ERHIFeatureLevel::SM6   → SM6 / Vulkan SM6 / Metal
ERHIFeatureLevel::ES3.1 → Mobile 平台
```

---

## 12. Shader 绑定与资源布局

### 12.1 绑定模型

UE5.7.4 支持多种 Shader 资源绑定模型：

| 模型 | 说明 | 平台 |
|------|------|------|
| Uniform Buffer | 传统 UUB 绑定 | 全平台 |
| Root Signature | D3D12 根签名 | D3D12 |
| Push Descriptors | Vulkan 推送描述符 | Vulkan |
| Argument Buffers | Metal 参数缓冲 | Metal |

### 12.2 Shader Binding Layout

```cpp
// 前向声明 (Shader.h:83)
class FRHIShaderBindingLayout;
```

`FRHIShaderBindingLayout` 定义了 Shader 资源绑定的布局描述，用于 Pipeline State 创建时的资源匹配。

---

## 13. 源码证据索引

| 源文件 | 关键内容 |
|--------|----------|
| `RenderCore/Public/Shader.h` | Shader 基类、类型系统、参数映射、Permutation (行 828+) |
| `RenderCore/Public/ShaderCore.h` | Shader 加载、DDC 集成 |
| `RenderCore/Public/ShaderParameters.h` | Shader 参数系统 |
| `RenderCore/Public/ShaderParameterMetadata.h` | 参数元数据 |
| `RenderCore/Public/ShaderPermutation.h` | 排列组合定义 |
| `RenderCore/Public/ShaderPermutationUtils.h` | 排列组合工具 |
| `RenderCore/Private/Shader.cpp` | Shader 编译实现 |
| `RenderCore/Private/ShaderCore.cpp` | Shader 核心实现 |
| `Programs/ShaderCompileWorker/` | 独立编译进程 |
| `Engine/Shaders/Private/` | 引擎 HLSL 源码 |
| `Engine/Shaders/Shared/` | 跨平台共享头文件 |
| `RHI/Public/RHIShaderPlatform.h` | Shader 平台定义 |
