from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def settings(request):
    return render(request, 'app-settings.html')

def error_404_view(request):
    return render(request, 'app-404.html')

@login_required
def change_profile_picture(request):
    if request.method == "POST" and request.FILES.get("profile_picture"):
        user = request.user
        user.profile_picture = request.FILES["profile_picture"]
        user.save()
        messages.success(request, "Profile picture updated successfully.")
        return redirect("settings")
    return render(request, "change_profile_picture.html")

@login_required
def change_password(request):
    if request.method == "POST":
        user = request.user
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        if not user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
        elif new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
        else:
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password changed successfully.")
            return redirect("settings")
    return render(request, "change_password.html")

@login_required
def change_email(request):
    if request.method == "POST":
        user = request.user
        new_email = request.POST.get("new_email")
        if new_email:
            user.email = new_email
            user.save()
            messages.success(request, "Email updated successfully.")
            return redirect("settings")
    return render(request, "change_email.html")

@login_required
def change_username(request):
    if request.method == "POST":
        user = request.user
        new_username = request.POST.get("new_username")
        if new_username:
            user.username = new_username
            user.save()
            messages.success(request, "Username updated successfully.")
            return redirect("settings")
    return render(request, "change_username.html")