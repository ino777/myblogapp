""" Main app(blogs) tests """
import io
import datetime
import urllib.parse
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model


from .models import Post, Comment, PostHit, PostEval


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
    Create post object 
    
    Args:
        author, title, days(negative for past, positive for future), text(default=TEST)
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
    """ Tests PostListView """
    def setUp(self):
        self.user = User.objects.create_user('tester', 'test@gmail.com', 'password')

    def test_no_post(self):
        """ If there are no posts, an appropriate message is displayed """
        response = self.client.get(reverse('blogs:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No post exists.')
        self.assertQuerysetEqual(response.context['latest_post_list'], [])

    def test_past_post(self):
        """ Posts with a published_date in the past are displayed on the index page """
        create_post(author=self.user, title='Past post', days=-30)
        response = self.client.get(reverse('blogs:index'))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Past post>']
        )
    
    def test_future_post(self):
        """ Posts with a published_date in the future are not displayed on the index page """
        create_post(author=self.user, title='Future post', days=+30)
        response = self.client.get(reverse('blogs:index'))
        self.assertContains(response, 'No post exists.')
        self.assertQuerysetEqual(response.context['latest_post_list'], [])

    def test_two_past_post(self):
        """ The index page display multiple post """
        create_post(author=self.user, title='Past post 1', days=-30)
        create_post(author=self.user, title='Past post 2', days=-5)
        response = self.client.get(reverse('blogs:index'))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Past post 2>', '<Post: Past post 1>']
        )

    def test_past_and_future_post(self):
        """ If there are past posts and future posts, only past posts are displayed """
        create_post(author=self.user, title='Past post', days=-30)
        create_post(author=self.user, title='Future post', days=+30)
        response = self.client.get(reverse('blogs:index'))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Past post>']
        )


class SearchResultPostViewTests(TestCase):
    """ Tests SearchResultPostView"""
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@gmail.com', 'password')
        self.other_user = User.objects.create_user('other', 'other@gmail.com', 'password')

    def test_no_post(self):
        """ If there are no posts, the user are redirected to index page """
        response = self.client.get(reverse('blogs:result'))
        self.assertRedirects(response, reverse('blogs:index'))

    def test_no_search_word(self):
        """ If there are no search words, the user are redirected to index page """
        response = self.client.get(reverse('blogs:result') + '?q=')
        self.assertRedirects(response, reverse('blogs:index'))
    
    def test_search_post_by_author(self):
        """ When the user search by author name, the matched posts are displayed """
        post1 = create_post(author=self.user, title='post1', days=-30)
        post2 = create_post(author=self.user, title='post2', days=-60)
        q = dict(q=self.user.username)
        response = self.client.get(reverse('blogs:result')  + '?' + urllib.parse.urlencode(q))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['result_post_list'], 
            ['<Post: post1>', '<Post: post2>']
        )
    
    def test_search_post_by_title(self):
        """ When the user search by title, the matched posts are displayed """
        post1 = create_post(author=self.user, title='testpost', days=-30)
        post2 = create_post(author=self.other_user, title='testpost', days=-20)
        q = dict(q='testpost')
        response = self.client.get(reverse('blogs:result')  + '?' + urllib.parse.urlencode(q))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['result_post_list'], 
            ['<Post: testpost>', '<Post: testpost>']
        )
    
    def test_not_matched_with_post(self):
        post1 = create_post(author=self.user, title='testpost', days=-30)
        q = dict(q='mismatch_word')
        response = self.client.get(reverse('blogs:result') + '?' + urllib.parse.urlencode(q))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['result_post_list'], [])


class PostDetailViewTests(TestCase):
    """ Tests PostDetailView """
    def setUp(self):
        self.user = User.objects.create_user('tester', 'test@gmail.com', 'password')

    def test_past_post(self):
        """ Posts with a published_date in the past are displayed on detail page """
        past_post = create_post(author=self.user, title='Past post', days=-30)
        response = self.client.get(reverse('blogs:detail', args=(past_post.id,)))
        self.assertContains(response, past_post.title)

    def test_future_post(self):
        """ Posts with a published_date in the future are not displayed on detail page """
        future_post = create_post(author=self.user, title='Future post', days=+30)
        response = self.client.get(reverse('blogs:detail', args=(future_post.id,)))
        self.assertEqual(response.status_code, 404)
    
    def test_get_comment(self):
        """ Comments related with the post are displayed on detail page """
        post = create_post(author=self.user, title='testpost', days=-30)
        comment = Comment.objects.create(user=self.user, post=post, text='comment', created_date=timezone.now(), updated_date=timezone.now())
        response = self.client.get(reverse('blogs:detail', args=(post.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['comment_list'], ['<Comment: Comment object (1)>'])

    def test_get_hit(self):
        """ Post hits of the post are displayed on detail page """
        post = create_post(author=self.user, title='testpost', days=-30)
        hit = PostHit.objects.create(user=self.user, post=post, hit=True, created_date=timezone.now())
        response = self.client.get(reverse('blogs:detail', args=(post.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post_hit'], 1)


class PostCreateViewTests(TestCase):
    """ Tests PostCreateView"""
    def test_not_logged_in_post(self):
        """ If the user are not authenticated, they are redirected to login page """
        form_data = {
            'title': 'Post',
            'text': 'TEST POST',
            'image': make_dummy_image()
        }
        response = self.client.post(reverse('blogs:post'), data=form_data)
        self.assertRedirects(
            response,
            reverse('login') + '?next=' + reverse('blogs:post')
        )

    def test_logged_in_post(self):
        """ If the user are authenticated, they can create post and are redirected to index page """
        self.client.force_login(
            User.objects.create_user('tester', 'test@gmail.com', 'password'))
        form_data = {
            'title': 'Post',
            'text': 'TEST POST',
            'image': make_dummy_image()
        }
        response = self.client.post(reverse('blogs:post'), data=form_data)
        self.assertRedirects(response, reverse('blogs:index'))


class PostUpdateViewTests(TestCase):
    """ Tests PostUpdateView """
    def setUp(self):
        self.user = User.objects.create_user('tester', 'test@gmail.com', 'password')
        self.post = create_post(author=self.user, title='Post', days=-30)
        self.post.save()

    def test_not_logged_in_update(self):
        """ If the user are not authenticated, they are redirected to login page """
        change_data = {
            'title': 'Changed Post',
            'text': 'Changed TEST',
            'image': make_dummy_image()
        }
        response = self.client.put(reverse('blogs:edit', args=(self.post.pk,)), data=change_data)
        self.assertRedirects(
            response,
            reverse('login') + '?next=' + reverse('blogs:edit', args=(self.post.pk,))
        )

    def test_other_user_update(self):
        """ If other user try to update the post, it reuturns 403 """
        change_data = {
            'title': 'Changed Post',
            'text': 'Changed TEST',
            'image': make_dummy_image()
        }
        self.client.force_login(User.objects.create_user('other_user', 'other@gmail.com', 'password'))
        response = self.client.put(reverse('blogs:edit', args=(self.post.pk,)), data=change_data)
        self.assertEqual(response.status_code, 403)

    def test_update(self):
        """ If the user are authenticated and the poster of the post, they can update it """
        change_data = {
            'title': 'Changed Post',
            'text': 'Changed TEST',
            'image': make_dummy_image()
        }
        self.client.force_login(self.user)
        response = self.client.put(reverse('blogs:edit', args=(self.post.pk,)), data=change_data)
        self.assertEqual(response.status_code, 200)


class PostDeleteViewTests(TestCase):
    """ Tests PostDelateView """
    def setUp(self):
        self.user = User.objects.create_user('tester', 'test@gmail.com', 'password')
        self.post = create_post(author=self.user, title='Post', days=-30)
        self.post.save()

    def test_not_logged_in_delete(self):
        """ If the user are not authenticated, they are redirected to login page """
        response = self.client.delete(reverse('blogs:delete', args=(self.post.pk,)))
        self.assertRedirects(
            response,
            reverse('login') + '?next=' + reverse('blogs:delete', args=(self.post.pk,))
        )

    def test_other_user_delete(self):
        """ If other user try to delete the post, it returns 403 """
        self.client.force_login(User.objects.create_user('other_user', 'other@gmail.com', 'password'))
        response = self.client.delete(reverse('blogs:delete', args=(self.post.pk,)))
        self.assertEqual(response.status_code, 403)

    def test_delete(self):
        """ If the user are authenticated and the poster of the post, they can delete it """
        self.client.force_login(self.user)
        response = self.client.delete(reverse('blogs:delete', args=(self.post.pk,)))
        self.assertRedirects(response, reverse('blogs:index'))


class UserPageViewTests(TestCase):
    """ Tests UserPageView """
    def setUp(self):
        self.user = User.objects.create_user('tester', 'test@gmail.com', 'password')

    def test_not_logged_in(self):
        """ Even if the user are not authenticated, user page is displayed """
        dest_user = self.user
        response = self.client.get(reverse('blogs:user_page', args=(dest_user.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_visit_by_myself(self):
        """ If the user visit their own user page, it is displayed """
        dest_user = self.user
        self.client.force_login(self.user)
        response = self.client.get(reverse('blogs:user_page', args=(dest_user.pk,)))
        self.assertEqual(response.status_code, 200)
    
    def test_visit_by_other(self):
        """ Even if the user visit other user page, it is displayed """
        dest_user = User.objects.create_user('other', 'other@gmail.com', 'password')
        self.client.force_login(self.user)
        response = self.client.get(reverse('blogs:user_page', args=(dest_user.pk,)))
        self.assertEqual(response.status_code, 200)


class UserPostListViewTests(TestCase):
    """ Tests UserPostListView """
    def setUp(self):
        self.user = User.objects.create_user('tester', 'test@gmail.com', 'password')

    def test_not_logged_in(self):
        """ Even if the user are not authenticated, user posts page is displayed """
        dest_user = self.user
        response = self.client.get(reverse('blogs:user_posts', args=(dest_user.pk,)))
        self.assertEqual(response.status_code, 200)
    
    def test_visit_by_myself(self):
        """ If the user visit their own user posts page, it is displayed """
        dest_user = self.user
        self.client.force_login(self.user)
        response = self.client.get(reverse('blogs:user_posts', args=(dest_user.pk,)))
        self.assertEqual(response.status_code, 200)
    
    def test_visit_by_other(self):
        """ Even if the user visit other user posts page, it is displayed """
        dest_user = User.objects.create_user('other', 'other@gmail.com', 'password')
        self.client.force_login(self.user)
        response = self.client.get(reverse('blogs:user_posts', args=(dest_user.pk,)))
        self.assertEqual(response.status_code, 200)
        
    def test_past_post(self):
        """ Posts with a published_date in the past are displayed on user posts page """
        dest_user = self.user
        past_post = create_post(author=self.user, title='Past post', days=-30)
        self.client.force_login(self.user)
        response = self.client.get(reverse('blogs:user_posts', args=(dest_user.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['my_post_list'], ['<Post: Past post>'])

    def test_future_post(self):
        """ Posts with a published_date in the future are not displayed on user posts page """
        dest_user = self.user
        future_post = create_post(author=self.user, title='Future post', days=+30)
        self.client.force_login(self.user)
        response = self.client.get(reverse('blogs:user_posts', args=(dest_user.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['my_post_list'], [])


class UserProfileViewTests(TestCase):
    """ Tests UserProfileView """
    def setUp(self):
        self.user = User.objects.create_user('tester', 'test@gmail.com', 'password')

    def test_not_logged_in(self):
        """ Even if the user are not authenticated, user profile page is displayed """
        dest_user = self.user
        response = self.client.get(reverse('blogs:user_profile', args=(dest_user.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_visit_by_myself(self):
        """ If the user visit their own user profile page, it is displayed """
        dest_user = self.user
        self.client.force_login(self.user)
        response = self.client.get(reverse('blogs:user_profile', args=(dest_user.pk,)))
        self.assertEqual(response.status_code, 200)
    
    def test_visit_by_other(self):
        """ Even if the user visit other user profile page, it is displayed """
        dest_user = User.objects.create_user('other', 'other@gmail.com', 'password')
        self.client.force_login(self.user)
        response = self.client.get(reverse('blogs:user_profile', args=(dest_user.pk,)))
        self.assertEqual(response.status_code, 200)