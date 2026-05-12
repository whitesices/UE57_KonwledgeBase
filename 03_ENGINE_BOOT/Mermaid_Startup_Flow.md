# UE5.7.4 启动流程 Mermaid 图集

## 摘要

本文档包含 UE5.7.4 引擎启动流程的所有 Mermaid 可视化图表。

---

## 1. 引擎启动总流程

```mermaid
flowchart TD
    subgraph 平台入口
        A[WinMain / main] --> B[GuardedMain]
    end

    subgraph PreInit阶段
        B --> C[EnginePreInit]
        C --> D[PreInitPreStartupScreen]
        D --> D1[GLog 初始化]
        D1 --> D2[命令行解析]
        D2 --> D3[AppInit]
        D3 --> D4[配置系统初始化]
        D4 --> D5[LoadCoreModules - CoreUObject]
        D5 --> D6[显示启动画面]
        D6 --> E[PreInitPostStartupScreen]
        E --> E1[初始化 RHI]
        E1 --> E2[LoadPreInitModules]
        E2 --> E3[Engine/Renderer/RenderCore]
        E3 --> E4[InitializeShaderTypes]
        E4 --> E5[LoadStartupModules]
    end

    subgraph Init阶段
        E5 --> F{GIsEditor?}
        F -->|是| G[EditorInit]
        F -->|否| H[EngineInit]
        G --> G1[NewObject UUnrealEdEngine]
        H --> H1[NewObject UGameEngine]
        G1 --> I[GEngine->Init]
        H1 --> I
        I --> I1[OnPostEngineInit 广播]
        I1 --> I2[加载默认地图]
    end

    subgraph 主循环
        I2 --> J[while !IsEngineExitRequested]
        J --> K[EngineTick]
        K --> K1[BeginFrame 渲染命令]
        K1 --> K2[PumpMessages 窗口消息]
        K2 --> K3[Slate 输入处理]
        K3 --> K4[GEngine->Tick]
        K4 --> K5[渲染提交]
        K5 --> J
        J -->|退出| L[EngineExit]
    end
```

---

## 2. 模块加载顺序

```mermaid
flowchart LR
    subgraph PreInitPreStartupScreen
        A[CoreUObject]
    end

    subgraph LoadPreInitModules
        B[Engine] --> C[Renderer]
        C --> D[AnimGraphRuntime]
        D --> E[平台模块]
        E --> F[SlateRHIRenderer]
        F --> G[Landscape]
        G --> G1[RHICore]
        G1 --> H[RenderCore]
        H --> I[TextureCompressor]
    end

    subgraph LoadStartupModules
        J[所有 Startup 模块]
    end

    A --> B
    I --> J
```

---

## 3. GameThread 与 RenderThread 交互

```mermaid
sequenceDiagram
    participant GT as GameThread
    participant RT as RenderThread
    participant RHI as RHIThread
    participant GPU as GPU

    loop 每帧
        GT->>GT: BeginFrame
        GT->>RT: ENQUEUE_RENDER_COMMAND(BeginFrame)
        RT->>RHI: RHICmdList.BeginFrame()
        RHI->>GPU: GPU BeginFrame

        GT->>GT: PumpMessages (窗口消息)
        GT->>GT: Slate 输入处理
        GT->>GT: GEngine->Tick (World/Actor Tick)

        GT->>RT: ENQUEUE_RENDER_COMMAND(渲染命令)
        RT->>RT: FSceneRenderer::Render
        RT->>RT: RDG 构建渲染图
        RT->>RHI: 提交 RDG Pass
        RHI->>GPU: Draw Calls
        GPU-->>RHI: 完成渲染

        GT->>RT: EndFrame
        RT->>RHI: Present
        RHI->>GPU: SwapChain Present
    end
```

---

## 4. 从启动到第一帧渲染

```mermaid
sequenceDiagram
    participant Main as main()
    participant Loop as FEngineLoop
    participant ModMan as ModuleManager
    participant Engine as UEngine
    participant World as UWorld
    participant Renderer as FRendererModule

    Main->>Loop: PreInit()
    Loop->>ModMan: LoadModule("CoreUObject")
    Loop->>ModMan: LoadModule("Engine")
    Loop->>ModMan: LoadModule("Renderer")
    Loop->>ModMan: LoadModule("RenderCore")

    Main->>Loop: Init()
    Loop->>Engine: NewObject<UGameEngine>()
    Loop->>Engine: Init()
    Engine->>World: CreateWorld()
    Engine->>World: InitializeNewWorld()

    Main->>Loop: Tick() [第1帧]
    Loop->>Engine: Tick(DeltaTime)
    Engine->>World: Tick()
    World->>World: Actor Tick
    Loop->>Renderer: BeginRenderingViewFamily
    Renderer->>Renderer: FSceneRenderer::Render
```

---

## 5. 引擎退出流程

```mermaid
flowchart TD
    A[IsEngineExitRequested] --> B[EngineExit]
    B --> C[GEngineLoop.Exit]
    C --> D[清理 EngineService]
    D --> E[清理 TraceService]
    E --> F[清理 SessionService]
    F --> G{GIsEditor?}
    G -->|是| H[EditorExit]
    G -->|否| I[跳过]
    H --> J[AppPreExit]
    I --> J
    J --> K[AppExit]
    K --> K1[清理模块]
    K1 --> K2[清理配置]
    K2 --> K3[清理日志]
    K3 --> K4[清理文件系统]
    K4 --> L[程序退出]
```

---

## 6. UEngine 类型选择

```mermaid
flowchart TD
    A[FEngineLoop::Init] --> B{GIsEditor?}
    B -->|否| C[读取 GameEngine 类名]
    C --> D[StaticLoadClass UGameEngine]
    D --> E["NewObject<UEngine>(EngineClass)"]
    E --> F[GEngine = 新实例]

    B -->|是| G[读取 UnrealEdEngine 类名]
    G --> H[StaticLoadClass UUnrealEdEngine]
    H --> I["NewObject<UUnrealEdEngine>(EngineClass)"]
    I --> J["GEngine = GEditor = GUnrealEd = 新实例"]

    F --> K[GEngine->ParseCommandline]
    J --> K
    K --> L[GEngine->Init]
```

---

## 7. 配置加载时序

```mermaid
sequenceDiagram
    participant EL as FEngineLoop
    participant CF as FConfigCacheIni
    participant FM as IFileManager
    participant FS as 文件系统

    EL->>EL: AppInit()
    EL->>CF: InitializeConfigSystem()
    CF->>FM: 读取 BaseEngine.ini
    FM->>FS: Engine/Config/BaseEngine.ini
    CF->>FM: 读取 DefaultEngine.ini
    FM->>FS: 项目 Config/DefaultEngine.ini
    CF->>FM: 读取平台特定配置
    FM->>FS: Engine/Config/Windows/...

    Note over CF: 合并配置层级

    EL->>EL: ApplyCVarsFromBootHotfix()
    EL->>EL: SetupGVarsFromIni()
```

---

## 相关文档

- [Launch_Flow.md](Launch_Flow.md) — 启动流程详解
- [EngineLoop.md](EngineLoop.md) — FEngineLoop 详解
- [GameInstance_Flow.md](GameInstance_Flow.md) — GameInstance 流程
- [World_Init_Flow.md](World_Init_Flow.md) — World 初始化

源码证据：
- Engine/Source/Runtime/Launch/Private/Launch.cpp
- Engine/Source/Runtime/Launch/Private/LaunchEngineLoop.cpp
