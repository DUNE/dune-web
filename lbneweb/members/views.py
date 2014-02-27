from django.shortcuts import render
from django.views import generic
from django.db.models import Q

from members.models import Individual, Institution, Role
from members.forms import SearchMemberListForm, ExportFilesForm
import datetime

from util import last_name_order, datestring2date, collatemembers, active_members_filter

def home(request):
    return render(request, 'home.html', dict())
    

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
    member_list = Individual.objects.all().filter(id=0)
    # search form
    from members.forms import SearchMemberListForm
    if request.method == 'POST':
        form = SearchMemberListForm(request.POST) # bound form
        if form.is_valid():
            member_list = Individual.objects.select_related()
            if form.cleaned_data['is_collaborator']:
                member_list = member_list.filter(collaborator=True)
            if not form.cleaned_data['institution'] == 'All':
                member_list = member_list.filter(institution__short_name=form.cleaned_data['institution'])
            if not form.cleaned_data['role'] == 'All':
                member_list = member_list.filter(role__name=form.cleaned_data['role'])
            if form.cleaned_data['name']:
                name = form.cleaned_data['name']
                member_list = member_list.filter( Q(last_name__icontains=name) 
                    | Q(first_name__icontains=name))          

            thedate = form.cleaned_data['date']
            member_list = active_members_filter(member_list, thedate)
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



def export(request):
    # form for filename and date
    filename = 'export.html'
    thedate = None
    datestr = '(undated)'
    form = None
    if request.method == 'POST':
        form = ExportFilesForm(request.POST) # bound form
        if form.is_valid():
            thedate = form.cleaned_data['date']
            filename = form.cleaned_data['filename']
    # is there a better way?
    if request.method == 'GET' and request.GET.get('filename'):
        filename = request.GET.get('filename')
        thedate = request.GET.get('date')
        if thedate and thedate.lower() in ['now','today']:
            thedate = datetime.date.today()
        else:
            thedate = datestring2date(thedate)

    else:
        form = ExportFilesForm()

    if thedate:
        datestr = thedate.isoformat()

    individuals = Individual.objects.select_related()

    # all people actively associated with LBNE
    associates = sorted(active_members_filter(individuals, thedate), key=last_name_order)
    assoc_insts, assoc_number, assoc_inst_members = collatemembers(associates)

    # active and collaborators
    collaborators = [m for m in associates if m.collaborator]
    collab_insts, collab_number, collab_inst_members = collatemembers(collaborators)

    context = dict(associates = associates,
                   assoc_insts = assoc_insts, 
                   assoc_number = assoc_number, 
                   assoc_inst_members = assoc_inst_members,
                   collaborators = collaborators,
                   collab_insts = collab_insts, 
                   collab_number = collab_number, 
                   collab_inst_members = collab_inst_members,
                   date = datestr, 
                   form = form)

    if filename.endswith('.xls'):
        wb = members_to_xls(associates) # fixme: pass context
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
    
