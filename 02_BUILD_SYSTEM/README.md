# Build 系统总览

## 摘要
UE5.7.4 的构建系统由 UnrealBuildTool (UBT) 和 UnrealHeaderTool (UHT) 两个核心工具组成。UBT 是 C# 写的构建系统，负责解析 .Build.cs 文件、确定模块依赖、驱动 C++ 编译器。UHT 是 C++ 写的头文件解析工具，负责解析 UCLASS/UPROPERTY/UFUNCTION 宏并生成 .generated.h 反射代码。

## 核心流程
1. UBT 读取 Target.cs 确定构建目标
2. UBT 扫描所有 Build.cs 解析模块依赖
3. UHT 处理头文件中的反射宏
4. UBT 生成编译命令并调用 C++ 编译器
5. 链接生成最终可执行文件

## 关键工具
- UBT: Engine/Source/Programs/UnrealBuildTool/ (C#)
- UHT: Engine/Source/Programs/UnrealHeaderTool/ (C++)
- 构建脚本: Engine/Build/BatchFiles/Build.bat

## 模块类型
- Runtime: 运行时必需，打包到 Shipping
- Editor: 仅编辑器使用，不打包
- Developer: 开发调试工具，不打包到 Shipping
- Program: 独立程序

## 文档索引
- [UBT.md](UBT.md) — UnrealBuildTool 详解
- [UHT.md](UHT.md) — UnrealHeaderTool 详解
- [ModuleRules.md](ModuleRules.md) — 模块规则
- [TargetRules.md](TargetRules.md) — 目标规则
- [BuildCs_Guide.md](BuildCs_Guide.md) — Build.cs 编写指南
- [Common_Build_Errors.md](Common_Build_Errors.md) — 常见构建错误
