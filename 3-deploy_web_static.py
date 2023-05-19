#!/usr/bin/env python3
"""Fabric script that creates and distributes an archive to your web servers"""
import os
from fabric.api import env, put, sudo, local
from datetime import datetime

env.user = 'ubuntu'
env.hosts = ['100.25.163.126', '52.3.240.73']


def do_pack():
    """Archive all the contents of web_static folder"""
    local("mkdir -p versions")
    now = datetime.now()
    timeformat = now.strftime("%Y%m%d%H%M%S")

    # Create the name of the archive
    archive_name = "web_static_{}.tgz".format(timeformat)

    # Create the path of the archive
    archive_path = "versions/{}".format(archive_name)

    # Create the archive
    arch = local("tar -cvzf {} web_static".format(archive_path))

    # Return the path of the archive if it was created successfully
    if arch:
        return archive_path
    else:
        return None

def do_deploy(archive_path):
    """Distribute an archive to the web servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')
        split_slash = archive_path.split("/")[-1]
        remove_tgz= split_slash.split(".")[0]
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

def deploy():
    """Creates and distributes an archive to your web servers"""
    arch_file = do_pack()
    if arch_file is None:
        return False
    return do_deploy(arch_file)
