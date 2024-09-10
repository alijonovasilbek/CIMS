from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import connections, DatabaseError
from django.http import JsonResponse
from django.shortcuts import redirect
from functools import wraps

def company_code_check(company_code_value):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.company_code != company_code_value:
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator




@login_required()
@company_code_check("telegram")
def index1(request):
    if request.method == "POST" and request.POST.get('delete_user', False):
        user_id = request.POST.get('id')

        if user_id and user_id.isdigit():
            user_id = int(user_id)

            try:
                with connections['postgres1'].cursor() as cursor:
                    cursor.execute("DELETE FROM users WHERE id = %s", [user_id])
                return JsonResponse({'status': 'success', 'message': 'User deleted successfully!'})
            except DatabaseError as e:
                return JsonResponse({'status': 'error', 'message': 'Error deleting user: ' + str(e)})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid user ID.'})

    if request.method == "GET":
        with connections['postgres1'].cursor() as cursor:
            cursor.execute('SELECT * FROM users')
            user_list = cursor.fetchall()
            user=request.user
        return render(request, 'index1.html', {'user_list': user_list,'user': user})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})





