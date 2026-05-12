# Claude Code / Codex 使用指南

## 摘要

本文档说明如何使用本知识库配合 Claude Code 或 Codex Agent 进行 UE5.7.4 源码分析和开发。

---

## 知识库结构

```
UE57_KnowledgeBase/
├── 00_INDEX.md          ← 全局索引（从这里开始）
├── 00_VERSION_CHECK.md  ← 版本确认
├── SCAN_RULES.md        ← 扫描规则
├── 01_SOURCE_TREE/      ← 源码目录结构
├── 02_BUILD_SYSTEM/     ← Build 系统
├── 03_ENGINE_BOOT/      ← 引擎启动
├── 04_CORE_OBJECT_SYSTEM/ ← UObject/反射/GC
├── 05_GAMEPLAY_FRAMEWORK/ ← Actor/Component/Tick
├── 06_RENDERING/        ← 渲染管线（最高优先级专题）
├── 07_ASSET_PIPELINE/   ← 资源管线
├── 08_EDITOR/           ← 编辑器
├── 09_ANIMATION/        ← 动画系统
├── 10_NETWORKING/       ← 网络系统
├── 11_UI/               ← Slate/UMG
├── 12_PLUGIN_SYSTEM/    ← 插件系统
├── 13_DEBUGGING/        ← 调试工具
├── 14_MODULE_DEEP_DIVE/ ← 模块深挖
├── 15_AGENT_INDEX/      ← Agent 索引（当前目录）
└── 99_APPENDIX/         ← 附录
```

---

## 使用方式

### 1. 查询类问题

直接阅读 `15_AGENT_INDEX/Query_Map.md`，按问题类型找到对应的文档。

### 2. 源码定位

使用 `01_SOURCE_TREE/Engine_Source_Map.md` 快速定位特定功能对应的源码文件。

### 3. 深度分析

使用 `14_MODULE_DEEP_DIVE/` 中的模块文档了解特定模块的内部实现。

### 4. RAG 检索

知识库文档已按主题切片，每个文档聚焦一个主题，适合作为 RAG 检索单元。

---

## 文档质量说明

- 所有文档均基于 UE5.7.4 源码分析
- 每篇文档包含源码证据（文件路径和行号）
- 不确定内容标记为"未确认"
- 包含 Mermaid 可视化图表
