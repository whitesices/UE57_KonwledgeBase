# 动画系统总览

## 摘要
UE5.7.4 动画系统基于 SkeletalMesh 和 AnimGraph 架构，支持动画蓝图、混合空间、状态机、Root Motion 等。

## 核心模块
- AnimationCore — 动画核心算法（IK、FABRIK）
- AnimGraphRuntime — 动画图运行时
- Engine 中的动画相关类 — USkeleton, UAnimSequence, UAnimBlueprint

## 关键类层级
```
UAnimationAsset
  → UAnimSequence — 动画序列
  → UAnimMontage — 动画蒙太奇
  → UBlendSpace — 混合空间
  → UAnimBlueprint — 动画蓝图

UAnimInstance — 动画实例（运行时）
  → UAnimInstanceProxy — 线程安全代理

USkeletalMeshComponent — 骨骼网格组件
  → FAnimSceneProxy — 渲染代理
```

## 动画评估流程
```
USkeletalMeshComponent::TickComponent
  → UAnimInstance::UpdateAnimation()
    → AnimGraph Evaluate (BP 节点)
      → FAnimNode_Base::Evaluate()
        → 输出 FComponentSpacePoseContext
  → USkinnedMeshComponent::UpdateSkelPose
    → ComputeWarping / RootMotion
```

## 文档索引
- [SkeletalMesh.md](SkeletalMesh.md) — 骨骼网格
- [Skeleton.md](Skeleton.md) — 骨骼
- [AnimSequence.md](AnimSequence.md) — 动画序列
- [AnimBlueprint.md](AnimBlueprint.md) — 动画蓝图
- [AnimGraph.md](AnimGraph.md) — 动画图
- [RootMotion.md](RootMotion.md) — Root Motion
