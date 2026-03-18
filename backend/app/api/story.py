"""
故事生成API - 支持异步任务
"""
from flask import Blueprint, request, jsonify
import logging
import threading

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
            "pages": [
                {
                    "page": 1,
                    "text": "阳光明媚的早晨，小美正在房间里玩。",
                    "scene_description": "温馨的儿童房间..."
                }
            ]
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
    一键生成完整绘本（异步任务）

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
        from app.services.task_manager import task_manager, TaskStatus
        from app.config import Config

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

        # 创建任务
        task_id = task_manager.create_task(data)

        # 在后台线程中处理任务
        thread = threading.Thread(
            target=process_storybook_generation,
            args=(task_id, data)
        )
        thread.daemon = True
        thread.start()

        logger.info(f"任务 {task_id} 已启动后台处理")

        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': '任务已创建，正在处理中'
        }), 200

    except Exception as e:
        logger.error(f"创建任务失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500


@story_bp.route('/api/task/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """
    查询任务状态

    响应:
    {
        "success": true,
        "task": {
            "task_id": "abc-123-def",
            "status": "processing",
            "progress": 60,
            "progress_text": "正在生成插图...",
            "created_at": "2024-03-18T10:30:00",
            "updated_at": "2024-03-18T10:35:00",
            "result": null,
            "error": null
        }
    }
    """
    try:
        from app.services.task_manager import task_manager

        task = task_manager.get_task(task_id)

        if not task:
            return jsonify({
                'success': False,
                'error': '任务不存在'
            }), 404

        return jsonify({
            'success': True,
            'task': task
        }), 200

    except Exception as e:
        logger.error(f"查询任务状态失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500


def process_storybook_generation(task_id, data):
    """
    处理绘本生成任务（后台线程）

    Args:
        task_id: 任务ID
        data: 请求数据
    """
    from app.services.task_manager import task_manager, TaskStatus
    from app.services.llm_service import LLMService
    from app.services.image_service import ImageService
    from app.config import Config

    try:
        # 更新任务状态为处理中
        task_manager.set_task_status(
            task_id,
            TaskStatus.PROCESSING,
            progress=10,
            progress_text='正在生成故事...'
        )

        # 步骤1: 生成故事
        llm_service = LLMService(Config.DASHSCOPE_API_KEY)

        story_request = {
            'age': data.get('age'),
            'theme': data.get('theme'),
            'child_name': data.get('child_name'),
            'child_characteristics': data.get('child_characteristics', '可爱的小朋友'),
            'toys_name': data.get('toys_name'),
            'creative_idea': data.get('creative_idea'),
            'page_count': data.get('page_count', 12)
        }

        story_result = llm_service.generate_story(story_request)

        if not story_result['success']:
            task_manager.fail_task(task_id, story_result.get('error', '故事生成失败'))
            return

        story = story_result['story']['pages']

        # 更新任务状态
        task_manager.set_task_status(
            task_id,
            TaskStatus.STORY_GENERATED,
            progress=40,
            progress_text=f'故事生成成功，共{len(story)}页'
        )

        # 步骤2: 生成插图
        task_manager.set_task_status(
            task_id,
            TaskStatus.IMAGES_GENERATED,
            progress=50,
            progress_text='正在生成插图...'
        )

        oss_config = {
            'access_key_id': Config.OSS_ACCESS_KEY_ID,
            'access_key_secret': Config.OSS_ACCESS_KEY_SECRET,
            'endpoint': Config.OSS_ENDPOINT,
            'bucket_name': Config.OSS_BUCKET_NAME
        }

        image_service = ImageService(Config.DASHSCOPE_API_KEY, oss_config)

        image_config = {
            'reference_image': data.get('child_photo'),
            'child_name': data.get('child_name'),
            'child_characteristics': data.get('child_characteristics'),
            'toys_name': data.get('toys_name'),
            'toys_characteristics': data.get('toys_characteristics', ''),
            'visual_style': data.get('visual_style', '水彩手绘'),
            'age': data.get('age')
        }

        image_result = image_service.generate_all_images(story, image_config)

        # 计算进度
        total_images = len(story)
        success_count = image_result['success_count']
        progress = 50 + int((success_count / total_images) * 40)

        task_manager.set_task_status(
            task_id,
            TaskStatus.IMAGES_GENERATED,
            progress=progress,
            progress_text=f'插图生成中... ({success_count}/{total_images})'
        )

        # 合并故事和插图
        storybook = []
        for page in story:
            page_num = page['page']
            # 找到对应的图片
            image_data = next((img for img in image_result['images'] if img['page'] == page_num), None)

            storybook.append({
                'page': page_num,
                'text': page['text'],
                'scene_description': page['scene_description'],
                'image_url': image_data['image_url'] if image_data else None
            })

        # 完成任务
        result = {
            'title': f"{data.get('child_name')}的冒险故事",
            'pages': storybook,
            'stats': {
                'total_pages': len(story),
                'success_images': image_result['success_count'],
                'failed_images': image_result['fail_count']
            }
        }

        task_manager.complete_task(task_id, result)

    except Exception as e:
        logger.error(f"任务处理失败: {task_id}, 错误: {str(e)}")
        task_manager.fail_task(task_id, str(e))
