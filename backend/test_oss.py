#!/usr/bin/env python3
"""
OSS 连接测试脚本
用于验证 OSS 配置是否正确
"""

import oss2
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 获取 OSS 配置
access_key_id = os.getenv('OSS_ACCESS_KEY_ID')
access_key_secret = os.getenv('OSS_ACCESS_KEY_SECRET')
bucket_name = os.getenv('OSS_BUCKET_NAME')
endpoint = os.getenv('OSS_ENDPOINT')

print("=" * 60)
print("  OSS 连接测试")
print("=" * 60)
print()

# 检查配置
print("1. 检查配置...")
print(f"   AccessKey ID: {access_key_id[:10]}...{access_key_id[-4:]}")
print(f"   AccessKey Secret: {access_key_secret[:10]}...{access_key_secret[-4:]}")
print(f"   Bucket: {bucket_name}")
print(f"   Endpoint: {endpoint}")
print()

if not all([access_key_id, access_key_secret, bucket_name, endpoint]):
    print("❌ 错误：缺少必需的 OSS 配置！")
    exit(1)

print("✓ 配置完整")
print()

# 创建 OSS 认证
print("2. 创建 OSS 认证...")
try:
    auth = oss2.Auth(access_key_id, access_key_secret)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    print("✓ 认证创建成功")
    print()
except Exception as e:
    print(f"❌ 认证失败：{e}")
    exit(1)

# 测试 Bucket 访问
print("3. 测试 Bucket 访问...")
try:
    bucket_info = bucket.get_bucket_info()
    print(f"✓ Bucket 信息获取成功")
    print(f"   - 名称: {bucket_info.name}")
    print(f"   - 位置: {bucket_info.location}")
    print(f"   - 创建时间: {bucket_info.creation_date}")
    print(f"   - 存储类型: {bucket_info.storage_class}")
    print()
except Exception as e:
    print(f"❌ Bucket 访问失败：{e}")
    print()
    print("可能的原因：")
    print("  1. Bucket 名称不存在")
    print("  2. AccessKey 权限不足")
    print("  3. Endpoint 配置错误")
    exit(1)

# 测试文件上传
print("4. 测试文件上传...")
test_filename = "test_oss_connection.txt"
try:
    content = "OSS 连接测试文件"
    result = bucket.put_object(test_filename, content)
    print(f"✓ 文件上传成功")
    print(f"   - 文件名: {test_filename}")
    print(f"   - ETag: {result.etag}")
    print()
except Exception as e:
    print(f"❌ 文件上传失败：{e}")
    exit(1)

# 测试文件列表
print("5. 测试文件列表...")
try:
    for obj in oss2.ObjectIterator(bucket, prefix=test_filename):
        print(f"✓ 找到文件: {obj.key} ({obj.size} bytes)")
    print()
except Exception as e:
    print(f"❌ 文件列表获取失败：{e}")
    exit(1)

# 清理测试文件
print("6. 清理测试文件...")
try:
    bucket.delete_object(test_filename)
    print(f"✓ 测试文件已删除")
    print()
except Exception as e:
    print(f"⚠️  清理测试文件失败（可忽略）：{e}")
    print()

print("=" * 60)
print("  ✅ OSS 连接测试全部通过！")
print("=" * 60)
print()
print("你的 OSS 配置正确，可以正常使用。")
print()
