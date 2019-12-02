from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

# Эта переменная является объектом класса template.Library
# и используется для регистрации пользовательских тегов и фильтров в системе.
register = template.Library()

# создадим простой шаблонный тег, который возвращает количество опубликованных в блоге статей. 
#  оборачиваем total_posts в декоратор @register.simple_tag для регистрации нового тега.

@register.simple_tag
def total_posts():
	return Post.published.count()

#  создадим тег для добавления последних статей блога на боковую панель.
# регистрируем тег с помощью декоратора @register.inclusion_tag
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
# помощью count мы сможем из шаблона указать количество статей для отображения. 
	# функция тега возвращает словарь переменных вместо простого значения. 
	# Инклюзивные теги должны возвращать только словари контекста
	latest_posts = Post.published.order_by('-publish')[:count]
	return {'latest_posts':latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
	# Count используется для вычисления количества комментариев
	# total_comments для каждого объекта Post
	return Post.published.annotate(total_comments = Count('comments')).order_by('-total_comments')[:count]
			# cортируем QuerySet по этому полю в порядке убывания

@register.filter(name='markdown')
def markdown_format(text):
	# По умолчанию Django не доверяет любому HTML, используем функцию mark_safe
	return mark_safe(markdown.markdown(text))


