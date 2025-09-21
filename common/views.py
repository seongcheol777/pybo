from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # authenticate 없이도 save()가 돌려준 user로 로그인 가능
            login(request, user)
            return redirect('index')
        # 실패: 에러가 담긴 form을 그대로 렌더
        return render(request, 'common/signup.html', {'form': form})
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

# Create your views here.
