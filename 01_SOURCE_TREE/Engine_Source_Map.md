# UE5.7.4 引擎源码地图

## 摘要
本文档是一份 UE5.7.4 引擎源码的"地图"，帮助开发者快速定位特定功能对应的源码位置。

## 核心数据结构

### 字符串
- FString: Engine/Source/Runtime/Core/Public/Containers/UnrealString.h
- FName: Engine/Source/Runtime/Core/Public/UObject/NameTypes.h
- FText: Engine/Source/Runtime/Core/Public/Internationalization/Text.h
- FStringView: Engine/Source/Runtime/Core/Public/Containers/StringView.h

### 容器
- TArray: Engine/Source/Runtime/Core/Public/Containers/Array.h
- TMap: Engine/Source/Runtime/Core/Public/Containers/Map.h
- TSet: Engine/Source/Runtime/Core/Public/Containers/Set.h
- TQueue: Engine/Source/Runtime/Core/Public/Containers/Queue.h

### 数学
- FVector: Engine/Source/Runtime/Core/Public/Math/Vector.h
- FRotator: Engine/Source/Runtime/Core/Public/Math/Rotator.h
- FTransform: Engine/Source/Runtime/Core/Public/Math/Transform.h
- FMatrix: Engine/Source/Runtime/Core/Public/Math/Matrix.h
- FQuat: Engine/Source/Runtime/Core/Public/Math/Quat.h

## 核心系统入口

### 引擎启动
- 程序入口: Engine/Source/Runtime/Launch/Private/Launch.cpp (GuardedMain)
- 主循环: Engine/Source/Runtime/Launch/Private/LaunchEngineLoop.cpp (FEngineLoop)
- UEngine 基类: Engine/Source/Runtime/Engine/Private/UnrealEngine.cpp
- UGameEngine: Engine/Source/Runtime/Engine/Private/GameEngine.cpp
- UUnrealEdEngine: Engine/Source/Editor/UnrealEd/Private/UnrealEdEngine.cpp

### 反射系统
- UObject: Engine/Source/Runtime/CoreUObject/Public/UObject/UObject.h
- UClass: Engine/Source/Runtime/CoreUObject/Public/UObject/UClass.h
- UFunction: Engine/Source/Runtime/CoreUObject/Public/UObject/UFunction.h
- UProperty/FProperty: Engine/Source/Runtime/CoreUObject/Public/UObject/UnrealType.h
- 反射生成: Engine/Source/Programs/UnrealHeaderTool/

### 垃圾回收
- GC 入口: Engine/Source/Runtime/CoreUObject/Private/UObject/GarbageCollectionVerification.cpp
- GC 核心: Engine/Source/Runtime/CoreUObject/Private/UObject/GC.cpp
- GC 参考: Engine/Source/Runtime/CoreUObject/Public/UObject/GCObject.h

### 序列化
- FArchive: Engine/Source/Runtime/Core/Public/Serialization/Archive.h
- Package: Engine/Source/Runtime/CoreUObject/Public/UObject/Package.h
- Linker: Engine/Source/Runtime/CoreUObject/Public/UObject/Linker.h

## Gameplay 框架

### World / Level
- UWorld: Engine/Source/Runtime/Engine/Classes/Engine/World.h
- ULevel: Engine/Source/Runtime/Engine/Classes/Engine/Level.h
- UGameInstance: Engine/Source/Runtime/Engine/Classes/Engine/GameInstance.h
- USceneComponent: Engine/Source/Runtime/Engine/Classes/Components/SceneComponent.h

### Actor
- AActor: Engine/Source/Runtime/Engine/Classes/GameFramework/Actor.h
- APawn: Engine/Source/Runtime/Engine/Classes/GameFramework/Pawn.h
- ACharacter: Engine/Source/Runtime/Engine/Classes/GameFramework/Character.h
- AController: Engine/Source/Runtime/Engine/Classes/GameFramework/Controller.h
- APlayerController: Engine/Source/Runtime/Engine/Classes/GameFramework/PlayerController.h
- AGameMode: Engine/Source/Runtime/Engine/Classes/GameFramework/GameModeBase.h
- AGameState: Engine/Source/Runtime/Engine/Classes/GameFramework/GameStateBase.h

### Component
- UActorComponent: Engine/Source/Runtime/Engine/Classes/Components/ActorComponent.h
- UPrimitiveComponent: Engine/Source/Runtime/Engine/Classes/Components/PrimitiveComponent.h
- USkeletalMeshComponent: Engine/Source/Runtime/Engine/Classes/Components/SkeletalMeshComponent.h
- UStaticMeshComponent: Engine/Source/Runtime/Engine/Classes/Components/StaticMeshComponent.h

## 渲染管线

### 渲染入口
- 渲染模块入口: Engine/Source/Runtime/Renderer/Private/RendererModule.cpp
- 视图族渲染: Engine/Source/Runtime/Renderer/Private/SceneRendering.cpp (BeginRenderingViewFamily)
- 延迟着色: Engine/Source/Runtime/Renderer/Private/DeferredShadingRenderer.cpp

### RDG
- Render Graph: Engine/Source/Runtime/RenderCore/Public/RenderGraph.h
- RDG 实现: Engine/Source/Runtime/RenderCore/Private/RenderGraph.cpp

### RHI
- RHI 接口: Engine/Source/Runtime/RHI/Public/RHI.h
- DynamicRHI: Engine/Source/Runtime/RHI/Public/DynamicRHI.h
- D3D12 实现: Engine/Source/Runtime/D3D12RHI/
- Vulkan 实现: Engine/Source/Runtime/VulkanRHI/

### Shader
- FShader 基类: Engine/Source/Runtime/RenderCore/Public/Shader.h
- GlobalShader: Engine/Source/Runtime/RenderCore/Public/GlobalShader.h
- Shader 编译: Engine/Source/Runtime/RenderCore/Private/ShaderCompiler.cpp

### Nanite
- Nanite 核心: Engine/Source/Runtime/Renderer/Private/Nanite/
- Nanite Shader: Engine/Shaders/Private/Nanite/

### Lumen
- Lumen 核心: Engine/Source/Runtime/Renderer/Private/Lumen/

### Virtual Shadow Map
- VSM 核心: Engine/Source/Runtime/Renderer/Private/VirtualShadowMaps/

## UI 系统

### Slate
- Slate 应用: Engine/Source/Runtime/Slate/Public/Framework/Application/SlateApplication.h
- SWidget: Engine/Source/Runtime/SlateCore/Public/Widgets/SWidget.h
- Slate 渲染: Engine/Source/Runtime/SlateRHIRenderer/

### UMG
- UUserWidget: Engine/Source/Runtime/UMG/Classes/UMG.h
- UMG 模块: Engine/Source/Runtime/UMG/

## 网络系统

### 复制
- UNetDriver: Engine/Source/Runtime/Engine/Classes/Engine/NetDriver.h
- UActorChannel: Engine/Source/Runtime/Engine/Classes/Engine/ActorChannel.h
- Iris: Engine/Source/Runtime/Net/Iris/

## 动画系统

### 核心
- USkeleton: Engine/Source/Runtime/Engine/Classes/Animation/Skeleton.h
- UAnimSequence: Engine/Source/Runtime/Engine/Classes/Animation/AnimSequence.h
- UAnimBlueprint: Engine/Source/Runtime/Engine/Classes/Animation/AnimBlueprint.h
- AnimGraph: Engine/Source/Runtime/AnimGraphRuntime/

## 物理系统

### Chaos
- PhysicsCore: Engine/Source/Runtime/PhysicsCore/
- Chaos 物理: Engine/Source/Runtime/Experimental/Chaos/

## 构建系统

### UBT
- UnrealBuildTool: Engine/Source/Programs/UnrealBuildTool/

### UHT
- UnrealHeaderTool: Engine/Source/Programs/UnrealHeaderTool/

## 资源系统

### Asset
- AssetRegistry: Engine/Source/Runtime/AssetRegistry/
- PakFile: Engine/Source/Runtime/PakFile/
- IOStore: Engine/Source/Runtime/Experimental/IO/

## 调试工具

### 日志
- FOutputDevice: Engine/Source/Runtime/Core/Public/Misc/OutputDevice.h
- UE_LOG: Engine/Source/Runtime/Core/Public/Logging/LogMacros.h

### Stats
- Stats 系统: Engine/Source/Runtime/Core/Public/Stats/Stats.h

### Unreal Insights
- Trace: Engine/Source/Runtime/TraceLog/
- Insights: Engine/Source/Developer/TraceInsights/

## 按问题定位源码

| 我想了解... | 应该查看 |
|------------|---------|
| 引擎如何启动 | Launch.cpp → LaunchEngineLoop.cpp |
| Actor 如何 Tick | UnrealEngine.cpp → FTickTaskManagerInterface |
| 渲染一帧做了什么 | DeferredShadingRenderer.cpp::Render() |
| 材质如何编译成 Shader | MaterialShader.cpp, ShaderCompiler.cpp |
| UObject 如何创建 | UObjectBaseUtility.cpp, StaticAllocateObject |
| GC 如何工作 | GC.cpp, GarbageCollectionVerification.cpp |
| 网络如何同步 | NetDriver.cpp, ActorChannel.cpp, DataChannel.cpp |
| 如何打包 Pak | UnrealPak 程序, PakFileUtilities 模块 |
| 如何加载资源 | LinkerLoad.cpp, Package.cpp |
| 输入事件如何流转 | SlateApplication.cpp, PlayerController.cpp |
