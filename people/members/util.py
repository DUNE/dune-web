#!/usr/bin/env python
'''
Some utility functions
'''

import datetime
from collections import defaultdict

def inst_name_order(inst):
    'Return a string used for ordering institutions.'
    if inst.sort_name:
        return inst.sort_name
    name = inst.full_name.upper()
    for ignore in ['UNIV. OF', 'UNIVERSITY COLLEGE', 'COLLEGE OF']:
        ignore += ' '
        if name.startswith(ignore):
            return name[len(ignore):]
    return name
def last_name_order(indi):
    return (indi.last_name.lower(), indi.first_name.lower())


def datestring2date(string):
    'Return a datetime.date object by parsing the date string.'
    try:
        ret = datetime.datetime.strptime(string, '%Y-%m-%d')
    except ValueError:
        return None
    return ret.date()

def collatemembers(members):
    '''Return three collections from the given members:

    inst_list : a sorted list of the members' institutions

    number : a dictionary mapping an institution ID to a number starting from 1

    inst_members : a sorted list of (inst,mems) pairs where mems are
    sorted lists of members in the institution.

    '''
    inst_list = sorted(set([m.institution for m in members]), key=inst_name_order)
    number = dict()
    for count,inst in enumerate(inst_list):
        number[inst.id] = count+1
    inst_members = []
    for inst in inst_list:
        im = []
        for m in inst.individual_set.all():
            if m in members:
               im.append(m)
        if not im:
            continue
        inst_members.append((inst,im))
    return (inst_list, number, inst_members)

def country_counts(insts, thedate):
    '''Return ordered list of tuples:
    (country, sequence of institution, sequence of individuals)
    '''
    country_insts = defaultdict(list)
    country_indiv = defaultdict(list)
    for inst in insts:
        country_insts[inst.country].append(inst)
        country_indiv[inst.country] += inst.get_active_members(thedate)
    ret = list()
    for c in list(set(country_insts.keys() + country_indiv.keys())):
        ret.append((c, country_insts[c], country_indiv[c]))
    return ret
    

def active_members_filter(query, date = None):
    'Given a query of members, return a filtered one that only has active members'
    keep_ids = [m.id for m in query if m.is_active(date)]
    return query.filter(id__in = keep_ids)

