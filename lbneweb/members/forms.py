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
        ('lbneiblist.txt', 'IB List (text)'),
        ('lbnephonelist.txt', 'Phone List (text)'),
        ('lbneauthor-main-authblk.tex', 'Main LaTeX file (authblk)'),
        ('lbneauthor-payload-authblk.tex', 'Body LaTeX (authblk)'),
        ('lbneauthor-main-revtex4.tex', 'Main LaTeX file (revtex4)'),
        ('lbneauthor-payload-revtex4.tex', 'Body LaTeX (revtex4)'),
        ('lbneauthor-main-authblk.pdf','PDF (authblk)'),
        ('lbneauthor-main-revtex4.pdf', 'PDF (revtex4)'),
        ('lbneauthors.xls', 'Spread sheet (xls)'),
        ])
    date = forms.DateField(
        label='Active date (YYYY-MM-DD)', required=False, initial = datetime.date.today,
    )
    

