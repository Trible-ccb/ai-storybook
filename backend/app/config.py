import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """应用配置"""
    # Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'True'
    
    # 服务器配置
    SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
    # 支持 Render 的 PORT 环境变量，默认为 5000
    SERVER_PORT = int(os.getenv('PORT', os.getenv('SERVER_PORT', 5000)))
    
    # 数据库配置
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_NAME = os.getenv('DB_NAME', 'ai_storybook')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
        'pool_size': 10,
        'max_overflow': 20
    }
    
    # Redis配置
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
    
    # 阿里云OSS配置
    OSS_ACCESS_KEY_ID = os.getenv('OSS_ACCESS_KEY_ID')
    OSS_ACCESS_KEY_SECRET = os.getenv('OSS_ACCESS_KEY_SECRET')
    OSS_BUCKET_NAME = os.getenv('OSS_BUCKET_NAME', 'ai-storybook')
    OSS_ENDPOINT = os.getenv('OSS_ENDPOINT')
    
    # 通义千问API配置
    DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')
    
    # 支付配置
    WECHAT_PAY_APP_ID = os.getenv('WECHAT_PAY_APP_ID')
    WECHAT_PAY_MCH_ID = os.getenv('WECHAT_PAY_MCH_ID')
    WECHAT_PAY_API_KEY = os.getenv('WECHAT_PAY_API_KEY')
    WECHAT_PAY_CERT_PATH = os.getenv('WECHAT_PAY_CERT_PATH')
    WECHAT_PAY_KEY_PATH = os.getenv('WECHAT_PAY_KEY_PATH')

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
