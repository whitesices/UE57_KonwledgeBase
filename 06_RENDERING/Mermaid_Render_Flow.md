# UE5.7.4 完整渲染流程 Mermaid 图集

## 摘要

本文档包含 UE5.7.4 渲染管线的所有 Mermaid 可视化图表。

---

## 1. GameThread → RenderThread → RHIThread → GPU

```mermaid
sequenceDiagram
    participant GT as GameThread
    participant RT as RenderThread
    participant RHI as RHIThread
    participant GPU as GPU

    Note over GT,GPU: === 每帧循环 ===

    GT->>GT: 1. World/Actor Tick
    GT->>GT: 2. Component 更新 SceneProxy
    GT->>RT: 3. ENQUEUE_RENDER_COMMAND(BeginFrame)
    RT->>RHI: 4. RHICmdList.BeginFrame()
    RHI->>GPU: 5. GPU BeginFrame

    GT->>GT: 6. PumpMessages (OS 输入)
    GT->>GT: 7. Slate 输入处理
    GT->>GT: 8. GEngine->Tick

    GT->>RT: 9. BeginRenderingViewFamily
    RT->>RT: 10. FSceneRenderer::Render
    RT->>RT: 11. 构建 RDG (Render Graph)

    Note over RT: RDG Passes:
    RT->>RHI: 12a. Z-Prepass
    RHI->>GPU: DrawIndexedPrimitive
    RT->>RHI: 12b. Nanite Pass
    RHI->>GPU: DispatchCompute
    RT->>RHI: 12c. BasePass (GBuffer)
    RHI->>GPU: DrawIndexedPrimitive
    RT->>RHI: 12d. Shadow Maps
    RHI->>GPU: DrawIndexedPrimitive
    RT->>RHI: 12e. Lighting Pass
    RHI->>GPU: DispatchCompute
    RT->>RHI: 12f. Lumen GI
    RHI->>GPU: RayTracing/Compute
    RT->>RHI: 12g. Translucency
    RHI->>GPU: DrawIndexedPrimitive
    RT->>RHI: 12h. PostProcess
    RHI->>GPU: FullScreen Pass

    GT->>RT: 13. EndFrame
    RT->>RHI: 14. SwapChain Present
    RHI->>GPU: 15. Present (VSync)
```

---

## 2. Actor / Component → SceneProxy → FScene

```mermaid
flowchart TD
    subgraph GameThread
        A1[AActor::Tick]
        A2[UPrimitiveComponent::UpdateTransform]
        A3[UPrimitiveComponent::CreateRenderState]
        A4["CreateSceneProxy() → FPrimitiveSceneProxy"]
        A5["ENQUEUE_RENDER_COMMAND(AddPrimitive)"]
    end

    subgraph RenderThread
        B1[FScene::AddPrimitiveSceneInfo_RT]
        B2[添加到 Primitives 数组]
        B3[添加到 Octree]
        B4[注册到 GPU Scene]
    end

    subgraph 渲染时
        C1[FScene::FrustumCull]
        C2[FScene::OcclusionCull]
        C3[生成 FMeshBatch]
        C4[提交 Draw Command]
    end

    A1 --> A2 --> A3 --> A4 --> A5
    A5 --> B1 --> B2 --> B3 --> B4
    B4 --> C1 --> C2 --> C3 --> C4
```

---

## 3. Renderer → RDG → RHI

```mermaid
flowchart LR
    subgraph FSceneRenderer
        A[构建 ViewFamily]
        B[InitViews - 可见性]
    end

    subgraph RDG
        C[CreateTexture - SceneColor]
        D[CreateTexture - Depth]
        E[AddPass - ZPrepass]
        F[AddPass - BasePass]
        G[AddPass - Lighting]
        H[AddPass - PostProcess]
    end

    subgraph RHI
        I[SetGraphicsPipelineState]
        J[SetVertexBuffer]
        K[SetShaderParameters]
        L[DrawIndexedPrimitive]
    end

    subgraph GPU
        M[Vertex Shader]
        N[Pixel Shader]
        O[Compute Shader]
        P[RenderTarget Write]
    end

    A --> B --> C
    C --> D --> E --> F --> G --> H
    H --> I --> J --> K --> L
    L --> M --> N --> P
    L --> O --> P
```

---

## 4. Material → ShaderMap → PipelineState

```mermaid
flowchart TD
    subgraph 材质编辑器
        A[UMaterial / UMaterialInstance]
        B[材质节点图]
    end

    subgraph Shader编译
        C[FMaterial::GetShaderMap]
        D[FMaterialShaderMap::Compile]
        E[生成 HLSL]
        F[ShaderCompileWorker]
        G["DXC → D3D12 Bytecode"]
        H["CrossCompile → Vulkan SPIR-V"]
    end

    subgraph 运行时
        I[FGraphicsPipelineState]
        J[FRHIGraphicsPipelineState]
        K[绑定到 RHI CommandList]
    end

    A --> B --> C
    C --> D --> E --> F
    F --> G
    F --> H
    G --> I
    H --> I
    I --> J --> K
```

---

## 5. RenderTarget → Readback → CPU

```mermaid
flowchart LR
    subgraph GPU
        A[RenderTarget 写入]
        B[CopyToStagingBuffer]
        C[GPU→CPU Fence]
    end

    subgraph CPU
        D[Map Staging Buffer]
        E[读取像素数据]
        F[FImageUtils::ExportRenderTarget]
    end

    A --> B --> C --> D --> E --> F
```

---

## 6. Nanite / Lumen / VSM 在渲染流程中的位置

```mermaid
flowchart TD
    A[FDeferredShadingSceneRenderer::Render] --> B[OnRenderBegin]

    B --> C{启用 Nanite?}
    C -->|是| D[Nanite Visibility Query]
    C -->|否| E[跳过]
    D --> F[更新 Lumen Scene]
    E --> F

    F --> G[BeginInitViews]
    G --> H[RenderPrePass / Z-Prepass]

    H --> I{启用 Nanite?}
    I -->|是| J[RenderNanite - 替代传统 Z-Prepass]
    I -->|否| K[传统 Z-Prepass]

    J --> L[RenderBasePass]
    K --> L

    L --> M[RenderShadowMaps]
    M --> N{启用 VSM?}
    N -->|是| O[Virtual Shadow Map 渲染]
    N -->|否| P[传统 Shadow Map]

    O --> Q[RenderLights]
    P --> Q

    Q --> R{启用 Lumen?}
    R -->|是| S[Lumen GI / Reflection]
    R -->|否| T[SSGI / SSR]

    S --> U[PostProcess]
    T --> U
    U --> V[Present]
```

---

## 7. Mesh Draw Command 生成流程

```mermaid
flowchart TD
    A[FPrimitiveSceneInfo] --> B[FMeshBatch]
    B --> C[FMeshPassProcessor]
    C --> D[FMeshDrawCommand]
    D --> E[排序和合并]
    E --> F[提交到 RHI]

    subgraph FMeshPassProcessor
        C1[DepthPassProcessor]
        C2[BasePassProcessor]
        C3[TranslucencyPassProcessor]
        C4[ShadowPassProcessor]
    end

    C --> C1
    C --> C2
    C --> C3
    C --> C4
```

---

## 8. GPU Scene 数据流

```mermaid
flowchart LR
    subgraph GameThread
        A[Component 数据更新]
    end

    subgraph RenderThread
        B[GPUScene::UpdatePrimitiveData]
        C[上传到 GPU Buffer]
        D[Shader 读取 GPU Scene]
    end

    subgraph GPU
        E[Instance Data Buffer]
        F[Vertex/Pixel Shader 读取]
    end

    A --> B --> C --> D --> E --> F
```

---

## 相关文档

- [Full_Render_Pipeline.md](Full_Render_Pipeline.md) — 完整渲染管线详解
- [RDG.md](RDG.md) — RDG 详解
- [RHI.md](RHI.md) — RHI 详解
- [Nanite.md](Nanite.md) — Nanite 详解
- [Lumen.md](Lumen.md) — Lumen 详解

源码证据：
- Engine/Source/Runtime/Renderer/Private/DeferredShadingRenderer.cpp
- Engine/Source/Runtime/Renderer/Private/SceneRendering.cpp
- Engine/Source/Runtime/RenderCore/Public/RenderGraph.h
