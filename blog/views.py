from django.views import generic
from .models import Post
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 2 #paginação

#class PostDetail(generic.DetailView):
#    model = Post
#    template_name = 'post_detail.html'

def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

def sobre(request):
    template_name = 'sobre.html'
    return render(request, template_name)


class PostCreate(generic.CreateView):
    model = Post
    fields = "__all__"
    success_url = reverse_lazy('home')


class PostUpdate(generic.UpdateView):
    model = Post
    fields = "__all__"
    success_url = reverse_lazy('home')


class PostDelete(generic.DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')

def contato(request):
    template_name = 'contato.html'
    return render(request, template_name)

class PostSearch(generic.ListView):
    model = Post
    template_name = 'search_results.html'
    paginate_by = 5 #paginação     

    def get_queryset(self): # new
        query = self.request.GET.get('search')
        object_list = Post.objects.filter(title__icontains=query).order_by('-created_on')
                
        return object_list
