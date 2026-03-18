"""
任务处理器 - 支持断点续传
"""
import logging
from app.services.task_service import TaskService
from app.services.llm_service import LLMService
from app.services.image_service import ImageService
from app.config import Config

logger = logging.getLogger(__name__)


class TaskProcessor:
    """任务处理器"""

    def __init__(self, task_id, data=None):
        """
        初始化处理器

        Args:
            task_id: 任务ID
            data: 任务数据（如果是新任务）
        """
        self.task_id = task_id
        self.data = data
        self.task = None

    def process(self):
        """
        处理任务（支持断点续传）
        """
        try:
            # 获取任务
            self.task = TaskService.get_task(self.task_id)
            if not self.task:
                raise Exception(f"任务不存在: {self.task_id}")

            # 如果是新任务，初始化数据
            if not self.data:
                self.data = self.task.input_data

            # 更新任务状态为处理中
            TaskService.update_task_status(
                self.task_id,
                'processing',
                current_step='uploading_images',
                progress=5,
                message='正在上传图片...'
            )

            # 执行各个步骤
            self._process_story_generation()
            self._process_image_generation()
            self._finalize_result()

            # 完成任务
            TaskService.complete_task(self.task_id, {
                'title': self.task.title,
                'pages': self.final_result,
                'stats': {
                    'total_pages': len(self.final_result),
                    'retry_count': self.task.retry_count
                }
            })

            logger.info(f"任务完成: {self.task_id}")
            return True

        except Exception as e:
            logger.error(f"任务处理失败: {self.task_id}, 错误: {str(e)}")
            TaskService.fail_task(self.task_id, str(e))
            return False

    def _process_story_generation(self):
        """
        处理故事生成
        """
        # 检查是否已经完成
        if self.task.status == 'processing' and self.task.story_data:
            logger.info(f"故事已存在，跳过生成")
            self.story = self.task.story_data
            return

        # 更新状态
        TaskService.update_task_status(
            self.task_id,
            'processing',
            current_step='story_generating',
            progress=10,
            message='正在生成故事...'
        )

        # 生成故事
        llm_service = LLMService(Config.DASHSCOPE_API_KEY)

        story_request = {
            'age': self.data.get('age'),
            'theme': self.data.get('theme'),
            'child_name': self.data.get('child_name'),
            'child_characteristics': self.data.get('child_characteristics', '可爱的小朋友'),
            'toys_name': self.data.get('toys_name'),
            'creative_idea': self.data.get('creative_idea'),
            'page_count': self.data.get('page_count', 12)
        }

        story_result = llm_service.generate_story(story_request)

        if not story_result['success']:
            raise Exception(story_result.get('error', '故事生成失败'))

        # 保存故事数据
        self.story = story_result['story']['pages']
        TaskService.update_task_story(self.task_id, self.story)

        # 更新状态
        TaskService.update_task_status(
            self.task_id,
            'processing',
            current_step='story_completed',
            progress=40,
            message=f'故事生成成功，共{len(self.story)}页'
        )

    def _process_image_generation(self):
        """
        处理图片生成（支持断点续传）
        """
        # 更新状态
        TaskService.update_task_status(
            self.task_id,
            'processing',
            current_step='images_generating',
            progress=50,
            message='正在生成插图...'
        )

        # 获取已生成的图片
        existing_images = {}
        if self.task.images_data:
            for img in self.task.images_data:
                existing_images[img['page']] = img

        # 初始化图片服务
        oss_config = {
            'access_key_id': Config.OSS_ACCESS_KEY_ID,
            'access_key_secret': Config.OSS_ACCESS_KEY_SECRET,
            'endpoint': Config.OSS_ENDPOINT,
            'bucket_name': Config.OSS_BUCKET_NAME
        }

        image_service = ImageService(Config.DASHSCOPE_API_KEY, oss_config)

        # 逐页生成图片（跳过已生成的）
        total_pages = len(self.story)
        generated_images = []

        for page in self.story:
            page_num = page['page']

            # 检查是否已经生成
            if page_num in existing_images:
                logger.info(f"第{page_num}页图片已存在，跳过")
                generated_images.append(existing_images[page_num])
                continue

            # 生成图片
            image_config = {
                'reference_image': self.data.get('child_photo'),
                'child_name': self.data.get('child_name'),
                'child_characteristics': self.data.get('child_characteristics'),
                'toys_name': self.data.get('toys_name'),
                'toys_characteristics': self.data.get('toys_characteristics', ''),
                'visual_style': self.data.get('visual_style', '水彩手绘'),
                'age': self.data.get('age')
            }

            try:
                image_result = image_service.generate_image(page, image_config)

                if image_result['success']:
                    generated_images.append(image_result)
                    logger.info(f"第{page_num}页图片生成成功")
                else:
                    logger.warning(f"第{page_num}页图片生成失败: {image_result.get('error')}")
                    generated_images.append({
                        'page': page_num,
                        'image_url': None,
                        'error': image_result.get('error')
                    })

                # 更新进度
                progress = 50 + int((len(generated_images) / total_pages) * 40)
                TaskService.update_task_status(
                    self.task_id,
                    'processing',
                    current_step='images_generating',
                    progress=progress,
                    message=f'正在生成插图... ({len(generated_images)}/{total_pages})'
                )

                # 保存中间结果
                TaskService.update_task_images(self.task_id, generated_images)

            except Exception as e:
                logger.error(f"第{page_num}页图片生成异常: {str(e)}")
                generated_images.append({
                    'page': page_num,
                    'image_url': None,
                    'error': str(e)
                })
                TaskService.update_task_images(self.task_id, generated_images)

        self.images = generated_images

        # 更新状态
        TaskService.update_task_status(
            self.task_id,
            'processing',
            current_step='images_completed',
            progress=90,
            message='插图生成完成'
        )

    def _finalize_result(self):
        """
        最终结果处理
        """
        # 合并故事和插图
        self.final_result = []

        for page in self.story:
            page_num = page['page']
            # 找到对应的图片
            image_data = next((img for img in self.images if img['page'] == page_num), None)

            self.final_result.append({
                'page': page_num,
                'text': page['text'],
                'scene_description': page['scene_description'],
                'image_url': image_data['image_url'] if image_data else None
            })

        # 更新状态
        TaskService.update_task_status(
            self.task_id,
            'processing',
            current_step='finalizing',
            progress=95,
            message='正在整理最终结果...'
        )

    @staticmethod
    def retry_task(task_id):
        """
        重试失败的任务

        Args:
            task_id: 任务ID

        Returns:
            success: 是否成功
        """
        try:
            task = TaskService.get_task(task_id)
            if not task:
                return False

            # 增加重试次数
            TaskService.increment_retry_count(task_id)

            # 创建处理器并处理
            processor = TaskProcessor(task_id)
            return processor.process()

        except Exception as e:
            logger.error(f"重试任务失败: {task_id}, 错误: {str(e)}")
            return False
