# Tick 系统详解

## 摘要
UE5.7.4 的 Tick 系统是每帧执行逻辑的核心机制，由 FTickTaskManagerInterface 管理。

## 1. Tick 执行顺序
```
FEngineLoop::Tick()
  → UEngine::Tick()
    → UWorld::Tick()
      → FTickTaskManagerInterface::StartFrame()
        → PrePhysics Tick Group
        → DuringPhysics Tick Group（物理计算并行）
        → PostPhysics Tick Group
        → PostUpdateWork Tick Group
      → FTickTaskManagerInterface::EndFrame()
```

## 2. Tick Group
| Tick Group | 时机 | 用途 |
|-----------|------|------|
| TG_PrePhysics | 物理前 | 输入处理、角色移动 |
| TG_DuringPhysics | 物理中 | 与物理并行执行 |
| TG_PostPhysics | 物理后 | 基于物理结果的更新 |
| TG_PostUpdateWork | 更新后 | 相机更新、UI |

## 3. 关键类
- FTickFunction — Tick 函数基类
- FActorTickFunction — Actor Tick
- FComponentTickFunction — Component Tick
- FTickTaskManager — Tick 任务管理器
- FTickTaskManagerInterface — Tick 管理接口

## 4. 并行 Tick
UE5 使用 TaskGraph 系统实现 Tick 并行：
- 独立的 Actor 可以并行 Tick
- 有依赖关系的 Actor 按顺序 Tick
- 通过 Prerequisites 声明依赖

## 5. 性能优化
- SetTickFunctionEnable(false) — 禁用不需要的 Tick
- PrimaryActorTick.bStartWithTickEnabled = false — 延迟启动
- 使用 Timer 替代每帧 Tick
- 使用 Tick Interval 降低 Tick 频率

## 6. 源码证据
- Engine/Source/Runtime/Engine/Private/UnrealEngine.cpp (UEngine::Tick)
- Engine/Source/Runtime/Engine/Public/EngineBaseTypes.h (ETickingGroup)
- Engine/Source/Runtime/Engine/Private/TickTaskManager.cpp
