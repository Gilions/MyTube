from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import cache

from posts.models import User, Post, Group, Follow


class PostsTest(TestCase):
    def setUp(self):
        # Создаем 3 клиента, первый/ третий залогинен
        self.client_1 = Client()
        self.client_2 = Client()
        self.client_3 = Client()

        # Создаем тестувую группу
        self.group = Group.objects.create(title="test_group", slug="t_group")
        self.group.save()

        # Логинимся на сайте
        self.client_1.force_login(User.objects.get_or_create(username='Tc')[0])
        self.client_3.force_login(User.objects.get_or_create(username='T')[0])

        # Создаем новый пост client_1, username Tc
        with open('media/posts/test.jpg', 'rb') as img:
            test_context = {
                "group": self.group.id, "text": "Hello test", "image": img}
            response = self.client_1.post(reverse('new'), test_context)
        self.assertEqual(response.status_code, 302)

        # Подписываемся на автора
        self.client_3.get(reverse('profile_follow',
                          kwargs={"username": 'Tc'}))

    # Удаляем записи
    def tearDown(self):
        self.group.delete()

    def checking_posts(self, url, message):
        # Проверяем новые посты и отредактированные посты
        response = self.client_1.get(url)
        if response.context.get("paginator") is not None:
            text = response.context["page"][0].text
            return (self.assertEqual(text, message),
                    self.assertContains(response, '<img', status_code=200))
        text = response.context["post"].text
        return (self.assertEqual(text, message),
                self.assertContains(response, '<img', status_code=200))

    def test_auth_profile(self):
        # Проверяем доступ на страницу автора
        url = reverse("profile", kwargs={'username': "Tc"})
        response = self.client_1.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client_1.get(reverse('new'))
        self.assertEqual(response.status_code, 200)

    def test_new_post(self):
        # Проверяем наличие поста на страницах профиля, поста и группы
        urls = (
         reverse("profile", kwargs={'username': 'Tc'}),
         reverse('post', kwargs={'username': 'Tc', 'post_id': 1}),
         reverse('group_posts', kwargs={'slug': 't_group'}),)
        for url in urls:
            self.checking_posts(url, 'Hello test')

    def test_edit_post(self):
        # Редактируем новый пост
        with open('media/posts/test.jpg', 'rb') as img:
            url = reverse('post_edit', kwargs={'username': 'Tc', 'post_id': 1})
            response = self.client_1.post(url, {'group': self.group.id,
                                                'text': 'post edit',
                                                "image": img})
        self.assertEqual(response.status_code, 302)
        # Проверяем изменился ли пост на главной станице
        # на страницах профиля, поста, группы
        urls = (
         reverse('index'),
         reverse("profile", kwargs={'username': 'Tc'}),
         reverse('post', kwargs={'username': 'Tc', 'post_id': 1}),
         reverse('group_posts', kwargs={'slug': 't_group'}),)
        for url in urls:
            self.checking_posts(url, 'post edit')

    def test_follower(self):
        # Проверяем подписку
        count = Follow.objects.all().count()
        self.assertEqual(count, 1)

    def test_unfollow(self):
        # Отписываемся от автора
        url = reverse('profile_unfollow', kwargs={"username": 'Tc'})
        response = self.client_3.get(url)
        count = Follow.objects.all().count()
        self.assertEqual(count, 0)

    def test_follower_post(self):
        # Переходим на страницу авторов, проверяем наличие поста
        response = self.client_3.get(reverse('follow_index'))
        self.assertEqual(response.status_code, 200)
        count = len(response.context["page"])
        self.assertEqual(count, 1)

        # Проверяет клиент без подписки
        response = self.client_1.get(reverse('follow_index'))
        self.assertEqual(response.status_code, 200)
        count = len(response.context["page"])
        self.assertEqual(count, 0)

    def test_add_comment(self):
        # Комментирует авторизованный пользователь
        response = self.client_3.get(reverse('add_comment',
                                             kwargs={"username": 'Tc',
                                                     "post_id": 1}))
        self.assertEqual(response.status_code, 200)
        # Комментирует не авторизованный пользователь
        response = self.client_2.get(reverse('add_comment',
                                             kwargs={"username": 'Tc',
                                                     "post_id": 1}))
        self.assertEqual(response.status_code, 302)

    def test_index_and_cache(self):
        # Context должен отсутствовать
        response = self.client_1.get(reverse('index'))
        self.assertEqual(response.context, None)
        # Чистим cache
        cache.clear()
        # Пост появляется
        response = self.client_1.get(reverse('index'))
        self.assertEqual(len(response.context['page']), 1)

    def test_page_note_found(self):
        response = self.client_1.get('Test')
        self.assertEqual(response.status_code, 404)

    def test_protect(self):
        with open('media/posts/try.txt', 'rb') as img:
            test_context = {
                "group": self.group.id, "text": "Try", "image": img}
            response = self.client_1.post(reverse('new'), test_context)
            self.assertEqual(response.status_code, 200)

    def test_unlogged_client(self):
        # Проверяем доступ к станице new с не авторизованным юзером
        response = self.client_2.get(reverse('new'), follow=True)
        self.assertRedirects(response, "/auth/login/?next=/new/")

        # попытка создать пост не авторизованным пользователем
        test_context = {"group": self.group.id, "text": "Hello test"}
        response = self.client_2.post(reverse('new'), test_context)
        self.assertRedirects(response, "/auth/login/?next=/new/")

        # Попытка подписаться не авторизованным пользователем
        response = self.client_2.get(reverse('profile_follow',
                                     kwargs={"username": 'Tc'}))
        self.assertEqual(response.status_code, 302)

        # Пробуем отписаться
        response = self.client_2.get(reverse('profile_unfollow',
                                     kwargs={"username": 'Tc'}))
        self.assertEqual(response.status_code, 302)
