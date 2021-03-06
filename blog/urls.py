from django.urls import path
from . import views
from .feeds import LatestPostsFeed

# пространство имен приложения в переменной app_name
app_name = 'blog'
'''
Второй path  вызывает функцию post_detail и принимает в качестве параметров следующие:
 year – целое число, задающее год публикации статьи;
 month – целое число, задающее месяц;
 day – целое число, представляющее день публикации;
 post – строка, которая может содержать буквы, цифры и дефисы или нижние подчеркивания.
Треугольные скобки нужны для извлечения значений из URL’а. 
Любое значение, определенное в шаблоне как <parameter>, 
возвращается в виде строки. Мы используем конвертер, например <int:year>,
 чтобы явно указать, что год должен быть извлечен из адреса в виде целого числа; 
 <slug:post> – слаг будет извлечен как строка, которая может содержать только
  буквы, цифры и дефисы с нижними подчеркиваниями (в соответствии со стандартом ASCII).
'''
urlpatterns = [
	path('',views.post_list,name='post_list'),
	# path('', views.PostListView.as_view(), name='post_list'),
	path('<int:year>/<int:month>/<int:day>/<slug:post>/',
			views.post_detail,name='post_detail'),
	path('<int:post_id>/share/', views.post_share, name = 'post_share'),
	path('tag/<slug:tag_slug>/',views.post_list, name='post_list_by_tag'),
   path('feed/', LatestPostsFeed(), name='post_feed'),
   path('search/', views.post_search, name='post_search'),
]