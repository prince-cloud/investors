from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import forms
from .models import Investor
from django.db.models import Q 
from django.http import HttpResponse
import csv
# Create your views here.

def login(request):
    return render(request, 'registration/login.html')


@login_required
def index(request):
    investors = Investor.objects.all()

    search_query = request.GET.get('q')
    search_type = request.GET.get('filter_type')
    if search_query and search_type:
        investors = investors.filter(
            Q(user__first_name = search_query) | Q(user__last_name = search_query)
        )
            
    return render(request, 'index.html',
    {
        'search_query':search_query,
        'investors':investors,
        'search_type': search_type,
    })

@login_required
def register(request):
    if request.method == 'POST':
        investor_user_form = forms.RegisterForm(data=request.POST, files=request.FILES)
        investor_form = forms.InvestorForm(data=request.POST, files=request.FILES)
        if investor_user_form.is_valid() and investor_form.is_valid():
            
            user = investor_user_form.save(commit=False)
            investor_user_profile = investor_form.save(commit=False)

            user.username = user.first_name + " " + user.last_name

            user.password = "password1234@?.112PRINCE.**"
            user.password2 = "password1234@?.112PRINCE.**"
            user.save()

            investor_user_profile.user = user
            investor_user_profile.save()

            messages.success(request, "User Successfully Added")
            return redirect("/")
        else:
            messages.warning(request, "invalid data entry. plase check and try again")
    else:
        investor_user_form = forms.RegisterForm()
        investor_form = forms.InvestorForm()
    
    return render(request, "registration/add_investor.html",{
        "investor_user_form": investor_user_form,
        "investor_form": investor_form,
    })


@login_required
def export_to_csv(request):
    filters_list = (
        ['zip_code', "Zip code"],
        ['country_to_invest', "Countries to Invest"],
        ['city', 'Cities'],
        ['state', 'States']
    )
    filter_by = request.GET.get('filter_by', '')
    filter_value = request.GET.get('filter_value', '')
    investors = None
    def filter(*args):
        investors = Investor.objects.all()
        if filter_by and filter_value:
            if filter_by == 'all':
                query = None
                for filter_type in filters_list:
                    if query:
                        query = query | Q(**{f'{filter_type[0]}__icontains': filter_value})
                    else:
                        query = Q(**{f'{filter_type[0]}__icontains': filter_value})

                investors = investors.filter(query)
            else:
                query = {f'{filter_by}__icontains': filter_value}
                investors = investors.filter(**query)
        return investors

    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)

    writer.writerow(['Full Name', 'Sex', 'Phone', 'email','Country To Invest', 'State', 'City', 'Zip Code'])

    for investor in filter().values_list('user__username', 'sex', 'phone', 'user__email', 'country_to_invest', 'state', 'city', 'zip_code'):
        writer.writerow(investor)

    response['Content-Disposition'] = 'attachment; filename="investors.csv"'
    return response
