from django.contrib import admin

from .models import Follow, Group, Post

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Указываем поля, которые будут отображаться в Админке
    list_display = ("pk", "text", "pub_date", "author")

# Добавляем интерфейс для поиска данных
    search_fields = ("text",)
# Добавляем возможность фильтрации по дате
    list_filter = ("pub_date",)
# это свойство сработает для всех колонок: где пусто - там будет эта строка
    empty_value_display = "-пусто-"

@admin.register(Follow)
class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "author")


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "slug", "description")
    search_fields = ("title", "slug")
    empty_value_display = "-пусто-"
