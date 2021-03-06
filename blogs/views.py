""" Main app(blogs) Views """
import re
import datetime
from urllib.parse import urlencode
from logging import getLogger, config
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q


from .models import Post, PostEval, PostHit, Comment
from .forms import PostForm
from .logging_config import _config


config.dictConfig(_config)
logger = getLogger('blogsLogger')

User = get_user_model()


# Create your views here.
class PostListView(generic.ListView):
    """ List view of the posts created in the past """
    template_name = 'blogs/index.html'
    context_object_name = 'latest_post_list'
    paginate_by = 24

    def get_queryset(self):
        """ Return a queryset of posts whose pub_date is before now."""
        queryset = Post.objects.filter(
            published_date__lte=timezone.now()
        ).order_by('-hits')
        if not queryset:
            messages.info(self.request, 'No post exists.')
        return queryset


class SearchResultPostView(generic.ListView):
    """ List view for rendering search results of the given query """
    template_name = 'blogs/result.html'
    context_object_name = 'result_post_list'
    paginate_by = 24

    def __init__(self):
        super().__init__()
        self.sort_key = '-hits'
        self.start_day = 1

    def get(self, request, *args, **kwargs):
        if not request.GET.get('q'):
            return redirect('blogs:index')

        return super().get(request, *args, **kwargs)


    def get_queryset(self):
        """ Return queryset filtered by the given parameters """
        if not self.request.GET.get('q'):
            return None
        
        """ Get queryset matching with search words """
        query_list = self.parse_search_params(self.request.GET['q'])
        query = Q()
        for word in query_list:
            query = (
                query
                | Q(author__username__icontains=word)
                | Q(title__icontains=word)
            )
        
        """ sort """
        if self.request.GET.get('sort'):
            self.sort_key = self.request.GET['sort']
        
        """"""" filter """""""""
        """ day """
        if self.request.GET.get('day'):
            self.start_day = int(self.request.GET['day'])
            start_datetime = timezone.now() - datetime.timedelta(days=self.start_day)
            query = query & Q(
                published_date__range=(start_datetime, timezone.now()))

        return Post.objects.filter(query).order_by(self.sort_key)

    def get_context_data(self, **kwargs):
        """
        Return the context including some paths. Each path's query does not including one param.
        """
        context = super().get_context_data(**kwargs)
        query_context = {}
        if self.request.GET.get('q'):
            query_context['q'] = self.request.GET['q']
        if self.request.GET.get('sort'):
            query_context['sort'] = self.request.GET['sort']
        if self.request.GET.get('day'):
            query_context['day'] = self.request.GET['day']

        base_path = reverse_lazy('blogs:result')
        result_url = '{}?{}'.format(base_path, urlencode(query_context))
        result_urls = {
            'sort_path': re.sub(r'&sort=.+(?=&)|&sort=.+$', '', result_url),
            'day_path': re.sub(r'&day=.+(?=&)|&day=.+$', '', result_url),
        }
        context.update(result_urls)
        return context

    def parse_search_params(self, words):
        """ Parse the given search words into a list of words """
        words = str(words)
        search_words = re.split(r'\s+', words)
        return search_words


class PostDetailView(generic.DetailView):
    """ Detail view of posts """
    model = Post
    template_name = 'blogs/detail.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        """ Comment list """
        context['comment_list'] = Comment.objects.filter(
            post = post
        ).order_by('-updated_date')

        """ Post Hit """
        context['post_hit'] = post.count_hits()

        """ Post Eval """
        context['post_eval_good'] = post.count_goods()
        context['post_eval_bad'] = post.count_bads()

        if not self.request.user.is_authenticated:
            return context

        """"""""""""" Login required functions """""""""""""""""""

        """" Post Eval """
        try:
            context['my_post_eval'] = post.posteval_set.get(user=self.request.user)
        except PostEval.DoesNotExist:
            context['my_post_eval'] = post.posteval_set.create(user=self.request.user)

        return context


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    """ Create view of posts """
    login_url = reverse_lazy('login')
    model = Post
    form_class = PostForm
    template_name = 'blogs/post.html'
    success_url = reverse_lazy('blogs:index')

    def form_valid(self, form):
        form.instance.create(self.request.user)
        messages.success(self.request, 'saved successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'not saved - alert!')
        return super().form_invalid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    """ Update view of posts """
    login_url = reverse_lazy('accounts:login')
    model = Post
    form_class = PostForm
    template_name = 'blogs/edit.html'

    def test_func(self):
        current_user = self.request.user
        post = get_object_or_404(self.model, pk=self.kwargs['pk'])
        author = post.author
        return current_user.pk == author.pk or current_user.is_superuser

    def get_success_url(self):
        """ If user can update the post, they are redirected to here """
        return reverse_lazy('blogs:detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.publish()
        messages.success(self.request, 'saved successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'not saved - alert!')
        return super().form_invalid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """ Delete view of posts """
    login_url = reverse_lazy('accounts:login')
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blogs:index')

    def test_func(self):
        current_user = self.request.user
        post = get_object_or_404(self.model, pk=self.kwargs['pk'])
        author = post.author
        return current_user.pk == author.pk or current_user.is_superuser

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(self.request, '"{}" was deleted.'.format(self.object))
        return result


class UserPageView(generic.TemplateView):
    """ User page view """
    template_name = 'blogs/user_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dest_user'] = get_object_or_404(User, pk=self.kwargs['pk'])
        return context


class UserPostListView(generic.ListView):
    """ List view of the posts published by the user """
    template_name = 'blogs/user_posts.html'
    context_object_name = 'my_post_list'
    paginate_by = 15

    def get_queryset(self):
        queryset = Post.objects.filter(
            published_date__lte=timezone.now(),
            author=self.kwargs['pk'],
        ).order_by('-published_date')
        if not queryset:
            messages.info(self.request, 'No post exist')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dest_user'] = get_object_or_404(User, pk=self.kwargs['pk'])
        return context


class UserProfileView(generic.TemplateView):
    """ User profile view """
    template_name = 'blogs/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dest_user'] = get_object_or_404(User, pk=self.kwargs['pk'])
        return context
