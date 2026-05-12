# Property 系统详解

## 摘要

UE5.7.4 的 Property 系统是反射系统的核心组成部分，通过 FProperty 及其子类描述 UObject 中的每个成员变量，支持编辑器显示、序列化、GC 追踪、网络复制和 Blueprint 访问。

---

## 1. FProperty 类层级

```
FProperty (基类)
├── FNumericProperty — 数值类型
│   ├── FInt8Property, FInt16Property, FIntProperty, FInt64Property
│   ├── FUInt16Property, FUInt32Property, FUInt64Property
│   └── FFloatProperty, FDoubleProperty
├── FBoolProperty — 布尔类型
├── FStrProperty — FString
├── FNameProperty — FName
├── FTextProperty — FText
├── FObjectProperty — UObject*
│   ├── FWeakObjectProperty — TWeakObjectPtr
│   ├── FLazyObjectProperty — TLazyObjectPtr
│   ├── FSoftObjectProperty — TSoftObjectPtr
│   └── FClassProperty — UClass*
├── FInterfaceProperty — TScriptInterface
├── FEnumProperty — UEnum 枚举
├── FStructProperty — UStruct 结构体
├── FArrayProperty — TArray
├── FMapProperty — TMap
├── FSetProperty — TSet
├── FDelegateProperty — 单播委托
├── FMulticastDelegateProperty — 多播委托
├── FFieldPathProperty — FFieldPath
└── FOptionalProperty — TOptional
```

## 2. FProperty 关键成员

| 成员 | 类型 | 描述 |
|------|------|------|
| ArrayDim | int32 | 数组维度（通常为1） |
| ElementSize | int32 | 单个元素大小（字节） |
| PropertyFlags | EPropertyFlags | 属性标志 |
| RepIndex | int32 | 复制索引 |
| Offset_Internal | int32 | 在结构体中的偏移量 |
| Name | FName | 属性名称 |

## 3. EPropertyFlags 关键标志

| 标志 | 描述 |
|------|------|
| CPF_Edit | 可在编辑器中编辑 |
| CPF_BlueprintVisible | Blueprint 可见 |
| CPF_BlueprintReadOnly | Blueprint 只读 |
| CPF_Net | 网络复制 |
| CPF_Transient | 不序列化 |
| CPF_DuplicateTransient | 复制时忽略 |
| CPF_SaveGame | SaveGame 序列化 |
| CPF_DisableEditOnTemplate | 禁止编辑 CDO |
| CPF_DisableEditOnInstance | 禁止编辑实例 |
| CPF_MetaData | 元数据 |

## 4. UPROPERTY() 宏参数到 Flags 的映射

```
EditAnywhere → CPF_Edit | CPF_DisableEditOnInstance = false
EditDefaultsOnly → CPF_Edit | CPF_DisableEditOnInstance
EditInstanceOnly → CPF_Edit | CPF_DisableEditOnTemplate
BlueprintReadWrite → CPF_BlueprintVisible
BlueprintReadOnly → CPF_BlueprintVisible | CPF_BlueprintReadOnly
Replicated → CPF_Net
ReplicatedUsing=XXX → CPF_Net | CPF_RepNotify
Transient → CPF_Transient
SaveGame → CPF_SaveGame
```

## 5. Property 访问接口

```cpp
// FProperty 通用接口
virtual void GetPropertyValueText(void* Data) const;
virtual void SetPropertyValueText(void* Data, const FString& Value) const;
virtual void ExportTextItem(FString& ValueStr, const void* Data, ...) const;
virtual void ImportTextItem(const TCHAR* Buffer, void* Data, ...) const;
virtual void SerializeItem(FStructuredArchive::FSlot Slot, void* Value, ...) const;
virtual void CopySingleValue(void* Dest, const void* Src) const;
virtual bool Identical(const void* A, const void* B) const;
```

## 6. 运行时属性遍历

```cpp
// 遍历 UObject 的所有属性
for (FProperty* Property = GetClass()->PropertyLink; Property; Property = Property->PropertyLinkNext)
{
    void* Value = Property->ContainerPtrToValuePtr<void>(this);
    // 访问属性值
}

// 按名查找
FProperty* FoundProp = GetClass()->FindPropertyByName(FName("MyProperty"));
```

## 7. 属性与编辑器

Property 系统与编辑器 Details Panel 紧密集成：
- IDetailCustomization — 自定义属性显示
- IPropertyTypeCustomization — 自定义类型显示
- PropertyEditor 模块 — 属性编辑器框架

## 8. 属性与网络复制

```cpp
// 网络复制自动使用 Property 系统
void AMyActor::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);
    DOREPLIFETIME(AMyActor, Health);
    DOREPLIFETIME_CONDITION(AMyActor, Ammo, COND_OwnerOnly);
}
```

DOREPLIFETIME 宏展开后，使用 FProperty 的 RepIndex 进行属性复制。

## 9. 源码证据

- Engine/Source/Runtime/CoreUObject/Public/UObject/UnrealType.h — FProperty 定义
- Engine/Source/Runtime/CoreUObject/Private/UObject/PropertyHelper.cpp
- Engine/Source/Runtime/CoreUObject/Public/UObject/ObjectMacros.h — UPROPERTY 宏

---

## 相关文档

- [UObject.md](UObject.md)
- [UClass_Reflection.md](UClass_Reflection.md)
- [GC.md](GC.md)
