# 插件系统总览

## 摘要
UE5.7.4 插件系统通过 `.uplugin` JSON 描述文件定义插件的元数据、模块列表、依赖关系和内容目录。`IPluginManager` 负责发现、启用、加载插件模块，支持 Engine/Project/Mod/External 四种插件来源。模块通过 `EHostType`（Runtime/Editor/DeveloperTool 等）和 `ELoadingPhase`（14 个阶段）控制编译目标和加载时机。

## 核心流程

```
DiscoverAllPlugins() → Parse .uplugin files
  → ConfigureEnabledPlugins() (过滤启用)
    → ProcessEnabledPlugins() (加载 Config)
      → MountContentPlugins() (挂载 Content)
        → LoadModulesForEnabledPlugins() (按 Phase 加载模块)
```

## 插件目录结构

```
MyPlugin/
├── MyPlugin.uplugin          ← 描述文件 (JSON)
├── Resources/                ← 图标等资源
│   └── Icon128.png
├── Content/                  ← 资产内容 (bCanContainContent=true)
├── Config/                   ← INI 配置
└── Source/
    ├── MyPlugin/             ← Runtime 模块
    │   ├── MyPlugin.Build.cs
    │   ├── Public/
    │   └── Private/
    └── MyPluginEditor/       ← Editor 模块
        ├── MyPluginEditor.Build.cs
        ├── Public/
        └── Private/
```

## 文档索引

| 文档 | 内容 |
|------|------|
| [Plugin_Descriptor.md](Plugin_Descriptor.md) | .uplugin 描述符 — FPluginDescriptor 全部 30+ 字段, FModuleDescriptor, ELoadingPhase, FileVersion |
| [Runtime_Plugin.md](Runtime_Plugin.md) | Runtime 插件 — EHostType::Runtime, 生命周期, 打包行为, CanContainContent |
| [Editor_Plugin.md](Editor_Plugin.md) | Editor 插件 — Editor vs EditorNoCommandlet, 加载时机, Shipping 排除, 编辑器扩展点 |
| [ThirdParty_Libraries.md](ThirdParty_Libraries.md) | 第三方库集成 — ModuleType.External, 目录约定, 动/静态库, libcurl/OpenSSL/Oodle 示例 |
| [Packaging.md](Packaging.md) | 插件打包 — PlatformDenyList, TargetAllowList, 模块过滤, Content 打包, DLL 分发 |

## EHostType 速查

| 类型 | 编译目标 | Shipping |
|------|----------|----------|
| `Runtime` | 所有非 Program 目标 | ✅ |
| `RuntimeNoCommandlet` | 非 Program, 非 Commandlet | ✅ |
| `CookedOnly` | 仅 Cooked 构建 | ✅ |
| `UncookedOnly` | 仅非 Cooked (Editor) | ❌ |
| `Editor` | 仅 Editor 目标 | ❌ |
| `EditorNoCommandlet` | Editor 非 Commandlet | ❌ |
| `DeveloperTool` | bBuildDeveloperTools=true | ❌ |
| `Program` | 仅 Program 目标 | ❌ |
| `ServerOnly` | 非 Client/Program | ✅ |
| `ClientOnly` | 非 Server/Program | ✅ |

## ELoadingPhase 加载阶段

| 阶段 | 时机 |
|------|------|
| `EarliestPossible` | 最早（PlatformFile 之后） |
| `PostConfigInit` | 配置系统初始化后 |
| `PostSplashScreen` | 闪屏显示后 |
| `PreEarlyLoadingScreen` | 早期加载屏幕前 |
| `PreLoadingScreen` | 加载屏幕触发前 |
| `PreDefault` | 默认阶段之前 |
| `Default` | **标准加载阶段** |
| `PostDefault` | 默认阶段之后 |
| `PostEngineInit` | 引擎完全初始化后 |
| `None` | 不自动加载（手动） |

## 源码路径
- Engine/Source/Runtime/Projects/ — IPluginManager, FPluginDescriptor, FModuleDescriptor
- Engine/Source/Programs/UnrealBuildTool/ — ModuleRules, Plugins.cs 编译过滤
- Engine/Plugins/ — 500+ 内置插件示例
