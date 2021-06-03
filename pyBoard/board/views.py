from django.shortcuts import render, redirect
from board.models import Board, Comment
from django.views.decorators.csrf import csrf_exempt
import os
from django.utils.http import urlquote
from django.http.response import HttpResponse, HttpResponseRedirect
from django.db.models import Q

UPLOAD_DIR='D:/upload/'

@csrf_exempt
def list(request):
    try:
        search_option=request.POST['search_option']
    except:
        search_option=""
    
    try:
        search=request.POST['search']
    except:
        search=""
    
    if search_option=='all':
        boardCount=Board.objects.filter(Q(writer__contains=search)|
                                        Q(title__contains=search)|
                                        Q(content__contains=search)).count()
        boardList=Board.objects.filter(Q(writer__contains=search)|
                                        Q(title__contains=search)|
                                        Q(content__contains=search)).order_by("-idx")                               
    elif search_option=='writer':    
        boardCount=Board.objects.filter(Q(writer__contains=search)).count()
        boardList=Board.objects.filter(Q(writer__contains=search)).order_by("-idx")
    elif search_option=='title':    
        boardCount=Board.objects.filter(Q(title__contains=search)).count()  
        boardList=Board.objects.filter(Q(title__contains=search)).order_by("-idx")  
    elif search_option=='content':    
        boardCount=Board.objects.filter(Q(content__contains=search)).count()
        boardList=Board.objects.filter(Q(content__contains=search)).order_by("-idx")
    else:
        boardCount=Board.objects.all.count()
        boardList=Board.objects.all.count()
                                    
    return render(request, "board/list.html", {"boardList":boardList,"boardCount":boardCount})

def write_form(request):
    return render(request, "board/write.html")

@csrf_exempt
def insert(request):
    fname=''
    fsize=0
    if 'file' in request.FILES:
        file=request.FILES['file']
        fname=file.name
        fsize=file.size
        fp=open('%s%s' %(UPLOAD_DIR,fname),'wb')
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()
    
    dto=Board(writer=request.POST['writer'],
              title=request.POST['title'],
              content=request.POST['content'],
              filename=fname,
              filesize=fsize)
    dto.save()
    return redirect("/list/")

def download(request):
    id=request.GET['idx']
    dto=Board.objects.get(idx=id)
    path=UPLOAD_DIR+dto.filename
    filename=urlquote(os.path.basename(path))
    with open(path,'rb') as file:
        response=HttpResponse(file.read(),
                              content_type='application/actet-stream')
        response['content-Disposition']="attachment;filename*=UTF-8''{0}".format(filename)
        dto.cnt_download_up()
        dto.save()
        return response
    
def detail(request):
    id=request.GET['idx']
    dto=Board.objects.get(idx=id)
    dto.hit_up()
    dto.save()
    commentList=Comment.objects.filter(board_idx=id).order_by("-idx")
    filesize="%0.2f" %(dto.filesize/1024)
    return render(request, "board/detail.html", {"dto":dto,"filesize":filesize,"commentList":commentList})

@csrf_exempt
def update(request):
    id=request.POST['idx']
    dto=Board.objects.get(idx=id)
    fname=dto.filename
    fsize=dto.filesize
    
    if 'file' in request.FILES:
        file=request.FILES['file']
        fname=file.name
        fp=open('%s%s' %(UPLOAD_DIR,fname),'wb')
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()
        fsize=os.path.getsize(UPLOAD_DIR+fname)
    dto_new=Board(idx=id,
                  writer=request.POST['writer'],
                  title=request.POST['title'],
                  content=request.POST['content'],
                  filename=fname,
                  filesize=fsize)
    dto_new.save()
    return redirect("/list/")
  
@csrf_exempt  
def delete(request):
    id=request.POST['idx']
    Board.objects.get(idx=id).delete()   
    return redirect("/list/")

@csrf_exempt
def reply_insert(request):
    id=request.POST['idx']
    print(id)
    dto=Comment(board_idx=id,
                writer=request.POST['writer'],
                content=request.POST['content'])
    dto.save()
    return HttpResponseRedirect('/detail?idx='+id)

def reply_delete(request):
    id=request.GET['idx']
    print(id)
    board_idx=request.GET['board_idx']
    Comment.objects.get(idx=id).delete()
    return HttpResponseRedirect('/detail?idx='+board_idx)