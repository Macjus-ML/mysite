from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post

	# Атрибуты title, link и description будут представлены 
	# RSS элементами <title>, <link> и <description> соответственно.
class LatestPostsFeed(Feed):
    title = 'My blog'
    link = '/blog/'
    description = 'New posts of my blog.'

	# tems() получает (5) объекты, которые будут включены в рассылку
    def items(self):
        return Post.published.all()[:5]
	# Методы item_title() и item_description() получают для каждого объекта из результата items() заголовок и описание
    def item_title(self, item):
        return item.title
	# используем встроенный шаблонный фильтр truncatewords, чтобы ограничить описание статей тридцатью словами.
    def item_description(self, item):
        return truncatewords(item.body, 30)
