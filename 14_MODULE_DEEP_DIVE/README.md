# 14_MODULE_DEEP_DIVE — 模块深度详解

## 摘要

本目录包含 UE5.7.4 核心/运行时/编辑器模块的深度分析文档。每个模块一篇，统一结构：模块定位、路径、依赖、API、关键类/函数、初始化流程、调用链、扩展点、调试方法、Mermaid 图、源码证据。

---

## 已完成文档

| 模块 | 文档 | 类型 | 主要职责 |
|------|------|------|----------|
| Core | [Core.md](Core.md) | Runtime | 基础容器、数学、平台抽象、多线程 |
| CoreUObject | [CoreUObject.md](CoreUObject.md) | Runtime | UObject、反射、GC、序列化 |
| Engine | [Engine.md](Engine.md) | Runtime | AActor、UWorld、Gameplay Framework |
| Launch | [Launch.md](Launch.md) | Runtime | 引擎入口、主循环 FEngineLoop |
| Projects | [Projects.md](Projects.md) | Runtime | 项目/插件描述文件管理 |
| ApplicationCore | [ApplicationCore.md](ApplicationCore.md) | Runtime | 应用主循环、窗口、输入抽象 |
| Slate | [Slate.md](Slate.md) | Runtime | UI 框架 (C++ 原生) |
| SlateCore | [SlateCore.md](SlateCore.md) | Runtime | Slate 渲染和输入基础 |
| UMG | [UMG.md](UMG.md) | Runtime | Blueprint 可见 UI 组件 |
| InputCore | [InputCore.md](InputCore.md) | Runtime | 输入核心类型 (FKey, EKeys) |
| AssetRegistry | [AssetRegistry.md](AssetRegistry.md) | Runtime | 资产扫描、缓存、查询 |
| RenderCore | [RenderCore.md](RenderCore.md) | Runtime | RDG、Shader 基础、渲染线程 |
| Renderer | [Renderer.md](Renderer.md) | Runtime | 延迟/前向渲染器、Lumen/Nanite/VSM |
| RHI | [RHI.md](RHI.md) | Runtime | GPU 抽象接口 |
| D3D12RHI | [D3D12RHI.md](D3D12RHI.md) | Runtime | DirectX 12 后端 |
| Niagara | [Niagara.md](Niagara.md) | Plugin | VFX 粒子系统 |
| AnimGraphRuntime | [AnimGraphRuntime.md](AnimGraphRuntime.md) | Runtime | 骨骼动画运行时 |
| MovieScene | [MovieScene.md](MovieScene.md) | Runtime | Sequencer 时间轴系统 |
| UnrealEd | [UnrealEd.md](UnrealEd.md) | Editor | 编辑器核心工具 |
| AssetTools | [AssetTools.md](AssetTools.md) | Developer | 资产导入/导出/操作工具 |
| ContentBrowser | [ContentBrowser.md](ContentBrowser.md) | Editor | 内容浏览器 UI |
| PakFile | [PakFile.md](PakFile.md) | Runtime | Pak 文件格式和挂载 |
| HTTP | [HTTP.md](HTTP.md) | Runtime | HTTP 请求/响应 |
| WebSockets | [WebSockets.md](WebSockets.md) | Plugin | WebSocket 连接 |
| Networking | [Networking.md](Networking.md) | Runtime | 网络驱动、Socket |
| PixelStreaming | [PixelStreaming.md](PixelStreaming.md) | Plugin | 像素流送 |

---

## 推荐阅读顺序

1. **Core** → 理解基础类型和平台抽象
2. **CoreUObject** → 理解对象模型和反射
3. **Engine** → 理解 Gameplay Framework
4. **Launch** → 理解引擎启动和主循环
5. **RenderCore** → 理解渲染基础设施
6. **RHI** → 理解 GPU 抽象
7. **Renderer** → 理解完整渲染管线
