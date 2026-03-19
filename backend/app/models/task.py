"""
任务数据库模型
"""
from datetime import datetime
from app.extensions import db


class Task(db.Model):
    """任务模型"""
    __tablename__ = 'tasks'

    id = db.Column(db.String(36), primary_key=True)  # UUID
    title = db.Column(db.String(200), nullable=False)  # 任务标题
    
    # 任务状态
    status = db.Column(db.String(50), default='pending')  # pending, processing, completed, failed, cancelled
    current_step = db.Column(db.String(50))  # 当前步骤
    progress = db.Column(db.Integer, default=0)  # 进度 0-100
    
    # 任务数据
    input_data = db.Column(db.JSON)  # 输入参数
    story_data = db.Column(db.JSON)  # 故事数据
    images_data = db.Column(db.JSON)  # 图片数据
    result_data = db.Column(db.JSON)  # 最终结果
    
    # 错误信息
    error_message = db.Column(db.Text)
    retry_count = db.Column(db.Integer, default=0)  # 重试次数
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'status': self.status,
            'current_step': self.current_step,
            'progress': self.progress,
            'error_message': self.error_message,
            'retry_count': self.retry_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'has_result': self.result_data is not None
        }
    
    def to_detail_dict(self):
        """转换为详细字典"""
        result = self.to_dict()
        
        # 根据状态返回不同的数据
        if self.status == 'completed' and self.result_data:
            result['result'] = self.result_data
        elif self.status == 'processing':
            # 返回当前步骤的中间结果
            if self.current_step in ['story_generating', 'images_generating']:
                result['story'] = self.story_data
                result['images'] = self.images_data
        
        return result


class TaskProgress(db.Model):
    """任务进度详情"""
    __tablename__ = 'task_progress'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(36), db.ForeignKey('tasks.id'), nullable=False)
    step_name = db.Column(db.String(100))  # 步骤名称
    step_status = db.Column(db.String(50))  # pending, processing, completed, failed
    step_progress = db.Column(db.Integer, default=0)  # 步骤进度
    message = db.Column(db.String(500))  # 步骤消息
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    task = db.relationship('Task', backref='progress_records')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'step_name': self.step_name,
            'step_status': self.step_status,
            'step_progress': self.step_progress,
            'message': self.message,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


def init_db():
    """初始化数据库表"""
    with db.app.app_context():
        db.create_all()
        print("数据库表创建成功")
