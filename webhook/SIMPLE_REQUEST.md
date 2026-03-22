# 给研发同学的一封信

你好！我是商业分析部门的李天宇（litianyu03）。

## 🎯 我想做什么？

我维护了一个**商业化洞察平台**（https://ailiuliuliu.github.io/ad-insight-platform/），需要一个小服务帮我实现：

**在手机KIM发送"更新平台" → 自动更新平台内容 → 收到完成通知**

就这么简单！🎉

---

## 📦 我需要你帮我

**部署一个小服务**，代码我都写好了，就差部署到咱们内网了。

### 这个服务：
- ✅ 代码已写好并测试通过
- ✅ 有完整的文档和Dockerfile
- ✅ 资源占用很小（0.5核CPU + 512Mi内存）
- ✅ 预计30分钟就能部署好

---

## 📂 材料在哪里？

### GitHub仓库
https://github.com/ailiuliuliu/ad-insight-platform

### 关键文件
- `ad-insight-demo/Dockerfile` - Docker配置
- `ad-insight-demo/webhook/` - 服务代码
- `ad-insight-demo/webhook/DEPLOYMENT_REQUEST.md` - **完整部署文档**（就是这个文件）

---

## 🚀 你需要做的

### 简化版（5步搞定）

```bash
# 1. 拉代码
git clone https://github.com/ailiuliuliu/ad-insight-platform.git
cd ad-insight-platform/ad-insight-demo

# 2. 构建镜像
docker build -t kim-webhook:latest .

# 3. 推送到内网镜像仓库
docker tag kim-webhook:latest registry.kuaishou.com/your-namespace/kim-webhook:latest
docker push registry.kuaishou.com/your-namespace/kim-webhook:latest

# 4. 在容器云创建服务
#    镜像：kim-webhook:latest
#    端口：8080
#    环境变量：见下方

# 5. 告诉我服务地址
#    例如：http://kim-webhook.internal
```

### 环境变量（必须配置）

```yaml
KIM_ROBOT_KEY: "271996bf-7424-4c93-984f-21830b354394"
ALLOWED_USERS: "litianyu6,litianyu03"
PORT: "8080"
```

**注意**：还需要配置SSH密钥用于Git push，详见完整文档。

---

## ❓ 如果遇到问题

1. **看完整文档**：`webhook/DEPLOYMENT_REQUEST.md`
2. **找我**：KIM @ litianyu03
3. **看技术文档**：
   - `webhook/README.md` - 快速上手
   - `webhook/DEPLOY.md` - 详细部署文档

---

## 🙏 非常感谢

这个服务会大大提升我的工作效率！

部署好后告诉我一声，我配置一下KIM机器人就能用了。

不紧急，你方便的时候帮我搞一下就行！

**再次感谢！** 🎉

---

**李天宇**  
商业分析部门  
KIM: litianyu03  
2026-03-22
