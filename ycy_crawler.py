import requests
import logging
import argparse
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning
from tqdm import tqdm
import os
import time
import concurrent.futures
from functools import wraps
from typing import Optional

# 禁用不安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 默认配置
DEFAULT_CONFIG = {
    'save_dir': 'D:/getnleman',
    'retries': 3,
    'retry_delay': 2,
    'request_timeout': 30,
    'concurrent_downloads': 3,
    'download_interval': 0.5
}

def retry_with_backoff(retries=DEFAULT_CONFIG['retries'], delay=DEFAULT_CONFIG['retry_delay']):
    """重试装饰器，使用指数退避策略"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except requests.Timeout:
                    logger.warning(f"请求超时 (尝试 {attempt + 1}/{retries})")
                except requests.RequestException as e:
                    logger.warning(f"请求异常 (尝试 {attempt + 1}/{retries}): {str(e)}")
                except Exception as e:
                    logger.warning(f"未知错误 (尝试 {attempt + 1}/{retries}): {str(e)}")
                
                if attempt < retries - 1:
                    sleep_time = delay * (2 ** attempt)
                    time.sleep(sleep_time)
            raise Exception(f"在 {retries} 次尝试后仍然失败")
        return wrapper
    return decorator

def validate_image(content: bytes) -> bool:
    """验证内容是否为有效的图片"""
    # 检查文件头部特征
    image_headers = {
        b'\xFF\xD8\xFF': 'jpg',
        b'\x89PNG\r\n': 'png',
        b'RIFF': 'webp',
        b'GIF8': 'gif'
    }
    for header, format_name in image_headers.items():
        if content.startswith(header):
            return True
    return False

@retry_with_backoff()
def fetch_image(url: str, timeout: int = DEFAULT_CONFIG['request_timeout']) -> Optional[bytes]:
    """获取图片内容"""
    response = requests.get(url, timeout=timeout, verify=False)
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type', '')
        if 'image' in content_type.lower() and validate_image(response.content):
            return response.content
        else:
            logger.warning(f"响应不是有效的图片: {content_type}")
            return None
    else:
        logger.warning(f"请求返回非200状态码: {response.status_code}")
        return None

def download_image(url: str, save_dir: str, index: int) -> bool:
    """下载单个图片"""
    try:
        image_data = fetch_image(url)
        if image_data:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(save_dir, f'ycy_image_{timestamp}_{index}.webp')
            
            with open(filename, 'wb') as f:
                f.write(image_data)
            
            logger.debug(f"成功保存图片: {filename}")
            return True
    except Exception as e:
        logger.error(f"下载第 {index} 张图片时出错: {str(e)}")
    return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='爬取指定数量的图片')
    parser.add_argument('-n', '--number', type=int, default=1, help='要爬取的图片数量（默认为1）')
    parser.add_argument('-d', '--dir', type=str, default=DEFAULT_CONFIG['save_dir'], help='保存目录路径')
    parser.add_argument('-c', '--concurrent', type=int, default=DEFAULT_CONFIG['concurrent_downloads'], 
                        help='并发下载数量')
    args = parser.parse_args()

    # 创建保存目录
    save_dir = os.path.expanduser(args.dir)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    url = 'https://t.alcy.cc/ycy'
    success_count = 0
    
    try:
        logger.info(f"开始爬取 {args.number} 张图片...")
        
        # 使用线程池进行并发下载
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrent) as executor:
            future_to_index = {
                executor.submit(download_image, url, save_dir, i): i 
                for i in range(args.number)
            }
            
            # 使用tqdm显示总体进度
            with tqdm(total=args.number, desc="下载进度") as pbar:
                for future in concurrent.futures.as_completed(future_to_index):
                    if future.result():
                        success_count += 1
                    pbar.update(1)
                    
                    # 添加短暂延迟，避免请求过于频繁
                    time.sleep(DEFAULT_CONFIG['download_interval'])
        
        logger.info(f"爬取完成！成功下载 {success_count} 张图片，保存在 {save_dir} 目录")
        
    except KeyboardInterrupt:
        logger.info("用户中断下载")
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")

if __name__ == '__main__':
    main()