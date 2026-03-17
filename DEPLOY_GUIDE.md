# 部署指南

## 📦 已完成的准备工作

✅ Git 仓库已初始化  
✅ README.md 已创建  
✅ Favicon 已添加（favicon.svg）  
✅ 链接已修复（GitHub 链接指向正确仓库）  
✅ 代码已提交到本地仓库

## 🚀 接下来的部署步骤

### 步骤 1：在 GitHub 上创建仓库

1. 访问 https://github.com/new
2. 填写以下信息：
   - **Repository name**: `ad-insight-platform`
   - **Description**: `商业化洞察平台 - 系统化追踪广告行业核心动态`
   - **Visibility**: **Public**（公开）
   - **❌ 不要勾选** "Add a README file"（我们已经有了）
   - **❌ 不要勾选** "Add .gitignore"
   - **❌ 不要勾选** "Choose a license"
3. 点击 **Create repository** 按钮

### 步骤 2：推送代码到 GitHub

在仓库创建成功后，执行以下命令：

```bash
cd ~/Documents/超级小李/ad-insight-demo

# 添加远程仓库
git remote add origin https://github.com/ailiuliuliu/ad-insight-platform.git

# 推送代码
git push -u origin main
```

或者直接运行准备好的脚本：

```bash
cd ~/Documents/超级小李/ad-insight-demo
./deploy.sh
```

### 步骤 3：配置 GitHub Pages

推送成功后：

1. 访问仓库页面：https://github.com/ailiuliuliu/ad-insight-platform
2. 点击 **Settings** 标签
3. 在左侧菜单中找到 **Pages**
4. 在 **Source** 部分：
   - Branch: 选择 `main`
   - Folder: 选择 `/ (root)`
5. 点击 **Save**
6. 等待 30-60 秒，页面会显示：
   ```
   Your site is live at https://ailiuliuliu.github.io/ad-insight-platform/
   ```

### 步骤 4：验证线上访问

1. 打开浏览器访问：https://ailiuliuliu.github.io/ad-insight-platform/
2. 检查：
   - [ ] 页面能正常加载
   - [ ] Favicon 图标显示正常
   - [ ] 标签切换功能正常
   - [ ] 侧边栏知识库可以正常打开/关闭
   - [ ] GitHub 链接可以正常跳转
3. 如果遇到 404 错误，等待 1-2 分钟后刷新（GitHub Pages 需要部署时间）

## 📝 最终交付

部署成功后，你将获得：

- **线上地址**: https://ailiuliuliu.github.io/ad-insight-platform/
- **源码地址**: https://github.com/ailiuliuliu/ad-insight-platform
- **所有人都可以访问** ✅
- **链接可以正常打开** ✅

## 🔧 后续更新

如果需要更新内容，按以下流程：

```bash
cd ~/Documents/超级小李/ad-insight-demo

# 1. 修改文件（如 index.html）

# 2. 提交更改
git add .
git commit -m "更新说明"

# 3. 推送到 GitHub
git push origin main

# 4. 等待 GitHub Pages 自动部署（30-60秒）

# 5. 刷新页面验证
```

## ❓ 常见问题

### Q: 推送时需要输入密码？

A: GitHub 不再支持密码认证，需要使用 Personal Access Token (PAT)：
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成后复制 token
5. 推送时用 token 替代密码

### Q: 页面显示 404？

A: 可能的原因：
1. GitHub Pages 还在部署中（等待 1-2 分钟）
2. Settings → Pages 中没有正确配置（检查 Source 设置）
3. 分支名称不对（确保是 `main` 分支）

### Q: Favicon 不显示？

A: 清除浏览器缓存：
- Chrome: Ctrl/Cmd + Shift + R
- Firefox: Ctrl/Cmd + F5
- Safari: Cmd + Option + R

## 📞 需要帮助？

如果遇到任何问题，请告诉我：
1. 具体在哪一步遇到了问题
2. 看到的错误信息是什么
3. 我会帮你解决！
