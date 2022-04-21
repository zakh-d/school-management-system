from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import TeacherSignUpView, SchoolAdminSignUpView, ProfileView, login_view

urlpatterns = [
    path('teacher/sign-up/', TeacherSignUpView.as_view(), name="sign_up_teacher"),
    path('admin/sign-up/', SchoolAdminSignUpView.as_view(), name="sign_up_admin"),
    path('login/', login_view, name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('profile/', ProfileView.as_view(), name="profile")
]