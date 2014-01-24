from django import forms
from members.models import Institution, Role
import datetime
from django.contrib.admin.widgets import AdminDateWidget

# Helper Functions
def institution2choices():
    choices = (('All', 'All Institutions'), )
    for inst in Institution.objects.all():
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
        label='Active date (YYYY-MM-DD)', required=False, initial = datetime.date.today,
    )

class ExportFilesForm(forms.Form):
    filename = forms.ChoiceField(choices = [
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
    

