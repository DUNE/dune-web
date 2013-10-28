from django.shortcuts import render
from django.views import generic
from django.db.models import Q

from members.models import Individual, Institution, Role
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
        
        
class CollaboratorView(generic.DetailView):
    model = Individual
    template_name = 'collaborator.html'
    context_object_name = 'member'


class InstitutionView(generic.DetailView):
    model = Institution
    template_name = 'institution.html'
    context_object_name = 'member'

class RoleView(generic.DetailView):
    model = Role
    template_name = 'role.html'
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

from django.http import HttpResponse
def xls_to_response(xls, fname):
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    xls.save(response)
    return response

from django.core import serializers
from collections import namedtuple
def serialize_members(member_list):
    '''
    Return a list of namedtuples of member info.
    '''
    serialized_members = serializers.serialize( "python", member_list)
    colnames = serialized_members[0]['fields'].keys() + ['country']
    inst_ind = colnames.index('institution')
    role_ind = colnames.index('role')
    MemberRow = namedtuple('MemberRow',colnames)
    ret = list()
    for irow, mem in enumerate(serialized_members):
        memobj = member_list[irow]
        row = list(mem['fields'].values())
        row[inst_ind] = memobj.institution.full_name
        row[role_ind] = ','.join([r.name for r in memobj.role.all()])
        row.append(memobj.institution.country)
        ret.append(MemberRow(*row))
    return ret
    
def members_to_xls(member_list):
    import xlwt
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Collaborators')

    members = serialize_members(member_list)
    for irow,mem in enumerate(members):
        if irow == 0:
            for icol, name in enumerate(mem._fields):
                ws.write(irow, icol, name)
        irow += 1
        for icol, value in enumerate(mem):
            #string = str(value)
            #ustring = string.encode('UTF-8')
            ustring = unicode(value)
            ws.write(irow, icol, ustring)
    return wb

def old_members_to_xls(member_list):
    import xlwt
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Collaborators')

    members = serializers.serialize( "python", member_list)
    for irow,mem in enumerate(members):
        if irow == 0:
            for icol, name in enumerate(mem['fields'].keys()):
                ws.write(irow, icol, name)
        irow += 1
        for icol, value in enumerate(mem['fields'].values()):
            #string = str(value)
            #ustring = string.encode('UTF-8')
            ustring = unicode(value)
            ws.write(irow, icol, ustring)
    return wb


import os
from latexer import process_latex
def latex_response(pdffile, context):
    #print pdffile
    texfile = os.path.splitext(pdffile)[0]+'.tex'
    pdf = process_latex(texfile, context)
    response = HttpResponse(mimetype="application/pdf")
    response['Content-Disposition'] = 'attachment; filename=%s' % pdffile
    response.write(pdf)
    return response


def inst_name_order(inst):
    name = inst.full_name.upper()
    for ignore in ['UNIV. OF', 'UNIVERSITY COLLEGE', 'COLLEGE OF']:
        ignore += ' '
        if name.startswith(ignore):
            return name[len(ignore):]
    return name
def last_name_order(indi):
    return (indi.last_name.lower(), indi.first_name.lower())

def export(request, filename):
    if not filename:
        filename = 'export.html'
    member_list = sorted(Individual.objects.select_related().filter(collaborator=True), key=last_name_order)
    inst_list = sorted(set([m.institution for m in member_list]), key=inst_name_order)
    context = dict(inst_list = inst_list, member_list = member_list)

    if filename.endswith('.xls'):
        wb = members_to_xls(member_list) # fixme: pass context
        return xls_to_response(wb, filename)

    if filename.endswith('.pdf'):
        return latex_response(filename, context)

    content_type = 'text/html'
    if filename.endswith('.tex'):
        content_type = 'text/plain; charset=utf-8'
    if filename.endswith('.txt'):
        content_type = 'text/plain; charset=utf-8'

    return render(request, filename, context,
                  content_type = content_type)
    
