from django.shortcuts import render, redirect
from datetime import datetime, date
import calendar
from django.http import JsonResponse
from pyIslam.hijri import HijriDate
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from myapp.models import CustomUser

MONTHS = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
COMPLETED = 0
REMAINING = 0
MONTH = datetime.now().month
YEAR = datetime.now().year
HIJRI_DATE = ""
CURRENT_DATE = datetime.now().date

def get_calendar():
    cal = calendar.HTMLCalendar(calendar.SUNDAY)
    return cal.formatmonth(YEAR, MONTH, withyear=False)

context = {
        'title': 'Home Page',
        'month': MONTHS[MONTH-1],
        'year': YEAR,
        'completed': 'completed',
        'days_completed': COMPLETED,
        'remaining': 'remaining',
        'days_remaining': REMAINING,
        'sun': 'S',
        'mon': 'M',
        'tue': 'T',
        'wed': 'W',
        'thu': 'T',
        'fri': 'F',
        'sat': 'S',
        'calendar_days': get_calendar(),
        'fasted': 'fasted today',
        'log': 'make up a day',
        'prev_month': '<',
        'next_month': '>',
        'hijri_date': HIJRI_DATE,
        'reset_calendar': 'jump to today',
        'user_taken': '',
        'password_mismatch': '',
        'invalid_user': '',
    }

def update_user(request):
    current_user = request.user
    if current_user.is_authenticated:
        current_user.completed_days = COMPLETED
        current_user.remaining_days = REMAINING
        current_user.save()

def increase(request):
    global REMAINING
    REMAINING += 1
    update_user(request)
    return JsonResponse({
        'days_remaining': get_remaining(),
    })

def decrease(request):
    global COMPLETED, REMAINING
    COMPLETED += 1
    REMAINING -= 1
    if REMAINING < 0:
        REMAINING = 0
    update_user(request)
    return JsonResponse({
        'days_completed': get_completed(),
        'days_remaining': get_remaining(),
    })

def prev_month(request):
    global MONTH, YEAR
    MONTH -= 1
    if MONTH == 0:
        MONTH = 12
        YEAR = int(YEAR) - 1
    return JsonResponse({
        'month': get_month(),
        'year': get_year(),
        'calendar_days': get_calendar(),
    })

def next_month(request):
    global MONTH, YEAR
    MONTH += 1
    if MONTH == 13:
        MONTH = 1
        YEAR = int(YEAR) + 1
    return JsonResponse({
        'month': get_month(),
        'year': get_year(),
        'calendar_days': get_calendar(),
    })

def reset_cal(request):
    global MONTH, YEAR
    MONTH = datetime.now().month
    YEAR = datetime.now().year
    return JsonResponse({
        'month': get_month(),
        'year': get_year(),
        'calendar_days': get_calendar(),
    })

def get_date(request):
    return JsonResponse({
        'month':  MONTHS[MONTH-1],
        'year': YEAR,
    })

def get_month():
    return MONTHS[MONTH-1]

def get_year():
    return YEAR

def get_completed():
    return str(COMPLETED)

def get_remaining():
    return str(REMAINING)

def get_hijri(request):
    day = int(request.GET.get('day')) + 2
    month = MONTH
    year = YEAR
    
    if not day:
        HIJRI_DATE = None
        return JsonResponse({'error': 'Day parameter is missing'}, status=400)

    if month == 2 and (day == 28 or day == 29 or day == 30) and year == 2025:
        day -= 1
    
    dat = date(year, month, day)
    hijri = HijriDate.get_hijri(dat)
    hijri_date = hijri.format(lang=2)
    HIJRI_DATE = hijri_date
    return JsonResponse({
        'hijri_date': hijri_date,
    })

def user_login(request):
    global COMPLETED, REMAINING
    context['no_invalid'] = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            remember_me = 'remember' in request.POST
            if remember_me: 
                request.session.set_expiry(604800) 
            else:
                request.session.set_expiry(0) 

            COMPLETED = user.completed_days
            REMAINING = user.remaining_days
            context['days_completed'] = get_completed()
            context['days_remaining'] = get_remaining()
            return redirect(index)
        else:
            messages.error(request, "Invalid username or password.")
            context['invalid_user'] = "Invalid username or password, try again!"
            return render(request, 'login.html', context)
    return render(request, 'login.html')

def signup(request):
    context['password_mismatch'] = ""
    context['user_taken'] = ""
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            context['user_taken'] = "Username is taken, try again!"
            context['password_mismatch'] = ""
            return render(request, 'signup.html', context)
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            context['password_mismatch'] = "Passwords do not match, try again!"
            context['user_taken'] = ""
            return render(request, 'signup.html', context)

        try:
            user = CustomUser.objects.create_user(username=username, password=password1)
            user.save()
            login(request, user)

            remember_me = 'remember' in request.POST
            if remember_me: 
                request.session.set_expiry(604800) 
            else:
                request.session.set_expiry(0) 
            
            context['days_completed'] = get_completed()
            context['days_remaining'] = get_remaining()
            return redirect(index)
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, 'signup.html', context)
    
    return render(request, 'signup.html')

def user_logout(request):
    global COMPLETED, REMAINING

    COMPLETED = 0
    REMAINING = 0
    logout(request)
    request.session.set_expiry(0) 
    context['days_completed'] = get_completed()
    context['days_remaining'] = get_remaining()
    return redirect(index)
    

def index(request):
    global COMPLETED, REMAINING
    context['password_mismatch'] = ""
    context['user_taken'] = ""
    context['invalid_user'] = ""
    if request.user.is_authenticated:
        current_user = request.user
        COMPLETED = current_user.completed_days
        REMAINING = current_user.remaining_days
        context['days_completed'] = get_completed()
        context['days_remaining'] = get_remaining()
    return render(request, 'index.html', context)