from django.shortcuts import render, redirect
from board.models import Board, Comment
from django.views.decorators.csrf import csrf_exempt
import os
from django.utils.http import urlquote
from django.http.response import HttpResponse, HttpResponseRedirect,\
    JsonResponse
from django.db.models import Q
import math
from django.core.serializers.json import DjangoJSONEncoder

UPLOAD_DIR='D:/upload/'

@csrf_exempt
def list(request):
    try:
        search_option=request.POST['search_option']
        search=request.POST['search']
        start=int(request.GET['start'])
    except:
        search_option=""
        search=""
        start=0
    
    page_size=10
    block_size=10
    end=start+page_size
            
    if search_option=='all':
        boardCount=Board.objects.filter(Q(writer__contains=search)|
                                        Q(title__contains=search)|
                                        Q(content__contains=search)).count()
        boardList=Board.objects.filter(Q(writer__contains=search)|
                                        Q(title__contains=search)|
                                        Q(content__contains=search)).order_by("-idx")[start:end]                               
    elif search_option=='writer':    
        boardCount=Board.objects.filter(Q(writer__contains=search)).count()
        boardList=Board.objects.filter(Q(writer__contains=search)).order_by("-idx")[start:end]
    elif search_option=='title':    
        boardCount=Board.objects.filter(Q(title__contains=search)).count()  
        boardList=Board.objects.filter(Q(title__contains=search)).order_by("-idx")[start:end]
    elif search_option=='content':    
        boardCount=Board.objects.filter(Q(content__contains=search)).count()
        boardList=Board.objects.filter(Q(content__contains=search)).order_by("-idx")[start:end]
    else:
        boardCount=Board.objects.count()
        boardList=Board.objects.order_by("-idx")[start:end]
        
    total_page=math.ceil(boardCount/page_size)
    current_page=math.ceil((start+1)/page_size)
    start_page=math.floor((current_page-1)/block_size)*block_size+1
    end_page=start_page+block_size+1
    
    if end_page < total_page:
        end_page=total_page
        next_list=end_page*page_size
    else:
        next_list=0
    
    if start_page >= block_size:
        prev_list=(start_page-2)*page_size
    else:
        prev_list=0
    
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

def json_test(request):
    boardList=Board.objects.all().order_by("-idx")
    return JsonResponse({'name':'aaa','age':30})