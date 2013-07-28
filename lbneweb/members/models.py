from django.db import models
from django.conf import settings
from datetime import datetime

'''
Example roles

Collaborator
Spokesperson (x2)
IB Representative
Executive board member
Physics Topic group leader
Project manager (l1, l2, l3, etc, WBS)
Career level (faculty, posdoc, engineer, student)
'''

class Role(models.Model):
    'A name + description'
    name = models.CharField(max_length=64)
    desc = models.CharField(max_length=1024)
        
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "%s/members/role/%d" % (settings.SITE_ROOT, self.id)

class Institution(models.Model):
    short_name = models.CharField(max_length=64)
    full_name =  models.CharField(max_length=1024)
    address =  models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['full_name', ]
        
    def __unicode__(self):
        return self.short_name
    
    def get_absolute_url(self):
        return "%s/members/institution/%d" % (settings.SITE_ROOT, self.id)

    def address_short(self):
        fields = [ x.strip() for x in self.address.split(',') ][-2:]
        return ', '.join(fields)        

class Individual(models.Model):
    'Information about an individual'

    # these duplicate what is in User, but want way to look up this record
    first_name = models.CharField('First Name',max_length=64)
    last_name = models.CharField('Last Name',max_length=64)
    email = models.EmailField()
    phone = models.CharField(max_length=64)
    collaborator = models.BooleanField()
    begin_date = models.DateField(max_length=50, default=datetime(2008,5,1))
    end_date = models.DateField(max_length=50, default=datetime(2038,5,1))
    institution = models.ForeignKey(Institution)
    role = models.ManyToManyField(Role)
    # docdb_id = models.IntegerField(blank=True,null=True)
    # user = models.OneToOneField(User,null=True,blank=True,default=None)
    class Meta:
        ordering = ['institution', 'last_name', 'first_name']
    
    def __unicode__(self):
        return self.first_name +' '+ self.last_name

    def get_absolute_url(self):
        return "%s/members/collaborator/%d" % (settings.SITE_ROOT, self.id)
        
    
    def full_name(self):
        return self.last_name + ', ' + self.first_name
    
    def first_name_initial(self):
        return self.first_name[0] + '.'
            
    def roles(self):
        rs = ''
        for obj in self.role.all():
            rs += obj.name + ', '
        return rs.rstrip(', ')  

    def roles_html(self):
        rs = []
        for obj in self.role.all():
            rs.append('<abbr title="' + obj.desc + '">' + obj.name + '</abbr>')
        return ', '.join(rs)
            
    def IBR(self):
        for obj in self.role.all():
            if obj.name == 'IBR':
                return 'IBR'
        return ''
    
    def career(self):
        for obj in self.role.all():
            if obj.name in ['F', 'P', 'E', 'S']:
                return obj.name
        return 'U'    
        
