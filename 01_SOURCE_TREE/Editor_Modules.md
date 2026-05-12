# Editor 模块总览

## 摘要

Editor 模块位于 Engine/Source/Editor/，包含约 145 个编辑器专用模块。这些模块仅在编辑器构建中加载。

---

## 按类别分类

### 编辑器核心
- **UnrealEd** — 编辑器核心模块（最大模块，500+ .cpp 文件），包含 AssetActions、Factories、编辑器工具
  - 路径: Engine/Source/Editor/UnrealEd/
  - 关键类: UUnrealEdEngine, UEditorEngine, FAssetEditorManager
- **EditorFramework** — 编辑器框架（视口、模式、工具）
- **MainFrame** — 编辑器主框架（菜单栏、主窗口）
- **LevelEditor** — 关卡编辑器
  - 关键类: SLevelViewport, FLevelEditorModule
- **EditorStyle** — 编辑器样式系统
- **EditorConfig** — 编辑器配置持久化
- **EditorSubsystem** — UEditorSubsystem 基类
- **StatusBar** — 状态栏

### 蓝图编辑器
- **Kismet** — 蓝图编辑器核心（100+ 文件）
  - 关键类: FBlueprintEditor, UBlueprint
- **BlueprintGraph** — 蓝图节点图
- **KismetCompiler** — 蓝图编译器（VM 后端）
- **KismetWidgets** — 蓝图 UI 控件
- **BlueprintEditorLibrary** — 蓝图编辑工具库
- **AnimGraph** — 动画蓝图图编辑器

### 资产编辑器
- **MaterialEditor** — 材质编辑器
- **Persona** — 动画编辑器（含骨骼编辑、蒙太奇编辑）
- **StaticMeshEditor** — 静态网格编辑器
- **SkeletalMeshEditor** — 骨骼网格编辑器
- **SkeletonEditor** — 骨骼编辑器
- **TextureEditor** — 纹理编辑器
- **FontEditor** — 字体编辑器
- **CurveEditor** — 曲线编辑器
- **CurveAssetEditor** — 曲线资产编辑器
- **CurveTableEditor** — 曲线表编辑器
- **DataTableEditor** — 数据表编辑器
- **StringTableEditor** — 字符串表编辑器
- **AudioEditor** — 音频编辑器
- **BehaviorTreeEditor** — 行为树编辑器
- **UMGEditor** — UMG 编辑器（UI 设计器）
- **ConfigEditor** — 配置编辑器
- **PhyaEditor** — 物理动画编辑器

### 图编辑器通用
- **GraphEditor** — 通用图编辑器框架
  - 关键类: SGraphEditor, SGraphPanel
- **AIGraph** — AI 图编辑器

### 属性编辑
- **PropertyEditor** — 属性编辑器（Details Panel 核心，100+ 文件）
  - 关键类: FDetailBuilder, IDetailCustomization
- **DetailCustomizations** — 各类型属性定制（100+ 文件）

### 内容浏览器
- **ContentBrowser** — 内容浏览器核心
- **ContentBrowserData** — 内容浏览器数据层

### Sequencer / 时间轴
- **Sequencer** — Sequencer 编辑器核心
- **SequencerCore** — Sequencer 核心逻辑
- **SequencerWidgets** — Sequencer UI 控件
- **MovieSceneTools** — MovieScene 工具
- **MovieSceneCaptureDialog** — 影片捕获对话框

### 视口与交互
- **ViewportInteraction** — 视口交互（变换 Gizmo）
- **ViewportSnapping** — 视口吸附
- **ComponentVisualizers** — 组件可视化器

### 场景管理
- **SceneOutliner** — 场景大纲
- **Layers** — 层系统
- **WorldBrowser** — World 浏览器
- **WorldPartitionEditor** — World Partition 编辑器
- **HierarchicalLODOutliner** — HLOD 大纲

### 植被与地形
- **FoliageEdit** — 植被编辑
- **LandscapeEditor** — 地形编辑器
- **MeshPaint** — 网格绘制

### 调试工具
- **StatsViewer** — Stats 查看器
- **OutputLog** — 输出日志
- **MessageLog** — 消息日志
- **PixelInspector** — 像素检查器
- **CollisionAnalyzer** — 碰撞分析器
- **GameplayDebugger** — Gameplay 调试器编辑器侧
- **MassEntityDebugger** — Mass Entity 调试器

### 项目管理
- **GameProjectGeneration** — 项目创建和代码生成
- **DeviceProfileEditor** — 设备配置编辑器
- **HardwareTargeting** — 硬件目标设置
- **ProjectSettingsViewer** — 项目设置查看器
- **ProjectTargetPlatformEditor** — 目标平台编辑器

### 源码控制
- **SourceControlWindows** — 源码控制窗口
- **SourceControlWindowExtender** — 源码控制扩展

### 虚拟制片
- **VREditor** — VR 编辑器模式

### 其他
- **AddContentDialog** — 添加内容对话框
- **ClassViewer** — 类查看器
- **StructViewer** — 结构体查看器
- **PlacementMode** — 放置模式
- **AdvancedPreviewScene** — 高级预览场景
- **AnimationModifiers** — 动画修改器
- **Blutility** — 编辑器工具（EditorUtilityWidget）
- **ClothPainter** — 布料绘制
- **ClothingSystemEditor** — 布料系统编辑器
- **MergeActors** — 合并 Actor
- **PinnedCommandList** — 固定命令列表
- **VirtualTexturingEditor** — 虚拟纹理编辑器
- **VirtualizationEditor** — 虚拟化编辑器
- **SparseVolumeTexture** — 稀疏体积纹理
- **NNEEditor** — NNE 神经网络编辑器
- **StructUtilsEditor** — 结构工具编辑器
- **SVGDistanceField** — SVG 距离场
- **DataLayerEditor** — 数据层编辑器
- **LevelInstanceEditor** — Level Instance 编辑器
- **DerivedDataEditor** — DDC 编辑器
- **DerivedDataWidgets** — DDC 控件
- **StorageServerWidgets** — 存储服务器控件
- **WorkspaceMenuStructure** — 工作区菜单结构
- **ToolMenusEditor** — 工具菜单编辑器
- **UserAssetTagsEditor** — 用户资产标签编辑器
- **OverlayEditor** — Overlay 编辑器
- **RewindDebuggerInterface** — 倒回调试器接口
- **UniversalObjectLocatorEditor** — 通用对象定位器编辑器
- **UndoHistoryEditor** — 撤销历史编辑器
- **EnvironmentLightingViewer** — 环境光照查看器
- **CommonMenuExtensions** — 通用菜单扩展
- **ScriptableEditorWidgets** — 可脚本化编辑器控件
- **PIEPreviewDeviceProfileSelector** — PIE 预览设备选择器
- **SubobjectDataInterface** — 子对象数据接口
- **SubobjectEditor** — 子对象编辑器
- **InternationalizationSettings** — 国际化设置
- **LocalizationDashboard** — 本地化面板
- **LocalizationCommandletExecution** — 本地化命令执行
- **SequenceRecorder** — 序列录制器
- **SequenceRecorderSections** — 序列录制器区段
- **CSVtoSVG** — CSV 转 SVG
- **TurnkeySupport** — Turnkey 支持
- **SwarmInterface** — Swarm 接口
- **UATHelper** — UAT 辅助
- **AssetDefinition** — 资产定义
- **AssetTagsEditor** — 资产标签编辑器
- **GameplayTasksEditor** — Gameplay Tasks 编辑器
- **AnimationEditMode** — 动画编辑模式
- **AnimationEditor** — 动画编辑器
- **AnimationEditorWidgets** — 动画编辑器控件
- **AnimationSettings** — 动画设置
- **AnimationBlueprintLibrary** — 动画蓝图库
- **ActorPickerMode** — Actor 选取模式
- **SceneDepthPickerMode** — 场景深度选取模式
- **InputBindingEditor** — 输入绑定编辑器
- **Documentation** — 文档系统
- **PackagesDialog** — 包对话框
- **NewLevelDialog** — 新建关卡对话框
- **DataHierarchyEditor** — 数据层级编辑器
- **ActionableMessage** — 可操作消息
- **EditorWidgets** — 编辑器控件
- **PluginWarden** — 插件授权
- **PListEditor** — PList 编辑器
- **DistCurveEditor** — 分布曲线编辑器
- **DeviceProfileServices** — 设备配置服务
- **EditorToolEvents** — 编辑器工具事件
- **ClothingSystemEditorInterface** — 布料系统编辑器接口
- **DesktopWidgets** — 桌面控件
- **MainFrane** — 主框架
- **GraphColor** — 图着色
- **HierarchicalLODUtilities** — HLOD 工具
- **MassEntityEditor** — Mass Entity 编辑器
- **NewLevelDialog** — 新建关卡对话框
- **ZenEditor** — Zen 编辑器

---

## 源码证据

- Engine/Source/Editor/ 目录扫描
- 各模块 Build.cs 文件
