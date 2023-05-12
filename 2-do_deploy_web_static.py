#!/usr/bin/python3
"""
Write a Fabric script (based on the file 1-pack_web_static.py) that
distributes an archive to your web servers, using the function do_deploy
"""
import os
from fabric.api import env, put, sudo
from os.path import exists

env.user = 'ubuntu'
env.hosts = ['100.25.163.126', '52.3.240.73']


def do_deploy(archive_path):
    """Distribute an archive to the web servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')
        split_slash = archive_path.split("/")[-1]
        remove_tgz = split_slash.split(".")[0]
        directory = '/data/web_static/releases/'
        sudo('mkdir -p {}{}'.format(directory, remove_tgz))
        sudo('tar -xzf /tmp/{0}.tgz -C {1}{0}'.format(remove_tgz, directory))
        sudo('rm /tmp/{}.tgz'.format(remove_tgz))
        sudo('mv {0}{1}/web_static/* {0}{1}'.format(directory, remove_tgz))
        sudo('rm -rf {}{}/web_static'.format(directory, remove_tgz))
        sudo('rm -rf /data/web_static/current')
        sudo('ln -s {}{}\
                /data/web_static/current'.format(directory, remove_tgz))
        return True
    except Exception as e:
        return False
