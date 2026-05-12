# UI 系统总览

## 摘要
UE5.7.4 的 UI 系统由两层组成：底层 Slate（C++ 原生 UI 框架）和上层 UMG（Blueprint 可视化 UI 框架）。

## 核心模块
- SlateCore — Slate 底层（SWidget、SPanel、Invalidate）
- Slate — Slate 框架（SApplication、高级控件）
- UMG — Blueprint UI 封装（UUserWidget）
- InputCore — 输入系统接口

## Slate 架构
```
FSlateApplication (应用入口)
  → SWindow (窗口)
    → SWidget (控件基类)
      → SPanel (布局面板)
        → SOverlay / SHorizontalBox / SVerticalBox
      → SCompoundWidget (复合控件)
        → SButton / SCheckBox / SEditableText
```

## UMG 架构
```
UUserWidget (蓝图控件)
  → UPanelWidget (面板)
    → UCanvasPanel / UVerticalBox / UHorizontalBox
  → UWidget (控件基类)
    → UButton / UTextBlock / UImage
```

## 输入事件流转
```
OS Input Event → FSlateApplication::OnKeyDown/OnMouseButtonDown
  → Route through Widget Hierarchy
    → FReply Handled/Unhandled
      → PlayerController → Actor
```

## 文档索引
- [Slate.md](Slate.md) — Slate 框架
- [UMG.md](UMG.md) — UMG 框架
- [Widget_Lifecycle.md](Widget_Lifecycle.md) — Widget 生命周期
- [Input_Flow.md](Input_Flow.md) — 输入事件流转
