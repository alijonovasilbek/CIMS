
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


from .forms import UserRegisterForm, LoginForm
from .models import User, Todo,Payments,Exhibition


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(email, password)  # Tekshirish uchun chop qilish (bu ishlab chiqishda yordam beradi)
            user = authenticate(request, username=email, password=password)
            print(user)  # Tekshirish uchun chop qilish

            if user is not None:
                login(request, user, backend='main.auth_backends.EmailBackend')

                # Userning company_code asosida yo'naltirish
                if user.company_code == "telegram":
                    return redirect('index1')  # `redirect` qaytarilishi kerak
                elif user.company_code == 'site':
                    return redirect('index')   # `redirect` qaytarilishi kerak
                else:
                    return redirect('default_index')  # Har qanday boshqa company_code uchun default yo'nalish
            else:
                # Agar autentifikatsiya muvaffaqiyatsiz bo'lsa, qayta formani render qilish
                return render(request, 'signin.html', {'form': form, 'invalid': True})
    else:
        form = LoginForm()

    return render(request, 'signin.html', {'form': form, 'invalid': False})

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})

from django.utils import  timezone
from  django.db.models import  Sum


# @login_required
# def index(request):
#     user = request.user
#     todos = Todo.objects.filter(reciver=user)
#     payments = Payments.objects.all()
#     today = timezone.now().date()
#     payments_today = Payments.objects.filter(date=today)
#     payments_total=Payments.objects.all()
#
#     today_amount = payments_today.aggregate(total_amount=Sum('amount')).get('total_amount', 0)
#     payments_total=payments_total.aggregate(total_amount=Sum('amount')).get('total_amount', 0)
#
#
#     today_revenue=today_amount*0.8
#     total_revenue=payments_total*0.8
#
#     return render(request, 'index.html', {'user': user, 'payments': payments,
#                                           'today_amount': today_amount,'today_revenue': today_revenue,'payments_total':payments_total,
#                                           'total_revenue':total_revenue,'todos':todos})

def todo(request):
    user = request.user
    todos = Todo.objects.filter(reciver=user)

    print(todos)
    return render(request, 'todo.html', {'user': user, 'todos': todos})


# def exb(request):
#     user = request.user
#     # todos = Todo.objects.filter(reciver=user)
#     return render(request, 'exhibitions.html', {'user': user})

# from django.shortcuts import render, redirect
# from .models import Exhibition
#
# def exb(request):
#     if request.method == 'POST':
#         Exhibition.objects.create(
#             event_name=request.POST.get('event_name'),
#             start_date=request.POST.get('start_date'),
#             end_date=request.POST.get('end_date'),
#             city=request.POST.get('city'),
#             venue=request.POST.get('venue'),
#             host=request.POST.get('host'),
#             organizer=request.POST.get('organizer'),
#             sector=request.POST.get('sector'),
#             phone=request.POST.get('phone'),
#             email=request.POST.get('email'),
#             website=request.POST.get('website')
#         )
#         return redirect('exb')
#
#     exhibitions = Exhibition.objects.all()
#     return render(request, 'exhibitions.html', {'exhibitions': exhibitions})
#


def userlist(request):
    user = request.user
    # todos = Todo.objects.filter(reciver=user)
    return render(request, 'users.html', {'user': user})





#
# def delete_exhibition(request):
#     exhibition_id = request.POST.get('id')
#     try:
#         exhibition = Exhibition.objects.get(id=exhibition_id)
#         exhibition.delete()
#     except Exhibition.DoesNotExist:
#         pass  # Agar ma'lumot topilmasa hech narsa qilma
#     return redirect('exb')  # Qayta yuklanadigan sahifa nomi


def assign(request):
   return  render(request,'assign.html')

#
# def users_page(request):
#     return  render(request,'users.html')
#



