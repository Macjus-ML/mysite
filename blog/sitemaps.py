from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
   # Атрибуты changefreq и priority показывают частоту обновления 
   # страниц статей и степень их совпадения с тематикой сайта (максимальное значение – 1)
   hangefreq = 'weekly'
   priority = 0.9

   # items() возвращает QuerySet объектов, которые будут отображаться в карте сайта.
   def items(self):
        return Post.published.all()

   # lastmod принимает каждый объект из результата вызова
   # items() и возвращает время последней модификации статьи
   def lastmod(self, obj):
        return obj.updated
