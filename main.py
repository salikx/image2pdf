import os, time, yaml
from PIL import Image
import tempfile
from PyPDF2 import PdfMerger
from jmcomic import *
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_album_info(album_id):
    """获取漫画信息"""
    try:
        logging.info(f"正在获取漫画 {album_id} 的信息...")
        # 客户端
        client = JmOption.default().new_jm_client()
        album = client.get_album_detail(album_id)
        # 获取作者（如果有多个作者，使用第一个）
        author = album.author if album.authors else "未知作者"
        # 获取漫画名
        name = album.name
        # # 组合文件夹名
        # folder_name = f"【{author}】{name}"
        # logging.info(f"获取成功：{folder_name}")
        # return folder_name
        return name
    except Exception as e:
        logging.error(f"获取漫画信息失败: {e}")
        return None

def convert_to_pdf(input_folder, output_path, batch_size=50):
    """
    将文件夹中的图片转换为PDF，采用分段处理避免内存溢出
    
    Args:
        input_folder (str): 输入文件夹路径
        output_path (str): 输出PDF路径
        batch_size (int): 每批处理的图片数量
    """
    try:
        logging.info(f"开始处理文件夹：{input_folder}")
        start_time = time.time()
        
        # 获取所有图片文件
        images = []
        with os.scandir(input_folder) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    images.append(os.path.join(input_folder, entry.name))
        
        if not images:
            logging.warning(f"在 {input_folder} 中没有找到图片")
            return
        
        # 按文件名排序
        images.sort()
        total_images = len(images)
        logging.info(f"找到 {total_images} 张图片")
        
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            # 分批处理图片
            batch_pdfs = []
            for i in range(0, total_images, batch_size):
                batch_images = images[i:i + batch_size]
                batch_num = i // batch_size + 1
                total_batches = (total_images + batch_size - 1) // batch_size
                
                logging.info(f"处理第 {batch_num}/{total_batches} 批图片")
                
                # 处理当前批次的图片
                try:
                    # 处理第一张图片
                    first_image = Image.open(batch_images[0])
                    if first_image.mode != "RGB":
                        first_image = first_image.convert("RGB")
                    
                    # 处理剩余图片
                    remaining_images = []
                    for img_path in batch_images[1:]:
                        img = Image.open(img_path)
                        if img.mode != "RGB":
                            img = img.convert("RGB")
                        remaining_images.append(img)
                    
                    # 保存临时PDF
                    temp_pdf = os.path.join(temp_dir, f"temp_batch_{batch_num}.pdf")
                    first_image.save(temp_pdf, "PDF", save_all=True, append_images=remaining_images)
                    batch_pdfs.append(temp_pdf)
                    
                    # 清理内存
                    first_image.close()
                    for img in remaining_images:
                        img.close()
                    
                    logging.info(f"第 {batch_num} 批图片处理完成")
                except Exception as e:
                    logging.error(f"处理第 {batch_num} 批图片时出错: {e}")
                    continue
            
            # 合并所有临时PDF
            if batch_pdfs:
                logging.info(f"开始合并 {len(batch_pdfs)} 个临时PDF...")
                merger = PdfMerger()
                for pdf in batch_pdfs:
                    merger.append(pdf)
                merger.write(output_path)
                merger.close()
                logging.info(f"PDF合并完成：{output_path}")
            else:
                logging.warning("没有成功生成任何PDF")
        
        end_time = time.time()
        run_time = end_time - start_time
        logging.info(f"总运行时间：{run_time:.2f} 秒")
        
    except Exception as e:
        logging.error(f"转换PDF时出错: {e}")
        raise

def process_manga(album_ids, should_convert_pdf=True):
    """
    处理漫画下载和转换
    
    Args:
        album_ids (list): 漫画ID列表
        should_convert_pdf (bool): 是否转换为PDF格式，默认为True
    
    Returns:
        bool: 处理是否成功
    """
    try:
        logging.info("程序启动")
        # 自定义设置：
        config = os.path.join(os.path.dirname(__file__), "config.yml")
        logging.info(f"正在加载配置文件：{config}")
        
        if not os.path.exists(config):
            logging.error(f"配置文件不存在：{config}")
            return False
            
        loadConfig = JmOption.from_file(config)
        logging.info("配置文件加载成功")
        
        # 获取下载目录
        with open(config, "r", encoding="utf8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            base_path = data["dir_rule"]["base_dir"]
            
        if not os.path.exists(base_path):
            logging.info(f"创建下载目录：{base_path}")
            os.makedirs(base_path)
        
        # 下载漫画
        for id in album_ids:
            # 获取漫画信息
            folder_name = get_album_info(id)
            if folder_name:
                logging.info(f"开始下载：{folder_name}")
                download_album(id, loadConfig)
                logging.info(f"下载完成：{folder_name}")
                
                # 如果需要转换为PDF
                if should_convert_pdf:
                    manga_path = os.path.join(base_path, folder_name)
                    if os.path.exists(manga_path):
                        pdf_path = os.path.join(base_path, f"{folder_name}.pdf")
                        if os.path.exists(pdf_path):
                            logging.info(f"文件：《{folder_name}》 已存在，跳过")
                            continue
                        else:
                            logging.info(f"开始转换：{folder_name}")
                            convert_to_pdf(manga_path, pdf_path)
                    else:
                        logging.warning(f"漫画文件夹不存在：{manga_path}")
            else:
                logging.error(f"跳过下载：{id}")
        
        logging.info("所有任务完成")
        return True
    except Exception as e:
        logging.error(f"程序运行出错: {e}")
        return False

if __name__ == "__main__":
    # 示例使用
    manga_ids = ['61572','36267']  # 漫画ID列表
    success = process_manga(manga_ids, should_convert_pdf=True)
    if success:
        print("处理完成")
    else:
        print("处理失败")
