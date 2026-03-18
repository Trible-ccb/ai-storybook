"""
PDF生成服务
"""
import os
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class PDFService:
    """PDF生成服务类"""
    
    def __init__(self):
        """初始化PDF服务"""
        pass
    
    def generate_pdf_html(self, storybook: Dict, title: str) -> str:
        """
        生成PDF的HTML内容
        
        Args:
            storybook: 绘本数据
            title: 绘本标题
        
        Returns:
            str: HTML内容
        """
        pages = storybook.get('pages', [])
        
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Arial', 'Microsoft YaHei', sans-serif;
            background-color: #f5f5f5;
        }}
        
        .page {{
            page-break-after: always;
            padding: 40px;
            text-align: center;
            background-color: white;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        
        .page-image {{
            max-width: 100%;
            max-height: 500px;
            object-fit: contain;
            margin-bottom: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .page-text {{
            font-size: 24px;
            line-height: 1.8;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        .page-number {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            font-size: 14px;
            color: #999;
        }}
        
        .cover {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 80px 40px;
        }}
        
        .cover-title {{
            font-size: 48px;
            margin-bottom: 20px;
            font-weight: bold;
        }}
        
        .cover-subtitle {{
            font-size: 24px;
            opacity: 0.9;
        }}
    </style>
</head>
<body>
    <!-- 封面 -->
    <div class="page cover">
        <h1 class="cover-title">{title}</h1>
        <p class="cover-subtitle">一份独一无二的童年记忆</p>
    </div>
"""
        
        # 生成每一页
        for i, page in enumerate(pages, 1):
            image_url = page.get('image_url', '')
            text = page.get('text', '')
            
            html += f"""
    <!-- 第{i}页 -->
    <div class="page">
        <img src="{image_url}" alt="第{i}页" class="page-image" />
        <p class="page-text">{text}</p>
        <span class="page-number">{i}</span>
    </div>
"""
        
        # 封底
        html += """
    <!-- 封底 -->
    <div class="page" style="background: linear-gradient(135deg, #764ba2 0%, #667eea 100%); color: white;">
        <p style="font-size: 24px; opacity: 0.9;">用AI记录孩子独一无二的童年</p>
        <p style="font-size: 18px; margin-top: 20px; opacity: 0.7;">Powered by AI Storybook</p>
    </div>
</body>
</html>
"""
        
        return html
    
    def generate_pdf(self, html_content: str, output_path: str) -> bool:
        """
        从HTML生成PDF文件
        
        Args:
            html_content: HTML内容
            output_path: 输出文件路径
        
        Returns:
            bool: 是否成功
        """
        try:
            # 导入PDF生成库
            # 注意：这里需要安装 pdfkit 或 weasyprint
            # 前端使用 html2pdf.js，后端主要生成HTML供前端使用
            # 如果需要后端生成PDF，可以使用以下代码
            
            import weasyprint
            
            # 生成PDF
            weasyprint.HTML(string=html_content).write_pdf(output_path)
            
            logger.info(f"PDF文件已生成: {output_path}")
            return True
        
        except ImportError:
            logger.warning("weasyprint未安装，无法生成PDF。请使用前端html2pdf.js生成。")
            return False
        
        except Exception as e:
            logger.error(f"生成PDF失败: {str(e)}")
            return False
    
    def generate_preview_url(self, storybook: Dict, title: str) -> str:
        """
        生成预览URL（前端使用）
        
        Args:
            storybook: 绘本数据
            title: 绘本标题
        
        Returns:
            str: HTML内容（直接返回给前端）
        """
        html = self.generate_pdf_html(storybook, title)
        return html
