from django.shortcuts import render
from django.views import generic
from django.db.models import Q

from django.http import HttpResponseRedirect


from members.models import Individual
from members.forms import SearchMemberListForm


class IndexView(generic.ListView):
    model = Individual
    template_name = 'index_list.html'
    context_object_name = 'data'

    def get_queryset(self):
        'Return what this lists'
        member_list = Individual.objects.select_related().filter(collaborator=True)

        return dict(member_list = member_list,
                    count = len(member_list),
                    instCount = len(set(member_list.values_list('institution'))),
                    institution = None, # later
                    form = None,        # later
                )
        
        
class DetailView(generic.DetailView):
    model = Individual
    template_name = 'detail.html'
    context_object_name = 'member'


def search(request):
    member_list = Individual.objects.select_related().filter(collaborator=True)
    
    # search form
    from members.forms import SearchMemberListForm
    if request.method == 'POST':
        form = SearchMemberListForm(request.POST) # bound form
        if form.is_valid():
            if not form.cleaned_data['institution'] == 'All':
                member_list = member_list.filter(institution__short_name=form.cleaned_data['institution'])
            if not form.cleaned_data['role'] == 'All':
                member_list = member_list.filter(role__name=form.cleaned_data['role'])
            if form.cleaned_data['name']:
                name = form.cleaned_data['name']
                member_list = member_list.filter( Q(last_name__icontains=name) 
                    | Q(first_name__icontains=name))          
        else:
            member_list = member_list.filter(id=0) # hack, no match

    else:
        form = SearchMemberListForm() # unbound form

    return render(request, 'index_list.html', 
                  dict(form=form, institution = None,
                       member_list = member_list,
                       instCount = len(set(member_list.values_list('institution'))),
                       count = member_list.count(),))


class SearchView(generic.edit.FormView):
    template_name = 'search.html'
    form_class = SearchMemberListForm
    success_url = '/'
    
    def form_valid(self, form):
        return super(SearchView, self).form_valid(form)
