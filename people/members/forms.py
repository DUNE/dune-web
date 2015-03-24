from django import forms
from members.models import Institution, Role
import datetime

from util import inst_name_order

# Helper Functions
def institution2choices():
    choices = (('All', 'All Institutions'), )
    inst_list = sorted(Institution.objects.all(), key=inst_name_order)
    for inst in inst_list:
        choices += ((inst.short_name, inst.full_name),)
    return choices

def role2choices():
    choices = (('All', 'All Roles'), )
    for role in Role.objects.all():
        choices += ((role.name, role.desc),)
    return choices

# Forms
class SearchMemberListForm(forms.Form):
    institution = forms.ChoiceField(
        label='Institution', required=False,
        choices=institution2choices(),
    )
    role = forms.ChoiceField(
        label='Role', required=False,
        choices=role2choices(),
    )
    is_collaborator = forms.BooleanField(
        label='Collaborator', required=False,
    )
    name = forms.CharField(
        label='Name', required=False,
    )
    date = forms.DateField(
        label='Active date (format: YYYY-MM-DD)', required=False, initial = datetime.date.today,
    )

class ExportFilesForm(forms.Form):
    filename = forms.ChoiceField(label = 'File type', choices = [
        ('iblist.txt', 'IB List (text)'),
        ('phonelist.txt', 'Phone List (text)'),
        ('author-main-authblk.tex', 'Main LaTeX file (authblk)'),
        ('author-payload-authblk.tex', 'Body LaTeX (authblk)'),
        ('author-main-revtex4.tex', 'Main LaTeX file (revtex4)'),
        ('author-payload-revtex4.tex', 'Body LaTeX (revtex4)'),
        ('author-main-authblk.pdf','PDF (authblk)'),
        ('author-main-revtex4.pdf', 'PDF (revtex4)'),
        ('authors.xls', 'Spread sheet (xls)'),
        ('author-arxiv.txt', 'arXiv list (txt)'),
        ])
    date = forms.DateField(
        label='Active date (YYYY-MM-DD)', required=False, initial = datetime.date.today,
    )
    

