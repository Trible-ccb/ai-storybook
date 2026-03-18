# AI 个性化绘本定制平台

一个基于 AI 技术的个性化绘本生成平台，将孩子的异想天开变成专属绘本。

## 项目简介

本平台利用通义千问大语言模型和通义万相图像生成技术，为3-12岁的儿童创作独一无二的个性化绘本。家长只需上传孩子和玩具的照片，填写基本信息，描述孩子的创意想法，AI 就会自动生成适合该年龄段的故事和精美插图。

## 核心功能

- 🎯 **角色真实**：上传孩子照片，主角就是孩子自己
- 🤖 **AI 智能创作**：先进大模型生成适合孩子年龄的故事
- 🎨 **精美插图**：多种风格可选（水彩、卡通、国风），角色一致性保证
- ⏱️ **快速生成**：5-10分钟完成整个绘本制作
- 📄 **PDF 导出**：支持生成高清 PDF 格式绘本

## 技术栈

### 后端
- Python 3.9+
- Flask (Web 框架)
- 通义千问 API (故事生成)
- 通义万相 API (图像生成)
- MySQL (数据存储)
- Redis (缓存)
- 阿里云 OSS (对象存储)

### 前端
- Vue 3
- Vite (构建工具)
- Element Plus (UI 组件库)
- Vue Router (路由)
- Axios (HTTP 客户端)
- html2pdf.js (PDF 生成)

## 快速开始

### 前置要求

- Python 3.9+
- Node.js 18+
- 阿里云账号（开通通义千问和通义万相服务）

### 后端配置

1. 克隆项目
```bash
git clone https://github.com/Trible-ccb/ai-storybook.git
cd ai-storybook/backend
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 API 密钥和配置
```

4. 初始化数据库
```bash
python -c "from app.models import db; from app import create_app; app = create_app(); app.app_context().push(); db.create_all()"
```

5. 启动后端服务
```bash
python app/main.py
```

后端服务将运行在 `http://localhost:5000`

### 前端配置

1. 进入前端目录
```bash
cd frontend
```

2. 安装依赖
```bash
pnpm install
```

3. 启动开发服务器
```bash
pnpm run dev
```

前端服务将运行在 `http://localhost:3000`

---

## 🚀 云端部署（推荐）

### 一键部署（免费）

如果你想快速部署到云端并获取公网访问地址，我们有以下选项：

#### 方法一：使用自动化脚本（最简单）

```bash
# 克隆项目
git clone https://github.com/Trible-ccb/ai-storybook.git
cd ai-storybook

# 运行一键部署脚本
chmod +x deploy.sh
./deploy.sh
```

脚本会自动：
- ✅ 部署前端到 Vercel（免费）
- ✅ 指导部署后端到 Render（免费）
- ✅ 配置前后端连接
- ✅ 提供公网访问地址

#### 方法二：手动部署

详见：[DEPLOYMENT.md](DEPLOYMENT.md) - 完整的云端部署指南

**部署平台**：
- **前端**：Vercel（免费，全球 CDN，自动 HTTPS）
- **后端**：Render（免费套餐，Python 托管）

**总费用**：完全免费 ✅

**部署后访问地址**：
- 前端：`https://ai-storybook-xxxx.vercel.app`
- 后端：`https://ai-storybook-backend.onrender.com`

---

## 项目结构

```
ai-storybook/
├── backend/
│   ├── app/
│   │   ├── api/          # API 路由
│   │   ├── services/     # 业务逻辑
│   │   │   ├── llm_service.py      # 故事生成服务
│   │   │   ├── image_service.py    # 图像生成服务
│   │   │   └── pdf_service.py      # PDF 生成服务
│   │   ├── models/       # 数据模型
│   │   └── main.py       # Flask 应用入口
│   ├── requirements.txt  # Python 依赖
│   └── .env.example      # 环境变量模板
├── frontend/
│   ├── src/
│   │   ├── views/        # 页面组件
│   │   │   ├── Home.vue        # 首页
│   │   │   ├── Create.vue      # 创作页面
│   │   │   ├── Preview.vue     # 预览页面
│   │   │   └── Payment.vue     # 支付页面
│   │   ├── api/          # API 调用
│   │   └── router/       # 路由配置
│   └── package.json      # Node 依赖
├── TECH_STACK.md         # 技术选型文档
└── README.md             # 项目说明
```

## API 接口

### 故事生成
- `POST /api/story/generate` - 根据输入参数生成故事文本

### 图像生成
- `POST /api/image/generate` - 生成故事插图

### 完整绘本生成
- `POST /api/storybook/generate-complete` - 一键生成完整绘本（故事+插图+PDF）

## 价格方案

| 版本 | 价格 | 页数 | 特色 |
|------|------|------|------|
| 基础版 | ¥99 | 12页 | PDF 格式、单一风格、5分钟生成 |
| 标准版 | ¥199 | 16页 | PDF + 有声、3种风格、优先生成 |
| 尊享版 | ¥399 | 20页 | PDF + 有声 + AR、精装实体书、专属客服 |

**首单优惠**：下单立减 30 元！

## 年龄适配

- **3-5岁**：简单词汇、短句、重复结构、鲜艳插图
- **6-8岁**：适中词汇、完整故事、教育主题
- **9-12岁**：丰富词汇、复杂情节、启发思考

## 待办事项

- [ ] 集成微信支付和支付宝
- [ ] 添加用户登录系统
- [ ] 实现有声绘本功能（TTS）
- [ ] 开发 AR 互动功能
- [ ] 添加绘本分享功能
- [ ] 建立内容审核机制
- [ ] 优化生成速度
- [ ] 添加更多视觉风格

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

- 项目主页：https://github.com/Trible-ccb/ai-storybook

---

**注意**：使用本平台需要阿里云账号并开通通义千问和通义万相服务。请确保遵守阿里云 API 使用条款和相关法律法规。
