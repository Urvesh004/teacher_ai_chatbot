from django.urls import path
from . import auth_view
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("login/", auth_view.login_view, name="login"),
    path("register/", auth_view.register_view, name="register"),
    path("logout/", auth_view.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("excel-upload/", views.upload_excel_view, name="upload_excel"),
    path("students/", views.student_list_view, name="student_list"),
    path("student/<int:student_id>/", views.student_detail_view, name="student_detail"),
    path('student/<int:id>/edit/', views.student_update_view, name='student_update'),
    path("chatbot/", views.chatbot_view, name="chatbot"),
]
