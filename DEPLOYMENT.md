# 🚀 云端部署指南

本指南将帮助你将 AI 个性化绘本平台部署到云端，并提供公网访问地址。

---

## 📋 部署方案

### 方案概述

| 组件 | 平台 | 费用 | 说明 |
|------|------|------|------|
| 前端 (Vue 3) | Vercel | 免费 | 全球 CDN，自动 HTTPS |
| 后端 (Flask) | Render | 免费 | Python 托管，自动 HTTPS |

**总费用**：免费 ✅

---

## 🎯 部署步骤

### 第一步：部署前端到 Vercel

#### 方法一：通过 Vercel Dashboard（推荐 - 最简单）

1. **访问 Vercel**
   - 打开：https://vercel.com/signup
   - 使用 GitHub 账号登录（如果已有账号，直接登录）

2. **导入项目**
   - 点击 "Add New..." → "Project"
   - 选择仓库：`Trible-ccb/ai-storybook`
   - Root Directory 设置为：`frontend`
   - Framework Preset 选择：`Vite`

3. **配置环境变量**
   - 点击 "Environment Variables"
   - 添加以下变量：
     ```
     VITE_API_URL=https://你的后端地址.onrender.com
     ```

4. **部署**
   - 点击 "Deploy" 按钮
   - 等待 1-2 分钟，部署完成

5. **获取前端地址**
   - 部署成功后，Vercel 会提供访问地址
   - 格式：`https://ai-storybook-xxxx.vercel.app`

#### 方法二：通过 Vercel CLI（自动化）

1. **安装 Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **登录 Vercel**
   ```bash
   cd frontend
   vercel login
   ```

3. **部署前端**
   ```bash
   vercel --prod
   ```

---

### 第二步：部署后端到 Render

#### 方法一：通过 Render Dashboard（推荐）

1. **访问 Render**
   - 打开：https://render.com/register
   - 使用 GitHub 账号登录

2. **创建新服务**
   - 点击 "New +" → "Web Service"
   - 选择仓库：`Trible-ccb/ai-storybook`
   - Root Directory 设置为：`backend`
   - Runtime 选择：`Python 3`

3. **配置构建和启动**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app/main.py`

4. **配置环境变量**（⚠️ 重要）
   添加以下环境变量（需要从阿里云获取）：
   ```
   QWEN_API_KEY=your_qwen_api_key_here
   WANXIANG_API_KEY=your_wanxiang_api_key_here
   OSS_ACCESS_KEY_ID=your_oss_access_key_id_here
   OSS_ACCESS_KEY_SECRET=your_oss_access_key_secret_here
   OSS_BUCKET_NAME=your_bucket_name
   OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
   DATABASE_URL=postgresql://...
   REDIS_URL=redis://...
   ```
   - 如果你还没有数据库，可以使用 Render 提供的免费 PostgreSQL
   - Redis 可以使用 Redis Cloud 的免费套餐

5. **部署**
   - 点击 "Create Web Service"
   - 等待 2-3 分钟，部署完成

6. **获取后端地址**
   - 部署成功后，Render 会提供访问地址
   - 格式：`https://ai-storybook-backend.onrender.com`

#### 方法二：使用 render.yaml 配置

我已经创建了 `backend/render.yaml` 配置文件，Render 会自动读取该配置。

---

### 第三步：连接前后端

1. **获取后端地址**
   - 从 Render Dashboard 复制后端地址
   - 例如：`https://ai-storybook-backend.onrender.com`

2. **更新前端环境变量**
   - 在 Vercel Dashboard 中
   - 找到你的项目 → Settings → Environment Variables
   - 添加或更新：`VITE_API_URL`
   - 值：你的后端地址

3. **重新部署前端**
   - 在 Vercel Dashboard 中
   - 点击 "Redeploy"

---

## 🔧 配置阿里云服务

### 1. 获取 API 密钥

- **通义千问 API Key**：https://dashscope.aliyun.com/apiKey
- **通义万相 API Key**：https://dashscope.aliyun.com/apiKey

### 2. 配置 OSS 对象存储

1. 创建 OSS Bucket
   - 访问：https://oss.console.aliyun.com
   - 创建 Bucket，设置权限为私有

2. 获取 OSS 配置
   ```
   OSS_ACCESS_KEY_ID
   OSS_ACCESS_KEY_SECRET
   OSS_BUCKET_NAME
   OSS_ENDPOINT
   ```

### 3. 配置数据库

**使用 Render PostgreSQL（免费）**
1. 在 Render Dashboard 创建 "PostgreSQL" 数据库
2. 复制 Internal Database URL
3. 添加到 Render 后端环境变量：`DATABASE_URL`

**使用 Redis（可选）**
1. 注册 Redis Cloud：https://redis.com/try-free/
2. 创建免费数据库
3. 复制连接 URL
4. 添加到 Render 后端环境变量：`REDIS_URL`

---

## 🌐 访问你的应用

部署完成后，你将拥有：

- **前端地址**：`https://ai-storybook-xxxx.vercel.app`
- **后端地址**：`https://ai-storybook-backend.onrender.com`

### 测试

1. 访问前端地址
2. 点击 "开始创作"
3. 按照步骤填写信息并提交
4. 如果一切正常，你应该能看到绘本生成过程

---

## 📝 常见问题

### 1. 前端无法连接后端

**原因**：CORS 错误或 API 地址配置错误

**解决方案**：
- 确保后端 API 地址正确配置在前端环境变量中
- 检查后端 `app/main.py` 中的 CORS 配置

### 2. 后端无法启动

**原因**：环境变量配置错误或依赖安装失败

**解决方案**：
- 检查所有必需的环境变量是否正确配置
- 查看 Render Logs 查看详细错误信息
- 确保 `requirements.txt` 中所有依赖都能正常安装

### 3. 图片生成失败

**原因**：阿里云 API 密钥无效或额度不足

**解决方案**：
- 确认 API 密钥是否正确
- 检查阿里云账户是否有足够额度
- 查看后端日志获取详细错误信息

### 4. Render 免费套餐限制

**限制**：
- 15 分钟无活动后休眠
- 再次访问需要 30-50 秒唤醒
- 每月 750 小时运行时间

**解决方案**：
- 升级到付费套餐（$7/月起）
- 或使用其他平台（如 Railway、Fly.io）

---

## 🔄 自动化部署脚本

如果你想完全自动化部署，可以使用以下脚本：

```bash
#!/bin/bash

# 前端部署到 Vercel
cd frontend
vercel --prod --token YOUR_VERCEL_TOKEN

# 后端部署到 Render（需要配置环境变量）
cd ../backend
# 使用 render-cli 部署
render deploy --key YOUR_RENDER_API_KEY
```

---

## 📊 平台对比

| 平台 | 免费额度 | 优点 | 缺点 |
|------|---------|------|------|
| Vercel | 100GB 带宽/月 | 极速部署，全球 CDN | 构建时长限制 |
| Render | 750 小时/月 | 支持多种语言 | 免费版会休眠 |
| Netlify | 100GB 带宽/月 | 简单易用 | Python 支持有限 |
| Railway | $5 免费额度 | 功能强大 | 免费额度较少 |
| Fly.io | 3 个应用/月 | 全球边缘节点 | 配置较复杂 |

---

## 🚀 其他部署方案

### 方案 A：部署到 Railway

1. 访问：https://railway.app/new
2. 连接 GitHub 仓库
3. 选择 `Trible-ccb/ai-storybook`
4. 配置环境变量
5. Deploy

### 方案 B：部署到 Fly.io

```bash
# 安装 flyctl
curl -L https://fly.io/install.sh | sh

# 登录
flyctl auth signup
flyctl auth login

# 部署
flyctl launch
```

### 方案 C：使用云服务器

如果你有自己的云服务器（阿里云、腾讯云等）：

```bash
# SSH 连接到服务器
ssh your-server

# 克隆项目
git clone https://github.com/Trible-ccb/ai-storybook.git
cd ai-storybook

# 安装依赖
cd backend
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 启动后端（使用 gunicorn）
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app.main:app

# 使用 Nginx 反向代理（推荐）
# 配置 SSL（使用 Let's Encrypt）
```

---

## 🎉 完成

恭喜！你的 AI 个性化绘本平台现在已经部署到云端，可以通过公网访问了！

**下一步**：
1. 分享你的平台链接
2. 收集用户反馈
3. 根据反馈优化产品
4. 考虑付费推广

---

## 📞 需要帮助？

如果遇到任何问题，请：
1. 查看平台文档
2. 查看项目 Issues
3. 提交新的 Issue

祝你部署成功！🚀
