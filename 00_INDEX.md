# UE5.7.4 源码知识树

## 摘要

本文档是 UE5.7.4 源码知识库的全局索引和学习路线图。

---

## 源码学习路线

```
入门 → 00_VERSION_CHECK.md → 01_SOURCE_TREE/ → 03_ENGINE_BOOT/
进阶 → 04_CORE_OBJECT_SYSTEM/ → 02_BUILD_SYSTEM/ → 05_GAMEPLAY_FRAMEWORK/
高级 → 06_RENDERING/ → 14_MODULE_DEEP_DIVE/ → 07_ASSET_PIPELINE/
专家 → 08_EDITOR/ → 12_PLUGIN_SYSTEM/ → 10_NETWORKING/ → 09_ANIMATION/
```

## 从启动到渲染的主流程

```
GuardedMain → FEngineLoop::PreInit → LoadModules → FEngineLoop::Init → GEngine->Init
→ 主循环: FEngineLoop::Tick → GEngine->Tick → World Tick → Actor Tick
→ BeginRenderingViewFamily → FSceneRenderer::Render → RDG Passes → RHI → GPU → Present
```

## 核心流程索引

| 流程 | 入口文档 |
|------|---------|
| 启动流程 | [03_ENGINE_BOOT/Launch_Flow.md](03_ENGINE_BOOT/Launch_Flow.md) |
| 渲染管线 | [06_RENDERING/Full_Render_Pipeline.md](06_RENDERING/Full_Render_Pipeline.md) |
| UObject 反射 | [04_CORE_OBJECT_SYSTEM/UObject.md](04_CORE_OBJECT_SYSTEM/UObject.md) |
| Build 系统 | [02_BUILD_SYSTEM/UBT.md](02_BUILD_SYSTEM/UBT.md) |
| 资源加载 | [07_ASSET_PIPELINE/AssetRegistry.md](07_ASSET_PIPELINE/AssetRegistry.md) |
| Gameplay 框架 | [05_GAMEPLAY_FRAMEWORK/Actor.md](05_GAMEPLAY_FRAMEWORK/Actor.md) |
| 网络复制 | [10_NETWORKING/Replication.md](10_NETWORKING/Replication.md) |
| UI 系统 | [11_UI/Slate.md](11_UI/Slate.md) |
| 动画系统 | [09_ANIMATION/SkeletalMesh.md](09_ANIMATION/SkeletalMesh.md) |
| 插件开发 | [12_PLUGIN_SYSTEM/Plugin_Descriptor.md](12_PLUGIN_SYSTEM/Plugin_Descriptor.md) |

## 常见问题快速入口

| 问题 | 查看文档 |
|------|---------|
| UE 启动流程怎么看？ | [03_ENGINE_BOOT/Launch_Flow.md](03_ENGINE_BOOT/Launch_Flow.md) |
| RenderTarget 如何 ReadPixels？ | [06_RENDERING/RenderTarget_Readback.md](06_RENDERING/RenderTarget_Readback.md) |
| 插件打包缺 DLL？ | [12_PLUGIN_SYSTEM/Packaging.md](12_PLUGIN_SYSTEM/Packaging.md) |
| UObject 反射和 GC？ | [04_CORE_OBJECT_SYSTEM/GC.md](04_CORE_OBJECT_SYSTEM/GC.md) |
| GameThread 到 RenderThread？ | [06_RENDERING/Full_Render_Pipeline.md](06_RENDERING/Full_Render_Pipeline.md) |
| Build 报 LNK2019？ | [02_BUILD_SYSTEM/Common_Build_Errors.md](02_BUILD_SYSTEM/Common_Build_Errors.md) |
| 如何开发编辑器插件？ | [08_EDITOR/Editor_Startup.md](08_EDITOR/Editor_Startup.md) |
| Pak 热更新怎么做？ | [07_ASSET_PIPELINE/Hot_Update.md](07_ASSET_PIPELINE/Hot_Update.md) |

## 文档目录总表

- [00_VERSION_CHECK.md](00_VERSION_CHECK.md) — 版本确认
- [SCAN_RULES.md](SCAN_RULES.md) — 扫描规则
- [01_SOURCE_TREE/](01_SOURCE_TREE/README.md) — 源码目录总览
- [02_BUILD_SYSTEM/](02_BUILD_SYSTEM/README.md) — Build 系统
- [03_ENGINE_BOOT/](03_ENGINE_BOOT/Launch_Flow.md) — 引擎启动
- [04_CORE_OBJECT_SYSTEM/](04_CORE_OBJECT_SYSTEM/UObject.md) — UObject 系统
- [05_GAMEPLAY_FRAMEWORK/](05_GAMEPLAY_FRAMEWORK/Actor.md) — Gameplay 框架
- [06_RENDERING/](06_RENDERING/Full_Render_Pipeline.md) — 渲染管线
- [07_ASSET_PIPELINE/](07_ASSET_PIPELINE/AssetRegistry.md) — 资源管线
- [08_EDITOR/](08_EDITOR/README.md) — 编辑器架构
- [09_ANIMATION/](09_ANIMATION/README.md) — 动画系统
- [10_NETWORKING/](10_NETWORKING/README.md) — 网络系统
- [11_UI/](11_UI/README.md) — UI 系统
- [12_PLUGIN_SYSTEM/](12_PLUGIN_SYSTEM/README.md) — 插件系统
- [13_DEBUGGING/](13_DEBUGGING/README.md) — 调试工具
- [14_MODULE_DEEP_DIVE/](14_MODULE_DEEP_DIVE/README.md) — 模块深挖
- [15_AGENT_INDEX/](15_AGENT_INDEX/README.md) — Agent 索引
