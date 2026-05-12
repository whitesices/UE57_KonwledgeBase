# 网络系统总览

## 摘要
UE5.7.4 网络系统基于 Server-Client 架构，核心是属性复制和 RPC。

## 核心模块
- Net — 网络核心（包含 Iris 复制系统）
- Networking — TCP/UDP Socket
- Sockets — 平台 Socket 抽象
- PacketHandlers — 包处理

## 关键概念
- Replication — 属性自动同步
- RPC — 远程过程调用 (Server/Client/NetMulticast)
- NetDriver — 网络驱动 (UNetConnection, UActorChannel)
- Iris — UE5 新复制系统（Filter/Prioritizer 管线）

## 文档索引
- [Replication.md](Replication.md) — 属性复制
- [NetDriver.md](NetDriver.md) — 网络驱动
- [RPC.md](RPC.md) — 远程过程调用
- [HTTP.md](HTTP.md) — HTTP 请求
- [WebSocket.md](WebSocket.md) — WebSocket
- [PixelStreaming.md](PixelStreaming.md) — 像素流送

## 源码路径
- Engine/Source/Runtime/Net/
- Engine/Source/Runtime/Networking/
- Engine/Source/Runtime/Sockets/
- Engine/Source/Runtime/Net/Iris/
