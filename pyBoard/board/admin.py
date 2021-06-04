from django.contrib import admin
from board.models import Board, Movie

# Register your models here.
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display=("writer","title","content")
    
@admin.register(Movie)    
class MovieAdmin(admin.ModelAdmin):
    list_display=("title","point")