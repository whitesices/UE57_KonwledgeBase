# Editor 架构总览

## 摘要
UE5.7.4 编辑器是一个模块化的桌面应用程序，基于 UEditorEngine (继承 UEngine) 构建。编辑器启动经历 PreInit → Init → Start 三阶段，加载 50+ 个编辑器模块，通过 UToolMenus 系统提供可扩展的菜单和工具栏，使用 AssetTools/ContentBrowser/PropertyEditor 等子系统提供完整的资源编辑体验。

## 核心模块

| 模块 | 路径 | 职责 |
|------|------|------|
| UnrealEd | `Engine/Source/Editor/UnrealEd/` | 编辑器核心引擎 (UEditorEngine, UUnrealEdEngine) |
| AssetTools | `Engine/Source/Developer/AssetTools/` | 资产操作 API (创建/导入/重命名/复制) |
| ContentBrowser | `Engine/Source/Editor/ContentBrowser/` | 内容浏览器 |
| PropertyEditor | `Engine/Source/Editor/PropertyEditor/` | Details Panel + 属性自定义 |
| Kismet | `Engine/Source/Editor/Kismet/` | Blueprint 编辑器 |
| BlueprintGraph | `Engine/Source/Editor/BlueprintGraph/` | Blueprint 节点类型 |
| KismetCompiler | `Engine/Source/Editor/KismetCompiler/` | Blueprint 编译器 |
| GraphEditor | `Engine/Source/Editor/GraphEditor/` | 通用图编辑器 |
| LevelEditor | `Engine/Source/Editor/LevelEditor/` | 关卡编辑器 |
| MainFrame | `Engine/Source/Developer/MainFrame/` | 主窗口框架 |

## 编辑器启动流程

```
Launch.cpp:GuardedMain()
  → EnginePreInit()     // FEngineLoop::PreInit()
  → EditorInit()        // UUnrealEdEngine::Init()
    → UEditorEngine::InitEditor()
      → UEngine::Init()  // 引擎基础初始化
      → LoadDefaultEditorModules()  // ~50+ 模块
    → UUnrealEdEngine::Init()
      → CookServer 初始化
      → DetailCustomizations 注册
  → Main Loop: EngineTick()
  → EditorExit()
```

## 文档索引

| 文档 | 内容 |
|------|------|
| [Editor_Startup.md](Editor_Startup.md) | 编辑器启动流程 — UEditorEngine::Init(), 模块加载时序, FEditorModeTools |
| [AssetTools.md](AssetTools.md) | 资产工具 — IAssetTools, 资产创建/导入/重命名, IAssetTypeActions 注册 |
| [ContentBrowser.md](ContentBrowser.md) | 内容浏览器 — FContentBrowserSingleton, SPathView/SAssetView, 上下文菜单 |
| [DetailsPanel.md](DetailsPanel.md) | 详情面板 — IDetailsView, IPropertyHandle, IDetailCustomization, IPropertyTypeCustomization |
| [BlueprintEditor.md](BlueprintEditor.md) | Blueprint 编辑器 — FBlueprintEditor, UEdGraph/K2Node, 编译管线, 调试 |
| [Commandlet.md](Commandlet.md) | Commandlet 系统 — UCommandlet 基类, 命令行执行, 内置 Commandlet |
