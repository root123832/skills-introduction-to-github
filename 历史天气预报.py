'''1月1号到10号的数据在静态网页有，后面31号的数据在动态链接地址有，
                                  城市      年份月份
链接规律：https://lishi.tianqi.com/changsha/202312.html
'''
'''本网站存在一个加密参数， 'crypte': 'P1g7GMD8wgNZEcSKn9k18kPa3p/4w0Aur340AXseOxg=',每次刷新参数值都不一样
参数逆向分析：
一、定位加密位置方法：1.xhr断点跟栈 2.关键字搜索 3.hook 4.根据启动器跟栈 ，采用第四种方法，启动器里面在匿名的位置，打开js代码
找到crypte参数，双击他，查找他是从哪来的，看到这里有一个定义var crypte = encrypt();在下面打断点
二、断点调试分析
点击加载让他断住，看到返回的值，既然这里就是他生成的地方，他是根据某个方法生成的，鼠标悬停在方法上，点进去，下滑看到返回值return encryptData['toString']();
把相关的代码复制到js代码里面，保存为js文件，_0x425f('0x12'),像这种就是混淆，这种要替换，把他复制到控制台去运行就可以看到值，
然后把他替换，然后在做其他的处理，如果运行能生成值没有报错，就成功了
总结:加密参数/内容都是通过js代码生成的
通过开发者工具分析加密/解密js代码位置，调用了什么方法，传入了什么参数，返回了什么值
'''
'''功能：能够实现查看几年几月的天气预报
说明：(成功)，要查看哪个城市的，就把changsha替换成城市的拼音，年份月份修改下面的for循环
'''
import time,random
import requests
import parsel
import csv
import execjs # 执行js代码的库，可以执行js代码，导入调用js代码模块
# 创建一个csv文件
f = open('一个月天气.csv','w',encoding='utf-8',newline='')
csv_writer = csv.DictWriter(f, fieldnames=['日期','星期', '最高气温', '最低气温', '天气', '风向'])
csv_writer.writeheader()
cookies = {
    'UserId': '17446965320957653',
    'Hm_lvt_7c50c7060f1f743bccf8c150a646e90a': '1744696533',
    'HMACCOUNT': '721B937D4ED7E719',
    'Hm_lpvt_7c50c7060f1f743bccf8c150a646e90a': '1744704674',
}
headers = {
    'referer': 'https://lishi.tianqi.com/zhuozhou/202101.html',
    # 'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"',
    # 'sec-fetch-dest': 'document',
    # 'sec-fetch-mode': 'navigate',
    # 'sec-fetch-site': 'same-origin',
    # 'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'cookie': 'UserId=17446965320957653; Hm_lvt_7c50c7060f1f743bccf8c150a646e90a=1744696533; HMACCOUNT=721B937D4ED7E719; Hm_lpvt_7c50c7060f1f743bccf8c150a646e90a=1744704674',
}
years = range(2021, 2022)  # 您可以根据需要修改年份范围
months = range(1,13)  # 1 到 12 月
# for循环遍历年份
for year in years:
    # for循环遍历月份
    for month in months:
        # 是先分别将年份和月份转换为字符串，并通过 zfill(2) 方法处理月份使其为两位数，然后再拼接得到最终的字符串
        month_str = str(year) + str(month).zfill(2)
        # print(month_str)
        print(f'------正在爬取{year}年{month}月的天气数据-------')
        # 1月1号到10号的数据在静态网页
        url = f'https://lishi.tianqi.com/zhuozhou/{month_str}.html'
        response = requests.get(url,headers=headers,cookies=cookies)
        # time.sleep(random.randint(1, 3))
        selector = parsel.Selector(response.text)
        # 提取所有li标签
        lis = selector.css('.tian_three .thrui li')
        for li in lis:
            # 提取日期
            date_info = li.css('.th200::text').get().split(' ')
            data = date_info[0]
            data_1 = date_info[1]
            # 提取相关信息列表
            info = li.css('.th140::text').getall()
            # # 提取最高气温
            max_temperature = info[0].replace('℃', '')
            # 提取最低气温
            min_temperature = info[1].replace('℃', '')
            # 天气
            weather = info[2]
            # 风向
            wind_direction = info[3]
            # 保存字典
            dit = {
                '日期': data,
                '星期': data_1,
                '最高气温': max_temperature,
                '最低气温': min_temperature,
                '天气': weather,
                '风向': wind_direction,
            }
            csv_writer.writerow(dit)
            print(dit)
        '''获取加密参数 通过python代码调用js代码'''
        city = "zhuozhou"
        # crypte = execjs.compile(open('天气.js', encoding='utf-8').read()).call('encrypt', city, month_str)
        crypte = execjs.compile(open('天气.js', encoding='utf-8').read()).call('encrypt', city, month_str)
        # print('加密参数：',crypte)
        # exit()
        # 后面11号到31号的数据在动态链接地址
        link = f'https://lishi.tianqi.com/monthdata/{city}/{month_str}'
        data = {
            'crypte': crypte,
        }
        try:
            json_data = requests.post(link,data=data,headers=headers,cookies=cookies).json()
            # time.sleep(random.randint(1, 3))
            # for循环列表
            for i in json_data:
                dit = {
                    '日期': i['date_str'],
                    '星期': i['week'],
                    '最高气温': i['htemp'],
                    '最低气温': i['ltemp'],
                    '天气': i['weather'],
                    '风向': i['WD'] + i['WS'],
                }
                csv_writer.writerow(dit)
                print(dit)
        except requests.exceptions.JSONDecodeError:
            print(f"无法解析 {year} 年 {month} 月的响应内容为 JSON 格式。")