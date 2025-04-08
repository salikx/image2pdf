import os
import time
import yaml
from PIL import Image
import jmcomic

def convert_images_to_pdf(input_folder, output_path, pdf_name):
    """
    将指定文件夹内的所有图片按顺序合并为PDF文件
    :param input_folder: 输入文件夹路径，包含按数字排序的子文件夹
    :param output_path: PDF输出目录
    :param pdf_name: 生成的PDF文件名（无需扩展名）
    """
    start_time = time.time()
    image_paths = []

    # 收集所有子文件夹并按数字排序
    subdirs = []
    try:
        with os.scandir(input_folder) as entries:
            for entry in entries:
                if entry.is_dir():
                    try:
                        subdirs.append(int(entry.name))
                    except ValueError:
                        print(f"警告：跳过非数字目录 '{entry.name}'")
    except FileNotFoundError:
        print(f"错误：输入目录不存在 '{input_folder}'")
        return

    subdirs.sort()

    # 收集所有图片路径
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
    for subdir in subdirs:
        subdir_path = os.path.join(input_folder, str(subdir))
        try:
            with os.scandir(subdir_path) as entries:
                files = []
                for entry in entries:
                    if entry.is_file():
                        ext = os.path.splitext(entry.name)[1].lower()
                        if ext in allowed_extensions:
                            files.append(entry.name)
                # 按文件名排序（简单数字排序）
                files.sort(key=lambda x: os.path.splitext(x)[0])
                for filename in files:
                    image_paths.append(os.path.join(subdir_path, filename))
        except FileNotFoundError:
            print(f"警告：子目录不存在 '{subdir_path}'，已跳过")
            continue

    if not image_paths:
        print("错误：未找到任何图片文件")
        return

    # 处理图片并生成PDF
    try:
        images = []
        for path in image_paths:
            try:
                img = Image.open(path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                images.append(img)
            except Exception as e:
                print(f"警告：无法处理文件 '{path}'，已跳过。错误信息：{str(e)}")
                continue

        if not images:
            print("错误：没有有效图片可生成PDF")
            return

        # 确保输出文件名正确
        pdf_name = f"{os.path.splitext(pdf_name)[0]}.pdf"
        output_path = os.path.normpath(output_path)
        os.makedirs(output_path, exist_ok=True)
        pdf_full_path = os.path.join(output_path, pdf_name)

        # 保存PDF
        images[0].save(
            pdf_full_path,
            "PDF", 
            save_all=True, 
            append_images=images[1:],
            optimize=True
        )
        print(f"成功生成PDF：'{pdf_full_path}'")

    except Exception as e:
        print(f"生成PDF时发生错误：{str(e)}")
    finally:
        # 关闭所有图片对象
        for img in images:
            img.close()

    print(f"处理完成，耗时 {time.time() - start_time:.2f} 秒")

def main():
    # 加载配置
    config_path = "D:/18comic_down/code/config.yml"
    try:
        option = jmcomic.JmOption.from_file(config_path)
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            base_dir = config["dir_rule"]["base_dir"]
    except Exception as e:
        print(f"加载配置失败：{str(e)}")
        return

    # 遍历根目录处理未转换的文件夹
    try:
        with os.scandir(base_dir) as entries:
            for entry in entries:
                if entry.is_dir():
                    pdf_name = f"{entry.name}.pdf"
                    pdf_path = os.path.join(base_dir, pdf_name)
                    
                    if os.path.exists(pdf_path):
                        print(f"PDF已存在，跳过：'{pdf_name}'")
                        continue
                    
                    print(f"\n开始转换：'{entry.name}'")
                    convert_images_to_pdf(
                        input_folder=entry.path,
                        output_path=base_dir,
                        pdf_name=entry.name
                    )
    except FileNotFoundError:
        print(f"根目录不存在：'{base_dir}'")

if __name__ == "__main__":
    main()
