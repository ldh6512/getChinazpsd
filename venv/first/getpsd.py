import urllib.request
import os, re,time
import rarfile

def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36')
    response = urllib.request.urlopen(url)
    html = response.read()
    return html

def get_page(url):
    html = url_open(url).decode('utf-8')
    print(html)
    '''
    a = html.find('current-comment-page')+23
    b = html.find(']', a)
    '''
    return 0

def find_imgs(url):
    html = url_open(url).decode('utf-8')
    img_addrs = []
    img_addrs= re.findall(r'[0-9]{12}', html)

    return img_addrs

def unrardelfile( file_name, file_path ):

    file = rarfile.RarFile(file_name)  #这里写入的是需要解压的文件，别忘了加路径
    file.extractall(file_path)  #这里写入的是你想要解压到的文件夹
    os.remove( file_path + "说明.htm")
    os.remove(file_name)

def save_imgs(folder, page_url):
    html = url_open(page_url).decode('utf-8')
    a = html.find("<title>") + 7
    b = html.find("_", a)
    filename = html[a:b]

    psd_addrs = []
    psd_addrs = re.findall(r'http://downsc.chinaz.net/Files/DownLoad/psd1/[0-9]{6}/psd[0-9]{5}.rar', html)
    # ------ 这里最好使用异常处理及多线程编程方式 ------
    try:
        filepath =  'G:\\MyPython\\getChinazpsd\\venv\\first\psd\\' + filename + '.rar'
        urllib.request.urlretrieve(psd_addrs[0], filepath)
    except Exception as e:
        if hasattr(e, 'code'):
            print(e.code)
        elif hasattr(e, 'reason'):
            print(e.reason)
    unrardelfile( filepath, filepath[:-4]+'\\')

def download_mm(folder):
    #os.mkdir(folder)
    os.chdir(folder)

    url = "http://sc.chinaz.com/psd/free.html"
    url_free = "http://sc.chinaz.com/psd/"
    #page_num = int(get_page(url))
    page_num = 1076   #总共的页数
    for i in range(page_num):
        if 8 > i:
            seqnum = 'free'
            continue
        else:
            seqnum = 'free_'+ str(i+1)
        page_url = url_free + seqnum + '.html'
        print(page_url)
        img_addrs = find_imgs(page_url)
        time.sleep(1)

        for j in img_addrs:
            page_url = url_free + j + '.htm' + '#down'
            save_imgs(folder, page_url)
            time.sleep(1)

if __name__ == '__main__':
    download_mm('./psd/')