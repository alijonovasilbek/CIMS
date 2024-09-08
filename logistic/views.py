from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.http import JsonResponse

from django.utils import  timezone
from  django.db.models import  Sum
from django.shortcuts import redirect, render
from django.db import connections
from django.urls import reverse
from django.utils import timezone







def postgres_users(request):
    with connections['base1'].cursor() as cursor:
        cursor.execute("SELECT id, username, email, first_name, last_name FROM public.user")
        rows = cursor.fetchall()
    with connections['base2'].cursor() as cursor:
        cursor.execute("SELECT id, username, email, first_name, last_name FROM public.user")
        rows1 = cursor.fetchall()
        print(rows1)
    return render(request, 'postgres_users.html', {'users': rows,'info':rows1})





from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    if request.method == "POST":
        if 'add_exhibition' in request.POST:

            event_name = request.POST.get('event_name')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            city = request.POST.get('city')
            venue = request.POST.get('venue')
            host = request.POST.get('host')
            organizer = request.POST.get('organizer')
            sector = request.POST.get('sector')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            website = request.POST.get('website')


            with connections['postgres'].cursor() as cursor:
                cursor.execute("""
                    INSERT INTO exhibitions (event_name, start_date, end_date, city, venue, host, organizer, sector, phone, email, website)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, [event_name, start_date, end_date, city, venue, host, organizer, sector, phone, email, website])

        if 'delete_exhibition' in request.POST:
            exhibition_id = request.POST.get('id')


            if exhibition_id and exhibition_id.isdigit():
                exhibition_id = int(exhibition_id)

                with connections['postgres'].cursor() as cursor:
                    cursor.execute("DELETE FROM exhibitions WHERE id = %s", [exhibition_id])

        if 'delete_user' in request.POST:
            user_id = request.POST.get('id')
            if user_id and user_id.isdigit():
                user_id = int(user_id)
                try:
                    with connections['postgres'].cursor() as cursor:
                        cursor.execute("DELETE FROM todos WHERE sender_id = %s", [user_id])
                        cursor.execute("DELETE FROM users WHERE id = %s", [user_id])
                    return JsonResponse({'status': 'success'})
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': str(e)})



        return redirect(('index'))



    with connections['postgres'].cursor() as cursor:
        cursor.execute("SELECT * FROM todos WHERE receiver_id = %s", [request.user.id])
        todos = cursor.fetchall()


        cursor.execute("SELECT * FROM payments")
        payments = cursor.fetchall()


        today = timezone.now().date()
        cursor.execute("SELECT SUM(amount) FROM payments WHERE date = %s", [today])
        today_amount = cursor.fetchone()[0] or 0


        cursor.execute("SELECT SUM(amount) FROM payments")
        total_amount = cursor.fetchone()[0] or 0


        cursor.execute("SELECT * FROM exhibitions")
        exhibitions = cursor.fetchall()


        cursor.execute("SELECT * FROM users")
        user_list = cursor.fetchall()


    today_revenue = today_amount * 0.8
    total_revenue = total_amount * 0.8

    return render(request, 'index.html', {
        'user': request.user,
        'todos': todos,
        'payments': payments,
        'today_amount': today_amount,
        'today_revenue': today_revenue,
        'total_amount': total_amount,
        'total_revenue': total_revenue,
        'exhibitions': exhibitions,
        'users': user_list
    })


# def todo(request):
#     user = request.user
#     todos = Todo.objects.filter(reciver=user)
#
#     print(todos)
#     return render(request, 'todo.html', {'user': user, 'todos': todos})
#
#
# # def exb(request):
# #     user = request.user
# #     # todos = Todo.objects.filter(reciver=user)
# #     return render(request, 'exhibitions.html', {'user': user})
#
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
#
#
# def userlist(request):
#     user = request.user
#     # todos = Todo.objects.filter(reciver=user)
#     return render(request, 'users.html', {'user': user})
#
#
#
#
#
#
# def delete_exhibition(request):
#     exhibition_id = request.POST.get('id')
#     try:
#         exhibition = Exhibition.objects.get(id=exhibition_id)
#         exhibition.delete()
#     except Exhibition.DoesNotExist:
#         pass  # Agar ma'lumot topilmasa hech narsa qilma
#     return redirect('exb')  # Qayta yuklanadigan sahifa nomi
#
#
# def assign(request):
#     return  render(request,'assign.html')
#
# #
# # def users_page(request):
# #     return  render(request,'users.html')
# #
#
#
#
