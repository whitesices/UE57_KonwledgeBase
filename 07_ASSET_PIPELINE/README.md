# 资源管线总览

## 摘要
UE5.7.4 的资源管线覆盖从资源创建、导入、注册、加载、Cook、打包到运行时热更新的完整生命周期。核心模块包括 AssetRegistry（资产注册查询）、UPackage/Package 格式（资源容器）、Cook 系统（平台数据生成）、Pak（文件打包）、IOStore（新一代存储格式）、动态加载系统（同步/异步 API）和热更新（补丁 Pak）。

## 核心流程全景

```
Editor Workflow:
  Content Browser → .uasset (UPackage) → AssetRegistry 注册

Cook Pipeline:
  源 .uasset → UCookCommandlet (CookOnTheFlyServer)
    → BeginCacheForCookedPlatformData (DDC)
    → SaveCookedPackage (.uasset + .uexp + .ubulk)
    → CreateIoStoreContainerFiles (.utoc + .ucas)
    → FPakFile::CreatePakFile (.pak)
    → 签名/加密

Runtime Loading:
  Mount Pak → FIoDispatcher → FIoStoreReader
    → LoadPackage / LoadObject<T>()
    → FLinkerLoad → 反序列化 → UObject 实例

Hot Update:
  补丁 Pak (_P.pak) → CDN Download → FPakPlatformFile::Mount
    → 高 Priority 遮蔽基础 Pak → 新内容即时可用
```

## 核心模块

| 模块 | 路径 | 职责 |
|------|------|------|
| AssetRegistry | `Engine/Source/Runtime/AssetRegistry/` | 资产发现、索引、依赖追踪 |
| CoreUObject | `Engine/Source/Runtime/CoreUObject/` | UPackage、FLinkerLoad/Save、序列化 |
| Cooker | `Engine/Source/Editor/UnrealEd/Private/Cooker/` | Cook 系统 (CookOnTheFlyServer) |
| PakFile | `Engine/Source/Runtime/PakFile/` | .pak 文件打包/挂载/加密 |
| IOStore | `Engine/Source/Runtime/Core/Private/IO/IoStore.cpp` | .utoc/.ucas 下一代存储 |
| ChunkDownloader | `Engine/Plugins/Runtime/ChunkDownloader/` | CDN 下载与热更新客户端 |

## 文档索引

| 文档 | 内容 |
|------|------|
| [AssetRegistry.md](AssetRegistry.md) | 资产注册表 — 发现、索引、查询、依赖追踪 |
| [Package.md](Package.md) | UPackage 与 Package 文件格式 — Import/Export 表、FLinkerLoad/Save、FPackageTrailer |
| [Cook.md](Cook.md) | Cook 系统 — UCookCommandlet、CookOnTheFlyServer 五阶段状态机、DDC 集成、增量 Cook |
| [IOStore.md](IOStore.md) | IOStore 存储格式 — .utoc/.ucas、FIoDispatcher、完美哈希、压缩加密、读取路径 |
| [Dynamic_Loading.md](Dynamic_Loading.md) | 动态加载 — StaticLoadObject/LoadObject、FSoftObjectPath、异步加载 ALT/EDL/ZenLoader、FStreamableManager |
| [Pak.md](Pak.md) | Pak 文件系统 — FPakFile/FPakPlatformFile、挂载/优先级、加密/签名、补丁 Pak、启动序列 |
| [Hot_Update.md](Hot_Update.md) | 热更新与补丁 — 补丁 Pak 遮蔽机制、ChunkDownloader、CDN 下载、ContentBuildId、运行时挂载 |

## 加载路径速查

```
同步加载:  LoadObject<T>() → StaticLoadObject() → LoadPackage() → FLinkerLoad
异步加载:  FStreamableManager::RequestAsyncLoad() → LoadPackageAsync() → ALT/EDL/ZenLoader
懒引用:    TSoftObjectPtr<T> → FSoftObjectPath::TryLoad() / LoadAsync()
批量:      FStreamableHandle → 多目标异步加载 + 完成回调
```

## Cook 输出文件类型

| 扩展名 | 用途 |
|--------|------|
| `.uasset` | Package 头部 + 元数据 |
| `.uexp` | Export 序列化数据 |
| `.ubulk` | 内联 Bulk Data |
| `.m.ubulk` | 内存映射 Bulk Data |
| `.opt.ubulk` | 可选 Bulk Data |
| `.utoc` | IOStore 容器目录索引 |
| `.ucas` | IOStore 容器数据归档 |
| `.pak` | Pak 文件归档 |
| `.sig` | Pak 签名文件 |
