# 🚀 快速部署指南

本指南帮助你快速将 AI 个性化绘本平台部署到云端。

---

## ✅ 已配置好的信息

### 阿里云服务

| 服务 | 密钥/配置 | 说明 |
|------|----------|------|
| 通义千问/通义万相 API Key | `sk-xxxxxxxxxxxxxxxx` | 用于故事和图像生成 |
| OSS Bucket 名称 | `cozeclawbucket` | 存储生成的图片和 PDF |
| OSS AccessKey ID | `LTAI5txxxxxxx` | OSS 访问密钥 ID |
| OSS AccessKey Secret | `xxxxxxxxxxxxxxxx` | OSS 访问密钥 Secret |
| OSS Endpoint | `oss-cn-hangzhou.aliyuncs.com` | OSS 服务地址（华东1-杭州） |

### OSS 状态

✅ Bucket 已创建
✅ 区域：华东1（杭州）
✅ 存储类型：IA（低频访问）
✅ 连接测试通过

---

## 📦 部署清单

- [x] GitHub 仓库创建完成
- [x] 前端代码准备完成
- [x] 后端代码准备完成
- [x] OSS 配置完成并测试通过
- [x] 阿里云 API Key 配置完成
- [ ] 部署前端到 Vercel
- [ ] 部署后端到 Render
- [ ] 配置前后端连接
- [ ] 测试完整流程

---

## 🎯 部署步骤（预计 5-10 分钟）

### 第一步：部署前端到 Vercel（2 分钟）

1. **访问 Vercel**
   - 打开：https://vercel.com/new

2. **导入项目**
   - 点击 "Import Project"
   - 选择 GitHub 仓库：`Trible-ccb/ai-storybook`
   - Root Directory 设置为：`frontend`
   - Framework Preset：`Vite`

3. **配置环境变量**
   - 点击 "Environment Variables"
   - 添加：`VITE_API_URL`
   - 值先填写：`https://ai-storybook-backend.onrender.com`
   - （部署后端后会更新）

4. **部署**
   - 点击 "Deploy"
   - 等待 1-2 分钟

5. **记录前端地址**
   - 例如：`https://ai-storybook-xxxx.vercel.app`

---

### 第二步：部署后端到 Render（3-5 分钟）

1. **访问 Render**
   - 打开：https://dashboard.render.com/select-repo

2. **连接 GitHub**
   - 点击 "New +" → "Web Service"
   - 选择仓库：`Trible-ccb/ai-storybook`

3. **配置基础信息**

```
Name: ai-storybook-backend
Environment: Python 3
Region: Singapore
Branch: main
Root Directory: backend
```

4. **配置构建和启动**

```
Build Command: pip install -r requirements.txt
Start Command: python app/main.py
```

5. **配置环境变量**（⚠️ 重要）

点击 "Advanced" → "Environment"，添加以下变量：

```
QWEN_API_KEY = sk-xxxxxxxxxxxxxxxx

OSS_ACCESS_KEY_ID = LTAI5txxxxxxx

OSS_ACCESS_KEY_SECRET = xxxxxxxxxxxxxxxx

OSS_BUCKET_NAME = cozeclawbucket

OSS_ENDPOINT = oss-cn-hangzhou.aliyuncs.com

SECRET_KEY = ai-storybook-production-secret-key-2024

PORT = 10000

CORS_ORIGINS = https://ai-storybook.vercel.app

LOG_LEVEL = INFO

DATABASE_URL = sqlite:///aistorybook.db
```

6. **部署**
   - 点击 "Create Web Service"
   - 等待 2-3 分钟

7. **记录后端地址**
   - 例如：`https://ai-storybook-backend.onrender.com`

---

### 第三步：更新前端配置（1 分钟）

1. **访问 Vercel Dashboard**
   - 打开：https://vercel.com/dashboard

2. **找到项目**
   - 点击 `ai-storybook` 项目

3. **更新环境变量**
   - Settings → Environment Variables
   - 编辑 `VITE_API_URL`
   - 值改为你的后端地址：`https://ai-storybook-backend.onrender.com`
   - 点击 Save

4. **重新部署**
   - 点击 "Redeploy"
   - 等待 1 分钟

---

## 🌐 访问你的应用

部署完成后，你将拥有：

- **前端地址**：`https://ai-storybook-xxxx.vercel.app`
- **后端地址**：`https://ai-storybook-backend.onrender.com`

访问前端地址，开始使用你的 AI 个性化绘本平台！

---

## ✅ 部署验证

部署完成后，测试以下功能：

1. **访问首页**
   - 打开前端地址
   - 查看页面是否正常显示

2. **测试创作流程**
   - 点击"开始创作"
   - 上传照片
   - 填写信息
   - 提交生成

3. **查看结果**
   - 等待 5-10 分钟
   - 查看生成的绘本
   - 下载 PDF

---

## 🐛 常见问题

### Q1: 前端无法连接后端

**解决方案**：
1. 检查 Vercel 环境变量 `VITE_API_URL` 是否正确
2. 检查 Render CORS_ORIGINS 是否包含前端地址
3. 查看 Render Logs 确认后端是否正常运行

### Q2: 图片生成失败

**解决方案**：
1. 检查阿里云 API Key 是否有效
2. 确认 API 账户有足够额度
3. 查看 Render Logs 获取详细错误信息

### Q3: OSS 上传失败

**解决方案**：
1. 确认 OSS 环境变量配置正确
2. 检查 OSS AccessKey 权限
3. 确认 Bucket 权限设置

---

## 📞 需要帮助？

查看详细文档：

- **完整部署指南**：[DEPLOYMENT.md](DEPLOYMENT.md)
- **Render 配置详解**：[RENDER_CONFIG.md](RENDER_CONFIG.md)
- **技术选型**：[TECH_STACK.md](TECH_STACK.md)

---

## 🎉 部署成功后

恭喜！你的平台已经部署到云端：

1. **分享链接**：分享给你的朋友测试
2. **收集反馈**：收集用户使用反馈
3. **持续优化**：根据反馈优化产品
4. **推广运营**：在社交媒体分享

---

**祝你部署成功！如有问题，请查看详细文档。** 🚀
