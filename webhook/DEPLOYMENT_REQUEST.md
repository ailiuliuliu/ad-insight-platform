# KIM Webhook服务部署请求

**申请人**：李天宇 (litianyu03)  
**日期**：2026-03-22  
**优先级**：中  

---

## 📋 需求说明

### 这是什么？

一个Webhook服务，用于接收KIM机器人消息，自动触发商业化洞察平台的内容更新。

### 使用场景

1. 我在外面用手机KIM发送"更新平台"
2. 自动触发平台更新（搜索资讯→AI分析→更新网页→推送GitHub）
3. 2-3分钟后收到完成通知

### 业务价值

- 随时随地更新平台，不依赖电脑
- 提升工作效率
- 自动化工作流程

---

## 🚀 部署要求

### 技术栈

- **语言**：Python 3.9+
- **框架**：Flask
- **容器化**：Docker
- **依赖**：已在`requirements.txt`中

### 资源需求

- **CPU**：0.5核
- **内存**：512Mi
- **副本数**：2（推荐）
- **端口**：8080

### 网络要求

- 需要访问内网域名：`kim-robot.internal`
- 需要访问外网：`github.com`（用于代码推送）

---

## 📦 部署内容

### 代码仓库

- **GitHub**：https://github.com/ailiuliuliu/ad-insight-platform
- **分支**：main
- **服务代码**：`webhook/` 目录
- **Dockerfile**：根目录的 `Dockerfile`

### 环境变量（必须配置）

```yaml
# KIM机器人Key
KIM_ROBOT_KEY: "271996bf-7424-4c93-984f-21830b354394"

# 允许触发的用户（逗号分隔）
ALLOWED_USERS: "litianyu6,litianyu03"

# 服务端口
PORT: "8080"

# SSH私钥（用于Git push）
# 注意：需要配置GitHub Deploy Key
SSH_PRIVATE_KEY: |
  -----BEGIN OPENSSH PRIVATE KEY-----
  [需要生成并配置，见下方说明]
  -----END OPENSSH PRIVATE KEY-----
```

---

## 🔑 SSH密钥配置（重要）

服务需要推送代码到GitHub，需要配置SSH密钥。

### 步骤1：生成SSH密钥

```bash
ssh-keygen -t ed25519 -C "kim-webhook@kuaishou.com" -f ~/.ssh/kim_webhook
```

### 步骤2：在GitHub配置Deploy Key

1. 打开：https://github.com/ailiuliuliu/ad-insight-platform/settings/keys
2. 点击 "Add deploy key"
3. 粘贴公钥内容（`~/.ssh/kim_webhook.pub`）
4. **必须勾选** "Allow write access"
5. 保存

### 步骤3：将私钥配置到环境变量

复制 `~/.ssh/kim_webhook` 的内容，配置到 `SSH_PRIVATE_KEY` 环境变量中。

---

## 🔌 KIM机器人配置

### 我这边需要做的：

1. 确认KIM机器人Webhook Key：`271996bf-7424-4c93-984f-21830b354394`
2. 配置Outgoing Webhook URL（等服务部署好后配置）

### 服务部署好后告诉我：

- 服务的内网访问地址（例如：`http://kim-webhook.internal`）
- 我会配置KIM机器人指向这个地址

---

## 📝 部署步骤（研发同学执行）

### 1. 拉取代码

```bash
git clone https://github.com/ailiuliuliu/ad-insight-platform.git
cd ad-insight-platform/ad-insight-demo
```

### 2. 构建Docker镜像

```bash
docker build -t kim-webhook:latest .
```

### 3. 推送到容器镜像仓库

```bash
# 登录
docker login registry.kuaishou.com

# 打标签（替换your-namespace）
docker tag kim-webhook:latest registry.kuaishou.com/your-namespace/kim-webhook:latest

# 推送
docker push registry.kuaishou.com/your-namespace/kim-webhook:latest
```

### 4. 在容器云创建服务

- **服务名称**：`kim-webhook`
- **镜像**：`registry.kuaishou.com/your-namespace/kim-webhook:latest`
- **端口**：8080
- **副本数**：2
- **环境变量**：见上方"环境变量"部分

### 5. 创建Service（内网访问）

```yaml
apiVersion: v1
kind: Service
metadata:
  name: kim-webhook
spec:
  selector:
    app: kim-webhook
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
```

---

## ✅ 验证测试

### 健康检查

```bash
curl http://kim-webhook.internal/health
```

**预期响应：**
```json
{
  "status": "healthy",
  "service": "kim-webhook",
  "timestamp": "2026-03-22T..."
}
```

### 功能测试

我会在KIM群聊发送"更新平台"，验证是否能触发更新。

---

## 📚 详细文档

如需更多技术细节，请查看：

- **快速上手**：`webhook/README.md`
- **详细部署文档**：`webhook/DEPLOY.md`
- **完整指南**：`KIM_WEBHOOK_GUIDE.md`
- **部署检查清单**：`webhook/DEPLOYMENT_CHECKLIST.md`

所有文档都在代码仓库中。

---

## 🐛 常见问题

### Q1: 无法连接 kim-robot.internal？

**A**: 确认服务部署在内网环境，且DNS配置正确。

### Q2: Git push失败？

**A**: 检查SSH密钥配置，确认GitHub Deploy Key有写权限。

### Q3: 服务启动失败？

**A**: 查看日志，检查环境变量是否配置正确。

---

## 📞 联系方式

**业务方（我）**：
- 姓名：李天宇
- KIM：litianyu03
- 如有问题随时联系

**预计部署时间**：1小时内

**紧急程度**：不紧急，方便时帮忙部署即可

---

## 🎁 部署完成后

部署完成后，请告诉我：

1. 服务的内网访问地址（例如：`http://kim-webhook.internal`）
2. 服务是否正常运行（健康检查是否通过）

我会配置KIM机器人，然后就可以使用了！

**非常感谢！** 🙏
