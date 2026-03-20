# KIM Webhook服务 - 快速上手

## 🎯 功能

通过手机KIM发送"更新平台"，自动触发商业化洞察平台更新。

## 🚀 快速测试（本地）

### 1. 启动服务

```bash
cd ad-insight-demo
chmod +x webhook/test_local.sh
./webhook/test_local.sh
```

### 2. 测试健康检查

```bash
curl http://localhost:5000/health
```

### 3. 测试手动触发

```bash
curl -X POST http://localhost:5000/trigger \
     -H "Content-Type: application/json" \
     -d '{"user": "litianyu6"}'
```

### 4. 模拟KIM消息

```bash
curl -X POST http://localhost:5000/webhook \
     -H "Content-Type: application/json" \
     -d '{
       "msgtype": "text",
       "text": {"content": "更新平台"},
       "sender": {"username": "litianyu6", "name": "李天宇"}
     }'
```

## 📦 部署到容器云

详细步骤请查看 [DEPLOY.md](./DEPLOY.md)

### 简化步骤：

1. **构建镜像**
   ```bash
   docker build -t kim-webhook:latest .
   ```

2. **推送到容器镜像仓库**
   ```bash
   docker push registry.kuaishou.com/your-namespace/kim-webhook:latest
   ```

3. **在容器云创建服务**
   - 镜像地址：`registry.kuaishou.com/your-namespace/kim-webhook:latest`
   - 环境变量：
     - `KIM_ROBOT_KEY`: 你的机器人key
     - `ALLOWED_USERS`: 允许触发的用户列表
   - 端口：8080

4. **配置KIM机器人Outgoing Webhook**
   - URL: `http://kim-webhook.internal/webhook`

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `KIM_ROBOT_KEY` | KIM机器人的webhook key | 必填 |
| `ALLOWED_USERS` | 允许触发的用户名（逗号分隔） | `litianyu6,litianyu03` |
| `PORT` | 服务端口 | `8080` |

### 触发关键词

以下任一关键词都可触发更新：
- `更新平台`
- `更新洞察`
- `update`
- `刷新平台`

## 📝 使用流程

1. **在KIM群聊发送**："更新平台"
2. **收到确认消息**："🚀 平台更新已启动..."
3. **等待2-3分钟**
4. **收到完成通知**："✅ 平台更新完成"
5. **刷新网页**查看最新内容

## 🐛 常见问题

### Q1: 消息发送后没反应？

- 检查服务是否正常运行：`curl http://kim-webhook.internal/health`
- 查看日志：`kubectl logs -f deployment/kim-webhook`
- 确认KIM机器人Webhook配置正确

### Q2: 提示"无权限"？

- 检查你的用户名是否在 `ALLOWED_USERS` 中
- 重启服务使环境变量生效

### Q3: 更新失败？

- 查看webhook日志：`tail -f webhook.log`
- 查看更新脚本日志：`tail -f scripts/update_platform.log`
- 确认SSH密钥配置正确（用于Git push）

## 📞 联系支持

- 查看详细文档：[DEPLOY.md](./DEPLOY.md)
- 提交issue到项目仓库
- 联系KIM服务端团队

---

**现在你可以随时随地通过手机KIM更新平台了！** 📱✨
