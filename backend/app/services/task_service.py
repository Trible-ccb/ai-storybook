"""
任务服务 - 支持持久化和断点续传
"""
import uuid
import json
from datetime import datetime
from app.models.task import Task, TaskProgress
from run import db
from flask import current_app


class TaskService:
    """任务服务"""

    @staticmethod
    def create_task(title, input_data):
        """
        创建任务

        Args:
            title: 任务标题
            input_data: 输入数据

        Returns:
            task: 任务对象
        """
        task = Task(
            id=str(uuid.uuid4()),
            title=title,
            status='pending',
            current_step=None,
            progress=0,
            input_data=input_data,
            created_at=datetime.utcnow()
        )

        db.session.add(task)
        db.session.commit()

        # 创建初始进度记录
        TaskService._create_progress_record(task.id, 'task_created', 'completed', 100, '任务已创建')

        return task

    @staticmethod
    def _create_progress_record(task_id, step_name, step_status, step_progress, message):
        """
        创建进度记录

        Args:
            task_id: 任务ID
            step_name: 步骤名称
            step_status: 步骤状态
            step_progress: 步骤进度
            message: 消息
        """
        progress = TaskProgress(
            task_id=task_id,
            step_name=step_name,
            step_status=step_status,
            step_progress=step_progress,
            message=message
        )

        db.session.add(progress)
        db.session.commit()

    @staticmethod
    def update_task_status(task_id, status, current_step=None, progress=None, message=None):
        """
        更新任务状态

        Args:
            task_id: 任务ID
            status: 任务状态
            current_step: 当前步骤
            progress: 进度
            message: 消息
        """
        task = Task.query.get(task_id)
        if not task:
            return None

        task.status = status
        task.updated_at = datetime.utcnow()

        if current_step:
            task.current_step = current_step

        if progress is not None:
            task.progress = progress

        # 更新或创建进度记录
        if current_step:
            existing_progress = TaskProgress.query.filter_by(
                task_id=task_id,
                step_name=current_step
            ).first()

            if existing_progress:
                existing_progress.step_status = status
                existing_progress.step_progress = progress
                existing_progress.message = message
                existing_progress.updated_at = datetime.utcnow()
            else:
                TaskService._create_progress_record(task_id, current_step, status, progress, message)

        db.session.commit()

        return task

    @staticmethod
    def update_task_story(task_id, story_data):
        """
        更新故事数据

        Args:
            task_id: 任务ID
            story_data: 故事数据
        """
        task = Task.query.get(task_id)
        if not task:
            return None

        task.story_data = story_data
        task.updated_at = datetime.utcnow()
        db.session.commit()

        return task

    @staticmethod
    def update_task_images(task_id, images_data):
        """
        更新图片数据

        Args:
            task_id: 任务ID
            images_data: 图片数据
        """
        task = Task.query.get(task_id)
        if not task:
            return None

        task.images_data = images_data
        task.updated_at = datetime.utcnow()
        db.session.commit()

        return task

    @staticmethod
    def complete_task(task_id, result_data):
        """
        完成任务

        Args:
            task_id: 任务ID
            result_data: 结果数据
        """
        task = Task.query.get(task_id)
        if not task:
            return None

        task.status = 'completed'
        task.progress = 100
        task.result_data = result_data
        task.completed_at = datetime.utcnow()
        task.updated_at = datetime.utcnow()

        db.session.commit()

        return task

    @staticmethod
    def fail_task(task_id, error_message):
        """
        任务失败

        Args:
            task_id: 任务ID
            error_message: 错误消息
        """
        task = Task.query.get(task_id)
        if not task:
            return None

        task.status = 'failed'
        task.error_message = error_message
        task.updated_at = datetime.utcnow()

        db.session.commit()

        return task

    @staticmethod
    def increment_retry_count(task_id):
        """
        增加重试次数

        Args:
            task_id: 任务ID
        """
        task = Task.query.get(task_id)
        if not task:
            return None

        task.retry_count += 1
        task.updated_at = datetime.utcnow()

        db.session.commit()

        return task

    @staticmethod
    def get_task(task_id):
        """
        获取任务

        Args:
            task_id: 任务ID

        Returns:
            task: 任务对象
        """
        return Task.query.get(task_id)

    @staticmethod
    def get_tasks(limit=20, offset=0):
        """
        获取任务列表

        Args:
            limit: 限制数量
            offset: 偏移量

        Returns:
            tasks: 任务列表
        """
        return Task.query.order_by(Task.created_at.desc()).limit(limit).offset(offset).all()

    @staticmethod
    def delete_task(task_id):
        """
        删除任务

        Args:
            task_id: 任务ID
        """
        task = Task.query.get(task_id)
        if not task:
            return False

        # 删除关联的进度记录
        TaskProgress.query.filter_by(task_id=task_id).delete()

        # 删除任务
        db.session.delete(task)
        db.session.commit()

        return True

    @staticmethod
    def get_progress_records(task_id):
        """
        获取任务的进度记录

        Args:
            task_id: 任务ID

        Returns:
            progress_records: 进度记录列表
        """
        return TaskProgress.query.filter_by(task_id=task_id).order_by(TaskProgress.created_at).all()
