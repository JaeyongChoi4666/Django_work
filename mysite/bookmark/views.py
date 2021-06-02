from django.shortcuts import render
from django.views.generic.list import ListView
from bookmark.models import Bookmark
from django.views.generic.detail import DetailView

# Create your views here.
# class BookmarkLV(ListView):
#     model=Bookmark
#
# class BookmarkDV(DetailView):
#     model=Bookmark

def home(request):
    urlList=Bookmark.objects.order_by("title")
    urlCount=Bookmark.objects.all().count()
    return render(request, "bookmark/list.html", {"urlList":urlList,"urlCount":urlCount})

def detail(request):
    addr=request.GET['url']
    dto=Bookmark.objects.get(url=addr)
    return render(request, "bookmark/detail.html", {"dto":dto})