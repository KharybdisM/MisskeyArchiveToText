import json
import os
import requests
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

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

        cw_content = item.get('cw', '')
        text_content = item.get('text', '')
        
        entry = f"发布时间：{entry_time}\n"
        if cw_content:
            entry += f"{cw_content}\n"
        entry += f"{text_content}\n"
        
        if 'files' in item and item['files']:
            files_info = []
            for file in item['files']:
                if 'url' in file:
                    file_url = file['url']
                    if picdl == 'y':
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
    
    messagebox.showinfo("处理完成", "数据处理完成！生成的Markdown文件保存在 misskey-archive 目录下，\n下载的媒体文件保存在该目录的 media 文件夹中。")

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    entry_file.delete(0, tk.END)
    entry_file.insert(0, filename)

def process_data():
    filename = entry_file.get()
    picdl = check_picdl.get()
    split_json_by_year(filename, picdl)


# GUI
root = tk.Tk()
root.title("JSON→MD")

label_file = tk.Label(root, text="选择从Misskey下载的JSON文件:")
label_file.pack(pady=10)

entry_file = tk.Entry(root, width=50)
entry_file.pack(pady=5)

btn_browse = tk.Button(root, text="浏览...", command=browse_file)
btn_browse.pack(pady=5)

check_picdl = tk.StringVar()
check_picdl.set("y")

label_picdl = tk.Label(root, text="下载图片到本地:")
label_picdl.pack(pady=5)

radio_yes = tk.Radiobutton(root, text="是，仅下载图片", variable=check_picdl, value="y")
radio_yes.pack()

radio_no = tk.Radiobutton(root, text="否，仅下载文本", variable=check_picdl, value="n")
radio_no.pack()

btn_process = tk.Button(root, text="Go!", command=process_data)
btn_process.pack(pady=10)

root.mainloop()
