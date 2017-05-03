# -*- coding: utf-8 -*-

import urllib.request
import os
import re
import json
import sys

api = 'https://www.zhihu.com/api/v4/questions/%s/answers'

headers = {
    'Host': 'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '\
        '(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
}

def format_url(question_id, params):
    return api % question_id + '?' + params

def get_params(offset):
    return 'include=data%5B*%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edi'\
        't%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_cou'\
        'nt%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time'\
        '%2Cupdated_time%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_th'\
        'anked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.author.badge%5B%3F(t'\
        'ype%3Dbest_answerer)%5D.topics&limit=20&sort_by=default&offset=' + str(offset)

def get_request(url, headers):
    req = urllib.request.Request(url)

    for key, value in headers.items():
        req.add_header(key, value)

    return req


if __name__ == '__main__':

    question_id = input("Please input the question id：")

    if len(question_id) < 1:
        print('Invalid question id.')
        sys.exit(1)

    offset = 0
    is_end = False

    downloaded_imgs = []

    download_path = os.path.join(os.getcwd(), 'imgs', question_id)
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    print('Downloading...')

    while not is_end:
        with urllib.request.urlopen(get_request(format_url(question_id, get_params(offset)), headers)) as f:
            js = json.loads(f.read())

            is_end = js['paging']['is_end']
            datas = js['data']

            for data in datas:
                imgs = re.findall("<img[^>]+>", data['content'])

                for img in imgs:

                    try:
                        img_url = img.split("data-original=\"")[1].split("\"")[0]

                        try:
                            downloaded_imgs.index(img_url)
                        except Exception as e:
                            with urllib.request.urlopen(img_url) as i:
                                with open(os.path.join(download_path, img_url.split('/')[-1]), 'wb') as o:
                                    o.write(i.read())

                        downloaded_imgs.append(img_url)

                    except Exception as e:
                        pass
        offset+=1

    print('Done')