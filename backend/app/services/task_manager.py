"""
任务管理器 - 用于异步处理绘本生成任务
"""
import threading
import uuid
import logging
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    PROCESSING = "processing"
    STORY_GENERATED = "story_generated"
    IMAGES_GENERATED = "images_generated"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskManager:
    """任务管理器"""

    def __init__(self):
        self.tasks = {}
        self.lock = threading.Lock()

    def create_task(self, task_data):
        """
        创建新任务

        Args:
            task_data: 任务数据

        Returns:
            task_id: 任务ID
        """
        task_id = str(uuid.uuid4())

        with self.lock:
            self.tasks[task_id] = {
                'task_id': task_id,
                'status': TaskStatus.PENDING.value,
                'progress': 0,
                'progress_text': '任务已创建',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'data': task_data,
                'result': None,
                'error': None
            }

        logger.info(f"创建新任务: {task_id}")
        return task_id

    def get_task(self, task_id):
        """
        获取任务信息

        Args:
            task_id: 任务ID

        Returns:
            task: 任务信息，如果不存在则返回 None
        """
        with self.lock:
            return self.tasks.get(task_id)

    def update_task(self, task_id, **kwargs):
        """
        更新任务状态

        Args:
            task_id: 任务ID
            **kwargs: 要更新的字段

        Returns:
            True: 更新成功
            False: 任务不存在
        """
        with self.lock:
            if task_id not in self.tasks:
                return False

            task = self.tasks[task_id]
            task.update(kwargs)
            task['updated_at'] = datetime.now().isoformat()

            logger.debug(f"更新任务 {task_id}: {kwargs}")
            return True

    def set_task_status(self, task_id, status, progress=None, progress_text=None):
        """
        设置任务状态

        Args:
            task_id: 任务ID
            status: 任务状态
            progress: 进度（0-100）
            progress_text: 进度文本
        """
        update_data = {
            'status': status.value if isinstance(status, TaskStatus) else status
        }

        if progress is not None:
            update_data['progress'] = progress

        if progress_text is not None:
            update_data['progress_text'] = progress_text

        self.update_task(task_id, **update_data)

    def complete_task(self, task_id, result):
        """
        完成任务

        Args:
            task_id: 任务ID
            result: 任务结果
        """
        self.set_task_status(
            task_id,
            TaskStatus.COMPLETED,
            progress=100,
            progress_text='生成完成'
        )
        self.update_task(task_id, result=result)
        logger.info(f"任务完成: {task_id}")

    def fail_task(self, task_id, error):
        """
        任务失败

        Args:
            task_id: 任务ID
            error: 错误信息
        """
        self.set_task_status(
            task_id,
            TaskStatus.FAILED,
            progress_text=f'失败: {error}'
        )
        self.update_task(task_id, error=str(error))
        logger.error(f"任务失败: {task_id}, 错误: {error}")

    def delete_task(self, task_id):
        """
        删除任务

        Args:
            task_id: 任务ID

        Returns:
            True: 删除成功
            False: 任务不存在
        """
        with self.lock:
            if task_id in self.tasks:
                del self.tasks[task_id]
                logger.info(f"删除任务: {task_id}")
                return True
            return False

    def cleanup_old_tasks(self, max_age_hours=24):
        """
        清理旧任务

        Args:
            max_age_hours: 最大保留时间（小时）
        """
        import datetime as dt

        with self.lock:
            now = datetime.now()
            to_delete = []

            for task_id, task in self.tasks.items():
                created_at = datetime.fromisoformat(task['created_at'])
                age = now - created_at

                if age.total_seconds() > max_age_hours * 3600:
                    to_delete.append(task_id)

            for task_id in to_delete:
                del self.tasks[task_id]

            if to_delete:
                logger.info(f"清理了 {len(to_delete)} 个旧任务")


# 全局任务管理器实例
task_manager = TaskManager()
