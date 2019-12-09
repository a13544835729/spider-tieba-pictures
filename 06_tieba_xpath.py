from lxml import etree
import requests
import random
import time
from urllib import parse
import os

class TiebaSpider():
    def __init__(self):
        self.url='https://tieba.baidu.com/f?'
        self.headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'}

    #1.获取主页的响应信息['','','']
    def parse_html(self,params,name):
        #创建文件夹
        img_dir = '/home/tarena/images/' + name
        vid_dir = '/home/tarena/video/' + name
        if not os.path.exists(img_dir) :
            os.makedirs(img_dir)
        if not os.path.exists(vid_dir) :
            os.makedirs(vid_dir)
        html=requests.get(url=self.url,headers=self.headers,params=params).text
        p=etree.HTML(html)
        href_list=p.xpath('//li[@class=" j_thread_list clearfix"]//div[@class="threadlist_title pull_left j_th_tit "]//a[@rel="noreferrer"]/@href')
        # print(href_list)
        #html=['','','']
        for href in href_list:
            #组成每个二级页面的url
            href_url='https://tieba.baidu.com'+href
            self.parse_second_page(href_url,name)

    #2.获取二级页面的响应信息,第二次请求,获取下载
    def parse_second_page(self,href_url,name):
        html=requests.get(url=href_url,headers=self.headers).text
        p=etree.HTML(html)
        images_list=p.xpath('//div[@class="d_post_content j_d_post_content "]/img[@class="BDE_Image"]/@src | //div[@class="video_src_wrapper"]/embed/@data-video')
        # vid_list=p.xpath('//div[@class="video_src_wrapper"]/embed/@data-video')
        # print(images_list)
        # print(vid_list)
        #图片
        for img in images_list:
            self.pic_download(img,name)
        #视频
        # for vid in vid_list:
        #     self.vid_download(vid,name)


    #3.下载文件
    def pic_download(self,img_url,name):
        dir='/home/tarena/images/'+name
        html = requests.get(url=img_url, headers=self.headers).content
        imgname=dir+'/'+img_url[-20:]
        print(imgname)
        with open(imgname,'wb') as f:
            f.write(html)
        print('图片下载完成')


    #4.视频下载
    def vid_download(self,vid_url,name):
        dir = '/home/tarena/video/' + name
        html = requests.get(url=vid_url, headers=self.headers).content
        vidname = dir+'/'+vid_url[-20:]
        with open(vidname, 'wb') as f:
            f.write(html)
        print('视频下载完成')

    #4.入口函数
    def run(self):
        name=input('请输入贴吧名:')
        begin=int(input('请输入起始页'))
        end=int(input('请输入最终页面'))
        n=1
        for page in range(begin,end+1):
            pn=(page-1)*50
            params={
                'kw':name,
                'pn':pn
            }
            self.parse_html(params,name)
            print('抓取第{}页'.format(n))
            n+=1
            time.sleep(random.randint(1,2))


if __name__ == '__main__':
    spider=TiebaSpider()
    spider.run()
