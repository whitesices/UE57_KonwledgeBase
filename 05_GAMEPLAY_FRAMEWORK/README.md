# Gameplay 框架总览

## 摘要
UE5.7.4 Gameplay 框架定义了游戏的基本结构：World、GameInstance、GameMode、GameState、PlayerController、Actor、Component 等核心概念。

## 核心类层级
```
UObject
  → UEngine → UGameEngine / UUnrealEdEngine
  → UGameInstance
  → UWorld
  → AActor → APawn → ACharacter
  → UActorComponent → USceneComponent → UPrimitiveComponent
  → AGameModeBase → AGameMode
  → AGameStateBase → AGameState
  → APlayerController → APlayerCameraManager
```

## 生命周期
```
GameInstance 创建 → UWorld 初始化 → AGameMode 生成
  → APlayerController 加入 → APawn 生成
  → 每帧 Tick → 关卡切换 → 销毁
```

## 文档索引
- [World.md](World.md) — UWorld 详解
- [Actor.md](Actor.md) — AActor 详解
- [Component.md](Component.md) — UActorComponent 详解
- [Tick.md](Tick.md) — Tick 系统详解
- [Subsystem.md](Subsystem.md) — Subsystem 系统详解
- [PlayerController.md](PlayerController.md) — 玩家控制器
- [GameMode_GameState.md](GameMode_GameState.md) — 游戏模式与状态
