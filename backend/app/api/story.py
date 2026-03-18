"""
故事生成API - 使用持久化任务系统
"""
from flask import Blueprint, request, jsonify
import logging
import threading
from app.services.task_service import TaskService
from app.services.task_processor import TaskProcessor

logger = logging.getLogger(__name__)

story_bp = Blueprint('story', __name__)


@story_bp.route('/api/generate-story', methods=['POST'])
def generate_story():
    """
    生成儿童故事（同步）

    请求体:
    {
        "age": 5,
        "theme": "友谊",
        "child_name": "小美",
        "child_characteristics": "活泼可爱的5岁女孩",
        "toys_name": "小白兔",
        "creative_idea": "小白兔会说话，带小美去森林里找彩虹糖",
        "page_count": 12
    }

    响应:
    {
        "success": true,
        "story": {
            "pages": [...]
        },
        "tokens_used": 650
    }
    """
    try:
        from app.services.llm_service import LLMService
        from app.config import Config

        # 获取请求数据
        data = request.get_json()

        # 参数验证
        required_fields = ['age', 'theme', 'child_name', 'toys_name', 'creative_idea']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'缺少必要参数: {field}'
                }), 400

        # 构建故事请求
        story_request = {
            'age': data.get('age'),
            'theme': data.get('theme', '友谊'),
            'child_name': data.get('child_name'),
            'child_characteristics': data.get('child_characteristics', '可爱的小朋友'),
            'toys_name': data.get('toys_name'),
            'creative_idea': data.get('creative_idea'),
            'page_count': data.get('page_count', 12)
        }

        # 初始化LLM服务
        llm_service = LLMService(Config.DASHSCOPE_API_KEY)

        # 生成故事
        result = llm_service.generate_story(story_request)

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500

    except Exception as e:
        logger.error(f"生成故事API错误: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500


@story_bp.route('/api/generate-complete-storybook', methods=['POST'])
def generate_complete_storybook():
    """
    一键生成完整绘本（持久化任务）

    请求体:
    {
        "age": 5,
        "theme": "友谊",
        "child_name": "小美",
        "child_characteristics": "活泼可爱的5岁女孩",
        "toys_name": "小白兔",
        "toys_characteristics": "毛绒玩具，有长长的耳朵",
        "creative_idea": "小白兔会说话，带小美去森林里找彩虹糖",
        "visual_style": "水彩手绘",
        "child_photo": "base64_image_data",
        "page_count": 12
    }

    响应（立即返回）:
    {
        "success": true,
        "task_id": "abc-123-def",
        "message": "任务已创建，正在处理中"
    }
    """
    try:
        # 获取请求数据
        data = request.get_json()

        # 参数验证
        required_fields = ['age', 'theme', 'child_name', 'toys_name', 'creative_idea', 'child_photo']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'缺少必要参数: {field}'
                }), 400

        # 创建持久化任务
        child_name = data.get('child_name', '未知')
        task = TaskService.create_task(
            title=f"{child_name}的冒险故事",
            input_data=data
        )

        # 在后台线程中处理任务
        processor = TaskProcessor(task.id, data)
        thread = threading.Thread(target=processor.process)
        thread.daemon = True
        thread.start()

        logger.info(f"任务 {task.id} 已启动后台处理")

        return jsonify({
            'success': True,
            'task_id': task.id,
            'message': '任务已创建，正在处理中',
            'title': task.title
        }), 200

    except Exception as e:
        logger.error(f"创建任务失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500
