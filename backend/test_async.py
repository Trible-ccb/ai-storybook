"""
测试异步任务 API
"""
import requests
import time
import json

# 配置
BASE_URL = 'https://ai-storybook-backend-w7h1.onrender.com'

def test_async_generation():
    """测试异步生成功能"""
    print("开始测试异步生成功能...")
    
    # 准备测试数据
    test_data = {
        "age": 5,
        "theme": "友谊",
        "child_name": "小美",
        "child_characteristics": "活泼可爱的5岁女孩",
        "toys_name": "小白兔",
        "toys_characteristics": "毛绒玩具，有长长的耳朵",
        "creative_idea": "小白兔会说话，带小美去森林里找彩虹糖",
        "visual_style": "水彩手绘",
        "child_photo": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",  # 1x1 透明图片
        "page_count": 6  # 减少页数以加快测试
    }
    
    # 步骤1：创建任务
    print("\n步骤1：创建任务...")
    response = requests.post(
        f'{BASE_URL}/api/generate-complete-storybook',
        json=test_data,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code != 200:
        print(f"❌ 创建任务失败: {response.status_code}")
        print(response.text)
        return
    
    result = response.json()
    if not result.get('success'):
        print(f"❌ 创建任务失败: {result.get('error')}")
        return
    
    task_id = result.get('task_id')
    print(f"✅ 任务创建成功: {task_id}")
    
    # 步骤2：轮询任务状态
    print("\n步骤2：开始轮询任务状态...")
    max_attempts = 40  # 最多轮询 40 次（每 3 秒一次，约 2 分钟）
    attempt = 0
    
    while attempt < max_attempts:
        attempt += 1
        print(f"\n尝试 #{attempt}...")
        
        response = requests.get(f'{BASE_URL}/api/task/{task_id}')
        
        if response.status_code != 200:
            print(f"❌ 查询任务失败: {response.status_code}")
            break
        
        task_result = response.json()
        if not task_result.get('success'):
            print(f"❌ 查询任务失败: {task_result.get('error')}")
            break
        
        task = task_result.get('task')
        print(f"状态: {task.get('status')}")
        print(f"进度: {task.get('progress')}%")
        print(f"进度文本: {task.get('progress_text')}")
        
        # 检查任务状态
        if task.get('status') == 'completed':
            print("\n✅ 任务完成！")
            print(f"结果: {json.dumps(task.get('result'), indent=2, ensure_ascii=False)}")
            return True
        
        if task.get('status') == 'failed':
            print(f"\n❌ 任务失败: {task.get('error')}")
            return False
        
        # 等待 3 秒后继续轮询
        print("等待 3 秒...")
        time.sleep(3)
    
    print(f"\n⚠️  轮询超时（{max_attempts} 次尝试）")
    return False

if __name__ == '__main__':
    try:
        test_async_generation()
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
