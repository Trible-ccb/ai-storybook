"""
任务管理API
"""
from flask import Blueprint, request, jsonify
import logging
import threading
from app.services.task_service import TaskService
from app.services.task_processor import TaskProcessor

logger = logging.getLogger(__name__)

task_bp = Blueprint('task', __name__)


@task_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    """
    获取任务列表

    Query参数:
    - limit: 返回数量（默认20，最大50）
    - offset: 偏移量（默认0）
    - status: 状态过滤（可选）

    响应:
    {
        "success": true,
        "tasks": [...],
        "total": 10
    }
    """
    try:
        # 限制最大查询数量
        limit = min(int(request.args.get('limit', 20)), 50)
        offset = int(request.args.get('offset', 0))
        status = request.args.get('status')

        # 查询任务（按创建时间倒序）
        query = Task.query.order_by(Task.created_at.desc())
        
        # 过滤状态
        if status:
            query = query.filter(Task.status == status)
        
        # 执行查询
        tasks = query.limit(limit).offset(offset).all()

        return jsonify({
            'success': True,
            'tasks': [t.to_dict() for t in tasks],
            'total': len(tasks)
        }), 200

    except Exception as e:
        logger.error(f"获取任务列表失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500


@task_bp.route('/api/task/<task_id>', methods=['GET'])
def get_task_detail(task_id):
    """
    获取任务详情

    响应:
    {
        "success": true,
        "task": {
            "id": "...",
            "status": "...",
            "result": {...},
            "progress": [...]
        }
    }
    """
    try:
        task = TaskService.get_task(task_id)

        if not task:
            return jsonify({
                'success': False,
                'error': '任务不存在'
            }), 404

        # 获取进度记录
        progress_records = TaskService.get_progress_records(task_id)

        return jsonify({
            'success': True,
            'task': task.to_detail_dict(),
            'progress': [p.to_dict() for p in progress_records]
        }), 200

    except Exception as e:
        logger.error(f"获取任务详情失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500


@task_bp.route('/api/task/<task_id>/retry', methods=['POST'])
def retry_task(task_id):
    """
    重试失败的任务

    响应:
    {
        "success": true,
        "message": "任务已重新开始处理"
    }
    """
    try:
        task = TaskService.get_task(task_id)

        if not task:
            return jsonify({
                'success': False,
                'error': '任务不存在'
            }), 404

        # 检查任务状态
        if task.status == 'completed':
            return jsonify({
                'success': False,
                'error': '任务已完成，无需重试'
            }), 400

        # 在后台线程中重试
        thread = threading.Thread(
            target=TaskProcessor.retry_task,
            args=(task_id,)
        )
        thread.daemon = True
        thread.start()

        logger.info(f"任务 {task_id} 开始重试")

        return jsonify({
            'success': True,
            'message': '任务已重新开始处理',
            'retry_count': task.retry_count + 1
        }), 200

    except Exception as e:
        logger.error(f"重试任务失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500


@task_bp.route('/api/task/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    删除任务

    响应:
    {
        "success": true,
        "message": "任务已删除"
    }
    """
    try:
        success = TaskService.delete_task(task_id)

        if not success:
            return jsonify({
                'success': False,
                'error': '任务不存在'
            }), 404

        return jsonify({
            'success': True,
            'message': '任务已删除'
        }), 200

    except Exception as e:
        logger.error(f"删除任务失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500
