# Programs 模块总览

## 摘要

Programs 目录包含 UE5.7.4 的独立工具程序，共约 87 个。分为 C# 工具和 C++ 工具两大类。

---

## 按类别分类

### 构建系统工具

| 程序 | 路径 | 语言 | 职责 |
|------|------|------|------|
| UnrealBuildTool | Programs/UnrealBuildTool/ | C# | 构建系统核心，解析 .Build.cs，驱动编译 |
| UnrealBuildAccelerator | Programs/UnrealBuildAccelerator/ | C++ | 分布式构建加速（UBA） |
| ShaderCompileWorker | Programs/ShaderCompileWorker/ | C++ | Shader 编译工作进程 |
| AutomationTool | Programs/AutomationTool/ | C# | UAT 自动化工具框架 |
| AutomationToolLauncher | Programs/AutomationToolLauncher/ | C# | UAT 启动器 |

### 打包工具

| 程序 | 职责 |
|------|------|
| UnrealPak | Pak 文件打包/解包/列表 |
| BuildPatchTool | 补丁构建 |
| UnrealPackageTool | 包管理工具 |
| TextureBuildWorker | 纹理构建工作进程 |
| BaseTextureBuildWorker | 基础纹理构建工作进程 |
| DerivedDataBuildWorker | DDC 构建工作进程 |
| DerivedDataTool | DDC 管理工具 |
| DiffAssetBulkData | 资产批量数据对比 |
| UnrealObjectPtrTool | UObject 指针工具 |
| UnrealVirtualizationTool | 虚拟化存储工具 |

### 开发者工具

| 程序 | 职责 |
|------|------|
| UnrealFrontend | 前端工具（项目启动、设备管理） |
| UnrealGameSync | 游戏同步工具（UGS） |
| UnrealInsights | 性能分析工具（Trace 可视化） |
| UnrealLightmass | 静态光照烘焙 |
| LiveCodingConsole | 热重载控制台 |
| LiveLinkHub | LiveLink 设备管理中心 |
| UnrealVersionSelector | .uproject 文件关联注册 |
| CrashReportClient | 崩溃报告客户端 |
| SwitchboardListener | Switchboard 监听器（虚拟制片） |
| UnrealRecoverySvc | 恢复服务 |
| UninstallHelper | 卸载助手 |

### 协作工具

| 程序 | 职责 |
|------|------|
| UnrealMultiUserServer | 多用户编辑服务器 |
| UnrealMultiUserSlateServer | Slate 多用户服务器 |

### 测试工具

| 程序 | 职责 |
|------|------|
| AutoRTFMTests | AutoRTFM 事务内存测试 |
| LowLevelTests | 底层基础测试 |
| NetworkPredictionTests | 网络预测测试 |
| ReplicationSystemTest | 复制系统测试 |
| ReplicationSystemLowLevelTests | 复制系统底层测试 |
| SlateTests | Slate UI 测试 |
| PlainPropsTests | PlainProps 序列化测试 |
| ChaosUserDataPTTests | Chaos 物理测试 |
| ToolMenusTests | 工具菜单测试 |
| HeadlessChaos | 无头 Chaos 物理测试 |
| HeadlessChaosPerf | Chaos 性能测试 |
| BenchmarkTool | 基准测试 |

### 平台工具

| 程序 | 职责 |
|------|------|
| BootstrapPackagedGame | 打包游戏启动引导 |
| UnrealLaunchDaemon | iOS 启动守护进程 |
| DsymExporter | macOS 调试符号导出 |
| UnrealAtoS | macOS 地址转符号 |
| DumpSyms | 符号导出（Breakpad 格式） |
| BreakpadSymbolEncoder | Breakpad 符号编码 |
| SymsLibDump | 符号库转储 |

### 云服务/分布式

| 程序 | 职责 |
|------|------|
| UnrealCloudDDC | 云端 DDC 服务（Jupiter） |
| Horde | 构建农场管理系统 |
| Unsync | 增量同步工具 |
| UbaCoordinatorHorde | UBA Horde 协调器 |

### 企业级工具

| 程序 | 路径 | 职责 |
|------|------|------|
| DatasmithCADWorker | Programs/Enterprise/Datasmith/ | CAD 数据转换工作进程 |
| DatasmithFacadeCSharp | Programs/Enterprise/Datasmith/ | Datasmith C# 接口 |
| DatasmithMaxExporter | Programs/Enterprise/Datasmith/ | 3ds Max 导出器（2017-2026） |
| DatasmithSDK | Programs/Enterprise/Datasmith/ | Datasmith SDK |

### 共享库

| 库 | 路径 | 职责 |
|-----|------|------|
| EpicGames.Core | Programs/Shared/ | 核心工具库 |
| EpicGames.Build | Programs/Shared/ | 构建工具库 |
| EpicGames.Horde | Programs/Shared/ | Horde 客户端库 |
| EpicGames.Perforce | Programs/Shared/ | Perforce 接口 |
| EpicGames.Serialization | Programs/Shared/ | 序列化库 |
| UGSCore | Programs/UGSCore/ | UnrealGameSync 核心库 |

### 其他工具

| 程序 | 职责 |
|------|------|
| BlankProgram | 空白程序模板 |
| CmdLink | 命令链接工具 |
| EpicWebHelper | Web 助手 |
| GeometryProcessing | 几何处理程序 |
| ImageValidator | 图像验证工具 |
| InterchangeWorker | Interchange 格式转换工作进程 |
| IoStoreOnDemand | IOStore 按需加载工具 |
| SubmitTool | 提交工具 |
| TestPAL | 测试 PAL |
| TraceAnalyzer | Trace 分析工具 |
| WebTests | Web 测试工具 |
| ZenDashboard | Zen 仪表盘 |
| ZenLaunch | Zen 启动器 |
| GitDependencies | Git 依赖下载 |
| NetworkProfiler | 网络性能分析 |
| ReplayServer | 回放服务器 |
| UnrealSwarm | Swarm 分布式渲染 |
| UnrealToolbox | UE 工具箱 |

---

## 源码证据

- Engine/Source/Programs/ 目录扫描
- 各程序目录下的 Build.cs / .csproj 文件
