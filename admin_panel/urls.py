from django.urls import path
from . import views

app_name = "admin_panel"

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("excel-sheets/", views.excel_sheet_list_view, name="excel_sheets"),
    # BUG FIX: was upload_id in urls.py but excel_id in view — now consistent: excel_id
    path("excel-sheets/delete/<int:excel_id>/", views.delete_excel_view, name="delete_excel"),
    path("users/", views.user_list_view, name="users"),
    path("users/edit/<int:user_id>/", views.edit_user_view, name="edit_user"),
    path("users/delete/<int:user_id>/", views.delete_user_view, name="delete_user"),
    path("user-logs/", views.user_logs_view, name="user_logs"),
    path("chatbot-logs/", views.chatbot_logs_view, name="chatbot_logs"),
    path("settings/", views.settings_view, name="settings"),
]
