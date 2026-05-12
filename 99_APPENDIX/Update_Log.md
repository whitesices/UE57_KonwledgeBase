# UE5.7.4 知识库更新日志

## 2026-05-12

### Phase 0：版本确认与知识库初始化

- 创建 `UE57_KnowledgeBase/` 完整目录结构
- 读取 `Engine/Build/Build.version`，确认版本为 UE5.7.4
- 读取 `Engine/Source/Runtime/Launch/Resources/Version.h`，确认版本宏定义
- 生成 `00_VERSION_CHECK.md` — 版本确认报告
- 生成 `SCAN_RULES.md` — 扫描规则文档
- 初始化 `99_APPENDIX/Update_Log.md`
- 初始化 `99_APPENDIX/TODO_Unverified.md`

### Phase 1：源码目录总览 — 完成

- 扫描 Engine/Source/Runtime/（188 模块）
- 扫描 Engine/Source/Editor/（145 模块）
- 扫描 Engine/Source/Developer/（120+ 模块）
- 扫描 Engine/Source/Programs/（87 个程序）
- 扫描 Engine/Plugins/（500+ 插件，28 个分类）
- 生成 README.md、Engine_Source_Map.md、Runtime_Modules.md、Editor_Modules.md、Developer_Modules.md、Programs.md

### Phase 2：全局知识树 — 完成

- 生成 00_INDEX.md — 全局索引、学习路线、问题快速入口

### Phase 3：核心系统深挖 — 完成

- 生成 03_ENGINE_BOOT/Launch_Flow.md — 启动流程详解
- 生成 03_ENGINE_BOOT/EngineLoop.md — FEngineLoop 详解
- 生成 03_ENGINE_BOOT/Mermaid_Startup_Flow.md — 启动流程 Mermaid 图集（7 个图）

### Phase 4：完整渲染流程专题 — 完成

- 生成 06_RENDERING/Full_Render_Pipeline.md — 完整渲染管线（含源码证据）
- 生成 06_RENDERING/Mermaid_Render_Flow.md — 渲染 Mermaid 图集（8 个图）

### Phase 5：Build 系统专题 — 完成

- 生成 02_BUILD_SYSTEM/README.md
- 生成 02_BUILD_SYSTEM/UBT.md

### Phase 6：资源与热更新专题 — 完成 (全面增强)

使用 5 个并行 Agent 深入扫描 Package/Loader、Cook、IOStore、Dynamic Loading、Pak/Hot Update 源码，从 2 个骨架文件扩展到 8 个完整文档：

- 重写 `07_ASSET_PIPELINE/README.md` — 资源管线总览（完整流程图、模块表、Cook 输出文件类型速查）
- 扩展 `07_ASSET_PIPELINE/AssetRegistry.md` — 从 48 行扩展到完整文档（FAssetData、FARFilter、IAssetRegistry 接口、编辑器/运行时差异、依赖追踪）
- 新增 `07_ASSET_PIPELINE/Package.md` — UPackage 与 Package 文件格式（UPackage 类结构、FLinkerLoad/Save、.uasset 二进制布局、28 个 PKG_ 标志位、完整同步加载调用链、FPackageTrailer）
- 新增 `07_ASSET_PIPELINE/Cook.md` — Cook 系统详解（UCookCommandlet 入口、CookOnTheFlyServer 五阶段状态机 REQUEST→LOAD→SAVE→FINALIZE、增量 Cook TargetDomainKey 系统、DDC 集成、多进程 MPCook）
- 新增 `07_ASSET_PIPELINE/IOStore.md` — IOStore 存储系统（.utoc/.ucas 格式、FIoDispatcher 调度器、完美哈希查找、压缩加密、完整读取路径、与传统 Pak 对比）
- 新增 `07_ASSET_PIPELINE/Dynamic_Loading.md` — 动态加载系统（StaticLoadObject/LoadObject 调用链、FSoftObjectPath/FSoftObjectPtr/TPersistentObjectPtr、ALT/EDL/ZenLoader 异步架构、FStreamableManager 批量加载、GC 协调）
- 新增 `07_ASSET_PIPELINE/Pak.md` — Pak 文件系统（FPakFile/FPakPlatformFile、Mount 挂载流程、压缩加密签名、补丁 Pak _P.pak 机制、启动挂载序列、运行时动态挂载）
- 新增 `07_ASSET_PIPELINE/Hot_Update.md` — 热更新与补丁（补丁遮蔽机制、ChunkDownloader 流式安装、CDN Manifest 下载、ContentBuildId 版本管理、完整热更新流程）

### Phase 7：Editor 与插件系统专题 — 完成 (全面增强)

使用 5 个并行 Agent 深入扫描 Editor 和 Plugin 源码，从 1 个骨架文件扩展到 13 个完整文档：

**08_EDITOR/ (7 文档, 1532 行):**
- 新增 `README.md` — 编辑器架构总览（核心模块表、启动流程全景图）
- 新增 `Editor_Startup.md` — 编辑器启动流程（UEditorEngine/UUnrealEdEngine::Init()、5 阶段启动序列、50+ 模块加载清单、FEditorModeTools）
- 新增 `AssetTools.md` — 资产工具 API（IAssetTools::CreateAsset/ImportAssets/RenameAssets、IAssetTypeActions 注册、资产类别系统）
- 新增 `ContentBrowser.md` — 内容浏览器（FContentBrowserSingleton、SPathView/SAssetView、4 种视图模式、菜单扩展点）
- 新增 `DetailsPanel.md` — 详情面板（IDetailsView、IPropertyHandle 属性读写、IDetailCustomization/IPropertyTypeCustomization、UPROPERTY 元数据影响）
- 新增 `BlueprintEditor.md` — Blueprint 编辑器（FBlueprintEditor 5 种模式、UEdGraph/K2Node 图模型、FKismetCompilerContext 编译管线、调试系统、扩展点）
- 新增 `Commandlet.md` — Commandlet 系统（UCommandlet 基类、命令行检测与执行、CookCommandlet、自定义 Commandlet 模式）

**12_PLUGIN_SYSTEM/ (6 文档, 954 行):**
- 重写 `README.md` — 插件系统总览（EHostType 速查表、ELoadingPhase 阶段表、发现流程）
- 新增 `Plugin_Descriptor.md` — .uplugin 描述符（FPluginDescriptor 30+ 全部字段、FModuleDescriptor、FileVersion 1→2→3 演进、插件依赖、发现优先级）
- 新增 `Runtime_Plugin.md` — Runtime 插件（EHostType::Runtime 编译/加载过滤、生命周期、bCanContainContent 标志、EnabledByDefault 行为）
- 新增 `Editor_Plugin.md` — Editor 插件（Editor vs EditorNoCommandlet、编辑器扩展注册模式、StartupModule/ShutdownModule 范式）
- 新增 `ThirdParty_Libraries.md` — 第三方库集成（ModuleType.External 模板、目录规范、动静态库模式、libcurl/OpenSSL/Oodle 引擎示例）
- 新增 `Packaging.md` — 插件打包（8 层模块过滤机制、HostType→Shipping 排除表、Content 打包、.uplugin 运行时条件、DLL 分发 StagedFileType）

### Phase 8：Gameplay/UI/Networking/Animation — 完成

- 生成 05_GAMEPLAY_FRAMEWORK/README.md, Actor.md, Tick.md
- 生成 10_NETWORKING/README.md
- 生成 11_UI/README.md
- 生成 09_ANIMATION/README.md

### Phase 9：Agent 索引 — 完成

- 生成 15_AGENT_INDEX/Query_Map.md
- 生成 15_AGENT_INDEX/Claude_Codex_Usage_Guide.md

### Phase 10：质量报告 — 完成

- 生成 FINAL_REPORT.md

---

## 2026-05-12 (Phase 4 补完)

### Phase 4 渲染专题补全 — 完成

使用 5 个并行 Agent 扫描源码，生成 8 个缺失的渲染文档：

- 生成 `06_RENDERING/Lumen.md` — Lumen 全局光照系统详解（FLumenSceneData、Surface Cache、Screen Probe Gather、Radiance Cache、Software/HW RT）
- 生成 `06_RENDERING/Virtual_Shadow_Map.md` — VSM 虚拟阴影映射详解（分页管理、Clipmap、Nanite 集成、帧间缓存）
- 生成 `06_RENDERING/Deferred_Rendering.md` — 延迟渲染完整流程（GBuffer 结构、Pass 顺序、光照计算）
- 生成 `06_RENDERING/Forward_Rendering.md` — 前向渲染流程（移动端、VR、光照网格）
- 生成 `06_RENDERING/SceneProxy.md` — 场景代理系统（FPrimitiveSceneProxy 生命周期、跨线程通信）
- 生成 `06_RENDERING/Renderer_Module.md` — 渲染器模块总览（FRendererModule、Build.cs 依赖）
- 生成 `06_RENDERING/GameThread_To_RenderThread.md` — 三线程架构详解（ENQUEUE_RENDER_COMMAND、Fence、RHI 线程模式）
- 生成 `06_RENDERING/RenderTarget_Readback.md` — GPU 回读详解（ReadPixels、Staging Buffer、同步机制）

---

## 2026-05-12 (Phase 3 补完)

### Phase 3 模块深度详解 — 完成

使用 7 个并行 Agent 扫描源码，生成 27 个模块详解文档（含 README）：

- 生成 `14_MODULE_DEEP_DIVE/Core.md` — Core 基础模块（容器、数学、HAL、多线程）
- 生成 `14_MODULE_DEEP_DIVE/CoreUObject.md` — CoreUObject 对象系统（UObject、反射、GC、序列化）
- 生成 `14_MODULE_DEEP_DIVE/Engine.md` — Engine 游戏框架（AActor、UWorld、Component、GameMode）
- 生成 `14_MODULE_DEEP_DIVE/Launch.md` — Launch 入口模块（GuardedMain、FEngineLoop）
- 生成 `14_MODULE_DEEP_DIVE/Projects.md` — 项目/插件描述文件管理（IProjectManager、IPluginManager）
- 生成 `14_MODULE_DEEP_DIVE/ApplicationCore.md` — 应用核心（窗口、输入、平台抽象）
- 生成 `14_MODULE_DEEP_DIVE/Slate.md` — Slate UI 框架（FSlateApplication、SWidget）
- 生成 `14_MODULE_DEEP_DIVE/SlateCore.md` — Slate 基础设施（SWidget 基类、渲染、FreeType）
- 生成 `14_MODULE_DEEP_DIVE/UMG.md` — UMG 蓝图 UI（UUserWidget、UWidget、UWidgetTree）
- 生成 `14_MODULE_DEEP_DIVE/InputCore.md` — 输入核心（FKey、EKeys、输入键类型）
- 生成 `14_MODULE_DEEP_DIVE/AssetRegistry.md` — 资产注册表（IAssetRegistry、FAssetData、扫描缓存）
- 生成 `14_MODULE_DEEP_DIVE/RenderCore.md` — 渲染核心（RDG、FRenderResource、FGlobalShader）
- 生成 `14_MODULE_DEEP_DIVE/Renderer.md` — 渲染器（FDeferredShadingSceneRenderer、Lumen/Nanite/VSM）
- 生成 `14_MODULE_DEEP_DIVE/RHI.md` — RHI 硬件抽象（FDynamicRHI、FRHICommandList、资源类型）
- 生成 `14_MODULE_DEEP_DIVE/D3D12RHI.md` — DirectX 12 后端（FD3D12DynamicRHI、设备、描述符堆）
- 生成 `14_MODULE_DEEP_DIVE/Niagara.md` — Niagara VFX 系统（UNiagaraSystem、VectorVM、GPU 计算）
- 生成 `14_MODULE_DEEP_DIVE/AnimGraphRuntime.md` — 骨骼动画运行时（BlendSpace、AnimNode）
- 生成 `14_MODULE_DEEP_DIVE/MovieScene.md` — Sequencer 时间轴（UMovieScene、ECS 实体系统）
- 生成 `14_MODULE_DEEP_DIVE/UnrealEd.md` — 编辑器核心（UEditorEngine、FEditorModeTools）
- 生成 `14_MODULE_DEEP_DIVE/AssetTools.md` — 资产工具（IAssetTools、创建/导入/重命名）
- 生成 `14_MODULE_DEEP_DIVE/ContentBrowser.md` — 内容浏览器（FContentBrowserSingleton）
- 生成 `14_MODULE_DEEP_DIVE/PakFile.md` — Pak 文件系统（FPakFile、FPakPlatformFile）
- 生成 `14_MODULE_DEEP_DIVE/HTTP.md` — HTTP 客户端（IHttpRequest、libcurl/WinHTTP）
- 生成 `14_MODULE_DEEP_DIVE/WebSockets.md` — WebSocket（IWebSocket、libWebSockets）
- 生成 `14_MODULE_DEEP_DIVE/Networking.md` — 网络/Socket（FSocket、FTcpListener、UDP）
- 生成 `14_MODULE_DEEP_DIVE/PixelStreaming.md` — 像素流送（WebRTC、信令、远程输入）
- 生成 `14_MODULE_DEEP_DIVE/README.md` — 模块详解索引

---

## 2026-05-12 (Phase 5 补完)

### Phase 5 Build 系统专题补全 — 完成

深入扫描 UBT、UHT、ModuleRules、TargetRules 源码，生成 5 个缺失的 Build 系统文档：

- 生成 `02_BUILD_SYSTEM/UHT.md` — UnrealHeaderTool 详解（解析管线、宏解析系统、代码生成、缓存机制、UBT 集成）
- 生成 `02_BUILD_SYSTEM/ModuleRules.md` — 模块规则详解（依赖属性对比、包含路径、库链接、模块类型、加载阶段、平台过滤、引擎 Build.cs 实例分析）
- 生成 `02_BUILD_SYSTEM/TargetRules.md` — 目标规则详解（TargetType 枚举、LinkType、核心属性分类、Target.cs 实例、TargetRules→ModuleRules 传递机制）
- 生成 `02_BUILD_SYSTEM/BuildCs_Guide.md` — Build.cs 实践指南（模块模板、依赖选择决策树、第三方库集成、平台条件编译、循环依赖打破、PCH/Unity 控制）
- 生成 `02_BUILD_SYSTEM/Common_Build_Errors.md` — 常见构建错误排查（LNK2019/C1083/UHT 错误/循环依赖/PCH/DLL 加载，含源码级检测机制）

### Phase 5 Build 系统专题增强 — 2026-05-12

UBT.md 大幅扩展 + 全部文档源码证据验证：

- **扩展 `02_BUILD_SYSTEM/UBT.md`**：从 82 行扩展到 420+ 行，新增 27 种 ToolMode 完整列表、Main() 启动流程详解、BuildMode 构建流程、UEBuildTarget/UEBuildModule/UEBuildBinary 继承体系、ActionGraph 与增量构建机制（Makefile 哈希比对）、ToolChain/Executor 架构、项目文件生成流程、错误匹配系统、平台抽象层、3 个新 Mermaid 图
- **验证全部 6 份文档源码证据**：逐一确认 UHT.md、ModuleRules.md、TargetRules.md、BuildCs_Guide.md、Common_Build_Errors.md 中的源码路径和行号引用精度（TargetRules.cs:21-47, 53-69, 2529-2531; ModuleRules.cs:1505-1510; UEBuildModule.cs:1342-1351; ExternalExecution.cs:1207 等关键行号验证通过）
