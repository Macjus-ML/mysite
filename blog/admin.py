from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    #позволяет перечислить поля модели, которые мы хотим отображать на странице списка
    list_display = ('title', 'slug', 'author', 'publish','status')
    # Справа на странице  блок фильтрации списка, который фильтрует статьи по полям
    list_filter = ('status', 'created', 'publish', 'author')
    # появилась строка поиска
    search_fields = ('title', 'body')
    #slug генерируется автоматически из поля title
    prepopulated_fields = {'slug': ('title',)}
    # поле author содержит поле поиска, что значительно упрощает выбор автора из выпадающего списка
    raw_id_fields = ('author',)
    # добавлены ссылки для навигации по датам.
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
