from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse

from django.urls import reverse

# Create your views here.

from .forms import SearchForm, InstitutionForm

from .models import Project

from collections import Counter


def index(request):
    return render(request, 'viewer/index.html')




def projects(request):
# if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            query_filters = []
            for filter_key in form.cleaned_data:
                if form.cleaned_data[filter_key]:
                    query_filters.append(''+ filter_key + '=' + str(form.cleaned_data[filter_key]))
            
            query_string = '?' + '&'.join(query_filters)
            return redirect(reverse('projects_all') + query_string)
            
            
    # if a GET (or any other method) we'll create a blank form
    else:
        projects_list = Project.objects.all()
        if request.GET.get('year'):
             projects_list = projects_list.filter(year=request.GET.get('year'))
        if request.GET.get('country'):
            projects_list = projects_list.filter(location__icontains = request.GET.get('country'))
        if request.GET.get('medal'):
            projects_list = projects_list.filter(medal__icontains = request.GET.get('medal'))
        if request.GET.get('keyword'):
            projects_list = projects_list.filter(abstract__icontains= request.GET.get('keyword'))
        if request.GET.get('institution'):
            projects_list = projects_list.filter(institution__icontains= request.GET.get('institution'))
        if request.GET.get('team_name'):
            projects_list = projects_list.filter(team_name__icontains= request.GET.get('team_name'))
        if request.GET.get('awards'):
            projects_list = projects_list.exclude(awards = "-")
        if request.GET.get('nominations'):
            projects_list = projects_list.exclude(nominations = "-")
        if request.GET.get('section'):
            projects_list = projects_list.filter(section__icontains= request.GET.get('section'))
        if request.GET.get('track'):
            projects_list = projects_list.filter(track__icontains= request.GET.get('track'))
        form = SearchForm(initial=request.GET)
        context = {'projects_list': projects_list, 'form':form}

    #return render(request, 'viewer/projects.html', {'form': form},context)
    return render(request, 'viewer/projects.html', context)


def detail(request,project_pk):
    project = Project.objects.get(pk = project_pk)
    context = {'project': project}
    return render(request, 'viewer/detail.html', context)


def teams(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InstitutionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            query_filters = []
            for filter_key in form.cleaned_data:
                if form.cleaned_data[filter_key]:
                    query_filters.append(''+ filter_key + '=' + str(form.cleaned_data[filter_key]))
            
            query_string = '?' + '&'.join(query_filters)
            return redirect(reverse('teams_all') + query_string)
    
    else:        
        institution_list = Project.objects.values_list('institution', flat=True).distinct()
        participation = 1
        year = 2004
        projects_all = Project.objects.all()
        if request.GET.get('participations'):
            participation = int(request.GET.get('participations'))
        if request.GET.get('year'):
            year = int(request.GET.get('year'))
            projects_all = projects_all.filter(year__gte = year)
        if request.GET.get('location'):
            location = request.GET.get('location')
            projects_all = projects_all.filter(location__icontains = location)
        #countries_list = [x for x in countries_list]
        projects_list = {}
        for institution in institution_list:
            institution_dict = {}
            projects_institution = projects_all.filter(institution = institution).exclude(section = 'High School')
            if projects_institution.count() >= participation:
                params = ['location', 'section', 'medal','awards','nominations']
                for p in params:
                    projects_p = projects_institution.values_list(p, flat=True)
                    projects_p = [y for x in projects_p for y in x.split(',')]
                    projects_p = {x:projects_p.count(x) for x in projects_p}
                    institution_dict[p] = projects_p
                institution_dict['awards'].pop('-', None)
                institution_dict['awards'].pop('', None)
                institution_dict['awards']['total'] = len(institution_dict['awards'])
                institution_dict['nominations'].pop('-', None)
                institution_dict['nominations'].pop('', None)
                institution_dict['nominations']['total'] = len(institution_dict['nominations'])
                country =  max(institution_dict['location'], key=institution_dict['location'].get)
                institution_dict['location'] = {country:institution_dict['location'][country]}
                projects_list[institution] = institution_dict
            
    form = InstitutionForm(initial=request.GET)
    context = {'projects_list': projects_list, 'form':form}
    return render(request, 'viewer/teams.html', context)


def locations(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InstitutionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            query_filters = []
            for filter_key in form.cleaned_data:
                if form.cleaned_data[filter_key]:
                    query_filters.append(''+ filter_key + '=' + str(form.cleaned_data[filter_key]))
            
            query_string = '?' + '&'.join(query_filters)
            return redirect(reverse('locations_all') + query_string)

    else:        
        location_list = Project.objects.values_list('location', flat=True).distinct()
        participation = 1
        year = 2004
        projects_all = Project.objects.all()
        if request.GET.get('participations'):
            participation = int(request.GET.get('participations'))
        if request.GET.get('year'):
            year = int(request.GET.get('year'))
            projects_all = projects_all.filter(year__gte = year)
        if request.GET.get('location'):
            location = request.GET.get('location')
            projects_all = projects_all.filter(location__icontains = location)
        #countries_list = [x for x in countries_list]
        projects_list = {}
        for location in location_list:
            institution_dict = {}
            projects_institution = projects_all.filter(location = location).exclude(section = 'High School')
            if projects_institution.count() >= participation:
                params = ['section', 'medal','awards','nominations']
                for p in params:
                    projects_p = projects_institution.values_list(p, flat=True)
                    projects_p = [y for x in projects_p for y in x.split(',')]
                    projects_p = {x:projects_p.count(x) for x in projects_p}
                    institution_dict[p] = projects_p
                institution_dict['awards'].pop('-', None)
                institution_dict['awards'].pop('', None)
                institution_dict['awards']['total'] = len(institution_dict['awards'])
                institution_dict['nominations'].pop('-', None)
                institution_dict['nominations'].pop('', None)
                institution_dict['nominations']['total'] = len(institution_dict['nominations'])
                institution_dict['count'] = projects_institution.count()
                projects_list[location] = institution_dict
            
    form = InstitutionForm(initial=request.GET)
    context = {'projects_list': projects_list, 'form':form}
    return render(request, 'viewer/locations.html', context)