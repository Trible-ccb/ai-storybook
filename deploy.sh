#!/bin/bash

# AI 个性化绘本平台 - 一键部署脚本
# 此脚本将帮助你快速部署项目到云端

set -e

echo "======================================"
echo "  AI 个性化绘本平台 - 云端部署工具"
echo "======================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查是否安装了必要的工具
check_requirements() {
    echo -e "${YELLOW}[1/5] 检查部署环境...${NC}"

    if command -v node &> /dev/null; then
        echo -e "${GREEN}✓ Node.js 已安装${NC}"
    else
        echo -e "${RED}✗ Node.js 未安装${NC}"
        echo "请访问 https://nodejs.org/ 安装 Node.js"
        exit 1
    fi

    if command -v npm &> /dev/null; then
        echo -e "${GREEN}✓ npm 已安装${NC}"
    else
        echo -e "${RED}✗ npm 未安装${NC}"
        exit 1
    fi

    echo ""
}

# 部署前端到 Vercel
deploy_frontend() {
    echo -e "${YELLOW}[2/5] 准备部署前端到 Vercel...${NC}"
    echo ""

    cd frontend

    # 检查是否安装了 Vercel CLI
    if ! command -v vercel &> /dev/null; then
        echo "安装 Vercel CLI..."
        npm install -g vercel
    fi

    echo "开始部署前端..."
    echo "请按照提示操作："
    echo "1. 登录你的 Vercel 账号（如果没有账号，会自动创建）"
    echo "2. 确认项目配置"
    echo ""

    vercel --prod

    echo -e "${GREEN}✓ 前端部署完成！${NC}"
    echo ""

    cd ..
}

# 部署后端到 Render
deploy_backend() {
    echo -e "${YELLOW}[3/5] 准备部署后端到 Render...${NC}"
    echo ""

    echo "后端需要手动部署到 Render，请按照以下步骤："
    echo ""
    echo "1. 访问：https://render.com/register"
    echo "2. 使用 GitHub 账号登录"
    echo "3. 点击 'New +' → 'Web Service'"
    echo "4. 选择仓库：Trible-ccb/ai-storybook"
    echo "5. Root Directory 设置为：backend"
    echo "6. Runtime 选择：Python 3"
    echo "7. 配置环境变量（参考 DEPLOYMENT.md）"
    echo "8. 点击 'Create Web Service'"
    echo ""

    read -p "完成上述步骤后，按 Enter 继续..."

    echo -e "${GREEN}✓ 后端部署完成！${NC}"
    echo ""
}

# 配置前后端连接
configure_connection() {
    echo -e "${YELLOW}[4/5] 配置前后端连接...${NC}"
    echo ""

    echo "请输入你的后端地址（例如：https://ai-storybook-backend.onrender.com）："
    read BACKEND_URL

    if [ -z "$BACKEND_URL" ]; then
        echo -e "${RED}错误：后端地址不能为空${NC}"
        exit 1
    fi

    # 更新前端 API 配置
    echo "更新前端 API 配置..."
    sed -i.bak "s|VITE_API_URL:.*|VITE_API_URL: '${BACKEND_URL}/api',|g" frontend/src/api/index.js
    rm frontend/src/api/index.js.bak

    echo ""
    echo -e "${GREEN}✓ 前后端连接配置完成！${NC}"
    echo ""
    echo "后端地址：$BACKEND_URL"
    echo ""

    # 提示重新部署前端
    echo "需要重新部署前端以应用更改..."
    read -p "是否现在重新部署前端？(y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd frontend
        vercel --prod
        cd ..
        echo -e "${GREEN}✓ 前端重新部署完成！${NC}"
    fi
}

# 显示部署信息
show_info() {
    echo -e "${YELLOW}[5/5] 部署完成！${NC}"
    echo ""
    echo "======================================"
    echo "  🎉 部署成功！"
    echo "======================================"
    echo ""
    echo "你的项目现在已经部署到云端！"
    echo ""
    echo "访问地址："
    echo "  - 前端：https://ai-storybook-xxxx.vercel.app"
    echo "  - 后端：${BACKEND_URL:-https://ai-storybook-backend.onrender.com}"
    echo ""
    echo "下一步："
    echo "  1. 访问前端地址，测试功能"
    echo "  2. 如果遇到问题，查看 DEPLOYMENT.md 文档"
    echo "  3. 根据需要调整配置"
    echo ""
    echo "更多帮助："
    echo "  - 查看文档：DEPLOYMENT.md"
    echo "  - 查看代码：https://github.com/Trible-ccb/ai-storybook"
    echo ""
}

# 主函数
main() {
    check_requirements
    deploy_frontend
    deploy_backend
    configure_connection
    show_info
}

# 运行主函数
main
