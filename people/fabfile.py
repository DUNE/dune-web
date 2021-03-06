#!/usr/bin/env python

from fabric.api import env, hosts, local

env.hosts = ['dune.bnl.gov']
env.user = 'django'

@hosts('django@dune.bnl.gov')
def deploy(dryrun=False):
    '''deploy to production site'''
    from fabric.contrib.project import rsync_project
    
    if dryrun: 
        dry_run = ' --dry-run'
    else: 
        dry_run = ''
    
    exclude = ['.git/', '.svn/', '.htaccess', '*.pyc', '*~']
    exclude.append('*.sqlite3')
    rsync_project(
        remote_dir='/srv/www/django/',
        # remote_dir='~/test/',
        exclude=exclude,
        extra_opts='--update' + dry_run,
    )

@hosts('p-lbne-web@cdcvs.fnal.gov')
def docs():
    #from fabric.operations import put
    #(local_path, remote_path, use_sudo=False, mirror_local_mode=False, mode=None)
    #put('README.html', 'html/index.html')
    local('scp README.html p-lbne-web@cdcvs.fnal.gov:html/index.html')
    # fabric's ssh doesn't speak kerberos

def server():
    local('python manage.py runserver_plus')
