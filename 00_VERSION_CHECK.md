# UE5.7.4 版本确认

## 摘要

本文档记录对本地源码版本的确认结果。

## 版本信息

| 字段 | 值 | 来源 |
|------|-----|------|
| MajorVersion | 5 | Engine/Build/Build.version |
| MinorVersion | 7 | Engine/Build/Build.version |
| PatchVersion | 4 | Engine/Build/Build.version |
| Changelist | 0 | Engine/Build/Build.version |
| CompatibleChangelist | 47537391 | Engine/Build/Build.version |
| IsLicenseeVersion | 0 (false) | Engine/Build/Build.version |
| IsPromotedBuild | 0 (false) | Engine/Build/Build.version |
| BranchName | UE5 | Engine/Build/Build.version |
| ENGINE_MAJOR_VERSION | 5 | Engine/Source/Runtime/Launch/Resources/Version.h:58 |
| ENGINE_MINOR_VERSION | 7 | Engine/Source/Runtime/Launch/Resources/Version.h:59 |
| ENGINE_PATCH_VERSION | 4 | Engine/Source/Runtime/Launch/Resources/Version.h:60 |
| static_assert | `5 == 5 && 7 == 7 && 4 == 4` | Engine/Source/Runtime/Launch/Resources/Version.h:67 |

## 版本确认结果

**已确认：当前源码版本为 Unreal Engine 5.7.4。**

证据：
- `Engine/Build/Build.version` 中 `"MajorVersion": 5, "MinorVersion": 7, "PatchVersion": 4`
- `Engine/Source/Runtime/Launch/Resources/Version.h` 中 `ENGINE_MAJOR_VERSION=5, ENGINE_MINOR_VERSION=7, ENGINE_PATCH_VERSION=4`
- `static_assert(ENGINE_MAJOR_VERSION == 5 && ENGINE_MINOR_VERSION == 7 && ENGINE_PATCH_VERSION == 4)` 编译时校验通过
- `BranchName` 为 `"UE5"`，无特定发布分支标记
- `CompatibleChangelist` 为 `47537391`
- `IsLicenseeVersion` 为 `0`，表示这是 Epic 官方版本，非 Licensee 修改版

## 构建 ID

由于没有 `BUILT_FROM_CHANGELIST` 和 `BRANCH_NAME` 的预定义宏，`ENGINE_VERSION_STRING` 将输出：
`5.7.4`（不带 changelist 后缀）

## 相关文件

- `Engine/Build/Build.version` — 版本描述 JSON
- `Engine/Source/Runtime/Launch/Resources/Version.h` — 版本宏定义
- `GenerateProjectFiles.bat` — 项目生成脚本
- `GenerateProjectFiles.sh` — Unix 项目生成脚本
