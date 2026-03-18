# Render 环境变量配置指南

本文档详细说明如何在 Render 上配置后端所需的所有环境变量。

---

## 📋 环境变量清单

### 必需的环境变量

| 变量名 | 说明 | 示例值 | 来源 |
|--------|------|--------|------|
| `QWEN_API_KEY` | 通义千问/通义万相 API Key | `sk-xxxxxxxxxxxxxxxx` | https://dashscope.aliyun.com/apiKey |
| `OSS_ACCESS_KEY_ID` | OSS AccessKey ID | `LTAI5txxxxxxx` | https://ram.console.aliyun.com/manage/ak |
| `OSS_ACCESS_KEY_SECRET` | OSS AccessKey Secret | `xxxxxxxxxxxxxxxx` | https://ram.console.aliyun.com/manage/ak |
| `OSS_BUCKET_NAME` | OSS Bucket 名称 | `cozeclawbucket` | 自己创建的 Bucket |
| `OSS_ENDPOINT` | OSS Endpoint | `oss-cn-hangzhou.aliyuncs.com` | Bucket 所在区域 |

### 可选的环境变量

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `DATABASE_URL` | PostgreSQL 数据库连接 | `postgresql://user:pass@host:5432/db` |
| `REDIS_URL` | Redis 连接地址 | `redis://user:pass@host:6379` |
| `SECRET_KEY` | Flask 密钥 | `your-secret-key` |
| `PORT` | 服务端口 | `10000` |
| `CORS_ORIGINS` | 允许的跨域来源 | `https://ai-storybook.vercel.app` |
| `LOG_LEVEL` | 日志级别 | `INFO` |

---

## 🚀 配置步骤

### 第一步：创建 Render 账号

1. 访问：https://render.com/register
2. 使用 GitHub 账号登录

### 第二步：创建 PostgreSQL 数据库（可选但推荐）

1. 在 Render Dashboard，点击 "New +" → "PostgreSQL"
2. 选择 Free 套餐
3. 创建数据库
4. 等待创建完成（约 1 分钟）
5. 复制 **Internal Database URL**

### 第三步：创建 Web Service

1. 在 Render Dashboard，点击 "New +" → "Web Service"
2. 连接 GitHub 仓库：`Trible-ccb/ai-storybook`
3. 配置如下：

#### Build & Deploy

```
Name: ai-storybook-backend
Environment: Python 3
Region: Singapore (或离你最近的区域)
Branch: main
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: python app/main.py
```

#### Environment Variables

点击 "Advanced" → "Add Environment Variable"，添加以下变量：

```
QWEN_API_KEY = sk-xxxxxxxxxxxxxxxx

OSS_ACCESS_KEY_ID = LTAI5txxxxxxx

OSS_ACCESS_KEY_SECRET = xxxxxxxxxxxxxxxx

OSS_BUCKET_NAME = cozeclawbucket

OSS_ENDPOINT = oss-cn-hangzhou.aliyuncs.com

DATABASE_URL = postgresql://user:password@host:5432/database (从 PostgreSQL 服务复制)

SECRET_KEY = ai-storybook-production-secret-key-2024

PORT = 10000

CORS_ORIGINS = https://ai-storybook.vercel.app

LOG_LEVEL = INFO
```

### 第四步：部署

1. 点击 "Create Web Service"
2. 等待部署完成（约 2-3 分钟）
3. 部署成功后，Render 会提供访问地址

### 第五步：获取后端地址

部署成功后，你会看到类似这样的地址：
```
https://ai-storybook-backend.onrender.com
```

---

## 🔐 安全提示

### 不要提交敏感信息

**重要**：不要将真实的 API Key 和 AccessKey 提交到 GitHub！

- `.env` 文件包含真实密钥，**已添加到 .gitignore**
- `.env.example` 只包含示例，**可以提交到 Git**
- 在 Render 上通过环境变量配置密钥

### 保护你的密钥

1. **定期轮换密钥**
   - 建议每 3-6 个月更换一次

2. **使用 RAM 子账号**
   - 不要使用主账号的 AccessKey
   - 为每个应用创建专用的子账号
   - 只授予必要的权限

3. **限制密钥权限**
   - OSS AccessKey 只授予 OSS 权限
   - 不要授予阿里云其他服务权限

4. **监控密钥使用**
   - 在阿里云控制台查看 AccessKey 使用记录
   - 发现异常立即撤销密钥

---

## 🔧 故障排查

### 问题 1：部署失败

**症状**：部署过程中报错

**可能原因**：
- Python 依赖安装失败
- Build Command 或 Start Command 错误
- 端口配置错误

**解决方案**：
1. 查看 Render Logs 查看详细错误
2. 确保 `requirements.txt` 中所有依赖都能正常安装
3. 检查 `app/main.py` 是否能正常启动

### 问题 2：OSS 连接失败

**症状**：上传图片时出错

**可能原因**：
- OSS 环境变量配置错误
- AccessKey 权限不足
- Endpoint 配置错误

**解决方案**：
1. 检查所有 OSS 相关的环境变量是否正确
2. 在阿里云控制台确认 AccessKey 有 OSS 权限
3. 确认 Endpoint 与 Bucket 区域一致

### 问题 3：数据库连接失败

**症状**：应用启动时数据库连接失败

**可能原因**：
- DATABASE_URL 配置错误
- PostgreSQL 服务未创建或未运行

**解决方案**：
1. 从 PostgreSQL 服务复制 Internal Database URL
2. 确保 DATABASE_URL 格式正确
3. 检查 PostgreSQL 服务状态

### 问题 4：CORS 错误

**症状**：前端无法连接后端

**可能原因**：
- CORS_ORIGINS 配置错误
- 前端地址不在允许列表中

**解决方案**：
1. 确保 CORS_ORIGINS 包含前端地址
2. 检查前端地址是否正确（包含 https://）
3. 多个地址用逗号分隔

---

## 📊 性能优化

### Free 套餐限制

Render Free 套餐有以下限制：

- **运行时间**：750 小时/月（约 25 天）
- **内存**：512 MB
- **CPU**：0.1 vCPU
- **休眠**：15 分钟无活动后休眠
- **唤醒时间**：30-50 秒

### 升级到付费套餐

如果需要更好的性能，可以考虑升级：

| 套餐 | 价格 | 内存 | CPU | 特性 |
|------|------|------|-----|------|
| Starter | $7/月 | 512 MB | 0.5 vCPU | 无休眠 |
| Standard | $25/月 | 1 GB | 1 vCPU | 更快响应 |
| Pro | $50/月 | 2 GB | 2 vCPU | 高性能 |

---

## 🔄 自动重启配置

Render 默认会在应用崩溃时自动重启。你也可以配置健康检查：

在 `render.yaml` 中添加：

```yaml
healthCheckPath: /health
```

然后在 `app/main.py` 中添加健康检查端点：

```python
@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200
```

---

## 📈 监控和日志

### 查看 Logs

1. 访问 Render Dashboard
2. 选择你的 Web Service
3. 点击 "Logs" 标签
4. 查看实时日志

### 设置告警

1. 在 Web Service 设置中
2. 点击 "Alerts"
3. 配置 CPU、内存、响应时间等指标告警
4. 设置告警接收邮箱

---

## ✅ 验证部署

部署完成后，测试以下端点：

```bash
# 健康检查
curl https://ai-storybook-backend.onrender.com/health

# 生成故事（需要 API Key）
curl -X POST https://ai-storybook-backend.onrender.com/api/story/generate \
  -H "Content-Type: application/json" \
  -d '{"age": 5, "theme": "友谊", ...}'
```

---

## 📞 需要帮助？

如果遇到问题：

1. 查看 [Render 文档](https://render.com/docs)
2. 查看 [项目 Issues](https://github.com/Trible-ccb/ai-storybook/issues)
3. 提交新的 Issue

---

祝你部署成功！🚀
