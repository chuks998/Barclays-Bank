from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import activate
from .tokens import account_activation_token
from django.contrib.auth.decorators import login_required
from transactions.models import Transaction
from django.db.models import Sum, Q


# Registration & Email Verification

User = get_user_model()

def register(request):
    if request.method == "POST":
        # Retrieve fields safely and strip extra whitespace
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        country = request.POST.get('country', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        
        # Check for required fields
        if not (name and email and country and username and password and password2):
            return HttpResponse("Missing required fields.", status=400)
        
        # Verify passwords match
        if password != password2:
            return HttpResponse("Passwords do not match.", status=400)
        
        user = User.objects.create_user(name=name, email=email, country=country, username=username, password=password)
        # Immediately activate user (remove email verification)
        user.is_active = True
        user.save()
        
        return redirect('user_login')

    return render(request, "app-register.html")


# LOGIN VIEW

def user_login(request):
    if request.method == "POST":
        login_input = request.POST['login_input']
        password = request.POST['password']
        
        try:
            user = User.objects.get(Q(email=login_input) | Q(username=login_input))
        except User.MultipleObjectsReturned:
            user = User.objects.filter(Q(email=login_input) | Q(username=login_input)).first()
        except User.DoesNotExist:
            user = None

        if user and user.check_password(password):
            user.backend = "authentifications.custom_backend.EmailOrUsernameBackend"
            login(request, user, backend=user.backend)
            return redirect('dashboard')  # Update with your actual dashboard URL name
        else:
            return render(request, 'app-login.html', {'error': 'Invalid credentials'})

    return render(request, "app-login.html")


#  Password Reset Views


def password_reset_request(request):
    if request.method == "POST":
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user:
            subject = "Password Reset Request"
            message = render_to_string('authentication/password_reset_email.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail(subject, message, 'noreply@xyzbank.com', [user.email])
        return HttpResponse("Check your email for a password reset link.")

    return render(request, "authentication/password_reset_form.html")

# To handle language and currency settings

def set_language(request):
    """Set user-selected language and store it in session."""
    if request.method == "POST":
        lang = request.POST.get("language")
        activate(lang)
        request.session["django_language"] = lang
        return redirect(request.META.get("HTTP_REFERER", "/"))

def set_currency(request):
    """Set user-selected currency and store it in session."""
    if request.method == "POST":
        request.session["currency"] = request.POST["currency"]
        return redirect(request.META.get("HTTP_REFERER", "/"))


# To handle user authentication for dashboard access
@login_required
def dashboard(request):
    user = request.user

    # Fetch user's balance
    balance = user.balance  

    # Get total credit (Money received)
    total_credit = Transaction.objects.filter(receiver=user).aggregate(Sum('amount'))['amount__sum'] or 0

    # Get total debit (Money sent)
    total_debit = Transaction.objects.filter(sender=user).aggregate(Sum('amount'))['amount__sum'] or 0

    # Fetch recent 5 transactions (both sent & received)
    transactions = Transaction.objects.filter(sender=user) | Transaction.objects.filter(receiver=user)
    transactions = transactions.order_by("-created_at")[:5]  # Show only the last 5 transactions

    return render(request, 'dashboard.html', {
        'balance': balance, 
        'transactions': transactions,
        'total_credit': total_credit,
        'total_debit': total_debit
    })