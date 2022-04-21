from django.urls import path

from accounts.views import TeacherSignUpView, SchoolAdminSignUpView

urlpatterns = [
    path('teacher/sign-up/', TeacherSignUpView.as_view(), name="sign_up_teacher"),
    path('admin/sign-up/', SchoolAdminSignUpView.as_view(), name="sign_up_admin"),
]