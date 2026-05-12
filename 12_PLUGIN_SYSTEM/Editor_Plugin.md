# Editor 插件开发详解

## 摘要
Editor 插件是只在编辑器环境中加载的功能扩展，不会进入 Shipping 构建。`EHostType::Editor` 和 `EHostType::EditorNoCommandlet` 仅在 `TargetType::Editor` 目标中编译。Editor 插件是编辑器扩展（菜单、工具栏、资产操作、Detail 自定义、自定义编辑器）的标准载体。

## 适合解决的问题
- 如何确保插件代码不进入 Shipping 构建？
- Editor 插件和 Runtime 插件的生命周期有何不同？
- 如何在 Editor 中添加菜单和工具栏扩展？
- Editor 和 EditorNoCommandlet 的区别是什么？

## 核心结论
1. `EHostType::Editor` 模块仅在 Editor 目标编译——UBT 为 Game/Server/Client 编译时跳过
2. `EHostType::EditorNoCommandlet` 额外排除 Commandlet 执行环境
3. Editor 插件模块在 `GIsEditor && WITH_EDITOR` 条件下才加载
4. Editor 插件常用于：菜单/Toolbar 扩展、IAssetTypeActions、IDetailCustomization、自定义资产编辑器
5. 常见的编辑器扩展模式：在 `StartupModule()` 注册，在 `ShutdownModule()` 注销

## 源码位置

| 组件 | 路径 | 作用 |
|------|------|------|
| Editor HostType | `Engine/Source/Runtime/Projects/Public/ModuleDescriptor.h:110` | Editor 类型定义 |
| 编译过滤 | `Engine/Source/Runtime/Projects/Private/ModuleDescriptor.cpp:617` | IsCompiledInConfiguration |
| 加载过滤 | `Engine/Source/Runtime/Projects/Private/ModuleDescriptor.cpp:724` | IsLoadedInCurrentConfiguration |

## 1. Editor vs EditorNoCommandlet

```cpp
// ModuleDescriptor.cpp:617-618
case EHostType::Editor:
case EHostType::EditorNoCommandlet:
    return TargetType == EBuildTargetType::Editor;
// 两者都仅在 Editor 目标编译

// ModuleDescriptor.cpp:724-741
case EHostType::Editor:              
    #if WITH_EDITOR
        if(GIsEditor) return true;   // 编辑器环境（含 Commandlet）
    #endif

case EHostType::EditorNoCommandlet:  
    #if WITH_EDITOR
        if(GIsEditor && !IsRunningCommandlet()) return true;  // 非 Commandlet
    #endif
```

| 特性 | Editor | EditorNoCommandlet |
|------|--------|--------------------|
| 编译条件 | TargetType::Editor | TargetType::Editor |
| 加载条件 | `WITH_EDITOR && GIsEditor` | `WITH_EDITOR && GIsEditor && !IsRunningCommandlet()` |
| Commandlet 中加载 | ✅ 是 | ❌ 否 |
| 使用场景 | 在线/离线编辑器工具 | 仅交互式编辑器 UI |

## 2. Editor 插件加载时机

Editor 插件模块遵循标准的 `ELoadingPhase` 加载顺序，但仅在 `WITH_EDITOR` 构建中生效：

```
IPM::LoadModulesForEnabledPlugins(EarliestPossible)   // 非常早
IPM::LoadModulesForEnabledPlugins(PostConfigInit)     // Config 初始化后
IPM::LoadModulesForEnabledPlugins(Default)            // 标准阶段
IPM::LoadModulesForEnabledPlugins(PostEngineInit)     // 引擎初始化后
```

**重要注意事项：**
- `EarliestPossible` 和 `PostConfigInit` 阶段 `GIsEditor` 可能尚未设置
- `ModuleDescriptor.cpp:727-728` 有 `ensure` 检查：Editor 类型不应使用过早的 LoadingPhase

## 3. 编辑器扩展类型

| 扩展类型 | 接口/类 | 注册位置 |
|----------|---------|----------|
| 菜单/Toolbar 扩展 | `FExtender`, `UToolMenus::ExtendMenu()` | StartupModule |
| 资产类型操作 | `IAssetTypeActions` → `IAssetTools::RegisterAssetTypeActions()` | StartupModule |
| Detail 面板定制 | `IDetailCustomization` → `RegisterCustomClassLayout()` | StartupModule |
| 属性类型定制 | `IPropertyTypeCustomization` → `RegisterCustomPropertyTypeLayout()` | StartupModule |
| 自定义资产编辑器 | `FAssetEditorToolkit` 子类 | AssetTypeActions |
| 编辑器模式 | `FEditorModeInfo` 注册 | StartupModule |
| 设置页面 | `UDeveloperSettings` / `ISettingsSection` | Module 中 |
| Blueprint 节点 | `UK2Node` 子类 | 自动发现 |
| ContentBrowser 菜单 | `ContentBrowserMenuExtender` | ContentBrowserModule |

### 典型 StartupModule/ShutdownModule 模式

```cpp
class FMyEditorModule : public IModuleInterface
{
public:
    virtual void StartupModule() override
    {
        // 注册资产类型
        IAssetTools& AssetTools = FModuleManager::LoadModuleChecked<FAssetToolsModule>("AssetTools").Get();
        AssetTools.RegisterAssetTypeActions(MakeShareable(new FMyAssetTypeActions));
        
        // 注册 Detail 自定义
        FPropertyEditorModule& PropertyModule = FModuleManager::LoadModuleChecked<FPropertyEditorModule>("PropertyEditor");
        PropertyModule.RegisterCustomClassLayout("MyClass", ...);
        
        // 扩展菜单
        UToolMenus::RegisterStartupCallback(FSimpleMulticastDelegate::FDelegate::CreateRaw(this, &FMyEditorModule::RegisterMenus));
    }
    
    virtual void ShutdownModule() override
    {
        // 注销所有注册
    }
};
```

## 4. Shipping 排除机制

Editor 插件模块通过两层过滤确保不进 Shipping：

**编译级过滤 (UBT)：**
```cpp
// ModuleDescriptor.cpp:617
case EHostType::Editor:
    return TargetType == EBuildTargetType::Editor;
// Game/Client/Server 目标 → 不编译此模块
```

**运行级过滤 (模块加载器)：**
```cpp
// ModuleDescriptor.cpp:724
#if WITH_EDITOR
    if(GIsEditor) return true;
#endif
// 即使在 Editor 构建中，非编辑器运行时也不加载
```

## 5. Editor 插件示例

### EditorScriptingUtilities

```json
{
    "FileVersion": 3,
    "FriendlyName": "Editor Scripting Utilities",
    "Category": "Scripting",
    "EnabledByDefault": false,
    "Modules": [{
        "Name": "EditorScriptingUtilities",
        "Type": "Editor",
        "LoadingPhase": "Default"
    }]
}
```

- 仅 Editor 目标编译
- 提供编辑器自动化的 Blueprint 函数
- 不在 Shipping 中存在

## 6. 常见误区

| 误区 | 正确理解 |
|------|----------|
| Editor 插件用 Runtime 类型也可以 | Runtime 类型会在 Shipping 编译和加载，Editor 类型被 UBT 过滤 |
| Editor 插件需手动排除 Shipping | Editor 类型和 `UncookedOnly` 类型自动被 UBT 过滤 |
| 所有编辑器扩展都应放在 Editor 插件中 | Runtime 功能 + 编辑器扩展推荐用 Runtime+Editor 双模块模式 |

## 源码证据
- Engine/Source/Runtime/Projects/Public/ModuleDescriptor.h:110-116（Editor HostType 定义）
- Engine/Source/Runtime/Projects/Private/ModuleDescriptor.cpp:617-618（编译过滤）
- Engine/Source/Runtime/Projects/Private/ModuleDescriptor.cpp:724-741（加载过滤）
- Engine/Plugins/Editor/EditorScriptingUtilities/EditorScriptingUtilities.uplugin（示例）

## 相关文档
- [Plugin_Descriptor.md](Plugin_Descriptor.md) — .uplugin 描述文件
- [Runtime_Plugin.md](Runtime_Plugin.md) — Runtime 插件开发
- [../08_EDITOR/AssetTools.md](../08_EDITOR/AssetTools.md) — 资产工具 API
- [../08_EDITOR/DetailsPanel.md](../08_EDITOR/DetailsPanel.md) — 详情面板定制
