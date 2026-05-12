# WebSockets 模块详解

## 摘要

WebSockets 模块提供 WebSocket 协议的客户端实现，支持双向实时通信。底层使用 libWebSockets（跨平台）或 WinHTTP WebSocket API（Windows 8.1+）。用于 PixelStreaming 信令、多人游戏实时通信等场景。

---

## 1. 模块定位

WebSockets 提供：
- WebSocket 客户端连接
- 文本和二进制消息收发
- SSL/TLS 安全连接
- 事件驱动回调（Connected, Closed, Message, Error）

---

## 2. 所在路径

- **Public**: `Engine/Source/Runtime/Online/WebSockets/Public/`
- **Private**: `Engine/Source/Runtime/Online/WebSockets/Private/`
- **Build.cs**: `Engine/Source/Runtime/Online/WebSockets/WebSockets.Build.cs`

---

## 3. Build.cs 依赖关系

### 私有依赖
- `Core`, `HTTP`

---

## 4. Public API 关键类

| 类 | 文件 | 职责 |
|----|------|------|
| `IWebSocket` | `IWebSocket.h` | WebSocket 接口（事件驱动） |
| `FWebSocketsModule` | `WebSocketsModule.h` | 模块单例 |
| `IWebSocketsManager` | `IWebSocketsManager.h` | 管理器接口 |

---

## 5. 关键函数

| 函数 | 文件 | 作用 |
|------|------|------|
| `FWebSocketsModule::CreateWebSocket()` | `WebSocketsModule.h:62` | 创建 WebSocket 连接 |
| `IWebSocket::Connect()` | `IWebSocket.h:17` | 连接到服务器 |
| `IWebSocket::Send()` | `IWebSocket.h:35` | 发送消息 |
| `IWebSocket::Close()` | `IWebSocket.h:24` | 关闭连接 |

---

## 6. 初始化流程

```
FWebSocketsModule::StartupModule()
  └─ 创建平台特定的 IWebSocketsManager
      ├─ FLwsWebSocketsManager (libWebSockets)
      └─ FWinHttpWebSocketManager (WinHTTP)
```

---

## 7. 运行时调用链

```
FWebSocketsModule::CreateWebSocket(URL, Protocols)
  └─ 返回 IWebSocket 实例
      ├─ OnConnected().BindLambda(...)
      ├─ OnConnectionError().BindLambda(...)
      ├─ OnClosed().BindLambda(...)
      ├─ OnRawMessage().BindLambda(...)
      ├─ Connect()
      └─ Send(BinaryData)
```

---

## 8. 与其他模块的关系

- **依赖**: HTTP（复用基础设施）
- **被依赖**: PixelStreaming（信令服务器连接）

---

## 9. 源码证据

- `Engine/Source/Runtime/Online/WebSockets/Public/IWebSocket.h:6` — IWebSocket
- `Engine/Source/Runtime/Online/WebSockets/Public/WebSocketsModule.h:21` — FWebSocketsModule

---

## 10. 相关文档

- [HTTP 模块详解](HTTP.md)
- [PixelStreaming 模块详解](PixelStreaming.md)
