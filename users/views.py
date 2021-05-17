#  импортируем CreateView, чтобы создать ему наследника
#  функция reverse_lazy позволяет получить URL по параметру "name" функции path
#  берём, тоже пригодится
from django.urls import reverse_lazy
from django.views.generic import CreateView

#  импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    # где login — это параметр "name" в path()
    success_url = reverse_lazy("login")
    template_name = "signup.html"
