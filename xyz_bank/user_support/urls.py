from django.urls import path
from . import views

urlpatterns = [
    path("chat/", views.chat_view, name="chat"),
    path("send_message/", views.send_message, name="send_message"),
    path("fetch_messages/", views.fetch_messages, name="fetch_messages"),
    path("admin/chats/", views.admin_chat_list, name="admin_chat_list"),
    path("admin/chats/<int:chat_id>/", views.admin_chat_detail, name="admin_chat_detail"),
    path("admin/chats/<int:chat_id>/send/", views.admin_send_message, name="admin_send_message"),
]
