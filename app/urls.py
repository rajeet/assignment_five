from django.urls import path
from .views import signup_view, login_view, profile_view, LogoutView, editProfile, addpic, delete_profile, activate
from .crudview import CreateBlog, ManageBlog, DeleteBlog, UpdateBlog, BlogDetail
app_name = "account"

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("profile/", profile_view, name="profile"),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("create-blog/", CreateBlog.as_view(), name="create-blog"),
    path("manage-blog/", ManageBlog.as_view(), name="manage-blog"),
    path("<pk>/delete/", DeleteBlog.as_view(), name="deleteblog"),
    path("update-blog/<pk>", UpdateBlog.as_view(), name="updateblog"),
    path("editprofile/", editProfile, name="editprofile"),
    path("profilepic", addpic, name="profilepic"),
    path("deatilblog/<pk>", BlogDetail.as_view(), name="detailblog"),
    path("deleteprofile/", delete_profile ,name="deleteprofile"),
    path('activate/<uidb64>/<token>/',activate, name='activate'),  





]