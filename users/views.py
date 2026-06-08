from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '註冊成功,請使用新帳號登入!')
            return redirect('users:login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})
