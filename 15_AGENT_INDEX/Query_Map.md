# UE5.7.4 问题查询地图

## 摘要

本文档为 Agent（Claude Code / Codex）提供快速查询入口，按问题类型映射到具体的知识库文档和源码路径。

---

## 如果用户问：UE 启动流程怎么看？

优先阅读：
- [03_ENGINE_BOOT/Launch_Flow.md](03_ENGINE_BOOT/Launch_Flow.md) — 完整启动流程
- [03_ENGINE_BOOT/EngineLoop.md](03_ENGINE_BOOT/EngineLoop.md) — FEngineLoop 详解
- [03_ENGINE_BOOT/Mermaid_Startup_Flow.md](03_ENGINE_BOOT/Mermaid_Startup_Flow.md) — Mermaid 图集

关键源码：
- Engine/Source/Runtime/Launch/Private/Launch.cpp
- Engine/Source/Runtime/Launch/Private/LaunchEngineLoop.cpp

---

## 如果用户问：RenderTarget 如何 ReadPixels？

优先阅读：
- [06_RENDERING/RenderTarget_Readback.md](06_RENDERING/RenderTarget_Readback.md)
- [06_RENDERING/Full_Render_Pipeline.md](06_RENDERING/Full_Render_Pipeline.md)

关键源码：
- Engine/Source/Runtime/Renderer/Private/
- Engine/Source/Runtime/RenderCore/Public/
- Engine/Source/Runtime/RHI/Public/

---

## 如果用户问：插件打包缺 DLL？

优先阅读：
- [12_PLUGIN_SYSTEM/ThirdParty_Libraries.md](12_PLUGIN_SYSTEM/ThirdParty_Libraries.md)
- [12_PLUGIN_SYSTEM/Packaging.md](12_PLUGIN_SYSTEM/Packaging.md)
- [02_BUILD_SYSTEM/BuildCs_Guide.md](02_BUILD_SYSTEM/BuildCs_Guide.md)

关键源码：
- Engine/Source/Developer/DesktopPlatform/
- .uplugin 文件中的 PlatformAllowList

---

## 如果用户问：UObject 反射和 GC？

优先阅读：
- [04_CORE_OBJECT_SYSTEM/UObject.md](04_CORE_OBJECT_SYSTEM/UObject.md)
- [04_CORE_OBJECT_SYSTEM/UClass_Reflection.md](04_CORE_OBJECT_SYSTEM/UClass_Reflection.md)
- [04_CORE_OBJECT_SYSTEM/GC.md](04_CORE_OBJECT_SYSTEM/GC.md)

关键源码：
- Engine/Source/Runtime/CoreUObject/Public/UObject/
- Engine/Source/Runtime/CoreUObject/Private/UObject/

---

## 如果用户问：GameThread 到 RenderThread？

优先阅读：
- [06_RENDERING/GameThread_To_RenderThread.md](06_RENDERING/GameThread_To_RenderThread.md)
- [06_RENDERING/Full_Render_Pipeline.md](06_RENDERING/Full_Render_Pipeline.md)
- [06_RENDERING/Mermaid_Render_Flow.md](06_RENDERING/Mermaid_Render_Flow.md)

关键源码：
- Engine/Source/Runtime/Renderer/Private/SceneRendering.cpp
- Engine/Source/Runtime/RenderCore/Public/RenderingThread.h

---

## 如果用户问：Build 报 LNK2019？

优先阅读：
- [02_BUILD_SYSTEM/Common_Build_Errors.md](02_BUILD_SYSTEM/Common_Build_Errors.md)
- [02_BUILD_SYSTEM/ModuleRules.md](02_BUILD_SYSTEM/ModuleRules.md)

排查步骤：
1. 检查 Build.cs 中的 PublicDependencyModuleNames
2. 检查是否有 .generated.h 未生成（运行 UHT）
3. 检查模块的 Public/Private 头文件路径

---

## 如果用户问：如何开发编辑器插件？

优先阅读：
- [08_EDITOR/Editor_Startup.md](08_EDITOR/Editor_Startup.md)
- [12_PLUGIN_SYSTEM/Plugin_Descriptor.md](12_PLUGIN_SYSTEM/Plugin_Descriptor.md)
- [12_PLUGIN_SYSTEM/Editor_Plugin.md](12_PLUGIN_SYSTEM/Editor_Plugin.md)

关键源码：
- Engine/Source/Editor/UnrealEd/
- Engine/Source/Editor/PropertyEditor/

---

## 如果用户问：Pak 热更新怎么做？

优先阅读：
- [07_ASSET_PIPELINE/Hot_Update.md](07_ASSET_PIPELINE/Hot_Update.md)
- [07_ASSET_PIPELINE/Pak.md](07_ASSET_PIPELINE/Pak.md)
- [07_ASSET_PIPELINE/IOStore.md](07_ASSET_PIPELINE/IOStore.md)

关键源码：
- Engine/Source/Runtime/PakFile/
- Engine/Source/Programs/UnrealPak/

---

## 如果用户问：动画蓝图如何执行？

优先阅读：
- [09_ANIMATION/AnimBlueprint.md](09_ANIMATION/AnimBlueprint.md)
- [09_ANIMATION/AnimGraph.md](09_ANIMATION/AnimGraph.md)
- [09_ANIMATION/RootMotion.md](09_ANIMATION/RootMotion.md)

关键源码：
- Engine/Source/Runtime/AnimGraphRuntime/
- Engine/Source/Editor/AnimGraph/

---

## 如果用户问：网络复制原理？

优先阅读：
- [10_NETWORKING/Replication.md](10_NETWORKING/Replication.md)
- [10_NETWORKING/RPC.md](10_NETWORKING/RPC.md)
- [10_NETWORKING/NetDriver.md](10_NETWORKING/NetDriver.md)

关键源码：
- Engine/Source/Runtime/Net/
- Engine/Source/Runtime/Engine/Private/PackageMapClient.cpp

---

## 如果用户问：Slate UI 如何自定义？

优先阅读：
- [11_UI/Slate.md](11_UI/Slate.md)
- [11_UI/UMG.md](11_UI/UMG.md)
- [11_UI/Input_Flow.md](11_UI/Input_Flow.md)

关键源码：
- Engine/Source/Runtime/Slate/
- Engine/Source/Runtime/SlateCore/

---

## 如果用户问：Nanite 渲染原理？

优先阅读：
- [06_RENDERING/Nanite.md](06_RENDERING/Nanite.md)
- [06_RENDERING/Full_Render_Pipeline.md](06_RENDERING/Full_Render_Pipeline.md)

关键源码：
- Engine/Source/Runtime/Renderer/Private/Nanite/
- Engine/Shaders/Private/Nanite/

---

## 如果用户问：Lumen GI 原理？

优先阅读：
- [06_RENDERING/Lumen.md](06_RENDERING/Lumen.md)
- [06_RENDERING/Full_Render_Pipeline.md](06_RENDERING/Full_Render_Pipeline.md)

关键源码：
- Engine/Source/Runtime/Renderer/Private/Lumen/

---

## 如果用户问：模块加载顺序？

优先阅读：
- [03_ENGINE_BOOT/Launch_Flow.md](03_ENGINE_BOOT/Launch_Flow.md)（LoadPreInitModules 小节）
- [02_BUILD_SYSTEM/ModuleRules.md](02_BUILD_SYSTEM/ModuleRules.md)

关键源码：
- Engine/Source/Runtime/Launch/Private/LaunchEngineLoop.cpp:4379

---

## 如果用户问：UHT 反射代码是如何生成的？

优先阅读：
- [02_BUILD_SYSTEM/UHT.md](02_BUILD_SYSTEM/UHT.md) — UHT 完整流程、宏解析、代码生成

关键源码：
- Engine/Source/Programs/UnrealBuildTool/Modes/UnrealHeaderToolMode.cs
- Engine/Source/Programs/Shared/EpicGames.UHT/Exporters/CodeGen/

---

## 如果用户问：PublicDependency 和 PrivateDependency 区别？

优先阅读：
- [02_BUILD_SYSTEM/ModuleRules.md](02_BUILD_SYSTEM/ModuleRules.md) — 依赖属性对比表
- [02_BUILD_SYSTEM/BuildCs_Guide.md](02_BUILD_SYSTEM/BuildCs_Guide.md) — 依赖选择决策树

---

## 如果用户问：Target.cs 和 Build.cs 的关系？

优先阅读：
- [02_BUILD_SYSTEM/TargetRules.md](02_BUILD_SYSTEM/TargetRules.md) — TargetRules→ModuleRules 传递机制
- [02_BUILD_SYSTEM/BuildCs_Guide.md](02_BUILD_SYSTEM/BuildCs_Guide.md) — 编写模板

---

## 如果用户问：UHT 报 Unknown specifier？

优先阅读：
- [02_BUILD_SYSTEM/Common_Build_Errors.md](02_BUILD_SYSTEM/Common_Build_Errors.md) — UHT 错误排查
- [02_BUILD_SYSTEM/UHT.md](02_BUILD_SYSTEM/UHT.md) — UHT 宏解析系统

---

## 如果用户问：循环依赖怎么打破？

优先阅读：
- [02_BUILD_SYSTEM/Common_Build_Errors.md](02_BUILD_SYSTEM/Common_Build_Errors.md) — 循环依赖修复
- [02_BUILD_SYSTEM/BuildCs_Guide.md](02_BUILD_SYSTEM/BuildCs_Guide.md) — 打破循环依赖方案

---

## 如果用户问：如何集成第三方库？

优先阅读：
- [02_BUILD_SYSTEM/BuildCs_Guide.md](02_BUILD_SYSTEM/BuildCs_Guide.md) — 第三方库集成模式
- [02_BUILD_SYSTEM/ModuleRules.md](02_BUILD_SYSTEM/ModuleRules.md) — 库链接属性

---

## 如果用户问：RDG 是什么？

优先阅读：
- [06_RENDERING/RDG.md](06_RENDERING/RDG.md)
- [06_RENDERING/Full_Render_Pipeline.md](06_RENDERING/Full_Render_Pipeline.md)

关键源码：
- Engine/Source/Runtime/RenderCore/Public/RenderGraph.h

---

## 如果用户问：Lumen GI 如何工作？

优先阅读：
- [06_RENDERING/Lumen.md](06_RENDERING/Lumen.md)
- [06_RENDERING/Full_Render_Pipeline.md](06_RENDERING/Full_Render_Pipeline.md)

关键源码：
- Engine/Source/Runtime/Renderer/Private/Lumen/Lumen.h
- Engine/Source/Runtime/Renderer/Private/Lumen/LumenSceneData.h
- Engine/Source/Runtime/Renderer/Private/Lumen/LumenSceneRendering.cpp

---

## 如果用户问：Virtual Shadow Map 如何工作？

优先阅读：
- [06_RENDERING/Virtual_Shadow_Map.md](06_RENDERING/Virtual_Shadow_Map.md)

关键源码：
- Engine/Source/Runtime/Renderer/Private/VirtualShadowMaps/VirtualShadowMapArray.h
- Engine/Source/Runtime/Renderer/Private/VirtualShadowMaps/VirtualShadowMapCacheManager.h

---

## 如果用户问：延迟渲染 vs 前向渲染？

优先阅读：
- [06_RENDERING/Deferred_Rendering.md](06_RENDERING/Deferred_Rendering.md)
- [06_RENDERING/Forward_Rendering.md](06_RENDERING/Forward_Rendering.md)

关键源码：
- Engine/Source/Runtime/Renderer/Private/DeferredShadingRenderer.cpp
- Engine/Source/Runtime/Renderer/Private/MobileShadingRenderer.cpp

---

## 如果用户问：SceneProxy 是什么？

优先阅读：
- [06_RENDERING/SceneProxy.md](06_RENDERING/SceneProxy.md)
- [06_RENDERING/GameThread_To_RenderThread.md](06_RENDERING/GameThread_To_RenderThread.md)

关键源码：
- Engine/Source/Runtime/Engine/Public/PrimitiveSceneProxy.h
- Engine/Source/Runtime/Renderer/Private/PrimitiveSceneInfo.cpp

---

## 如果用户问：GameThread 和 RenderThread 如何通信？

优先阅读：
- [06_RENDERING/GameThread_To_RenderThread.md](06_RENDERING/GameThread_To_RenderThread.md)

关键源码：
- Engine/Source/Runtime/RenderCore/Private/RenderingThread.cpp
- Engine/Source/Runtime/RenderCore/Public/RenderCommandFence.h

---

## 如果用户问：GPU 回读性能问题？

优先阅读：
- [06_RENDERING/RenderTarget_Readback.md](06_RENDERING/RenderTarget_Readback.md)

关键源码：
- Engine/Source/Runtime/Engine/Private/UnrealClient.cpp
- Engine/Source/Runtime/RHI/Public/RHICommandList.h

---

## 如果用户问：Renderer 模块整体结构？

优先阅读：
- [06_RENDERING/Renderer_Module.md](06_RENDERING/Renderer_Module.md)

关键源码：
- Engine/Source/Runtime/Renderer/Private/Renderer.cpp
- Engine/Source/Runtime/Renderer/Renderer.Build.cs
