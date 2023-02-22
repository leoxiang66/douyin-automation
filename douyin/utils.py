import requests
from PIL import Image

def download_image(image_url:str, filename:str):

    # 发送GET请求并获取响应
    response = requests.get(image_url)

    # 检查响应状态码，确保请求成功
    if response.status_code == 200:

        # 以二进制写入模式打开文件
        with open(filename, 'wb') as f:
            # 写入响应内容
            f.write(response.content)
        print('图片下载完成！')
    else:
        print('请求失败！')


def resize_image(image_path):

    # 打开原始图片
    image = Image.open(image_path)

    # 将图片调整为720*1280大小
    resized_image = image.resize((720, 1280))

    # 保存调整后的图片
    resized_image.save(image_path)

if __name__ == '__main__':
    resize_image("C:\git\leoxiang66\douyin-automation\downloades\cover.jpg")