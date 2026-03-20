#!/bin/bash
# 本地测试Webhook服务

echo "========================================="
echo "  KIM Webhook本地测试"
echo "========================================="
echo ""

# 设置环境变量
export KIM_ROBOT_KEY="271996bf-7424-4c93-984f-21830b354394"
export ALLOWED_USERS="litianyu6,litianyu03"
export PORT="5000"

# 检查依赖
echo "🔍 检查Python依赖..."
pip3 install -q -r webhook/requirements.txt

# 启动服务
echo ""
echo "🚀 启动Webhook服务..."
echo "   监听地址: http://localhost:5000"
echo "   健康检查: http://localhost:5000/health"
echo "   Webhook接口: http://localhost:5000/webhook"
echo ""
echo "💡 测试命令："
echo "   健康检查: curl http://localhost:5000/health"
echo "   手动触发: curl -X POST http://localhost:5000/trigger -H 'Content-Type: application/json' -d '{\"user\": \"litianyu6\"}'"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

cd webhook && python3 app.py
