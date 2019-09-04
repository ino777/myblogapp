""" Main app(blogs) tests """
import io
import datetime
from PIL import Image
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model


from .models import Post


User = get_user_model()


# Create your tests here.
def make_dummy_image():
    """ Return dummy image (io.BytesIO())"""
    file_obj = io.BytesIO()
    content = Image.new('RGBA', size=(10, 10), color=(256, 0, 0))
    content.save(file_obj, 'png')
    file_obj.name = 'dummy_im.png'
    file_obj.seek(0)
    return file_obj

def create_post(author, title, days, text='TEST'):
    """ 
    Return post object 
    
    Args:
        author, title, days, text(default=TEST)
    """
    img = make_dummy_image()
    time = timezone.now() + datetime.timedelta(days=days)
    return Post.objects.create(
        author=author,
        title=title,
        text=text,
        image=SimpleUploadedFile(img.name, img.read(), content_type='image/png'),
        created_date=timezone.now(),
        published_date=time
    )


class PostListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', 'a@gfmk.com', 'password')

    def test_no_post(self):
        response = self.client.get(reverse('blogs:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No post exists.')
        self.assertQuerysetEqual(response.context['latest_post_list'], [])

    def test_past_post(self):
        create_post(author=self.user, title='Past post', days=-30)
        response = self.client.get(reverse('blogs:index'))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Past post>']
        )
    
    def test_future_post(self):
        create_post(author=self.user, title='Future post', days=+30)
        response = self.client.get(reverse('blogs:index'))
        self.assertContains(response, 'No post exists.')
        self.assertQuerysetEqual(response.context['latest_post_list'], [])

    def test_two_past_post(self):
        create_post(author=self.user, title='Past post 1', days=-30)
        create_post(author=self.user, title='Past post 2', days=-5)
        response = self.client.get(reverse('blogs:index'))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Past post 2>', '<Post: Past post 1>']
        )

    def test_past_and_future_post(self):
        create_post(author=self.user, title='Past post', days=-30)
        create_post(author=self.user, title='Future post', days=+30)
        response = self.client.get(reverse('blogs:index'))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Past post>']
        )

 
class PostDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', 'a@gfmk.com', 'password')
        self.user.icon_image = File(make_dummy_image())
        self.user.save()

    def test_past_post(self):
        past_post = create_post(author=self.user, title='Past post', days=-30)
        response = self.client.get(reverse('blogs:detail', args=(past_post.id,)))
        self.assertContains(response, past_post.title)

    def test_future_post(self):
        future_post = create_post(author=self.user, title='Future post', days=+30)
        response = self.client.get(reverse('blogs:detail', args=(future_post.id,)))
        self.assertEqual(response.status_code, 404)


class PostCreateViewTests(TestCase):
    def test_not_logined_post(self):
        form_data = {
            'title': 'Post',
            'text': 'TEST POST',
            'image': make_dummy_image()
        }
        response = self.client.post(reverse('blogs:post'), data=form_data)
        query = dict(next=reverse('blogs:post'))
        self.assertRedirects(
            response,
            reverse('login') + ''.join('?{}={}'.format(key, value) for key, value in query.items())
        )

    def test_logined_post(self):
        self.client.force_login(
            User.objects.create_user('tester', 'tarou.xxx.0129@gmail.com', 'password'))
        form_data = {
            'title': 'Post',
            'text': 'TEST POST',
            'image': make_dummy_image()
        }
        response = self.client.post(reverse('blogs:post'), data=form_data)
        self.assertRedirects(response, reverse('blogs:index'))


class PostUpdateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', 'a@gfmk.com', 'password')
        self.post = create_post(author=self.user, title='Post', days=-30)
        self.post.save()

    def test_not_logined_update(self):
        change_data = {
            'title': 'Changed Post',
            'text': 'Changed TEST',
            'image': make_dummy_image()
        }
        response = self.client.put(reverse('blogs:edit', args=(self.post.pk,)), data=change_data)
        query = dict(next=reverse('blogs:edit', args=(self.post.pk,)))
        self.assertRedirects(
            response,
            reverse('login') + ''.join('?{}={}'.format(key, value) for key, value in query.items())
        )

    def test_other_user_update(self):
        change_data = {
            'title': 'Changed Post',
            'text': 'Changed TEST',
            'image': make_dummy_image()
        }
        self.client.force_login(User.objects.create_user('other_user', 'b@gfmk.com', 'password'))
        response = self.client.put(reverse('blogs:edit', args=(self.post.pk,)), data=change_data)
        self.assertEqual(response.status_code, 403)

    def test_update(self):
        change_data = {
            'title': 'Changed Post',
            'text': 'Changed TEST',
            'image': make_dummy_image()
        }
        self.client.force_login(self.user)
        response = self.client.put(reverse('blogs:edit', args=(self.post.pk,)), data=change_data)
        self.assertEqual(response.status_code, 200)


class PostDeleteViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', 'a@gfmk.com', 'password')
        self.post = create_post(author=self.user, title='Post', days=-30)
        self.post.save()

    def test_not_logined_delete(self):
        response = self.client.delete(reverse('blogs:delete', args=(self.post.pk,)))
        query = dict(next=reverse('blogs:delete', args=(self.post.pk,)))
        self.assertRedirects(
            response,
            reverse('login') + ''.join('?{}={}'.format(key, value) for key, value in query.items())
        )

    def test_other_user_delete(self):
        self.client.force_login(User.objects.create_user('other_user', 'b@gfmk.com', 'password'))
        response = self.client.delete(reverse('blogs:delete', args=(self.post.pk,)))
        self.assertEqual(response.status_code, 403)

    def test_delete(self):
        self.client.force_login(self.user)
        response = self.client.delete(reverse('blogs:delete', args=(self.post.pk,)))
        self.assertRedirects(response, reverse('blogs:index'))