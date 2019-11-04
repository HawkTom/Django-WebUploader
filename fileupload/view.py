from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import time

def index(request):
    return render(request, "index.html")

@csrf_exempt 
def upload_index(request):
    if request.method == 'POST':
        task = request.POST.get('task_id')  # 获取文件的唯一标识符
        chunk = request.POST.get('chunk', 0)  # 获取该分片在所有分片中的序号
        filename = '%s%s' % (task, chunk)  # 构造该分片的唯一标识符

        upload_file = request.FILES['file']
        with open('upload/%s' % filename, 'wb') as f:
            f.write(upload_file.read())
        print("upload ...")
    return HttpResponse('ok')

@csrf_exempt
def upload_complete(request):
    target_filename = request.GET.get('filename')  # 获取上传文件的文件名
    task = request.GET.get('task_id')  # 获取文件的唯一标识符
    chunk = 0  # 分片序号
    print(target_filename, task)
    with open('upload/%s' % target_filename, 'wb') as target_file:  # 创建新文件
        while True:
            try:
                filename = 'upload/%s%d' % (task, chunk)
                source_file = open(filename, 'rb')  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
            except IOError as msg:
                break

            chunk += 1
            os.remove(filename)  # 删除该分片，节约空间
    time.sleep(5)
    print("back back ...")
    return render(request, "index.html")




def save_agent(f, username):
    # whether the existing is in tesing or validation 
    path_valid = "validateAgent/" + username + "/"
    path_test = "testingAgent/" + username + "/"
    if os.path.exists(path_valid) or os.path.exists(path_test):
        return False
    path = 'uploadAgent/' + username + '.zip'
    print("start.....")
    with open(path, 'wb+') as destination:
        print("open safely")
        for chunk in f.chunks():
            destination.write(chunk)
    print("submit finished!")
    return True

