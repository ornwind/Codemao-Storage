import requests
import time
import hashlib
import json
from requests_toolbelt import MultipartEncoder
import os
def login( name, password):
    data = {'pid': '65edCTyg',
            'identity': name,
            'password': password
            }
    w = requests.post('https://api.codemao.cn/tiger/v3/web/accounts/login', json=data)
    data = json.loads(w.text)
    # print(data)
    # print(w.headers)
    try:
        name = data["user_info"]["nickname"]
        id = data["user_info"]["id"]
        cookie = "__ca_uid_key__=5e47f24e-8f21-4921-aecb-ff08e70b1b82; " + w.headers["Set-Cookie"].split(";")[
            0] + "; authorization=" + data["auth"]["token"]
    except:
        print("无法登录，请检查账号密码。")
        exit(-1)
    return cookie
def md5(text):
    n=hashlib.md5(str(text).encode("UTF-8")).hexdigest()
    return n
def http_get(url,header,paths):
    w = requests.get(url,headers=header)
    print(w.text)
    data = json.loads(w.text)
    lst=[]
    for i in paths:
        lst.append(eval("data"+i))
    return lst
def http_post(url,header,data):
    w=requests.post(url,data=data,headers=header)
    print(w.text)
def upload(path):
    cookie=login("edu1197107077"	,143382)
    print(cookie)
    filename, ext = os.path.splitext(os.path.basename(path))

    time_md5=md5(time.time())
    name="mw/"+time_md5+ext
    url=f"https://open-service.codemao.cn/cdn/qi-niu/tokens/uploading?projectName=community_frontend&filePaths={name}&filePath={name}&tokensCount=1&fileSign=p1&cdnName=qiniu"

    header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36","cookie":cookie,"Content-Type":"application/json;charset=utf-8"}

    bucket,pic_host,pic,token,upload_url=http_get(url,header,["[\"bucket\"]","[\"bucket_url\"]","[\"tokens\"][0][\"file_path\"]","[\"tokens\"][0][\"token\"]","[\"upload_url\"]"])
    ak=token.split(":")[0]
    url=f"https://api.qiniu.com/v2/query?ak={ak}&bucket={bucket}"
    http_get(url,header,[])

    field={"file": (name,open(path,"rb"),"image/png"),
            "token":token,
            "key":pic,
            "fname":name+ext}
    print(field)
    data=MultipartEncoder(fields=field,boundary = '----WebKitFormBoundary'+time_md5)
    header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36","Content-Type":data.content_type,"Origin":"https://shequ.codemao.cn","Referer":"https://shequ.codemao.cn/"}

    http_post(upload_url,header,data)
    return pic_host+pic
if __name__=="__main__":
    import win32ui

    dlg = win32ui.CreateFileDialog(1)
    dlg.SetOFNInitialDir(os.path.join(os.environ['USERPROFILE'], 'Desktop'))
    dlg.DoModal()
    path = dlg.GetPathName()
    print("文件路径:",path)
    print("\n文件url:",upload(path))
    time.sleep(100)