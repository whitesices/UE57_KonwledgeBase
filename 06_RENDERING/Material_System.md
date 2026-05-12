# 材质系统详解

## 摘要

UE5.7.4 材质系统是将材质编辑器中的可视化节点图编译为可执行 GPU Shader 代码的完整管线。它支持从 UMaterial 节点图到 HLSL 的翻译、Shader 排列组合管理、材质实例化和运行时动态参数修改。

**核心源码位置**:
- `Engine/Source/Runtime/Engine/Public/Materials/MaterialInterface.h` — UMaterialInterface 基类
- `Engine/Source/Runtime/Engine/Public/Materials/Material.h` — UMaterial 资产类
- `Engine/Source/Runtime/Engine/Public/Materials/MaterialInstance.h` — UMaterialInstance 实例类
- `Engine/Source/Runtime/Engine/Public/Materials/MaterialInstanceDynamic.h` — UMaterialInstanceDynamic
- `Engine/Source/Runtime/Engine/Private/Materials/HLSLMaterialTranslator.h` — HLSL 翻译器
- `Engine/Source/Runtime/Engine/Public/MaterialDomain.h` — 材质域枚举
- `Engine/Source/Runtime/Engine/Classes/Engine/EngineTypes.h` — 着色模型枚举

---

## 1. 材质类层次

### 1.1 继承关系

```
UObject
└── UMaterialInterface (抽象基类, MaterialInterface.h:101)
    ├── UMaterial (材质资产, 节点图, Material.h)
    │   └── UMaterialInstance (材质实例, 参数覆盖, MaterialInstance.h)
    │       └── UMaterialInstanceDynamic (动态实例, 运行时创建, MaterialInstanceDynamic.h)
    └── UMaterialFunctionInterface (材质函数接口)
```

### 1.2 UMaterialInterface — 抽象基类

源码: `MaterialInterface.h:101`

```cpp
UCLASS(Abstract)
class UMaterialInterface : public UObject, public IBlendableInterface, public IInterface_AssetUserData
{
    // 材质参数访问
    virtual FMaterialRenderProxy* GetRenderProxy() const PURE_VIRTUAL(..., return NULL;);

    // 材质资源
    virtual FMaterialResource* GetMaterialResource(ERHIFeatureLevel::Type FeatureLevel,
        EShaderPlatform ShaderPlatform = SP_NumPlatforms) const;

    // 物理材质
    UPROPERTY()
    UPhysicalMaterial* PhysMaterial;

    // 材质使用标志
    // ...
};
```

UMaterialInterface 定义了所有材质类型的公共接口，包括获取渲染代理、物理材质和材质参数。

### 1.3 材质使用标志 (EMaterialUsage)

源码: `MaterialInterface.h:71-99`

```cpp
UENUM(BlueprintType)
enum EMaterialUsage : int
{
    MATUSAGE_SkeletalMesh,
    MATUSAGE_ParticleSprites,
    MATUSAGE_BeamTrails,
    MATUSAGE_MeshParticles,
    MATUSAGE_StaticLighting,
    MATUSAGE_MorphTargets,
    MATUSAGE_SplineMesh,
    MATUSAGE_InstancedStaticMeshes,
    MATUSAGE_GeometryCollections,
    MATUSAGE_Clothing,
    MATUSAGE_NiagaraSprites,
    MATUSAGE_NiagaraRibbons,
    MATUSAGE_NiagaraMeshParticles,
    MATUSAGE_GeometryCache,
    MATUSAGE_Water,
    MATUSAGE_HairStrands,
    MATUSAGE_LidarPointCloud,
    MATUSAGE_VirtualHeightfieldMesh,
    MATUSAGE_Nanite,
    MATUSAGE_Voxels,
    MATUSAGE_VolumetricCloud,
    MATUSAGE_HeterogeneousVolumes,
    MATUSAGE_StaticMesh,
    MATUSAGE_MAX,
};
```

每种使用场景可能触发不同的 Shader 排列组合编译。

---

## 2. UMaterial — 材质资产

### 2.1 类定义

源码: `Material.h`

```cpp
UCLASS()
class UMaterial : public UMaterialInterface
{
    // 材质节点图相关
    // 着色模型
    // 材质域
    // Blend 模式
    // 编译状态追踪

#if WITH_EDITOR
    // 编辑器相关：节点图、表达式、连接
    FMaterialsWithDirtyUsageFlags DirtyUsageFlags;
#endif
};
```

UMaterial 是在编辑器中创建的材质资产，包含可视化的节点表达式图。

### 2.2 材质表达式

材质节点图由一系列 `UMaterialExpression` 子类组成：

```
UMaterialExpression (基类)
├── UMaterialExpressionConstant          -- 常量
├── UMaterialExpressionConstant2Vector   -- 2D 常量
├── UMaterialExpressionConstant3Vector   -- 3D 常量
├── UMaterialExpressionTextureSample     -- 纹理采样
├── UMaterialExpressionMultiply          -- 乘法
├── UMaterialExpressionAdd               -- 加法
├── UMaterialExpressionLerp              -- 线性插值
├── UMaterialExpressionPower             -- 幂运算
├── UMaterialExpressionClamp             -- 钳制
├── UMaterialExpressionSine              -- 正弦
├── UMaterialExpressionWorldPosition     -- 世界位置
├── UMaterialExpressionNormal            -- 法线
├── UMaterialExpressionCameraVector      -- 相机向量
├── UMaterialExpressionPixelDepth        -- 像素深度
├── UMaterialExpressionTime              -- 时间
├── UMaterialExpressionPanner            -- 平移器
├── UMaterialExpressionCustom            -- 自定义 HLSL 代码
├── UMaterialExpressionMaterialFunctionCall -- 材质函数调用
├── UMaterialExpressionDynamicParameter  -- 动态参数 (MID)
├── UMaterialExpressionCollectionParameter -- 集合参数
├── UMaterialExpressionShadingModel      -- 着色模型选择
└── ... (100+ 种表达式类型)
```

---

## 3. 材质实例系统

### 3.1 UMaterialInstance — 静态实例

源码: `MaterialInstance.h`

```cpp
UCLASS()
class UMaterialInstance : public UMaterialInterface
{
    // 父材质
    UMaterialInterface* Parent;

    // 覆盖的标量参数
    TArray<FScalarParameterValue> ScalarParameterValues;

    // 覆盖的向量参数
    TArray<FVectorParameterValue> VectorParameterValues;

    // 覆盖的纹理参数
    TArray<FTextureParameterValue> TextureParameterValues;

    // 覆盖的颜色参数
    TArray<FColorParameterValue> ColorParameterValues;

    // 覆盖的静态开关参数
    TArray<FStaticSwitchParameter> StaticParameters;

    // 是否覆盖特定属性
    // ...
};
```

材质实例允许在不重新编译 Shader 的情况下覆盖父材质的参数值。静态开关参数的改变会触发重新编译。

### 3.2 UMaterialInstanceDynamic — 动态实例

源码: `MaterialInstanceDynamic.h`

```cpp
UCLASS()
class UMaterialInstanceDynamic : public UMaterialInstance
{
    // 运行时创建
    static UMaterialInstanceDynamic* Create(UMaterialInterface* ParentMaterial);

    // 运行时参数设置
    void SetScalarParameterValue(FName ParameterName, float Value);
    void SetVectorParameterValue(FName ParameterName, FVector Value);
    void SetTextureParameterValue(FName ParameterName, UTexture* Value);
};
```

动态材质实例可以在游戏运行时通过蓝图或 C++ 创建和修改参数。

### 3.3 实例化层次示例

```
UMaterial "M_BaseMetal"
  ├── UMaterialInstance "MI_RustyMetal" (覆盖: Roughness=0.8, BaseColor=锈迹纹理)
  │   └── UMaterialInstanceDynamic (运行时: 覆盖 Emissive 为闪烁效果)
  ├── UMaterialInstance "MI_PolishedChrome" (覆盖: Roughness=0.1, Metalic=1.0)
  └── UMaterialInstance "MI_BrushedMetal" (覆盖: Normal=拉丝法线, Roughness=0.3)
```

---

## 4. 材质域 (EMaterialDomain)

源码: `MaterialDomain.h:12-30`

```cpp
UENUM()
enum EMaterialDomain : int
{
    MD_Surface UMETA(DisplayName = "Surface"),                   // 表面材质（最常见）
    MD_DeferredDecal UMETA(DisplayName = "Deferred Decal"),      // 延迟贴花
    MD_LightFunction UMETA(DisplayName = "Light Function"),      // 光照函数
    MD_Volume UMETA(DisplayName = "Volume"),                     // 体积材质
    MD_PostProcess UMETA(DisplayName = "Post Process"),          // 后处理材质
    MD_UI UMETA(DisplayName = "User Interface"),                 // UI 材质
    MD_RuntimeVirtualTexture UMETA(Hidden),                      // 运行时虚拟纹理（已弃用）
    MD_MAX
};

ENGINE_API FString MaterialDomainString(EMaterialDomain MaterialDomain);
```

| 材质域 | 说明 | 典型用途 |
|--------|------|----------|
| `MD_Surface` | 标准 3D 表面 | 网格体渲染 |
| `MD_DeferredDecal` | 投射到场景表面 | 贴花效果 |
| `MD_LightFunction` | 修改光照分布 | 投影纹理灯光 |
| `MD_Volume` | 体积渲染 | 云、雾、大气 |
| `MD_PostProcess` | 后处理效果 | Bloom、色差、色调映射 |
| `MD_UI` | 界面渲染 | UMG/Slate 材质 |

---

## 5. 着色模型 (EMaterialShadingModel)

源码: `EngineTypes.h:704-725`

```cpp
UENUM()
enum EMaterialShadingModel : int
{
    MSM_Unlit               UMETA(DisplayName="Unlit"),
    MSM_DefaultLit          UMETA(DisplayName="Default Lit"),
    MSM_Subsurface          UMETA(DisplayName="Subsurface"),
    MSM_PreintegratedSkin   UMETA(DisplayName="Preintegrated Skin"),
    MSM_ClearCoat           UMETA(DisplayName="Clear Coat"),
    MSM_SubsurfaceProfile   UMETA(DisplayName="Subsurface Profile"),
    MSM_TwoSidedFoliage     UMETA(DisplayName="Two Sided Foliage"),
    MSM_Hair                UMETA(DisplayName="Hair"),
    MSM_Cloth               UMETA(DisplayName="Cloth"),
    MSM_Eye                 UMETA(DisplayName="Eye"),
    MSM_SingleLayerWater    UMETA(DisplayName="SingleLayerWater"),
    MSM_ThinTranslucent      UMETA(DisplayName="Thin Translucent"),
    MSM_Strata              UMETA(DisplayName="Substrate", Hidden),
    MSM_NUM                 UMETA(Hidden),
    MSM_FromMaterialExpression UMETA(DisplayName="From Material Expression"),
    MSM_MAX
};
```

### 5.1 着色模型字段

源码: `EngineTypes.h:730-759`

```cpp
USTRUCT()
struct FMaterialShadingModelField {
    GENERATED_USTRUCT_BODY()

    void AddShadingModel(EMaterialShadingModel InShadingModel);
    void RemoveShadingModel(EMaterialShadingModel InShadingModel);
    bool HasShadingModel(EMaterialShadingModel InShadingModel) const;
    bool HasOnlyShadingModel(EMaterialShadingModel InShadingModel) const;
    bool IsUnlit() const { return HasShadingModel(MSM_Unlit); }
    bool IsLit() const { return !IsUnlit(); }

private:
    UPROPERTY()
    uint16 ShadingModelField = 0;
};

static_assert(MSM_NUM <= 16, "Do not exceed 16 shading models without expanding...");
```

`FMaterialShadingModelField` 使用位域存储，支持一个材质同时使用多个着色模型（通过 `MSM_FromMaterialExpression`）。

### 5.2 着色模型特性对照

| 模型 | 关键输入通道 | 典型应用 |
|------|-------------|----------|
| `MSM_Unlit` | Emissive Color | UI、特效、光源 |
| `MSM_DefaultLit` | BaseColor + Metal + Rough + Normal | 大多数标准材质 |
| `MSM_Subsurface` | + Subsurface Color | 皮肤、蜡烛、玉石 |
| `MSM_PreintegratedSkin` | 预积分皮肤着色 | 角色皮肤 |
| `MSM_ClearCoat` | + ClearCoat + ClearCoatRough | 车漆、陶瓷 |
| `MSM_TwoSidedFoliage` | 双面次表面 | 树叶、草 |
| `MSM_Hair` | 发丝着色 | 角色头发 |
| `MSM_Cloth` | 布料着色 | 衣物、织物 |
| `MSM_Eye` | 角膜/虹膜/瞳孔 | 角色眼睛 |
| `MSM_SingleLayerWater` | 单层水着色 | 水面 |
| `MSM_ThinTranslucent` | 薄半透明 | 玻璃、薄膜 |

---

## 6. 材质编译流程

### 6.1 编译管线

```
1. 材质节点图 (UMaterial)
   ↓
2. FMaterial::Compile()
   ↓ 遍历所有连接的 MaterialExpression
3. FHLSLMaterialTranslator (节点图 → HLSL)
   ↓ 每个表达式生成对应的 HLSL 代码片段
4. 生成完整 HLSL 文件
   ↓
5. FMaterialShaderMap::Compile()
   ↓ 为每个需要的 Shader Type 编译
6. ShaderCompileWorker 进程
   ↓ 调用 DXC/FXC/Glslang/Metal Compiler
7. 编译后的 Shader 字节码
   ↓
8. 缓存到 DDC
```

### 6.2 FHLSLMaterialTranslator

源码: `HLSLMaterialTranslator.h:237`

```cpp
class FHLSLMaterialTranslator : public FMaterialCompiler
{
    // 将材质表达式翻译为 HLSL 代码
    // 管理代码生成的各个阶段
};
```

翻译器负责将每个 `UMaterialExpression` 节点转换为等效的 HLSL 代码。例如：
- `UMaterialExpressionMultiply` -> `MaterialFloat3 x = A * B;`
- `UMaterialExpressionTextureSample` -> `MaterialFloat4 x = Texture.Sample(Sampler, UV);`
- `UMaterialExpressionAdd` -> `MaterialFloat3 x = A + B;`

### 6.3 材质模板代码

翻译器生成的 HLSL 使用引擎定义的材质模板结构：

```hlsl
// 引擎生成的材质参数结构
struct FMaterialPixelParameters {
    float3 WorldPosition;
    float3 WorldNormal;
    float3 TangentToWorld[3];
    float2 TexCoords[4];
    float3 ViewDir;
    // ... 更多参数
};

// 生成的材质函数
MaterialFloat3 GetBaseColor(FMaterialPixelParameters Params) {
    // 从节点图翻译来的代码
    return Texture1.Sample(Texture1Sampler, Params.TexCoords[0]) * 0.8;
}

float GetRoughness(FMaterialPixelParameters Params) {
    return 0.5;
}
// ... 等等
```

---

## 7. FMaterialRenderProxy — 线程安全的材质代理

### 7.1 类层次

源码: `MaterialRenderProxy.h:101`

```cpp
class FMaterialRenderProxy : public FRenderResource, public FNoncopyable
{
    // 线程安全的材质渲染接口
    // 由渲染线程使用，不依赖游戏线程的 UObject
};

class FColoredMaterialRenderProxy : public FMaterialRenderProxy
{
    // 颜色覆盖代理
};

class FOverrideSelectionColorMaterialRenderProxy : public FMaterialRenderProxy
{
    // 选择颜色覆盖代理
};
```

### 7.2 代理用途

`FMaterialRenderProxy` 是材质在渲染线程中的表示。游戏线程修改材质参数时，通过代理安全地将更新传递到渲染线程。UMaterialInterface 的 `GetRenderProxy()` 方法返回此代理。

---

## 8. 材质编译触发与管理

### 8.1 编译触发条件

| 条件 | 说明 |
|------|------|
| 材质首次使用 | 新材质被应用到网格体 |
| 参数改变 | 静态开关参数变化需要重新编译 |
| 着色模型改变 | 切换着色模型需要新 Shader |
| 使用标志改变 | 新增使用场景（如标记为 "Used with Skeletal Mesh"） |
| 平台变更 | 目标平台不同需要重新编译 |
| 引擎 Shader 更新 | Engine/Shaders 下的文件被修改 |

### 8.2 编译状态

```cpp
// 材质编译可能处于以下状态之一
enum EMaterialCompilationStatus {
    NotCompiled,        // 未编译
    Compiling,          // 正在编译中
    Compiled_Success,   // 编译成功
    Compiled_Failure,   // 编译失败
};
```

### 8.3 异步编译

编辑器中材质修改后异步编译：
1. 修改触发编译请求
2. ShaderCompileWorker 后台编译
3. 编译期间使用默认材质或旧版本
4. 编译完成自动切换到新材质

---

## 9. Blend 模式 (EDecalBlendMode)

源码: `Material.h:72-113`

```cpp
UENUM()
enum EDecalBlendMode : int
{
    DBM_Translucent,                          // 半透明混合
    DBM_Stain,                                // 污渍（调制 BaseColor）
    DBM_Normal,                               // 仅法线混合
    DBM_Emissive,                             // 仅自发光
    DBM_DBuffer_ColorNormalRoughness,         // DBuffer: 颜色+法线+粗糙度
    DBM_DBuffer_Color,                        // DBuffer: 仅颜色
    DBM_DBuffer_ColorNormal,                  // DBuffer: 颜色+法线
    DBM_DBuffer_ColorRoughness,               // DBuffer: 颜色+粗糙度
    DBM_DBuffer_Normal,                       // DBuffer: 仅法线
    DBM_DBuffer_NormalRoughness,              // DBuffer: 法线+粗糙度
    DBM_DBuffer_Roughness,                    // DBuffer: 仅粗糙度
    DBM_DBuffer_Emissive,                     // DBuffer: 自发光
    DBM_DBuffer_AlphaComposite,               // DBuffer: Alpha 合成
    DBM_DBuffer_EmissiveAlphaComposite,       // DBuffer: 自发光 Alpha 合成
    DBM_Volumetric_DistanceFunction,          // 体积距离函数
    DBM_AlphaComposite,                       // Alpha 合成（预乘）
    DBM_AmbientOcclusion,                     // 环境遮蔽
    DBM_MAX,
};
```

### 9.1 材质贴花响应

源码: `Material.h:116-127`

```cpp
UENUM()
enum EMaterialDecalResponse : int
{
    MDR_None,       // 不接收贴花
    MDR_Simple,     // 简单响应
    // ...
};
```

---

## 10. 材质参数系统

### 10.1 参数类型

| 参数类型 | 结构 | 说明 |
|----------|------|------|
| 标量 | `FScalarParameterValue` | float 值 |
| 向量 | `FVectorParameterValue` | FVector/FLinearColor |
| 纹理 | `FTextureParameterValue` | UTexture 引用 |
| 颜色 | `FColorParameterValue` | FColor |
| 静态开关 | `FStaticSwitchParameter` | bool 值（影响排列） |
| 运行时虚拟纹理 | `FRuntimeVirtualTextureParameter` | VTT 参数 |
| 字体 | `FFontParameterValue` | 字体纹理 |
| Lightmass | `FLightmassParameterValue` | 烘焙参数 |

### 10.2 参数传递路径

```
游戏线程: UMaterialInstance::SetParameterValue()
    → FMaterialRenderProxy 更新
        → 渲染线程: FMaterialShader::SetParameters()
            → GPU: Uniform Buffer 更新
                → Shader: 读取参数值
```

---

## 11. 材质与渲染管线交互

### 11.1 渲染 Pass 使用材质

```
延迟渲染管线中材质的使用:

BasePass:
  → FMeshMaterialShader (FBasePassPS)
    → 读取材质参数 → 写入 GBuffer
      → BaseColor, Normal, Roughness, Metal, Emissive, AO, ...

ShadowPass:
  → FMeshMaterialShader (FShadowDepthPS)
    → 读取材质的 Alpha/Opacity → 深度写入

TranslucencyPass:
  → FMeshMaterialShader (FTranslucencyPS)
    → 前向渲染 → 直接计算光照

VelocityPass:
  → FMeshMaterialShader
    → 写入运动矢量
```

### 11.2 GBuffer 写入

材质的着色模型决定了 GBuffer 的编码方式：

```
GBuffer A (R8G8B8A8): BaseColor.r/g/b + SelectiveOutputMask
GBuffer B (R8G8B8A8): Normal.xy + Roughness + ShadingModelID
GBuffer C (R8G8B8A8): Metal + Specular + AO + ...
GBuffer D (R8G8B8A8): CustomData (按 ShadingModel 不同而异)
```

### 11.3 自定义数据

不同着色模型使用 GBuffer D 的方式不同：

| 着色模型 | GBuffer D 用途 |
|----------|----------------|
| Subsurface | 次表面颜色 + 半径 |
| Clear Coat | Clear Coat 值 + 粗糙度 |
| Hair | 切线 + 背光 |
| Cloth | 布料颜色 + 颜色变化 |
| Eye | 角膜/虹膜参数 |
| SingleLayerWater | 水面参数 |

---

## 12. Substrate (原 Strata) 材质系统

### 12.1 新一代材质框架

源码中可见 `MSM_Strata` (Hidden) 和 Substrate 相关类型（`Material.h:28`, `MaterialExpressionSubstrate.h`）。Substrate 是 UE5 的实验性新一代材质框架，使用 BSDF 组合替代固定的着色模型。

### 12.2 Substrate 表达式

源码: `MaterialExpressionSubstrate.h`

```cpp
UCLASS()
class UMaterialExpressionSubstrate : public UMaterialExpression
{
    TEnumAsByte<EMaterialShadingModel> ShadingModelOverride = MSM_DefaultLit;
    // ...
};
```

---

## 13. 材质调试与诊断

### 13.1 视图模式

| 视图模式 | 显示内容 |
|----------|----------|
| Shader Complexity | Shader 指令数/像素 |
| Quad Overdraw | 四边形过度绘制 |
| Shader Complexity 3D | 3D 空间中的复杂度 |
| Material ID | 材质 ID 颜色映射 |
| Base Color | 仅显示 Base Color |
| Roughness | 仅显示粗糙度 |
| Normal | 仅显示法线 |

### 13.2 材质编辑器统计

材质编辑器 "Stats" 标签页显示：
- Shader 指令数 (Pixel/Vertex)
- 纹理采样器数
- 插值器（Varying）数
- 是否有编译错误或警告

### 13.3 控制台命令

| 命令 | 功能 |
|------|------|
| `r.MaterialQualityLevel 0/1/2` | 切换材质质量级别 |
| `r.ForceMaterialQualityLevel` | 强制材质质量 |
| `ShowFlag.MaterialMipProfiles 1` | 显示纹理 MIP 调试覆盖 |
| `r.CompileMaterialsForShaderPipeline` | 控制编译策略 |

---

## 14. 源码证据索引

| 源文件 | 关键内容 |
|--------|----------|
| `Engine/Public/Materials/MaterialInterface.h` | UMaterialInterface 基类 (行 101+)、EMaterialUsage 枚举 |
| `Engine/Public/Materials/Material.h` | UMaterial 资产类、EDecalBlendMode、EMaterialDecalResponse |
| `Engine/Public/Materials/MaterialInstance.h` | UMaterialInstance 静态实例 |
| `Engine/Public/Materials/MaterialInstanceDynamic.h` | UMaterialInstanceDynamic 动态实例 |
| `Engine/Public/Materials/MaterialRenderProxy.h` | FMaterialRenderProxy (行 101+) |
| `Engine/Public/MaterialDomain.h` | EMaterialDomain 材质域枚举 (行 12-30) |
| `Engine/Classes/Engine/EngineTypes.h` | EMaterialShadingModel 着色模型 (行 704-725)、FMaterialShadingModelField (行 730+) |
| `Engine/Private/Materials/HLSLMaterialTranslator.h` | FHLSLMaterialTranslator (行 237) |
| `Engine/Private/Materials/Material.cpp` | 材质编译逻辑实现 |
| `Engine/Public/MaterialShaderType.h` | 材质 Shader 类型系统 |
| `Engine/Public/MaterialShared.h` | 共享材质定义 |
| `Engine/Public/MaterialCompiler.h` | 材质编译器接口 |
| `Engine/Public/Materials/MaterialExpressionSubstrate.h` | Substrate 新材质系统表达式 |
| `RenderCore/Public/Shader.h` | FShader 基类、Shader 类型注册 |
