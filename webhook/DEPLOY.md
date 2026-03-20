# KIM Webhook服务部署指南

## 📋 功能说明

通过手机KIM发送"更新平台"指令，自动触发商业化洞察平台更新流程。

## 🏗️ 架构

```
手机KIM发送"更新平台"
    ↓
KIM机器人接收消息
    ↓
调用Webhook服务（快手容器云）
    ↓
执行更新脚本
    ├─ 搜索最新资讯
    ├─ AI分析生成洞察
    ├─ 更新HTML页面
    └─ 推送到GitHub
    ↓
推送结果到KIM
```

## 🚀 部署步骤

### 1. 准备工作

#### 1.1 配置KIM机器人

1. 在KIM群聊中创建自定义机器人
2. 获取Webhook URL（包含机器人key）
3. 配置机器人的Outgoing Webhook：
   - Webhook URL: `http://your-service-url/webhook`
   - 触发词：可选（建议不设置，由服务端判断）

#### 1.2 配置SSH密钥（用于Git push）

```bash
# 生成SSH密钥
ssh-keygen -t ed25519 -C "kim-webhook@kuaishou.com" -f ~/.ssh/kim_webhook

# 将公钥添加到GitHub
# 1. 复制公钥内容
cat ~/.ssh/kim_webhook.pub

# 2. 在GitHub仓库 Settings -> Deploy keys 中添加
#    勾选 "Allow write access"
```

### 2. 容器云部署

#### 2.1 构建镜像

```bash
# 在ad-insight-demo目录下
docker build -t kim-webhook:latest .
```

#### 2.2 推送到容器镜像仓库

```bash
# 登录快手容器镜像仓库
docker login registry.kuaishou.com

# 打标签
docker tag kim-webhook:latest registry.kuaishou.com/your-namespace/kim-webhook:latest

# 推送
docker push registry.kuaishou.com/your-namespace/kim-webhook:latest
```

#### 2.3 在容器云创建服务

**服务配置：**
- 镜像：`registry.kuaishou.com/your-namespace/kim-webhook:latest`
- 端口：8080
- 副本数：2（建议）
- 资源配置：
  - CPU: 0.5核
  - 内存: 512Mi

**环境变量：**
```yaml
# KIM机器人Key
KIM_ROBOT_KEY: "271996bf-7424-4c93-984f-21830b354394"

# 允许触发更新的用户（逗号分隔）
ALLOWED_USERS: "litianyu6,litianyu03"

# 端口
PORT: "8080"

# SSH私钥（用于Git push）
SSH_PRIVATE_KEY: |
  -----BEGIN OPENSSH PRIVATE KEY-----
  [你的私钥内容]
  -----END OPENSSH PRIVATE KEY-----
```

**挂载配置：**
- 将SSH私钥挂载到 `/root/.ssh/id_ed25519`
- 或通过环境变量 `SSH_PRIVATE_KEY` 传入

#### 2.4 配置Service和Ingress

```yaml
# service.yaml
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

---
# ingress.yaml（如果需要外网访问）
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: kim-webhook
spec:
  rules:
    - host: kim-webhook.your-domain.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: kim-webhook
                port:
                  number: 80
```

### 3. 配置KIM机器人Outgoing Webhook

在KIM机器人管理页面配置：

- **Webhook URL**: `http://kim-webhook.internal/webhook`（内网域名）
- **HTTP Method**: POST
- **Content-Type**: application/json

### 4. 测试

#### 4.1 健康检查

```bash
curl http://kim-webhook.internal/health
```

预期返回：
```json
{
  "status": "healthy",
  "timestamp": "2026-03-20T17:45:00",
  "service": "kim-webhook"
}
```

#### 4.2 手动触发测试

```bash
curl -X POST http://kim-webhook.internal/trigger \
     -H "Content-Type: application/json" \
     -d '{"user": "litianyu6"}'
```

#### 4.3 KIM消息测试

在KIM群聊中发送：
```
更新平台
```

应该收到回复：
```
🚀 平台更新已启动

正在执行：
1. 搜索最新商业化资讯
2. AI分析生成洞察
3. 更新HTML页面
4. 推送到GitHub

预计需要2-3分钟，请稍候...
```

## 📝 使用指南

### 触发更新

在KIM群聊中发送以下任一指令：
- `更新平台`
- `更新洞察`
- `update`
- `刷新平台`

### 权限控制

只有在 `ALLOWED_USERS` 环境变量中配置的用户可以触发更新。

默认允许用户：
- `litianyu6`
- `litianyu03`

如需添加其他用户，修改环境变量并重启服务。

### 查看日志

```bash
# 容器云控制台查看日志
# 或使用kubectl
kubectl logs -f deployment/kim-webhook -n your-namespace
```

## 🔧 故障排查

### 1. Webhook未响应

**检查：**
```bash
# 查看服务状态
kubectl get pods -n your-namespace | grep kim-webhook

# 查看日志
kubectl logs kim-webhook-xxx-xxx -n your-namespace
```

**常见问题：**
- 服务未启动：检查镜像拉取是否成功
- 端口配置错误：确认8080端口正常监听
- KIM机器人配置错误：确认Webhook URL正确

### 2. Git push失败

**检查：**
```bash
# 进入容器
kubectl exec -it kim-webhook-xxx-xxx -n your-namespace -- /bin/bash

# 测试SSH连接
ssh -T git@github.com

# 查看Git配置
git config --list
```

**常见问题：**
- SSH密钥未配置：检查环境变量或挂载
- 权限不足：确认GitHub Deploy key有写权限
- 网络问题：确认容器可以访问github.com

### 3. 更新超时

默认超时时间为5分钟，如果更新流程耗时过长：

1. 检查网络连接（搜索API、GitHub）
2. 优化更新脚本（减少搜索范围）
3. 增加超时时间（修改 `app.py` 中的 `timeout=300`）

### 4. 权限问题

如果用户无法触发更新：

1. 检查用户名是否在 `ALLOWED_USERS` 中
2. 查看日志确认用户名识别是否正确
3. 重启服务使环境变量生效

## 🔐 安全建议

1. **SSH密钥管理**
   - 使用专用密钥，不要使用个人密钥
   - 定期轮换密钥
   - 限制密钥权限（只授权需要的仓库）

2. **权限控制**
   - 严格控制 `ALLOWED_USERS` 列表
   - 定期审查用户权限
   - 记录所有触发操作

3. **KIM机器人Key保护**
   - 不要将Key硬编码
   - 使用环境变量或Secret管理
   - 定期更换Key

4. **日志审计**
   - 保留操作日志至少30天
   - 监控异常触发行为
   - 设置告警（失败率、频率等）

## 📊 监控指标

建议监控以下指标：

- **服务健康**
  - `/health` 接口响应时间
  - Pod重启次数
  - 内存/CPU使用率

- **业务指标**
  - 更新触发次数
  - 更新成功率
  - 平均更新耗时

- **告警规则**
  - 连续3次更新失败
  - 单次更新超过10分钟
  - 服务不可用超过5分钟

## 🔄 升级和维护

### 代码更新

```bash
# 1. 更新代码
git pull origin main

# 2. 重新构建镜像
docker build -t kim-webhook:v2 .

# 3. 推送新镜像
docker push registry.kuaishou.com/your-namespace/kim-webhook:v2

# 4. 更新容器云服务
kubectl set image deployment/kim-webhook \
  kim-webhook=registry.kuaishou.com/your-namespace/kim-webhook:v2 \
  -n your-namespace

# 5. 查看滚动更新状态
kubectl rollout status deployment/kim-webhook -n your-namespace
```

### 回滚

```bash
# 查看历史版本
kubectl rollout history deployment/kim-webhook -n your-namespace

# 回滚到上一版本
kubectl rollout undo deployment/kim-webhook -n your-namespace

# 回滚到指定版本
kubectl rollout undo deployment/kim-webhook --to-revision=2 -n your-namespace
```

## 📞 支持

如有问题，请联系：
- KIM服务端团队
- 容器云支持团队
- 或提交issue到项目仓库

---

**部署完成后，就可以通过手机KIM随时随地触发平台更新了！** 🎉
