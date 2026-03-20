#!/bin/bash
# KIM推送定时任务快速配置脚本
# 用途：一键配置每周一10点自动推送

echo "========================================="
echo "  KIM商业化洞察推送 - 定时任务配置"
echo "========================================="
echo ""

# 获取当前脚本目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_PATH=$(which python3)

echo "📍 脚本目录: $SCRIPT_DIR"
echo "🐍 Python路径: $PYTHON_PATH"
echo ""

# 检查依赖
echo "🔍 检查Python依赖..."
$PYTHON_PATH -c "import beautifulsoup4, requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 缺少依赖包，正在安装..."
    pip3 install beautifulsoup4 requests
fi
echo "✅ 依赖检查完成"
echo ""

# 测试推送
echo "🧪 测试推送功能..."
cd "$SCRIPT_DIR"
$PYTHON_PATH kim_push.py
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 推送测试成功！"
else
    echo ""
    echo "❌ 推送测试失败，请检查日志"
    exit 1
fi
echo ""

# 选择配置方式
echo "========================================="
echo "  请选择定时任务配置方式:"
echo "========================================="
echo "1. macOS launchd (推荐，系统原生)"
echo "2. cron (通用)"
echo "3. 手动配置（稍后自行配置）"
echo ""
read -p "请输入选项 [1-3]: " choice

case $choice in
    1)
        echo ""
        echo "📝 配置 launchd..."
        PLIST_FILE=~/Library/LaunchAgents/com.kuaishou.kim.push.plist
        
        cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.kuaishou.kim.push</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>$PYTHON_PATH</string>
        <string>$SCRIPT_DIR/kim_push.py</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>$SCRIPT_DIR</string>
    
    <key>StandardOutPath</key>
    <string>$SCRIPT_DIR/kim_push_launchd.log</string>
    
    <key>StandardErrorPath</key>
    <string>$SCRIPT_DIR/kim_push_launchd_error.log</string>
    
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>10</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF
        
        # 加载任务
        launchctl load "$PLIST_FILE"
        
        echo "✅ launchd配置完成！"
        echo ""
        echo "⏰ 定时任务已设置为：每周一 10:00 自动推送"
        echo ""
        echo "📝 管理命令："
        echo "   查看状态: launchctl list | grep kim.push"
        echo "   手动运行: launchctl start com.kuaishou.kim.push"
        echo "   停止任务: launchctl unload $PLIST_FILE"
        echo "   查看日志: tail -f $SCRIPT_DIR/kim_push_launchd.log"
        ;;
        
    2)
        echo ""
        echo "📝 配置 cron..."
        CRON_LINE="0 10 * * 1 cd $SCRIPT_DIR && $PYTHON_PATH kim_push.py >> kim_push_cron.log 2>&1"
        
        # 检查是否已存在
        crontab -l 2>/dev/null | grep -q "kim_push.py"
        if [ $? -eq 0 ]; then
            echo "⚠️  crontab中已存在KIM推送任务"
            read -p "是否覆盖? [y/N]: " overwrite
            if [ "$overwrite" != "y" ]; then
                echo "❌ 取消配置"
                exit 0
            fi
            # 删除旧的
            crontab -l | grep -v "kim_push.py" | crontab -
        fi
        
        # 添加新的
        (crontab -l 2>/dev/null; echo "# KIM商业化洞察推送 - 每周一10点"; echo "$CRON_LINE") | crontab -
        
        echo "✅ cron配置完成！"
        echo ""
        echo "⏰ 定时任务已设置为：每周一 10:00 自动推送"
        echo ""
        echo "📝 管理命令："
        echo "   查看任务: crontab -l"
        echo "   编辑任务: crontab -e"
        echo "   删除任务: crontab -l | grep -v kim_push.py | crontab -"
        echo "   查看日志: tail -f $SCRIPT_DIR/kim_push_cron.log"
        ;;
        
    3)
        echo ""
        echo "📖 请参考 KIM_PUSH_README.md 进行手动配置"
        ;;
        
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "========================================="
echo "  ✅ 配置完成！"
echo "========================================="
echo ""
echo "💡 提示："
echo "   - 每周一早上10点会自动推送商业化洞察到KIM"
echo "   - 如需修改推送时间，请编辑配置文件"
echo "   - 详细文档请查看: KIM_PUSH_README.md"
echo ""
