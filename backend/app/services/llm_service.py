"""
大语言模型服务 - 故事生成
"""
import json
import logging
from dashscope import Generation
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class LLMService:
    """大语言模型服务类"""
    
    def __init__(self, api_key: str):
        """
        初始化LLM服务
        
        Args:
            api_key: 通义千问API密钥
        """
        self.api_key = api_key
    
    def generate_story(self, story_request: Dict) -> Dict:
        """
        生成儿童故事
        
        Args:
            story_request: 故事生成请求
                - age: 孩子年龄
                - theme: 故事主题
                - child_name: 孩子名字
                - child_characteristics: 孩子特点
                - toys_name: 玩具名字
                - creative_idea: 异想天开的创意
                - page_count: 页数（默认12页）
        
        Returns:
            Dict: 包含成功状态和故事数据
        """
        try:
            # 构建Prompt
            prompt = self._build_story_prompt(story_request)
            
            # 调用通义千问API
            response = Generation.call(
                api_key=self.api_key,
                model='qwen-turbo',
                prompt=prompt,
                result_format='message',
                temperature=0.7,  # 创造性
                top_p=0.9,
                max_tokens=2000
            )
            
            # 解析响应
            if response.status_code == 200:
                content = response.output.choices[0].message.content
                
                # 尝试解析JSON
                try:
                    story_json = json.loads(content)
                    
                    # 适龄化调整
                    story_json = self._adjust_for_age(story_request['age'], story_json)
                    
                    return {
                        'success': True,
                        'story': story_json,
                        'tokens_used': response.usage.total_tokens
                    }
                except json.JSONDecodeError:
                    # JSON解析失败，尝试提取故事内容
                    story_json = self._parse_story_from_text(content)
                    story_json = self._adjust_for_age(story_request['age'], story_json)
                    
                    return {
                        'success': True,
                        'story': story_json,
                        'tokens_used': response.usage.total_tokens
                    }
            else:
                logger.error(f"LLM API调用失败: {response.message}")
                return {
                    'success': False,
                    'error': f'生成失败: {response.message}'
                }
        
        except Exception as e:
            logger.error(f"生成故事时发生错误: {str(e)}")
            return {
                'success': False,
                'error': f'生成失败: {str(e)}'
            }
    
    def _build_story_prompt(self, request: Dict) -> str:
        """
        构建故事生成Prompt
        
        Args:
            request: 故事生成请求
        
        Returns:
            str: 完整的Prompt
        """
        age = request.get('age', 5)
        theme = request.get('theme', '友谊')
        child_name = request.get('child_name', '小朋友')
        child_characteristics = request.get('child_characteristics', '可爱的小朋友')
        toys_name = request.get('toys_name', '小玩偶')
        creative_idea = request.get('creative_idea', '一起冒险')
        page_count = request.get('page_count', 12)
        
        # 根据年龄设置参数
        max_words_map = {3: 20, 4: 20, 5: 20, 6: 30, 7: 30, 8: 30, 9: 40, 10: 40, 11: 40, 12: 40}
        max_words = max_words_map.get(age, 30)
        
        educational_value_map = {
            "友谊": "培养分享和合作精神",
            "勇气": "鼓励勇敢面对困难",
            "学习": "激发好奇心和求知欲",
            "环保": "培养爱护环境意识"
        }
        educational_value = educational_value_map.get(theme, "培养积极向上的品质")
        
        prompt = f"""你是一位专业的儿童故事作家，擅长创作适合{age}岁孩子的故事。
请根据以下信息创作一个"{theme}"主题的故事：

【故事要求】
1. 主角：{child_name}，{child_characteristics}
2. 配角：{toys_name}，是孩子最喜欢的玩具
3. 核心创意：{creative_idea}（孩子的异想天开）
4. 页数：{page_count}页
5. 每页文字：不超过{max_words}字
6. 语言风格：适合{age}岁儿童理解，词汇简单生动
7. 教育意义：{educational_value}

【故事结构】
第1页：引入主角和背景
第2-{page_count-2}页：故事发展，情节起伏
第{page_count-1}页：高潮部分
第{page_count}页：结局，温馨有教育意义

【输出格式】
请以JSON格式输出，每页包含：
- page: 页码（整数）
- text: 页面文字（字符串，不超过{max_words}字）
- scene_description: 场景描述（字符串，用于生成插画，包含画面主体、环境、色彩、构图等信息）

示例输出格式：
{{
  "pages": [
    {{
      "page": 1,
      "text": "阳光明媚的早晨，{child_name}正在房间里玩。",
      "scene_description": "温馨的儿童房间，阳光透过窗户洒进来，{child_characteristics}，{child_name}坐在地毯上，{toys_name}放在旁边，色彩明亮温暖，水彩手绘风格"
    }}
  ]
}}

请严格按照JSON格式输出，不要有其他文字说明。"""
        
        return prompt
    
    def _adjust_for_age(self, age: int, story: Dict) -> Dict:
        """
        根据年龄调整故事内容
        
        Args:
            age: 孩子年龄
            story: 故事数据
        
        Returns:
            Dict: 调整后的故事
        """
        pages = story.get('pages', [])
        
        # 根据年龄设置最大字数
        max_words_map = {3: 20, 4: 20, 5: 20, 6: 30, 7: 30, 8: 30, 9: 40, 10: 40, 11: 40, 12: 40}
        max_words = max_words_map.get(age, 30)
        
        # 调整每页文字长度
        for page in pages:
            text = page.get('text', '')
            if len(text) > max_words:
                # 简化文字
                words = text.split('，')
                page['text'] = '，'.join(words[:max_words // 5]) + '。'
        
        return story
    
    def _parse_story_from_text(self, text: str) -> Dict:
        """
        从文本中解析故事（当JSON解析失败时）
        
        Args:
            text: 原始文本
        
        Returns:
            Dict: 解析后的故事
        """
        # 这里实现一个简单的解析逻辑
        # 实际项目中可能需要更复杂的NLP处理
        
        pages = []
        lines = text.split('\n')
        
        current_page = 1
        current_text = ""
        current_scene = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('第') and '页' in line:
                # 保存上一页
                if current_text:
                    pages.append({
                        'page': current_page,
                        'text': current_text,
                        'scene_description': current_scene or '温馨的儿童场景，色彩明亮'
                    })
                    current_page += 1
                    current_text = ""
                    current_scene = ""
            elif line.startswith('场景：') or line.startswith('画面：'):
                current_scene = line.replace('场景：', '').replace('画面：', '')
            else:
                current_text += line
        
        # 保存最后一页
        if current_text:
            pages.append({
                'page': current_page,
                'text': current_text,
                'scene_description': current_scene or '温馨的儿童场景，色彩明亮'
            })
        
        return {'pages': pages}
