#\!/bin/bash

# KIM自动推送定时任务配置脚本
# 配置：每周一、周四上午11:00推送

echo "======================================"
echo "KIM自动推送定时任务配置（每周一、周四11:00）"
echo "======================================"

# 1. 卸载旧任务（如果存在）
echo "1. 卸载旧任务..."
launchctl unload ~/Library/LaunchAgents/com.ad-insight.kim-push.plist 2>/dev/null || true

# 2. 复制plist文件到LaunchAgents
echo "2. 复制plist文件..."
cp com.ad-insight.kim-push.plist ~/Library/LaunchAgents/

# 3. 加载新任务
echo "3. 加载新任务..."
launchctl load ~/Library/LaunchAgents/com.ad-insight.kim-push.plist

# 4. 验证任务状态
echo "4. 验证任务状态..."
launchctl list | grep com.ad-insight.kim-push

echo ""
echo "======================================"
echo "✅ 配置完成！"
echo "======================================"
echo ""
echo "📅 推送时间："
echo "   - 每周一 上午11:00"
echo "   - 每周四 上午11:00"
echo ""
echo "📝 日志文件："
echo "   - 正常日志: $(pwd)/kim_push.log"
echo "   - 错误日志: $(pwd)/kim_push_error.log"
echo ""
echo "🔍 查看任务状态："
echo "   launchctl list | grep com.ad-insight.kim-push"
echo ""
echo "🗑️  删除任务："
echo "   launchctl unload ~/Library/LaunchAgents/com.ad-insight.kim-push.plist"
echo "   rm ~/Library/LaunchAgents/com.ad-insight.kim-push.plist"
echo ""
echo "🧪 手动测试推送："
echo "   python3 kim_push.py"
echo ""

