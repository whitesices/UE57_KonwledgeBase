# ThirdParty Libraries 第三方库集成详解

## 摘要
UE5.7.4 通过 `ModuleType.External` 在 Build.cs 中声明第三方库。External 模块不参与 C++ 编译，仅作为头文件路径和库文件的聚合单元传递给 UBT。平台条件 (`Target.Platform`) 和配置条件 (`Target.Configuration`) 用于选择正确的库变体。DLL 分发通过 `RuntimeDependencies` + `PublicDelayLoadDLLs` 实现。

## 适合解决的问题
- 如何为第三方库编写 Build.cs？
- `ModuleType.External` 和 `ModuleType.CPlusPlus` 的区别？
- 如何为不同平台提供不同的库文件？
- 静态库和动态库的集成模式有什么区别？
- 如何确保 DLL 随游戏打包分发？

## 核心结论
1. `Type = ModuleType.External` 声明模块不参与 C++ 编译，创建 `UEBuildModuleExternal` 实例
2. `PublicSystemIncludePaths` 用于第三方头文件（不检查依赖关系）
3. `PublicAdditionalLibraries` 添加 .lib/.a 文件
4. `RuntimeDependencies` + `PublicDelayLoadDLLs` 处理 DLL 分发和延迟加载
5. 推荐目录结构：`ThirdParty/<Lib>/<Version>/include/` + `lib/<Platform>/`

## 源码位置

| 组件 | 路径 | 作用 |
|------|------|------|
| ModuleType 枚举 | `Engine/Source/Programs/UnrealBuildTool/Configuration/ModuleRules.cs:108` | ModuleType.External 定义 |
| UEBuildModuleExternal | `Engine/Source/Programs/UnrealBuildTool/Configuration/UEBuildModuleExternal.cs:8` | External 模块内部表示 |
| RuntimeDependencies | `Engine/Source/Programs/UnrealBuildTool/Configuration/ModuleRules.cs:1354` | 运行时依赖属性 |
| 引擎示例目录 | `Engine/Source/ThirdParty/` | libcurl, OpenSSL, zlib, Oodle 等 |

## 1. External 模块 Build.cs 模板

```csharp
// ThirdParty/MyLib/MyLib.Build.cs
using UnrealBuildTool;
using System.IO;

public class MyLib : ModuleRules
{
    public MyLib(ReadOnlyTargetRules Target) : base(Target)
    {
        Type = ModuleType.External;  // 关键声明

        // 头文件路径
        string IncludePath = Path.Combine(ModuleDirectory, "include");
        PublicSystemIncludePaths.Add(IncludePath);  // System 路径不检查依赖

        // 按平台选择库文件
        if (Target.Platform == UnrealTargetPlatform.Win64)
        {
            string LibPath = Path.Combine(ModuleDirectory, "lib", "Win64");
            PublicAdditionalLibraries.Add(Path.Combine(LibPath, "mylib.lib"));
            
            // DLL 分发
            string DllPath = Path.Combine(ModuleDirectory, "bin", "Win64", "mylib.dll");
            RuntimeDependencies.Add("$(BinaryOutputDir)/mylib.dll", DllPath);
            PublicDelayLoadDLLs.Add("mylib.dll");
        }
        else if (Target.Platform == UnrealTargetPlatform.Mac)
        {
            PublicAdditionalLibraries.Add(
                Path.Combine(ModuleDirectory, "lib", "Mac", "libmylib.a"));
        }
    }
}
```

## 2. 目录结构规范

```
Engine/Source/ThirdParty/<LibraryName>/
    <Version>/                        // e.g., "1.3", "8.12.1"
        include/
            <library>/                 // 头文件
        lib/
            Win64/
                Release/mylib.lib      // Windows 静态库导入
            Mac/
                libmylib.a             // macOS 静态库
            Unix/x86_64-unknown-linux-gnueabi/
                Release/libmylib.a     // Linux 静态库
            Android/ARM64/libmylib.a   // Android 多架构
        bin/
            Win64/mylib.dll            // Windows DLL（运行时需要）
```

## 3. 关键属性速查

| 属性 | 用途 | 示例 |
|------|------|------|
| `Type = ModuleType.External` | 声明为外部模块 | — |
| `PublicSystemIncludePaths` | 第三方头文件（不检查依赖） | `"include/"` |
| `PublicAdditionalLibraries` | 静态库 .lib/.a | `"lib/Win64/mylib.lib"` |
| `PublicDelayLoadDLLs` | 延迟加载 DLL | `"mylib.dll"` |
| `RuntimeDependencies` | 运行时文件分发 | `$(BinaryOutputDir)/mylib.dll` |
| `PublicSystemLibraries` | 系统库名 | `"psapi"`, `"z"` |
| `PublicFrameworks` | Apple Framework | `"Foundation"`, `"AppKit"` |
| `PublicRuntimeLibraryPaths` | Linux .so 搜索路径 | `"lib/Linux/"` |

## 4. 静态库 vs 动态库

### 静态库模式

```csharp
// 纯静态：只需头文件 + .lib/.a
PublicAdditionalLibraries.Add(Path.Combine(LibPath, "zlibstatic.lib"));
// .lib 链接到 EXE/DLL 中，无需 RuntimeDependencies
```

### 动态库模式

```csharp
// 动态：导入库 + 运行时 DLL 分发 + 延迟加载
PublicAdditionalLibraries.Add(Path.Combine(LibPath, "mylib.lib"));      // 导入库
RuntimeDependencies.Add("$(BinaryOutputDir)/mylib.dll", DllPath);       // DLL 分发
PublicDelayLoadDLLs.Add("mylib.dll");                                    // 延迟加载
PublicDefinitions.Add("MYLIB_DYNAMIC_LINK=1");                          // 宏标记
```

## 5. 平台条件判断模式

```csharp
// Windows 组 (Win64 + WinGDK)
if (Target.Platform.IsInGroup(UnrealPlatformGroup.Windows)) { }

// Unix 组 (Linux + LinuxArm64)
if (Target.IsInPlatformGroup(UnrealPlatformGroup.Unix)) { }

// Apple 组 (Mac + iOS + tvOS + visionOS)
if (Target.IsInPlatformGroup(UnrealPlatformGroup.Apple)) { }

// 单个平台
if (Target.Platform == UnrealTargetPlatform.Mac) { }

// Debug/Release
string ConfigFolder = (Target.Configuration == UnrealTargetConfiguration.Debug &&
    Target.bDebugBuildsActuallyUseDebugCRT) ? "Debug" : "Release";
```

## 6. 引擎示例

### libcurl (静态)
- `Engine/Source/ThirdParty/libcurl/libcurl.Build.cs:58`
- 跨所有平台的 `libcurl.a` / `libcurl.lib`
- 依赖 nghttp2, OpenSSL, zlib

### OpenSSL (静态)
- `Engine/Source/ThirdParty/OpenSSL/OpenSSL.Build.cs:84`
- 所有平台静态 .a/.lib
- Debug/Release 路径切换

### IntelTBB (动态)
- `Engine/Source/ThirdParty/Intel/TBB/IntelTBB.Build.cs`
- DLL 模式：导入库 + `RuntimeDependencies` + `PublicDelayLoadDLLs`

### EOS SDK (动态 + 复杂配置)
- `Engine/Source/ThirdParty/EOSSDK/EOSSDK.Build.cs:324`
- 跨平台 SDK 集成全功能示例

## 7. 第三方二进制分发规范

```
Engine/Binaries/ThirdParty/<Vendor>/<Library>/<Platform>/<file>.dll

示例：
Core.Build.cs: RuntimeDependencies.Add(
    "$(EngineDir)/Binaries/ThirdParty/DbgHelp/{ArchDir}dbghelp.dll");
```

## 源码证据
- Engine/Source/Programs/UnrealBuildTool/Configuration/ModuleRules.cs:108-119（ModuleType 枚举）
- Engine/Source/Programs/UnrealBuildTool/Configuration/ModuleRules.cs:1211（PublicSystemIncludePaths）
- Engine/Source/Programs/UnrealBuildTool/Configuration/ModuleRules.cs:1246（PublicAdditionalLibraries）
- Engine/Source/Programs/UnrealBuildTool/Configuration/ModuleRules.cs:1308（PublicDelayLoadDLLs）
- Engine/Source/Programs/UnrealBuildTool/Configuration/ModuleRules.cs:1354（RuntimeDependencies）
- Engine/Source/Programs/UnrealBuildTool/Configuration/UEBuildModuleExternal.cs:8（External 模块）
- Engine/Source/ThirdParty/libcurl/libcurl.Build.cs（静态库示例）
- Engine/Source/ThirdParty/Intel/TBB/IntelTBB.Build.cs（动态库示例）
- Engine/Source/ThirdParty/EOSSDK/EOSSDK.Build.cs（复杂 SDK 示例）

## 相关文档
- [Packaging.md](Packaging.md) — 插件打包与 DLL 分发
- [../02_BUILD_SYSTEM/BuildCs_Guide.md](../02_BUILD_SYSTEM/BuildCs_Guide.md) — Build.cs 编写指南
