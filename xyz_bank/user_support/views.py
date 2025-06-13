from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from django.views.decorators.csrf import csrf_exempt

@login_required
def chat_view(request):
    chat, created = Chat.objects.get_or_create(user=request.user)
    return render(request, "chat.html", {"chat": chat})

@login_required
def send_message(request):
    if request.method == "POST":
        chat = get_object_or_404(Chat, user=request.user)
        content = request.POST.get("content", "")
        image = request.FILES.get("image")
        # Fix: If no content and no image, do not create a message
        if not content and not image:
            return JsonResponse({"status": "error", "msg": "No content or image."}, status=400)
        msg = Message.objects.create(chat=chat, sender=request.user, content=content, image=image)
        return JsonResponse({
            "status": "success",
            "image_url": msg.image.url if msg.image else None
        })
    return JsonResponse({"status": "error"}, status=400)

@login_required
def fetch_messages(request):
    is_admin = request.GET.get("admin") == "true"
    if is_admin and request.user.is_staff:
        chat_id = request.GET.get("chat_id")
        chat = get_object_or_404(Chat, id=chat_id)
    else:
        chat = get_object_or_404(Chat, user=request.user)

    messages = chat.messages.order_by("timestamp")
    data = []
    for msg in messages:
        data.append({
            "sender__username": msg.sender.username,
            "content": msg.content,
            "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "image_url": msg.image.url if msg.image else None,
        })
    return JsonResponse(data, safe=False)

@staff_member_required
def admin_chat_list(request):
    chats = Chat.objects.select_related("user").all()
    return render(request, "admin_chat.html", {"chats": chats})

@staff_member_required
def admin_chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    messages = chat.messages.order_by("timestamp")
    return render(request, "admin_chat_detail.html", {
    "chat": chat,
    "messages": messages
})


@staff_member_required
@require_http_methods(["POST"])
def admin_send_message(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    content = request.POST.get("content")
    if content:
        Message.objects.create(chat=chat, sender=request.user, content=content)
        return JsonResponse({"status": "sent"})
    return JsonResponse({"status": "error"}, status=400)
