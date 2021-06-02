from django.shortcuts import render
from board.models import Board

# Create your views here.
def list(request):
    boardCount=Board.objects.count()
    boardList=Board.objects.order_by("-idx")    #내림차순정리
    return render(request, "board/list.html", {"boardList":boardList,"boardCount":boardCount})
