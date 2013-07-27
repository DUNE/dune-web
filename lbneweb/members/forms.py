from django import forms
from members.models import Institution, Role

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



