# UE5.7.4 知识库扫描规则

## 摘要

本文档定义 UE5.7.4 源码知识库的扫描规则、证据引用规范、增量更新策略。

---

## 1. 重点扫描目录

| 目录 | 优先级 | 说明 |
|------|--------|------|
| `Engine/Source/Runtime/` | P0 | 运行时核心模块 |
| `Engine/Source/Editor/` | P0 | 编辑器模块 |
| `Engine/Source/Developer/` | P1 | 开发者工具模块 |
| `Engine/Source/Programs/` | P1 | 独立程序（UBT, UHT, ShaderCompiler 等） |
| `Engine/Plugins/` | P1 | 内置插件 |
| `Engine/Shaders/` | P0 | Shader 源码 |
| `Engine/Binaries/` | P2 | 仅查看目录结构 |
| `Engine/Config/` | P2 | 配置文件 |
| `Engine/Content/` | P3 | 引擎内置资源 |

---

## 2. 忽略目录

以下目录在扫描时必须跳过：

```
Binaries/
Intermediate/
Saved/
DerivedDataCache/
.vs/
.git/
*.sln
*.vcxproj
*.pdb
*.obj
*.dll
*.lib
*.exp
*.ilk
*.map
```

---

## 3. 源码证据引用规范

每个重要结论必须附带源码证据，格式如下：

```
源码证据：
- Engine/Source/Runtime/Engine/Private/UnrealEngine.cpp:1234
- Engine/Source/Runtime/Renderer/Private/DeferredShadingRenderer.cpp:567
```

引用规则：
1. 使用相对于仓库根目录的相对路径
2. 包含行号
3. 引用实际源码文件，不引用生成文件（如 `.generated.h`）
4. 优先引用 `.cpp` 实现文件而非 `.h` 声明文件（除非是纯头文件模板类）

---

## 4. 不确定信息处理规范

如果无法从源码确认某个结论：

```markdown
未确认：当前扫描范围内没有找到直接源码证据。
```

处理流程：
1. 标记为"未确认"
2. 记录到 `99_APPENDIX/TODO_Unverified.md`
3. 注明推测来源（旧版本经验、文档、社区）
4. 留待后续验证

---

## 5. 增量更新规范

知识库支持增量更新：

1. 每次更新记录到 `99_APPENDIX/Update_Log.md`
2. 更新时注明日期、更新的 Phase、更新的文件
3. 已验证内容被重新确认时，更新验证日期
4. 新发现的未确认内容添加到 `TODO_Unverified.md`
5. 模块索引变更需要同步更新 `15_AGENT_INDEX/`

---

## 6. 知识库切片规范

每个文档应满足以下要求：

1. 每篇文档聚焦一个主题
2. 文档之间通过链接引用，不重复内容
3. 每篇文档开头必须有摘要
4. 每篇文档必须包含"适合解决的问题"章节
5. 文档长度建议 200-800 行，超过应考虑拆分
6. 适合作为 RAG 知识库的检索单元

---

## 7. Agent 查询索引规范

`15_AGENT_INDEX/` 目录下的索引文件必须：

1. 按问题类型组织查询入口
2. 每个查询入口指向具体的知识库文档和源码路径
3. `Symbol_Index.md` 记录关键符号（类名、函数名、宏名）
4. `Module_Index.json` 记录模块元数据（JSON 格式，便于程序化解析）
5. `Source_File_Index.json` 记录关键源码文件索引
6. `Query_Map.md` 按常见问题组织查询路径
7. `Claude_Codex_Usage_Guide.md` 提供给 Agent 的使用指南

---

## 8. 文档写作语言

所有文档使用中文。

---

## 9. 质量检查清单

每篇文档完成时自查：
- [ ] 是否有摘要？
- [ ] 是否有源码证据？
- [ ] 是否有 Mermaid 图？
- [ ] 不确定内容是否标记？
- [ ] 是否有调试建议？
- [ ] 是否有扩展点说明？
