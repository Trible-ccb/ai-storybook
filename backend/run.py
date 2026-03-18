"""
Flask应用主入口
"""
import os
import sys
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 初始化数据库
db = SQLAlchemy()

def create_app(config_name='default'):
    """
    创建Flask应用

    Args:
        config_name: 配置名称（development/production/testing）

    Returns:
        Flask应用实例
    """
    app = Flask(__name__)

    # 加载配置
    from app.config import config
    app.config.from_object(config[config_name])

    # 启用CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # 初始化数据库
    db.init_app(app)

    # 注册蓝图
    from app.api.story import story_bp

    app.register_blueprint(story_bp)

    # 注册错误处理器
    register_error_handlers(app)

    # 注册根路由
    @app.route('/')
    def index():
        return jsonify({
            'name': 'AI Storybook API',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'story': '/api/generate-story',
                'complete': '/api/generate-complete-storybook'
            }
        })

    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy'
        })

    logger.info(f"应用启动成功，配置: {config_name}")

    return app

def register_error_handlers(app):
    """
    注册错误处理器
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': '请求参数错误'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': '资源不存在'
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"服务器错误: {str(error)}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.error(f"未处理的异常: {str(error)}")
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(error)}'
        }), 500

# 创建应用实例
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    from app.config import Config

    app.run(
        host=Config.SERVER_HOST,
        port=Config.SERVER_PORT,
        debug=Config.DEBUG
    )
