# Developer 模块总览

## 摘要

Developer 模块位于 `Engine/Source/Developer/`，包含约 120 个开发时使用的模块。这些模块在 Development 和 Debug 构建中可用，但**不会打包到 Shipping 构建中**。它们为编辑器、构建管线、调试工具、测试框架和平台部署提供核心支撑功能。

Developer 模块与 Runtime 模块的关键区别：
- **Runtime 模块**：在所有构建配置中都会被编译和链接，包括 Shipping
- **Developer 模块**：仅在 Development/Debug 构建中可用，Shipping 构建时自动排除
- **Editor 模块**：仅在编辑器构建中可用

---

## 模块分类

### 构建与打包

本类模块负责资源编译、格式转换、缓存管理和打包输出。

| 模块名 | 说明 |
|--------|------|
| DerivedDataCache | DDC（Derived Data Cache）缓存系统，缓存编译后的派生数据以加速后续构建 |
| PakFileUtilities | Pak 文件工具，用于创建、查看和管理 .pak 归档文件 |
| IoStoreUtilities | IOStore 工具，负责 IoStore 容器的构建和管理（UE5 新一代资源打包系统） |
| CookOnTheFlyNetServer | 边 Cook 边运行服务器，支持在开发期间按需 Cook 资源 |
| CookMetadata | Cook 元数据管理，跟踪资源 Cook 状态和依赖信息 |
| CookedEditor | Cooked Editor 支持，允许使用已 Cook 的资源运行编辑器 |
| TextureBuild | 纹理构建系统，协调纹理资源的编译管线 |
| TextureBuildUtilities | 纹理构建工具集，提供纹理构建的辅助功能 |
| TextureCompressor | 纹理压缩器，将纹理数据压缩为 GPU 可用的格式 |
| TextureFormat | 纹理格式管理，统一的纹理格式注册与查询接口 |
| TextureFormatASTC | ASTC 纹理格式实现（移动端常用，自适应可伸缩纹理压缩） |
| TextureFormatDXT | DXT（BCn）纹理格式实现（桌面端常用，S3TC 压缩） |
| TextureFormatETC2 | ETC2 纹理格式实现（OpenGL ES 标准压缩格式） |
| TextureFormatIntelISPCTexComp | Intel ISPC 纹理压缩器实现（基于 ISPC 的高性能纹理压缩） |
| TextureFormatUncompressed | 无压缩纹理格式实现 |
| Virtualization | 虚拟化存储系统，支持将资源数据存储在远程或本地虚拟化后端 |
| ShaderCompilerCommon | Shader 编译公共代码，提供着色器编译的共享基础设施 |
| ShaderFormatOpenGL | OpenGL/GLSL Shader 格式处理 |
| ShaderFormatVectorVM | VectorVM Shader 格式处理（Niagara 使用的虚拟机格式） |
| ShaderPreprocessor | Shader 预处理器，处理 #include、#define 等预处理指令 |
| VulkanShaderFormat | Vulkan/SPIR-V Shader 格式处理 |
| HlslParser | HLSL 语法解析器，解析 HLSL 着色器代码 |
| NaniteBuilder | Nanite 几何构建器，将静态网格转换为 Nanite 虚拟化微多边形格式 |
| NaniteUtilities | Nanite 工具集，提供 Nanite 相关的辅助功能 |

### 网格处理

本类模块负责静态网格和骨骼网格的构建、简化、合并等操作。

| 模块名 | 说明 |
|--------|------|
| MeshBuilder | 网格构建器，负责网格数据的最终构建和优化 |
| MeshBuilderCommon | 网格构建公共代码，被各网格构建模块共享 |
| MeshUtilities | 网格工具集，提供网格操作的通用功能 |
| MeshUtilitiesEngine | 引擎网格工具，包含引擎级别的网格处理功能 |
| MeshMergeUtilities | 网格合并工具，支持多个网格合并为单一网格（用于 HLOD 等） |
| MeshReductionInterface | 网格简化接口，定义网格 LOD 简化的统一接口 |
| MeshSimplifier | 网格简化实现（基于 Quadric Error Metrics 的边折叠算法） |
| MeshBoneReduction | 骨骼网格简化，减少骨骼数量以优化性能 |
| MeshDescriptionOperations | 网格描述操作，对 FMeshDescription 进行各种几何操作 |
| MaterialBaking | 材质烘焙，将复杂材质烘焙为简单纹理 |
| MaterialUtilities | 材质工具，提供材质相关的辅助功能 |
| BSPUtils | BSP（Binary Space Partitioning）工具，处理 BSP 画刷几何 |
| SkeletalMeshUtilitiesCommon | 骨骼网格工具公共代码，骨骼网格处理的共享功能 |

### 资产管理

| 模块名 | 说明 |
|--------|------|
| AssetTools | 资产工具模块，提供资产的创建、导入、重命名、删除等操作接口 |
| CollectionManager | 集合管理器，管理资产集合（Asset Collections）的创建和维护 |
| HierarchicalLODUtilities | HLOD（分层级 LOD）工具，自动生成场景的分层级 LOD |

### 编辑器工具

| 模块名 | 说明 |
|--------|------|
| ToolMenus | 工具菜单系统，统一的编辑器菜单注册和管理框架 |
| ToolWidgets | 工具 UI 控件，提供编辑器工具常用的 Slate 控件 |
| SlateFileDialogs | Slate 文件对话框，跨平台的文件选择对话框 |
| SlateFontDialog | Slate 字体对话框，字体选择界面 |
| SlateReflector | Slate 反射器，调试工具，用于检查 Slate UI 树和样式 |
| DesktopPlatform | 桌面平台抽象层，提供文件系统、窗口管理等平台特定功能 |
| DesktopWidgets | 桌面 UI 控件，桌面平台特有的 UI 组件 |
| Settings | 设置系统接口，定义设置项的注册和查询机制 |
| SettingsEditor | 设置编辑器，提供设置项的编辑 UI |
| SharedSettingsWidgets | 共享设置 UI 控件，设置编辑器使用的通用控件 |
| SourceCodeAccess | 源码编辑器访问接口，支持打开 Visual Studio/Rider 等 IDE |
| HotReload | 热重载模块，支持在编辑器运行时重新编译和加载 C++ 代码 |
| WidgetRegistration | Widget 注册系统，统一管理编辑器 Widget 的注册 |

### 源码控制

| 模块名 | 说明 |
|--------|------|
| SourceControl | 版本控制系统接口，支持 Perforce、Git 等 VCS 的统一接口 |
| SourceControlCheckInPrompt | 提交提示，在资产保存时提醒用户进行版本控制提交 |
| SourceControlViewport | 视口源码控制集成，在视口中显示资产的版本控制状态 |

### 调试与分析

本类模块提供性能分析、日志查看、崩溃诊断等调试功能，大量使用 Unreal Insights 框架。

| 模块名 | 说明 |
|--------|------|
| TraceAnalysis | Trace 数据分析，提供 Trace 数据的分析框架 |
| TraceInsights | Trace Insights 工具，Unreal Insights 性能分析器的主要模块 |
| TraceInsightsCore | Trace Insights 核心，Insights 工具的核心框架和基础设施 |
| TraceInsightsFrontend | Trace Insights 前端，Insights 工具的 UI 层 |
| TraceServices | Trace 服务，提供 Trace 数据的收集、存储和查询服务 |
| TraceTools | Trace 工具集，提供 Trace 相关的辅助功能 |
| LogVisualizer | 日志可视化器，以图形化方式查看日志数据 |
| ProfileVisualizer | 性能分析可视化器，展示性能剖析数据 |
| CollisionAnalyzer | 碰撞分析器，分析和可视化碰撞查询性能 |
| DrawPrimitiveDebugger | 绘制图元调试器，调试渲染管线中的绘制调用 |
| OutputLog | 输出日志窗口，编辑器中的日志输出面板 |
| MessageLog | 消息日志系统，结构化的消息和警告显示 |
| UndoHistory | 撤销历史，查看和管理编辑器的撤销/重做操作栈 |
| CrashDebugHelper | 崩溃调试助手，辅助分析崩溃转储文件 |

### 测试框架

| 模块名 | 说明 |
|--------|------|
| AutomationController | 自动化测试控制器，驱动自动化测试的执行和报告 |
| AutomationDriver | 自动化驱动框架，支持 UI 自动化测试（模拟用户输入） |
| AutomationWindow | 自动化窗口，提供自动化测试的 UI 界面 |
| FunctionalTesting | 功能测试框架，支持关卡内的功能测试（蓝图和 C++） |
| CQTest | 连续质量测试框架，提供 Google Test 风格的测试 API |
| LowLevelTestsRunner | 底层测试运行器，运行不需要引擎完整初始化的底层单元测试 |
| StructUtilsTestSuite | 结构工具测试套件，StructUtils 模块的测试代码 |
| AITestSuite | AI 测试套件，AI 模块的自动化测试集合 |
| MassEntityTestSuite | Mass Entity 测试套件，MassEntity ECS 框架的测试代码 |

### 设备与平台

| 模块名 | 说明 |
|--------|------|
| TargetPlatform | 目标平台接口，定义各目标平台的抽象接口 |
| TargetDeviceServices | 目标设备服务，管理远程设备的连接和部署 |
| DeviceManager | 设备管理器，提供设备管理的 UI 和服务 |
| LauncherServices | 启动器服务，管理项目构建和部署到目标设备的流程 |
| LegacyProjectLauncher | 旧版项目启动器，向后兼容的项目启动工具 UI |
| DirectoryWatcher | 目录监控，监视文件系统目录的变化（文件增删改） |

### 音频格式

| 模块名 | 说明 |
|--------|------|
| AudioFormatADPCM | ADPCM 音频编解码格式 |
| AudioFormatBink | Bink 音频编解码格式 |
| AudioFormatOgg | Ogg Vorbis 音频编解码格式 |
| AudioFormatOpus | Opus 音频编解码格式（低延迟语音编码） |
| AudioFormatRad | Rad 音频编解码格式 |
| AudioSettingsEditor | 音频设置编辑器，提供音频设置的编辑 UI |

### 动画

| 模块名 | 说明 |
|--------|------|
| AnimationDataController | 动画数据控制器，管理动画蓝图的编辑操作 |
| AnimationWidgets | 动画 UI 控件，提供动画编辑器专用的 Slate 控件 |

### 网络

| 模块名 | 说明 |
|--------|------|
| DevHttp | 开发 HTTP 工具，提供开发期间的 HTTP 调试和测试功能 |

### 本地化

| 模块名 | 说明 |
|--------|------|
| Localization | 本地化系统，提供文本本地化的核心功能 |
| LocalizationService | 本地化服务，与本地化后端服务（如 Loc 千字）集成 |
| TranslationEditor | 翻译编辑器，提供文本翻译的编辑 UI |

### 工具与服务

| 模块名 | 说明 |
|--------|------|
| FileUtilities | 文件工具集，提供文件操作的辅助功能 |
| GraphColor | 图着色算法，用于寄存器分配等编译器优化场景 |
| TreeMap | 树形图可视化，以矩形树图方式展示层次结构数据 |
| VisualGraphUtils | 可视化图工具，提供蓝图、材质等图编辑器的图形化支持 |
| ScreenShotComparison | 截图对比系统，自动化测试中的截图回归对比 |
| ScreenShotComparisonTools | 截图对比工具，提供截图对比的辅助功能 |
| ExternalImagePicker | 外部图片选取器，从外部来源选择图片 |
| Merge | 资产合并工具，支持多人协作时的资产冲突合并 |
| PhysicsUtilities | 物理工具，提供物理相关的辅助功能 |
| SessionFrontend | 会话前端，管理编辑器与游戏实例的会话连接 |
| EditorAnalyticsSession | 编辑器分析会话，收集编辑器使用分析数据 |
| SlackIntegrations | Slack 集成，将构建通知等消息发送到 Slack |
| StandaloneRenderer | 独立渲染器，在非编辑器环境中提供渲染能力 |
| UncontrolledChangelists | 未控制变更列表，管理未纳入版本控制的文件变更 |
| UnsavedAssetsTracker | 未保存资产追踪，追踪编辑器中未保存的资产修改 |
| BlankModule | 空白模块模板，用作创建新模块的起始模板 |
| DistributedBuildInterface | 分布式构建接口，支持分布式编译（如 SN-DBS、Incredibuild） |
| GeometryProcessingInterfaces | 几何处理接口，定义几何处理的统一抽象接口 |
| Horde | Horde 构建系统接口，与 Epic Horde 持续集成系统集成 |
| UbaCoordinatorHorde | UBA（Unreal Build Accelerator）Horde 协调器 |
| Zen | Zen 存储服务，与 Zen 远程存储后端集成 |
| ZenPluggableTransport | Zen 可插拔传输层，支持自定义 Zen 数据传输方式 |
| S3Client | S3 客户端，与 Amazon S3 兼容的对象存储交互 |
| TurnkeyIO | Turnkey IO，Turnkey 平台供应系统的 IO 处理 |
| ScriptDisassembler | 脚本反汇编器，将蓝图字节码反汇编为可读文本 |
| DeveloperToolSettings | 开发者工具设置，管理开发者工具的配置 |
| CSVUtils | CSV 工具，提供 CSV 文件的读写和分析功能 |

### 平台子目录

平台子目录包含各平台特有的编辑器和构建支持模块，它们为特定平台提供设备检测、目标平台设置和 Shader 格式支持。

#### Android（`Developer/Android/`）

| 模块名 | 说明 |
|--------|------|
| AndroidDeviceDetection | Android 设备检测，自动发现连接的 Android 设备 |
| AndroidPlatformEditor | Android 平台编辑器设置 |
| AndroidTargetPlatform | Android 目标平台定义 |
| AndroidTargetPlatformControls | Android 目标平台控制接口 |
| AndroidTargetPlatformSettings | Android 目标平台配置 |
| AndroidZenServerPlugin | Android Zen 服务器插件 |

#### Apple（`Developer/Apple/`）

| 模块名 | 说明 |
|--------|------|
| MetalShaderFormat | Metal Shader 格式处理（macOS/iOS GPU 着色器编译） |

#### iOS（`Developer/IOS/`）

| 模块名 | 说明 |
|--------|------|
| IOSPlatformEditor | iOS 平台编辑器设置 |
| IOSTargetPlatform | iOS 目标平台定义 |
| IOSTargetPlatformControls | iOS 目标平台控制接口 |
| IOSTargetPlatformSettings | iOS 目标平台配置 |
| TVOSTargetPlatform | tvOS 目标平台定义 |
| TVOSTargetPlatformControls | tvOS 目标平台控制接口 |
| TVOSTargetPlatformSettings | tvOS 目标平台配置 |

#### Linux（`Developer/Linux/`）

| 模块名 | 说明 |
|--------|------|
| LinuxPlatformEditor | Linux 平台编辑器设置 |
| LinuxTargetPlatform | Linux x64 目标平台定义 |
| LinuxTargetPlatformControls | Linux x64 目标平台控制接口 |
| LinuxTargetPlatformSettings | Linux x64 目标平台配置 |
| LinuxArm64TargetPlatform | Linux ARM64 目标平台定义 |
| LinuxArm64TargetPlatformControls | Linux ARM64 目标平台控制接口 |
| LinuxArm64TargetPlatformSettings | Linux ARM64 目标平台配置 |

#### Mac（`Developer/Mac/`）

| 模块名 | 说明 |
|--------|------|
| MacPlatformEditor | Mac 平台编辑器设置 |
| MacTargetPlatform | Mac 目标平台定义 |
| MacTargetPlatformControls | Mac 目标平台控制接口 |
| MacTargetPlatformSettings | Mac 目标平台配置 |

#### Windows（`Developer/Windows/`）

| 模块名 | 说明 |
|--------|------|
| WindowsPlatformEditor | Windows 平台编辑器设置 |
| WindowsTargetPlatform | Windows 目标平台定义 |
| WindowsTargetPlatfomControls | Windows 目标平台控制接口 |
| WindowsTargetPlatformSettings | Windows 目标平台配置 |
| ShaderFormatD3D | Direct3D Shader 格式处理（DXBC/DXIL） |
| LiveCoding | Live Coding 实时编码，在编辑器运行时编译并加载 C++ 代码 |
| LiveCodingServer | Live Coding 服务器，处理 Live Coding 的编译请求 |

#### Datasmith（`Developer/Datasmith/`）

| 模块名 | 说明 |
|--------|------|
| DatasmithExporter | Datasmith 导出器，将场景数据导出为 Datasmith 格式 |
| DatasmithExporterUI | Datasmith 导出器 UI，提供导出操作的用户界面 |
| DatasmithFacade | Datasmith Facade 层，简化的 Datasmith API 接口 |

---

## 模块统计

| 分类 | 模块数量 |
|------|----------|
| 构建与打包 | 26 |
| 网格处理 | 13 |
| 资产管理 | 3 |
| 编辑器工具 | 14 |
| 源码控制 | 3 |
| 调试与分析 | 14 |
| 测试框架 | 9 |
| 设备与平台 | 6 |
| 音频格式 | 6 |
| 动画 | 2 |
| 网络 | 1 |
| 本地化 | 3 |
| 工具与服务 | 27 |
| 平台子目录 | 32 |
| **总计** | **约 159** |

> **说明**：总计数字包含平台子目录中的模块。顶层直接模块约 127 个，加上平台子目录中的 32 个模块。

---

## 模块依赖关系要点

1. **构建管线依赖链**：TextureBuild -> TextureCompressor -> TextureFormat* -> DerivedDataCache
2. **网格处理依赖链**：MeshBuilder -> MeshUtilities -> MeshReductionInterface -> MeshSimplifier
3. **Trace 分析依赖链**：TraceTools -> TraceServices -> TraceAnalysis -> TraceInsightsCore -> TraceInsights -> TraceInsightsFrontend
4. **平台模块模式**：每个平台通常包含 PlatformEditor、TargetPlatform、TargetPlatformControls、TargetPlatformSettings 四个标准模块
5. **公共依赖**：大多数 Developer 模块依赖于 Core、CoreUObject，工具类模块额外依赖 Slate、SlateCore、UnrealEd
