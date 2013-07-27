#!/usr/bin/env python
'''
Module to load the django database from text files.

The text files are as in DocDB 270 but fixed to give them more
consistent formatting and fix some typos.

'''
import sys
from members.models import Individual, Institution, Role
from datetime import datetime

def make_username(first,last):
    'Turn first and last name into single spaceless, StudlyCaps username'
    name = first+' '+last
    names = map(lambda x: x.capitalize(), name.split())
    return "".join(names)

def capitalize(word):
    words = word.split()
    out = []
    for w in words:
        if '/' in w:
            slashes = w.split('/')
            w = '/'.join(map(lambda x: x.capitalize(),slashes))
        elif '(' == w[0]:
            w = '('+w[1:].capitalize()
        else:
            w = w.capitalize()
        out.append(w)
    return " ".join(out)


def purge_db():
    Institution.objects.all().delete()
    Individual.objects.all().delete()
    return

    
def make_role_table():
    roles = {
        'F' : 'Faculty/Scientist',
        'P' : 'Postdoc',
        'E' : 'Engineer',
        'S' : 'Graduate Student',
        'IBR' : 'Institutional Board Representative',
    }
    for name, desc in roles.items():
        Role.objects.get_or_create(
            name = name,
            defaults = {'desc': desc},            
        )

class Data(object):


    def __init__(self):
        self.instlist = {
            # 'institution' : {
            #     'full_name' : '',
            #     'address' : ''
            # }
        }
        self.phonelist = {
            # 'institution' : [
            #     (first_name, last_name, role, email, phone),
            #     (...),
            # ]
        }
        self.iblist = {
            # 'institution' : [
            #     (first_name, last_name, joindate, is_IBR),
            #     (...),
            # ]
        }
        # combined member info
        self.memberlist = {
            # 'institution' : [
            #     {
            #         'first_name' : '',
            #         'last_name' : '',
            #         'role' : [],
            #         'email' : '',
            #         'phone' : '',
            #         'collaborator' : False,
            #         'begin_date' : '',
            #     },
            # ]
        }

    def load(self):
        import os;
        app_path = os.path.realpath(os.path.dirname(__file__))
        self.lbnephonelist(app_path + '/data/lbnephonelist.txt')
        self.lbneiblist(app_path + '/data/lbneiblist.txt')
        self.lbnememberlist()
        self.fill_institution_table()
        self.fill_indiviual_table()
    
    def fill_indiviual_table(self):
        roles = {}
        for role_obj in Role.objects.all():
            roles[role_obj.name] = role_obj
            
        for inst_name, people in self.memberlist.iteritems():
            inst_obj = Institution.objects.get(full_name = inst_name)
            for person in people:
                if person['begin_date']:
                    begin_date = person['begin_date'].split('/')
                    begin_date = datetime(
                        int(begin_date[0]), int(begin_date[1]), int(begin_date[2]))
                else:
                    begin_date = None
                
                defaults = {
                    'phone' : person['phone'],
                    'email' : person['email'],
                    'collaborator' : person['collaborator'],
                }
                if begin_date:
                    defaults['begin_date'] = begin_date
                                 
                person_obj, created = Individual.objects.get_or_create(
                    first_name = person['first_name'],
                    last_name = person['last_name'],
                    institution = inst_obj,
                    defaults = defaults,
                )
                if created:
                    print person['first_name'], person['last_name'], 'added' 
                    for role in person['role']:
                        role_obj = roles.get(role, '')
                        if role_obj:
                            person_obj.role.add(role_obj)
                    
    def fill_institution_table(self):
        for short_name, inst in self.instlist.iteritems():
            inst_obj, created = Institution.objects.get_or_create(
                short_name = short_name,
                defaults = {
                    'full_name' : inst['full_name'],
                    'address' : inst['address'],
                },            
            )
            if created: 
                print short_name, 'created'
                 
    def parse_phone_data(self,data):
        try:
            name,rest = data.split(' - ',1)
        except ValueError, err:
            print err
            print 'Failed to split phone data line "%s"'%data
            raise
        if ',' in name:
            try:
                last,first = name.split(',')
            except ValueError:
                print 'Failed to split phone data name: "%s"' % name
                raise
        else:
            try:
                first,last = name.split()
            except ValueError,err:
                print err
                print 'Failed to split name "%s"'%name
        chunks = rest.split()
        what = chunks[0]
        email = phone = ""
        try:
            email = chunks[1]
            phone = chunks[2]
        except IndexError:
            pass

        return (first.strip(),last.strip(),what.strip(),email.strip(),phone.strip())

    def parse_ib_data(self,data):
        isibr = False
        joindate = ""
        fields = data.split()
        #print 'parse_ib_data: |%s|'%'|'.join(fields)
        if "IBR" in fields[-1]:
            isibr = True
            fields.pop()
            data = " ".join(fields)
            pass
        if '/' in data:
            joindate = fields.pop()
            data = " ".join(fields)
        try:
            last,first = data.split(',')
        except ValueError:
            print 'Failed to parse IB data: "%s"'%data
            raise
        ret = (first.strip(),last.strip(),joindate.strip(),isibr)
        #print '|'.join(map(str,ret))
        return ret
        

    def spin_file(self,fp,data_parser):
        in_inst = False
        ret = {}
        inst = None
        for line in fp:
            #print 'line:',line
            stripped = line.strip()

            if not stripped:        # empty
                #print '\tleft inst'
                in_inst = False
                continue

            if line[0] not in [ ' ', '\t', '(']:
                inst_addr = stripped.split(';') 
                inst = capitalize(inst_addr[0])
                self.instlist.setdefault(inst, {
                    'full_name' : inst,
                    'address' : ','.join(inst_addr[1:]).lstrip(', '),
                })
                if not self.instlist[inst]['address']:
                    print 'WARNING: ', inst, ' is not in phonelist'
                    
                ret[inst] = []
                in_inst = True
                #print 'Institute:',inst
                continue
        
            if in_inst:
                data = data_parser(stripped)
                if not data: sys.exit(1)
                #print len(data),data
                ret[inst].append(data)
                continue
            continue
        return ret

    def lbnephonelist(self,filename):
        'Parse a list of contact info formated like DocDB 270, (with some cleanup)'
        if self.phonelist: return self.phonelist
        fp = open(filename)
        ret = self.spin_file(fp,self.parse_phone_data)
        self.phonelist = ret
        return ret

    def lbneiblist(self,filename):
        'Parse a list of collaborators formated like DocDB 270, (with some cleanup)'
        if self.iblist: return self.iblist
        fp = open(filename)
        ret = self.spin_file(fp,self.parse_ib_data)
        self.iblist = ret
        return ret

    def lbnememberlist(self):
        'combines iblist and phonelist to memeberlist'
        if self.memberlist: return self.memberlist
        for inst, people in self.phonelist.iteritems():
            # self.memberlist[inst] = []
            # print inst
            # print "======="
            ib_people = self.iblist.get(inst, '')
            ib_dict = {}
            for person in ib_people:
                ib_dict[(person[0], person[1])] = (person[2], person[3])
            for person in people:
                (first_name, last_name, role, email, phone) = person
                ib_person = ib_dict.get( (first_name, last_name) )
                if ib_person:
                    collaborator = True
                    begin_date = ib_person[0]
                    is_IBR = ib_person[1]
                else:
                    collaborator = False
                    begin_date = None
                    is_IBR = False
                # print first_name, last_name, collaborator, begin_date

                member = {
                    'first_name' : first_name,
                    'last_name' : last_name,
                    'role' : [role],
                    'email' : email,
                    'phone' : phone,
                    'collaborator' : collaborator,
                    'begin_date' : begin_date,
                }
                if is_IBR:
                    member['role'].insert(0, 'IBR')
                self.memberlist.setdefault(inst, []).append(member)
            # print

        return self.memberlist
        


if '__main__' == __name__:
    data = Data()
    # data.purge_db()
    # data.load()

            
        
