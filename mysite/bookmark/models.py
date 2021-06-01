from django.db import models

# Create your models here.
class Bookmark(models.Model): #djang의 Model class를 상속받음
    #필드선언, blank 빈값허용여부, null null허용여부
    title=models.CharField(max_length=100, blank=True, null=True)
    #unique "primary key
    url=models.URLField('url', unique=True)
    
    #객체를 문자열로 표현하는 함수
    def __str__(self):
        return self.title