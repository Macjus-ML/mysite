from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # с помощью include,подключим конфигурацию приложения блога
    # Мы будем об- ращаться к шаблонам приложения по пространству имен,
    # например blog:post_ list, blog:post_detail.
    path('blog/',include('blog.urls', namespace = 'blog'))
]
