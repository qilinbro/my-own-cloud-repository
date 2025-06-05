import requests
import logging
import argparse
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning
from tqdm import tqdm
import os
import time  # 添加time模块导入

# 禁用不安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 设置保存目录（使用绝对路径）
SAVE_DIR = 'D:/code_repository/getnleman'

def fetch_image(url, retries=3):
    """获取图片内容"""
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=30, verify=False)
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                if 'image' in content_type.lower():
                    return response.content
                else:
                    logger.warning(f"响应不是图片类型: {content_type}")
            else:
                logger.warning(f"请求返回非200状态码: {response.status_code}")
        except requests.Timeout:
            logger.warning(f"请求超时 (尝试 {attempt + 1}/{retries})")
        except Exception as e:
            logger.warning(f"请求失败 (尝试 {attempt + 1}/{retries}): {str(e)}")
        
        if attempt < retries - 1:
            time.sleep(2 ** attempt)
    
    raise Exception(f"在 {retries} 次尝试后仍然无法获取图片")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='爬取指定数量的图片')
    parser.add_argument('-n', '--number', type=int, default=1, help='要爬取的图片数量（默认为1）')
    args = parser.parse_args()

    # 创建保存目录
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    url = 'https://t.alcy.cc/ycy'
    success_count = 0
    
    try:
        logger.info(f"开始爬取 {args.number} 张图片...")
        
        # 使用tqdm显示进度
        for i in tqdm(range(args.number), desc="爬取进度"):
            try:
                image_data = fetch_image(url)
                
                # 保存图片
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(SAVE_DIR, f'ycy_image_{timestamp}.webp')
                
                with open(filename, 'wb') as f:
                    f.write(image_data)
                
                success_count += 1
                logger.debug(f"成功保存图片: {filename}")
                
                # 添加短暂延迟，避免请求过于频繁
                if i < args.number - 1:
                    time.sleep(0.5)
                    
            except Exception as e:
                logger.error(f"下载第 {i+1} 张图片时出错: {str(e)}")
        
        logger.info(f"爬取完成！成功下载 {success_count} 张图片，保存在 {SAVE_DIR} 目录")
        
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")

if __name__ == '__main__':
    main()