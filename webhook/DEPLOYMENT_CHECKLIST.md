# 🚀 KIM Webhook部署检查清单

## 📋 部署前准备

### 1. 容器云信息
- [ ] 容器云平台：________（例如：快手容器云、K8s集群）
- [ ] 容器镜像仓库地址：________（例如：registry.kuaishou.com）
- [ ] Namespace：________（例如：commercial-insight）
- [ ] 有权限操作容器云：是 / 否

### 2. KIM机器人信息
- [ ] 已有KIM自定义机器人：是 / 否
  - 如果有：
    - 机器人名称：________
    - Webhook Key：`271996bf-7424-4c93-984f-21830b354394`
  - 如果没有：需要先创建

### 3. GitHub配置
- [ ] GitHub仓库：`ailiuliuliu/ad-insight-platform`
- [ ] 已配置SSH Deploy Key：是 / 否
- [ ] SSH私钥文件位置：`~/.ssh/kim_webhook`

### 4. 权限用户
- [ ] 允许触发的用户：`litianyu6`, `litianyu03`

---

## 🎯 部署步骤

### Step 1: 准备Docker镜像

```bash
# 1.1 构建镜像
cd ad-insight-demo
docker build -t kim-webhook:latest .

# 1.2 打标签（替换your-namespace为你的namespace）
docker tag kim-webhook:latest registry.kuaishou.com/your-namespace/kim-webhook:latest

# 1.3 登录容器镜像仓库
docker login registry.kuaishou.com

# 1.4 推送镜像
docker push registry.kuaishou.com/your-namespace/kim-webhook:latest
```

**状态**：[ ] 完成

---

### Step 2: 配置SSH密钥（用于Git push）

```bash
# 2.1 生成SSH密钥（如果还没有）
ssh-keygen -t ed25519 -C "kim-webhook@kuaishou.com" -f ~/.ssh/kim_webhook

# 2.2 复制公钥
cat ~/.ssh/kim_webhook.pub

# 2.3 在GitHub仓库添加Deploy Key
# 1. 打开 https://github.com/ailiuliuliu/ad-insight-platform/settings/keys
# 2. 点击 "Add deploy key"
# 3. 粘贴公钥内容
# 4. 勾选 "Allow write access"
# 5. 保存

# 2.4 复制私钥内容（用于容器云环境变量）
cat ~/.ssh/kim_webhook
```

**状态**：[ ] 完成

---

### Step 3: 在容器云创建服务

#### 3.1 基本配置

- **服务名称**：`kim-webhook`
- **镜像地址**：`registry.kuaishou.com/your-namespace/kim-webhook:latest`
- **副本数**：2（推荐）
- **端口**：8080

#### 3.2 资源配置

- **CPU**：0.5核
- **内存**：512Mi

#### 3.3 环境变量

```yaml
# KIM机器人Key
KIM_ROBOT_KEY: "271996bf-7424-4c93-984f-21830b354394"

# 允许触发的用户（逗号分隔）
ALLOWED_USERS: "litianyu6,litianyu03"

# 服务端口
PORT: "8080"

# SSH私钥（用于Git push）
SSH_PRIVATE_KEY: |
  -----BEGIN OPENSSH PRIVATE KEY-----
  [粘贴~/.ssh/kim_webhook的内容]
  -----END OPENSSH PRIVATE KEY-----
```

**状态**：[ ] 完成

---

### Step 4: 配置Service（内网访问）

```yaml
apiVersion: v1
kind: Service
metadata:
  name: kim-webhook
  namespace: your-namespace
spec:
  selector:
    app: kim-webhook
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
```

**内网访问地址**：`http://kim-webhook.your-namespace.svc.cluster.local/webhook`

或使用快手内网域名：`http://kim-webhook.internal/webhook`

**状态**：[ ] 完成

---

### Step 5: 配置KIM机器人Outgoing Webhook

#### 5.1 如果还没有机器人

1. 在KIM群聊中：右上角 → 机器人 → 自定义机器人
2. 创建新机器人
3. 记录Webhook Key

#### 5.2 配置Outgoing Webhook

1. 进入机器人管理页面
2. 配置Outgoing Webhook：
   - **Webhook URL**：`http://kim-webhook.internal/webhook`
   - **HTTP Method**：POST
   - **Content-Type**：application/json
3. 保存配置

**状态**：[ ] 完成

---

### Step 6: 测试验证

#### 6.1 健康检查

```bash
# 方式1：在容器云内网环境
curl http://kim-webhook.internal/health

# 方式2：通过kubectl
kubectl exec -it deployment/kim-webhook -n your-namespace -- curl http://localhost:8080/health
```

**预期响应**：
```json
{
  "status": "healthy",
  "service": "kim-webhook",
  "timestamp": "2026-03-22T..."
}
```

**状态**：[ ] 完成

#### 6.2 KIM消息测试

在KIM群聊中发送：
```
更新平台
```

**预期流程**：
1. 收到确认消息："🚀 平台更新已启动..."
2. 等待2-3分钟
3. 收到完成通知："✅ 平台更新完成"

**状态**：[ ] 完成

---

## 🔍 故障排查

### 1. 查看Pod状态

```bash
kubectl get pods -n your-namespace | grep kim-webhook
```

### 2. 查看日志

```bash
kubectl logs -f deployment/kim-webhook -n your-namespace
```

### 3. 进入容器调试

```bash
kubectl exec -it deployment/kim-webhook -n your-namespace -- /bin/bash

# 测试内网连接
curl http://kim-robot.internal/health

# 测试Git
ssh -T git@github.com
```

### 4. 常见问题

| 问题 | 解决方法 |
|------|----------|
| Pod启动失败 | 检查镜像地址是否正确 |
| 无法连接KIM | 确认在内网环境，检查`kim-robot.internal`是否可访问 |
| Git push失败 | 检查SSH密钥配置，确认Deploy Key有写权限 |
| 权限错误 | 检查`ALLOWED_USERS`环境变量 |

---

## ✅ 部署完成

当所有步骤都完成后，你就可以：

📱 **在手机KIM发送"更新平台"**  
⏰ **2-3分钟后收到完成通知**  
🌐 **刷新网页查看最新洞察**

---

## 📞 需要帮助？

- 查看详细文档：`webhook/DEPLOY.md`
- 查看完整指南：`KIM_WEBHOOK_GUIDE.md`
- 提交issue到项目仓库
