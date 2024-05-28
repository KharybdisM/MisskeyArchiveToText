import json
import os
import requests
import argparse
from datetime import datetime

def download_file(url, directory='misskey-archive/media'):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        os.makedirs(directory, exist_ok=True)
        with open(os.path.join(directory, local_filename), 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return local_filename

def split_json_by_year(filename, picdl=None):
    with open(filename, 'r', encoding='utf-8') as f:
      data = json.load(f)
    
    file_cache = {}
    for item in data:
        entry_time = datetime.strptime(item['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
        year = datetime.strptime(item['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ").year

        entry = f"发布时间：{entry_time}\n"
        entry += f"{item['text']}\n"
        if item['files']:
            if 'files' in item:
                files_info = []
                for file in item['files']:
                    if 'url' in file:
                        file_url = file['url']
                        if picdl is None:
                            local_filename = download_file(file_url)
                            local_url = os.path.join('media', local_filename)
                            files_info.append(f"![{local_filename}]({local_url})")
                        else:
                            files_info.append(f"![Picture]({file_url})")
                entry += f"媒体文件：\n{'\n'.join(files_info)}\n"
        entry += '\n-----\n\n'
        
        if year not in file_cache:
            file_cache[year] = entry
        else:
            file_cache[year] += entry
    
    if not os.path.exists('misskey-archive'):
        os.makedirs('misskey-archive')

    for year, entries in file_cache.items():
        with open(os.path.join('misskey-archive', f"{year}.md"), 'w', encoding='utf-8') as f:
            f.write(entries)

# 创建一个解析器
parser = argparse.ArgumentParser(description='从给定的json文件中处理数据')
# 添加一个名为jsonfile的参数，类型为str，引用时使用--jsonfile，在help中显示的说明为'输入的json文件'
parser.add_argument('--j', type=str, required=True, help='输入的json文件')
parser.add_argument('--p', type=str, help='是否下载图片到本地，n为不下载，留空为下载')
# 解析参数
args = parser.parse_args()
filename = args.j
picdl = args.p

# Call the function
split_json_by_year(filename,picdl)
