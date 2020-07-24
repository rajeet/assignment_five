from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from .form import BlogForm
from .models import Blogging


class CreateBlog(CreateView):
    form_class = BlogForm
    template_name = "app/createblog.html"
    success_url="/account/manage-blog"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)



class ManageBlog(ListView):
    template_name = "app/manageblog.html"
    def get_queryset(self):
        return Blogging.objects.filter(user=self.request.user)


    context_object_name = "data"


class DeleteBlog(DeleteView):
    model = Blogging
    success_url = "/account/manage-blog/"


class UpdateBlog(UpdateView):
    form_class=BlogForm
    template_name="app/updateblog.html"
    success_url="/account/manage-blog/"
    model = Blogging

    def form_valid(self, form):
        return super().form_valid(form)



class BlogDetail(DetailView):
    model = Blogging
    template_name="app/blogdetail.html"
    context_object_name = "data"
