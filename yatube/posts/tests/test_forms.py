from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Comment, Group, Post

User = get_user_model()


class PostFormTests(TestCase):
    """Создание тестового юзера и постов в группу"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestUser')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title='Тестовое название группы',
            slug='test-slug',
            description='Тестовое описание группы'
        )
        cls.post = Post.objects.create(
            title='Тестовое название группы',
            author=cls.user,
            text='Тестовый пост',
            group=cls.group
        )
        cls.form_data_posts = {
            "title":'Тестовое название группы',
            "text": 'Тестовый текст',
            "group": cls.group.id
        }
        cls.form_data_comment = {
            'text': 'Тестовый комментарий'
        }

    def test_create_post(self):
        """Создание тестовой записи"""
        count = Post.objects.count() + 1
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=self.form_data_posts,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': self.user.username})
        )
        self.assertEqual(Post.objects.count(), count)
        self.assertTrue(Post.objects.filter(text=self.form_data_posts["text"])
                        .exists())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit(self):
        """Редактирование тестовой записи"""
        count = Post.objects.count()
        response = self.authorized_client.post(
            reverse(
                'posts:post_edit', kwargs={'post_id': self.post.id}),
            data=self.form_data_posts,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse(
                "posts:post_detail", kwargs={"post_id": self.post.id}
            )
        )
        self.assertEqual(Post.objects.count(), count)
        self.assertTrue(Post.objects.filter(text=self.form_data_posts['text'])
                        .exists())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_comment(self):
        """Валидная форма создает запись в Comment."""
        comment_count = Comment.objects.count()
        response = self.authorized_client.post(
            reverse(
                'posts:add_comment',
                kwargs={'post_id': self.post.pk}
            ),
            data=self.form_data_comment,
            follow=True
        )
        comment = Comment.objects.first()
        self.assertRedirects(response, reverse(
            'posts:post_detail',
            kwargs={'post_id': self.post.pk}
        ))
        self.assertEqual(Comment.objects.count(), comment_count + 1)
        self.assertEqual(comment.text, self.form_data_comment['text'])
        self.assertEqual(comment.post, PostFormTests.post)
        self.assertEqual(comment.author, PostFormTests.user)
