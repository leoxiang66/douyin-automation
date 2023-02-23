import selenium
from selenium import webdriver
from pathlib import Path
import time
from pytube import YouTube, Playlist
from .utils import download_image, resize_image
import random

class Automator:
    def __init__(self):
        options = webdriver.ChromeOptions()
        # options.add_experimental_option("debuggerAddress", "127.0.0.1:5003")
        self.driver = webdriver.Chrome(options=options)
        self.download_dir = Path('downloades')
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.clear_cache()



    def work(self):
        self.login()
        urls =  self.top5recent()
        for i in urls:
            title = self.download_yt(i)
            self.publish_video(self.download_dir.joinpath('download.mp4').absolute().__str__(),title)

    def top5recent(self):
        yasuo = "https://www.youtube.com/playlist?list=PL-TM5XNBRKzQ4HYxwCTNCh4dqjblLcVn3"
        playlist = Playlist(yasuo)

        yone = 'https://www.youtube.com/playlist?list=PL-TM5XNBRKzT2MjKkUCrGa0qnQMYFOGpf'
        playlist2 = Playlist(yone)
        ret = list(playlist2.video_urls[:5] + playlist.video_urls[:5])
        random.shuffle(ret)
        return ret

    @classmethod
    def rmrf(cls,path):
        path = Path(path)
        if path.exists():
            if path.is_file():
                path.unlink()
            else:
                for child in path.glob('*'):
                    cls.rmrf(child)
                # path.rmdir()

    def clear_cache(self):
        self.rmrf(self.download_dir.__str__())





    def download_yt(self,yt_url: str):
        self.clear_cache()
        yt = YouTube(yt_url)
        download_image(yt.thumbnail_url,self.download_dir.joinpath('cover.jpg').__str__())
        resize_image(self.download_dir.joinpath('cover.jpg').__str__())

        while True:
            try:
                yt.streams.filter(progressive=True, file_extension='mp4').order_by(
                    'resolution').desc().first().download(
                    output_path=self.download_dir,
                    filename=f'download.mp4'
                )
                break
            except Exception as e:
                print(e)
        return yt.title


    def login(self):
        # 进入创作者页面，并上传视频
        self.driver.get("https://creator.douyin.com/")
        try:
            time.sleep(2)
            self.driver.find_element('xpath', '//*[text()="登录"]').click()
            time.sleep(2)
            self.driver.find_element('xpath', '//*[text()="确认"]').click()
            time.sleep(25)
            self.driver.find_element('xpath', '//*[text()="开始体验"]').click()
            time.sleep(2)
            self.driver.find_element('xpath', '//*[text()="下一步"]').click()
            time.sleep(2)
            self.driver.find_element('xpath', '//*[text()="完成"]').click()
        except Exception as e:
            print(e)
            self.login()

    def publish_video(self,filepath:str, title:str):
        title = '''【完整录像】''' + title
        time.sleep(2)
        self.driver.find_element('xpath', '//*[text()="发布作品"]').click()
        time.sleep(2)
        self.driver.find_element('xpath', '//*[text()="发布视频"]').click()
        time.sleep(2)
        self.driver.find_element('xpath', '//input[@type="file"]').send_keys(filepath)

        # 等待视频上传完成
        while True:
            time.sleep(3)
            try:
                self.driver.find_element('xpath', '//*[text()="重新上传"]')
                break
            except Exception as e:
                print("视频还在上传中···")

        print("视频已上传完成！")

        # 设置title
        self.driver.find_element('xpath', '//*[@class="editor-kit-editor-container"]').click()
        self.driver.find_element('xpath',
                                 '//*[@class="zone-container editor-kit-container editor editor-comp-publish notranslate chrome window chrome88"]').send_keys(
            f"{title}")

        # 添加封面
        self.driver.find_element('xpath','//*[text()="编辑封面"]').click()
        time.sleep(2)
        self.driver.find_element('xpath','//div[text()="上传封面"]').click()
        time.sleep(2)
        self.driver.find_element('xpath','//input[@type="file"]').send_keys(self.download_dir.joinpath('cover.jpg').absolute().__str__())
        time.sleep(3)
        self.driver.find_element('xpath','//*[text()="裁剪封面"]/..//*[text()="确定"]').click()
        time.sleep(3)
        self.driver.find_element('xpath','//*[text()="设置封面"]/..//*[contains(@class,"upload")]//*[text()="确定"]').click()
        time.sleep(10)



        # self.driver.find_element('xpath', '//*[@class="radio--4Gpx6"][contains(@style,"background-color: rgb(248, 249, 249))"]').click()

        # # 点击发布
        def publish_():
            try:
                fabu = self.driver.find_element('xpath', '//*[text()="发布"]')
                self.driver.execute_script("arguments[0].click();", fabu)
            except:
                publish_()

        publish_()



