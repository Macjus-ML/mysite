from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
	STATUS_CHOICES = (
		('draft','Draft'),
		('published', "Published"),
	)
	# поле заголовка статьи
	title  =models.CharField(max_length=250)
	# уникальная строка идентификатор, понятная человеку
	slug = models.SlugField(max_length=250,unique_for_date='publish')
	# каждая статья имеет автора, при- чем каждый пользователь может быть автором любого количества статей
	author = models.ForeignKey(User,on_delete = models.CASCADE,related_name='blog_posts')
	# основное содержание статьи
	body = models.TextField()
	# поле даты, которое сохраняет дату публикации статьи
	publish =models.DateTimeField(default=timezone.now)
	#  это поле даты указывает, когда статья была создана
	created = models.DateTimeField(auto_now_add=True)
	# дата и время, указывающие на период, когда статья была отредактирована.
	updated = models.DateTimeField(auto_now=True)
	# это поле отображает статус статьи
	status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')

class Meta:
	# порядок сортировки статей по умолчанию по убыванию даты публикации, поля publish. 
	# О том, что порядок убывающий, говорит префикс «-»
	ordering = ('-publish',)

# Метод возвращает отображение объекта, понятное человеку.
def __str__(self):
	return self.title