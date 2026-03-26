#\!/bin/bash

echo "======================================"
echo "重新加载KIM定时任务（修复环境变量问题）"
echo "======================================"

# 1. 卸载旧任务
echo "1. 卸载旧任务..."
launchctl unload ~/Library/LaunchAgents/com.ad-insight.kim-push.plist 2>/dev/null || true

# 2. 复制新配置
echo "2. 复制新配置文件..."
cp com.ad-insight.kim-push.plist ~/Library/LaunchAgents/

# 3. 加载新任务
echo "3. 加载新任务..."
launchctl load ~/Library/LaunchAgents/com.ad-insight.kim-push.plist

# 4. 验证状态
echo "4. 验证任务状态..."
launchctl list | grep com.ad-insight.kim-push

echo ""
echo "======================================"
echo "✅ 任务重新加载完成！"
echo "======================================"
echo ""
echo "🔧 本次修复："
echo "   - 添加PATH环境变量"
echo "   - 添加PYTHONPATH指向依赖库"
echo "   - 添加HOME环境变量"
echo ""
echo "📅 下次推送时间："
echo "   - 2026-03-31 (下周一) 11:00"
echo "   - 2026-04-03 (下周四) 11:00"
echo ""
echo "⚠️  今天不会再推送（已手动推过）"
echo ""

