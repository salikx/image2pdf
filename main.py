import os
import time
import yaml
from PIL import Image
import jmcomic

def sorted_numeric_filenames(file_list):
    """对文件名按数字部分排序"""
    def extract_number(s):
        name, _ = os.path.splitext(s)
        return int(''.join(filter(str.isdigit, name)) or 0)
    return sorted(file_list, key=extract_number)

def convert_images_to_pdf(input_folder, output_path, pdf_name):
    start_time = time.time()
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
    output_path = os.path.normpath(output_path)
    os.makedirs(output_path, exist_ok=True)
    pdf_full_path = os.path.join(output_path, f"{os.path.splitext(pdf_name)[0]}.pdf")

    image_iterator = []

    # 获取子目录并排序
    try:
        subdirs = sorted(
            [d for d in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, d))],
            key=lambda x: int(x) if x.isdigit() else float('inf')
        )
    except Exception as e:
        print(f"错误：无法读取目录 {input_folder}，原因：{e}")
        return

    for subdir in subdirs:
        subdir_path = os.path.join(input_folder, subdir)
        try:
            files = [f for f in os.listdir(subdir_path)
                     if os.path.isfile(os.path.join(subdir_path, f)) and os.path.splitext(f)[1].lower() in allowed_extensions]
            files = sorted_numeric_filenames(files)
            for f in files:
                image_iterator.append(os.path.join(subdir_path, f))
        except Exception as e:
            print(f"警告：读取子目录失败 {subdir_path}，原因：{e}")

    if not image_iterator:
        print("错误：未找到任何图片文件")
        return

    try:
        def open_image(path):
            img = Image.open(path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            return img

        # 用生成器延迟加载，首张图用作 PDF 的 base 图
        image_iter = (open_image(p) for p in image_iterator)
        first_image = next(image_iter, None)

        if not first_image:
            print("错误：没有有效图片可生成PDF")
            return

        print(f"开始生成PDF：{pdf_full_path}")
        first_image.save(
            pdf_full_path,
            "PDF",
            save_all=True,
            append_images=[img for img in image_iter],
            optimize=True
        )
        print(f"✅ 成功生成PDF：{pdf_full_path}")

    except Exception as e:
        print(f"❌ 生成PDF失败：{e}")

    print(f"处理完成，耗时 {time.time() - start_time:.2f} 秒")

def main():
    config_path = "D:/18comic_down/code/config.yml"
    try:
        option = jmcomic.JmOption.from_file(config_path)
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            base_dir = config["dir_rule"]["base_dir"]
    except Exception as e:
        print(f"加载配置失败：{e}")
        return

    if not os.path.exists(base_dir):
        print(f"错误：根目录不存在 {base_dir}")
        return

    for entry in os.scandir(base_dir):
        if entry.is_dir():
            pdf_name = f"{entry.name}.pdf"
            pdf_path = os.path.join(base_dir, pdf_name)
            if os.path.exists(pdf_path):
                print(f"跳过已有PDF：{pdf_name}")
                continue

            print(f"\n📄 转换中：{entry.name}")
            convert_images_to_pdf(
                input_folder=entry.path,
                output_path=base_dir,
                pdf_name=entry.name
            )

if __name__ == "__main__":
    main()
