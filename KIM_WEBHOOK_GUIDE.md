# 🎉 KIM消息触发平台更新 - 完整方案

## 📋 项目概览

通过手机KIM发送"更新平台"消息，自动触发商业化洞察平台的全流程更新。

```
手机KIM: "更新平台"
    ↓
KIM机器人接收
    ↓
调用Webhook服务（容器云）
    ↓
执行更新流程
    ├─ 🔍 搜索最新商业化资讯
    ├─ 🤖 AI分析生成洞察
    ├─ 📝 更新HTML页面
    └─ 🚀 推送到GitHub
    ↓
💬 推送结果到KIM
```

## 📁 项目结构

```
ad-insight-demo/
├── webhook/                    # Webhook服务
│   ├── app.py                 # Flask应用（核心）
│   ├── requirements.txt       # Python依赖
│   ├── test_local.sh         # 本地测试脚本
│   ├── README.md             # 快速上手指南
│   └── DEPLOY.md             # 详细部署文档
├── scripts/
│   ├── update_platform.py    # 统一更新脚本
│   └── kim_push.py           # KIM定时推送脚本
└── Dockerfile                # 容器镜像配置
```

## 🚀 快速开始

### 方式1：本地测试（推荐先测试）

```bash
# 1. 启动Webhook服务
cd ad-insight-demo
./webhook/test_local.sh

# 2. 新开终端，测试健康检查
curl http://localhost:5000/health

# 3. 测试手动触发
curl -X POST http://localhost:5000/trigger \
     -H "Content-Type: application/json" \
     -d '{"user": "litianyu6"}'

# 4. 模拟KIM消息
curl -X POST http://localhost:5000/webhook \
     -H "Content-Type: application/json" \
     -d '{
       "msgtype": "text",
       "text": {"content": "更新平台"},
       "sender": {"username": "litianyu6"}
     }'
```

### 方式2：部署到容器云（生产环境）

```bash
# 1. 构建Docker镜像
docker build -t kim-webhook:latest .

# 2. 推送到容器镜像仓库
docker push registry.kuaishou.com/your-namespace/kim-webhook:latest

# 3. 在容器云创建服务
# - 镜像：registry.kuaishou.com/your-namespace/kim-webhook:latest
# - 端口：8080
# - 环境变量：见下方配置

# 4. 配置KIM机器人Outgoing Webhook
# - URL: http://kim-webhook.internal/webhook
```

## ⚙️ 配置说明

### 环境变量（必填）

```bash
# KIM机器人Key
KIM_ROBOT_KEY=271996bf-7424-4c93-984f-21830b354394

# 允许触发的用户（逗号分隔）
ALLOWED_USERS=litianyu6,litianyu03

# 服务端口
PORT=8080

# SSH私钥（用于Git push，容器云部署必填）
SSH_PRIVATE_KEY=|
  -----BEGIN OPENSSH PRIVATE KEY-----
  [你的私钥内容]
  -----END OPENSSH PRIVATE KEY-----
```

### KIM机器人配置

1. **创建自定义机器人**
   - 在KIM群聊中创建
   - 获取Webhook Key

2. **配置Outgoing Webhook**
   - Webhook URL: `http://kim-webhook.internal/webhook`
   - HTTP Method: POST
   - Content-Type: application/json

## 📱 使用方式

### 触发更新

在KIM群聊中发送以下任一关键词：
- `更新平台`
- `更新洞察`
- `update`
- `刷新平台`

### 执行流程

1. **你发送消息**："更新平台"
2. **收到确认**：
   ```
   🚀 平台更新已启动
   
   正在执行：
   1. 搜索最新商业化资讯
   2. AI分析生成洞察
   3. 更新HTML页面
   4. 推送到GitHub
   
   预计需要2-3分钟，请稍候...
   ```

3. **等待2-3分钟**

4. **收到完成通知**：
   ```
   ✅ 平台更新完成
   
   更新时间: 2026-03-20 17:45:00
   
   📊 更新内容
   - ✅ 搜索最新商业化资讯
   - ✅ AI生成核心洞察
   - ✅ 更新HTML页面
   - ✅ 推送到GitHub
   
   🔗 查看更新后的平台
   ```

5. **刷新网页**查看最新内容

## 🎯 核心功能

### 1. 权限控制

只有在 `ALLOWED_USERS` 中的用户可以触发更新：
- 默认：`litianyu6`, `litianyu03`
- 未授权用户会收到提示

### 2. 实时反馈

每个步骤都会通过KIM消息实时反馈：
- 🚀 开始通知
- ✅ 成功通知（含更新内容）
- ❌ 失败通知（含错误信息）

### 3. 异步执行

Webhook立即响应，更新流程在后台执行，不阻塞KIM消息处理。

### 4. 完整日志

所有操作都有详细日志记录：
- `webhook.log` - Webhook服务日志
- `update_platform.log` - 更新脚本日志

## 🔧 API接口

### 1. 健康检查

```bash
GET /health
```

响应：
```json
{
  "status": "healthy",
  "timestamp": "2026-03-20T17:45:00",
  "service": "kim-webhook"
}
```

### 2. Webhook接口（KIM机器人调用）

```bash
POST /webhook
Content-Type: application/json

{
  "msgtype": "text",
  "text": {"content": "更新平台"},
  "sender": {"username": "litianyu6", "name": "李天宇"}
}
```

### 3. 手动触发（测试用）

```bash
POST /trigger
Content-Type: application/json

{"user": "litianyu6"}
```

## 📊 监控建议

### 关键指标

- **服务健康**：`/health` 接口响应时间
- **更新成功率**：成功次数/总触发次数
- **平均耗时**：从触发到完成的时间

### 告警规则

- 连续3次更新失败 → 告警
- 单次更新超过10分钟 → 告警
- 服务不可用超过5分钟 → 告警

## 🐛 故障排查

### 问题1：消息发送后没反应

**排查步骤：**
```bash
# 1. 检查服务状态
curl http://kim-webhook.internal/health

# 2. 查看日志
tail -f webhook/webhook.log

# 3. 检查KIM机器人配置
# 确认Webhook URL正确
```

### 问题2：提示"无权限"

**解决方法：**
- 检查 `ALLOWED_USERS` 环境变量
- 确认你的用户名正确
- 重启服务使配置生效

### 问题3：更新失败

**排查步骤：**
```bash
# 1. 查看更新日志
tail -f scripts/update_platform.log

# 2. 检查Git配置
git config --list

# 3. 测试SSH连接
ssh -T git@github.com

# 4. 手动执行更新脚本
python3 scripts/update_platform.py
```

## 🔒 安全注意事项

1. **SSH密钥保护**
   - 使用专用密钥，不要用个人密钥
   - 定期轮换密钥
   - 限制密钥权限

2. **KIM机器人Key保护**
   - 不要硬编码在代码中
   - 使用环境变量
   - 定期更换Key

3. **权限控制**
   - 严格控制 `ALLOWED_USERS`
   - 记录所有触发操作
   - 定期审查用户权限

4. **日志审计**
   - 保留操作日志至少30天
   - 监控异常触发行为

## 📚 相关文档

- **快速上手**：[webhook/README.md](webhook/README.md)
- **详细部署**：[webhook/DEPLOY.md](webhook/DEPLOY.md)
- **KIM定时推送**：[scripts/KIM_PUSH_README.md](scripts/KIM_PUSH_README.md)

## 🎊 完整功能清单

现在你的商业化洞察平台拥有：

✅ **内容自动更新**
- 每周自动搜索商业化资讯
- AI分析生成核心洞察
- 自动更新HTML并部署

✅ **KIM定时推送**（每周一10点）
- 自动推送周报到KIM群聊
- Markdown格式，美观易读
- 包含最新3条核心洞察

✅ **手机随时触发**（NEW！）
- 手机KIM发送"更新平台"
- 2-3分钟完成全流程更新
- 实时反馈执行结果

✅ **权限和安全**
- 用户权限控制
- 操作日志记录
- SSH密钥保护

---

## 🚀 下一步

1. **本地测试**
   ```bash
   ./webhook/test_local.sh
   ```

2. **部署到容器云**
   - 参考 `webhook/DEPLOY.md`
   - 配置环境变量
   - 创建K8s服务

3. **配置KIM机器人**
   - 设置Outgoing Webhook
   - 测试消息触发

4. **开始使用**
   - 在KIM发送"更新平台"
   - 等待更新完成
   - 查看最新洞察

---

**现在你可以随时随地通过手机KIM更新平台了！** 📱✨🎉
