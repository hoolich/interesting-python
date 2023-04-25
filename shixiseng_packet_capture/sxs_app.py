#!/usr/bin/python
# -*- coding:utf-8 -*-
import pandas as pd
import requests


def sxs_crawl(pages=30, kw='数据挖掘', c='全国'):
    list_urls = ["https://iosapi.shixiseng.com/app/interns/search?c={}&d=&ft=&i=&k={}"
                "&m=&page={}&s=-0&st=&t=zj&x=&z=".format(c, kw, page) for page in range(pages)]#查找网站中前30页里全国的数据挖掘岗位的链接数组
    job_list_data = []#新建一个空数组
    for url in list_urls:#在刚刚的链接数组中查找
        response = requests.get(url)#返回每一个请求的返回
        if response.json()['msg']:#如果返回的msg不为空
            job_list_data.extend(response.json()['msg'])#那么在刚刚新建的空数组里添加这条信息，这里信息本身是数组格式，而extend添加的是数组中的元素
        else:
            break#跳出循环
    job_list = pd.DataFrame(job_list_data)#用pandas读取数组，
    job_list.to_csv('/Users/apple/Desktop/job_list.csv', index=False)#然后放入到对应的csv里头，这里的csv需要改成我们自己的csv地址

    # 职位详情ID爬取
    uuids = list(job_list['uuid'])#拿到csv中uuid这个字段的信息，并变成数组
    job_detailed_url = ['https://iosapi.shixiseng.com/app/intern/info?uuid={}'.format(uuid) for uuid in uuids]#将所有对应岗位的链接数组放入到job_detailed_url数组中

    job_detailed_data = []#再新建一个工作信息数组
    for url in job_detailed_url:#我们在job_detailed_url数组中循环查找
        response = requests.get(url)#继续请求每一个返回
        job_detailed_data.append(response.json()['msg'])#添加每一个元素，append添加的是参数，参数就是元素，就算参数是数组，也会添加成数组中的数组
    job_detailed = pd.DataFrame(job_detailed_data)#继续写入到pandas
    job_detailed.to_csv('/Users/apple/Desktop/job_detailed.csv', index=False)#然后写到对应的csv里头去，这里的csv需要改成我们自己的csv地址

    # 公司信息爬取
    cuuids = list(job_detailed['cuuid'])#跟上面的步骤一样，上面爬的是职位详情，现在爬的是公司信息
    com_detailed_url = ['https://iosapi.shixiseng.com/app/company/info?uuid={}'.format(cuuid) for cuuid in cuuids]#依然是设置url数组
    com_detailed_data = []#新建空数组
    for url in com_detailed_url:#在url数组中查找
        response = requests.get(url)#得到我们想要的请求返回
        com_detailed_data.append(response.json()['msg'])#依然是将对应的信息添加到刚刚的空数组中去
    com_detailed = pd.DataFrame(com_detailed_data)#写到pandas中去
    com_detailed.to_csv('/Users/apple/Desktop/com_detailed.csv', index=False)#写入到对应的csv里头去，这里的csv需要改成我们自己的csv地址

    print('Successfully crawled {} jobs.'.format(job_list.shape[0]))#打印我们的岗位个数，shape[0]大概用的场景在x=np.array([[1,2,3],[4,5,6]])的这种情况下
    #我们如果想要查shape的话，那就是（2，3）代表的意思是有两行3列
    #如果查shape[0],那查的就是总共有两行
    #同理查shape[1],查的就是总共有3列


if __name__ == '__main__':
    sxs_crawl(pages=30, kw='数据挖掘', c='全国')
