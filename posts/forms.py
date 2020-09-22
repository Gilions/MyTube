from django import forms
from django.forms import ModelForm

from .models import Post, Comment


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ("text", "group", "image")

        labels = {
         "text": "Новое сообщение",
         "group": "Выберите группу"
         }
        help_texts = {
            "text": "Поле обязательное для заполнения.",
            }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)

        help_texts = {
            "text": "Поле обязательное для заполнения.",
            }
