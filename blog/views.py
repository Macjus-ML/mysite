from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post

'''
Это версия без разделения на страницы
# обработчик для отображения списка статей.
def post_list(request):
   # запрашиваем из базы данных все опубликованные статьи с помощью менеджера published.
   posts = Post.published.all()
   # render принимает объект запроса request, путь к шаблону и переменные контекста для этого шаблона
   return render(request, 'blog/post/list.html',{'posts':posts})
   # вернется объект HttpResponse со сформированным текстом
'''

'''
Это версия включает пагинатор -  разделения на страницы
'''
def post_list(request):
    object_list = Post.published.all()
   # инициализируем объект класса Paginator, указав количество объектов на одной странице;
   # По 3 статьи на каждой странице.
    paginator = Paginator(object_list, 3)
   # извлекаем из запроса GET-параметр page, который указывает текущую страницу
    page = request.GET.get('page')
   # получаем список объектов на нужной странице с помощью метода page()класса Paginator
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
      # Если страница не является целым числом, возвращаем первую страницу.
        posts = paginator.page(1)
    except EmptyPage:
      # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
        posts = paginator.page(paginator.num_pages)
   # передаем номер страницы и полученные объекты в шаблон.
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts})
# Обработчик PostListView является аналогом функции post_list 
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


# обработчик для отображения статьи
def post_detail(request, year, month, day, post):
   # используем get_object_or_404() - функция возвращает объект или вызывает исключение HTTP 404
    post = get_object_or_404(Post, slug=post,
      # добавлено ограничение, чтобы слаг был уникальным для статей, созданных в один день
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
   # используем функцию render() для формирования HTML-шаблона.
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})

