from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import Count
from .models import Post,Comment
from .forms import EmailPostForm, CommentForm
from taggit.models import Tag

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
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
      tag = get_object_or_404(Tag,slug=tag_slug)
      object_list=object_list.filter(tags__in=[tag])
   # инициализируем объект класса Paginator, указав количество объектов на одной странице;
   # По 3 статьи на каждой странице.
    paginator = Paginator(object_list, 5)
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
                   'posts': posts,
                   'tag': tag})

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
   # Список активных комментариев для этой статьи.
    comments = post.comments.filter(active = True)
    new_comment = None
   # Если приходит POST  запрос
    if request.method == 'POST':
      # Пользователь отправил комментарий.
      # заполняем форму данными из запроса
       comment_form = CommentForm(data=request.POST)
      # валидируем ее методом is_valid()
       if comment_form.is_valid():
         # Создаем комментарий, но пока не сохраняем в базе данных.
          new_comment = comment_form.save(commit=False)
         # Привязываем комментарий к текущей статье.
          new_comment.post = post
         # Сохраняем комментарий в базе данных.
          new_comment.save()
      #при GET-запросе используем запись comment = CommentForm()
    else:
       comment_form = CommentForm()
   # используем функцию render() для формирования HTML-шаблона.
   # Формирование списка похожих статей
   # получаем все ID тегов текущей статьи
   # flat=True,чтобы получить «плоский» список вида [1, 2, 3, ...]
    post_tags_ids = post.tags.values_list('id',flat=True)
    # получает все статьи, содержащие хоть один тег из полученных ранее,
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
    .exclude(id=post.id) #исключая текущую статью;
    # использует Count для формирования вычисляемого поля same_tags
    # сортирует список опубликованных статей в убывающем порядке по
    # количеству совпадающих тегов для отображения первыми максимально похожих статей
    # и делает срез результата для отображения только четырех статей
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
    .order_by('-same_tags','-publish')[:4]

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts
                   })


# определяем функцию post_share, которая принимает объект запроса request и параметр post_id;
def post_share(request, post_id):
   #Получение статьи по идентификатору и подтверждение, что статья опубликована
    post = get_object_or_404(Post, id=post_id, status='published')
   # Sent  будет установлена в True  после отправки сообщения
    sent = False
   # Если заполненная форма отправляется методом POST
   # обрабатываем данные формы и отправляем их на почту.
    if request.method == 'POST':
   # Форма была отправлена на сохранение.
        form = EmailPostForm(request.POST)
   # Проверка введенных данных с помощью метода формы is_valid()
        if form.is_valid():
   # Если все поля формы прошли валидацию.
   # получаем введенные данные с помощью form. cleaned_data
            cd = form.cleaned_data
   # добавим в сообщение абсолютную ссылку на сообщение
            post_url = request.build_absolute_uri(
                                          post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'bolshakovav@yandex.ru',[cd['to']])
            sent = True
   # Если метод запроса – GET, необходимо отобразить пустую форму;
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})






