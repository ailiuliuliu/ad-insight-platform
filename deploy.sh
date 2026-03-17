#!/bin/bash
# GitHub 部署脚本

cd ~/Documents/超级小李/ad-insight-demo

# 添加 GitHub 远程仓库
git remote add origin https://github.com/ailiuliuliu/ad-insight-platform.git

# 推送代码
git push -u origin main

echo "✅ 代码推送成功！"
echo "⏳ 正在配置 GitHub Pages..."
