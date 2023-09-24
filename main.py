import jmcomic, os, time, yaml
from PIL import Image
from pathlib import Path
from pyinstrument import Profiler


def all2PDF(input_folder, pdfpath, pdfname):
    start_time = time.time()
    paht = input_folder
    zimulu = []  # 子目录（里面为image）
    image = []  # 子目录图集
    sources = []  # pdf格式的图

    with os.scandir(paht) as entries:
        for entry in entries:
            if entry.is_dir():
                zimulu.append(int(entry.name))
    # 对数字进行排序
    zimulu.sort()

    for i in zimulu:
        with os.scandir(paht + "/" + str(i)) as entries:
            for entry in entries:
                if entry.is_dir():
                    print("这一级不应该有自录")
                if entry.is_file():
                    image.append(paht + "/" + str(i) + "/" + entry.name)

    if "jpg" in image[0]:
        output = Image.open(image[0])
        image.pop(0)

    for file in image:
        if "jpg" in file:
            img_file = Image.open(file)
            if img_file.mode == "RGB":
                img_file = img_file.convert("RGB")
            sources.append(img_file)

    pdf_file_path = pdfpath + "/" + pdfname
    if pdf_file_path.endswith(".pdf") == False:
        pdf_file_path = pdf_file_path + ".pdf"
    output.save(pdf_file_path, "pdf", save_all=True, append_images=sources)
    end_time = time.time()
    run_time = end_time - start_time
    print("运行时间：%3.2f 秒" % run_time)


if __name__ == "__main__":
    # 自定义设置：
    config = "D:/18comic_down/code/config.yml"
    loadConfig = jmcomic.JmOption.from_file(config)
    # manhua = ['146417']
    # for id in manhua:
    #     jmcomic.download_album(id,loadConfig)
    profiler = Profiler()
    profiler.start()

    with open(config, "r", encoding="utf8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        path = data["dir_rule"]["base_dir"]

    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_dir():
                if os.path.exists(os.path.join(path +'/' +entry.name + ".pdf")):
                    print("文件：《%s》 已存在，跳过" % entry.name)
                    continue
                else:
                    print("开始转换：%s " % entry.name)
                    all2PDF(path + "/" + entry.name, path, entry.name)
    profiler.stop()
