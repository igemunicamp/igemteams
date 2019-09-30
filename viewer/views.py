from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse

from django.urls import reverse

# Create your views here.

from .forms import SearchForm

from .models import Project




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
            projects_list = projects_list.filter(location = request.GET.get('country'))
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
        form = SearchForm(initial=request.GET)
        context = {'projects_list': projects_list, 'form':form}

    #return render(request, 'viewer/projects.html', {'form': form},context)
    return render(request, 'viewer/projects.html', context)


def detail(request,project_pk):
    project = Project.objects.get(pk = project_pk)
    context = {'project': project}
    return render(request, 'viewer/detail.html', context)


