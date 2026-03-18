"""
故事生成API
"""
from flask import Blueprint, request, jsonify
import logging

logger = logging.getLogger(__name__)

story_bp = Blueprint('story', __name__)

@story_bp.route('/api/generate-story', methods=['POST'])
def generate_story():
    """
    生成儿童故事
    
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
    一键生成完整绘本（故事+插图）
    
    请求体:
    {
        "age": 5,
        "theme": "友谊",
        "child_name": "小美",
        "child_characteristics": "活泼可爱的5岁女孩",
        "toys_name": "小白兔",
        "creative_idea": "小白兔会说话，带小美去森林里找彩虹糖",
        "visual_style": "水彩手绘",
        "child_photo": "https://oss.example.com/child.jpg",
        "page_count": 12
    }
    
    响应:
    {
        "success": true,
        "storybook": {
            "pages": [
                {
                    "page": 1,
                    "text": "...",
                    "scene_description": "...",
                    "image_url": "https://oss.example.com/page_1.jpg"
                }
            ]
        }
    }
    """
    try:
        from app.services.llm_service import LLMService
        from app.services.image_service import ImageService
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
        
        # 步骤1: 生成故事
        logger.info("开始生成故事...")
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
            return jsonify(story_result), 500
        
        story = story_result['story']['pages']
        logger.info(f"故事生成成功，共{len(story)}页")
        
        # 步骤2: 生成插图
        logger.info("开始生成插图...")
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
        
        if not image_result['success']:
            logger.warning(f"部分图片生成失败: {image_result['fail_count']}页")
        
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
        
        logger.info(f"绘本生成完成，成功{image_result['success_count']}/{len(story)}页")
        
        return jsonify({
            'success': True,
            'storybook': {
                'title': f"{data.get('child_name')}的冒险故事",
                'pages': storybook,
                'stats': {
                    'total_pages': len(story),
                    'success_images': image_result['success_count'],
                    'failed_images': image_result['fail_count']
                }
            }
        }), 200
    
    except Exception as e:
        logger.error(f"生成完整绘本API错误: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500
