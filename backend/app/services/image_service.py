"""
图像生成服务
"""
import os
import logging
import requests
import oss2
from dashscope import ImageSynthesis
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class ImageService:
    """图像生成服务类"""
    
    def __init__(self, api_key: str, oss_config: Dict):
        """
        初始化图像生成服务
        
        Args:
            api_key: 通义万相API密钥
            oss_config: OSS配置
        """
        self.api_key = api_key
        self.oss_config = oss_config
        self.oss_bucket = self._init_oss_bucket()
    
    def _init_oss_bucket(self):
        """初始化OSS Bucket"""
        try:
            auth = oss2.Auth(
                self.oss_config['access_key_id'],
                self.oss_config['access_key_secret']
            )
            bucket = oss2.Bucket(
                auth,
                self.oss_config['endpoint'],
                self.oss_config['bucket_name']
            )
            return bucket
        except Exception as e:
            logger.error(f"初始化OSS Bucket失败: {str(e)}")
            return None
    
    def generate_single_image(self, image_request: Dict) -> Dict:
        """
        生成单张图片
        
        Args:
            image_request: 图像生成请求
                - prompt: 场景描述
                - child_name: 孩子名字
                - toys_name: 玩具名字
                - visual_style: 视觉风格
                - reference_image: 参考图片URL（垫图）
                - page_index: 页码
        
        Returns:
            Dict: 包含成功状态和图片URL
        """
        try:
            # 构建Prompt
            prompt = self._build_image_prompt(image_request)
            
            # 调用通义万相API
            response = ImageSynthesis.call(
                api_key=self.api_key,
                model='wanx-v1',
                prompt=prompt,
                reference_image=image_request.get('reference_image'),  # 垫图，保持角色一致性
                n=1,
                size='1024*1024'
            )
            
            # 解析响应
            if response.status_code == 200:
                image_url = response.output.results[0].url
                
                # 下载并上传到OSS
                oss_url = self._download_and_upload(image_url, f"page_{image_request.get('page_index', 1)}.jpg")
                
                return {
                    'success': True,
                    'image_url': oss_url,
                    'original_url': image_url
                }
            else:
                logger.error(f"图像生成API调用失败: {response.message}")
                return {
                    'success': False,
                    'error': f'生成失败: {response.message}'
                }
        
        except Exception as e:
            logger.error(f"生成图片时发生错误: {str(e)}")
            return {
                'success': False,
                'error': f'生成失败: {str(e)}'
            }
    
    def generate_all_images(self, story: List[Dict], image_config: Dict) -> Dict:
        """
        批量生成所有图片
        
        Args:
            story: 故事页面列表
            image_config: 图像配置
                - reference_image: 参考图片URL
                - child_name: 孩子名字
                - child_characteristics: 孩子特点
                - toys_name: 玩具名字
                - toys_characteristics: 玩具特点
                - visual_style: 视觉风格
                - age: 孩子年龄
        
        Returns:
            Dict: 包含成功状态和所有图片URL
        """
        try:
            images = []
            success_count = 0
            fail_count = 0
            
            for page in story:
                page_index = page['page']
                scene_description = page.get('scene_description', '')
                
                # 构建图像生成请求
                image_request = {
                    'page_index': page_index,
                    'scene_description': scene_description,
                    'child_name': image_config.get('child_name'),
                    'child_characteristics': image_config.get('child_characteristics'),
                    'toys_name': image_config.get('toys_name'),
                    'toys_characteristics': image_config.get('toys_characteristics', ''),
                    'visual_style': image_config.get('visual_style', '水彩手绘'),
                    'age': image_config.get('age', 5),
                    'reference_image': image_config.get('reference_image')
                }
                
                # 生成图片
                result = self.generate_single_image(image_request)
                
                if result['success']:
                    images.append({
                        'page': page_index,
                        'image_url': result['image_url']
                    })
                    success_count += 1
                    logger.info(f"第{page_index}页图片生成成功")
                else:
                    # 失败重试一次
                    logger.warning(f"第{page_index}页图片生成失败，尝试重试...")
                    result = self.generate_single_image(image_request)
                    
                    if result['success']:
                        images.append({
                            'page': page_index,
                            'image_url': result['image_url']
                        })
                        success_count += 1
                    else:
                        images.append({
                            'page': page_index,
                            'image_url': None,
                            'error': result.get('error', '未知错误')
                        })
                        fail_count += 1
                        logger.error(f"第{page_index}页图片生成失败: {result.get('error')}")
            
            return {
                'success': fail_count == 0,
                'images': images,
                'success_count': success_count,
                'fail_count': fail_count
            }
        
        except Exception as e:
            logger.error(f"批量生成图片时发生错误: {str(e)}")
            return {
                'success': False,
                'error': f'批量生成失败: {str(e)}',
                'images': []
            }
    
    def _build_image_prompt(self, request: Dict) -> str:
        """
        构建图像生成Prompt
        
        Args:
            request: 图像生成请求
        
        Returns:
            str: 完整的Prompt
        """
        scene_description = request.get('scene_description', '')
        child_name = request.get('child_name', '小朋友')
        child_characteristics = request.get('child_characteristics', '可爱的小朋友')
        toys_name = request.get('toys_name', '小玩偶')
        toys_characteristics = request.get('toys_characteristics', '')
        visual_style = request.get('visual_style', '水彩手绘')
        age = request.get('age', 5)
        
        # 视觉风格配置
        visual_styles = {
            "水彩手绘": {
                "description": "柔和的水彩笔触，温暖色调，梦幻感",
                "color_palette": "柔和粉色、蓝色、黄色、橙色",
                "composition": "中心构图，留白充足"
            },
            "卡通风格": {
                "description": "线条清晰，色彩鲜艳，造型可爱",
                "color_palette": "明亮橙色、绿色、紫色、蓝色",
                "composition": "动态构图，活力十足"
            },
            "国风": {
                "description": "传统水墨风格，淡雅古典",
                "color_palette": "墨色、朱红、黛蓝、米黄",
                "composition": "留白意境，禅意构图"
            }
        }
        
        style = visual_styles.get(visual_style, visual_styles["水彩手绘"])
        
        # 根据年龄调整视觉风格
        if age <= 5:
            style['description'] += "，造型简洁，色彩柔和，适合低龄儿童"
        elif age <= 8:
            style['description'] += "，细节丰富，色彩明快，充满童趣"
        else:
            style['description'] += "，构图精美，色彩和谐，富有艺术感"
        
        prompt = f"""儿童绘本插图，第{request.get('page_index', 1)}页画面

【画面描述】
{scene_description}

【角色设定】
主角：{child_name}，{child_characteristics}
配饰：{toys_name}，{toys_characteristics if toys_characteristics else '孩子最爱的玩具伙伴'}

【视觉风格】
- 整体风格：{visual_style}
- 风格描述：{style['description']}
- 色彩：{style['color_palette']}
- 构图：{style['composition']}
- 年龄适配：适合{age}岁儿童审美

【技术要求】
- 分辨率：1024x1024
- 比例：1:1
- 画质：高清，细节丰富
- 光影：自然柔和，温馨明亮

请确保角色形象与参考图保持一致，画面清晰，色彩协调，适合儿童阅读。"""
        
        return prompt
    
    def _download_and_upload(self, image_url: str, filename: str) -> Optional[str]:
        """
        下载图片并上传到OSS
        
        Args:
            image_url: 图片URL
            filename: 文件名
        
        Returns:
            Optional[str]: OSS URL，失败返回None
        """
        try:
            # 下载图片
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            image_data = response.content
            
            # 上传到OSS
            if self.oss_bucket:
                oss_key = f"storybooks/{filename}"
                self.oss_bucket.put_object(oss_key, image_data)
                
                # 返回OSS URL
                oss_url = f"https://{self.oss_config['bucket_name']}.{self.oss_config['endpoint'].replace('https://', '')}/{oss_key}"
                logger.info(f"图片已上传到OSS: {oss_url}")
                return oss_url
            else:
                logger.error("OSS Bucket未初始化")
                return None
        
        except Exception as e:
            logger.error(f"下载并上传图片失败: {str(e)}")
            return None
