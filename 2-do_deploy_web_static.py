#!/usr/bin/python3
"""
Write a Fabric script (based on the file 1-pack_web_static.py) that
distributes an archive to your web servers, using the function do_deploy
"""
import os
from fabric.api import env, put, run, sudo
from os.path import exists

env.user = 'ubuntu'
env.hosts = ['100.25.163.126', '52.3.240.73']


def do_deploy(archive_path):
    """Distribute an archive to the web servers"""
    if not exists(archive_path):
        return False
    try:
        archive_filename = archive_path.split("/")[-1]
        archive_basename = archive_filename.split(".")[0]
        folders = '/data/web_static/releases/'
        put(archive_path, '/tmp/')
        sudo("mkdir -p folders{}/".format(archive_basename))
        sudo("tar -xzf /tmp/{} -C folders{}/".format(
            archive_filename, archive_basename))
        sudo("rm /tmp/{}".format(archive_filename))
        sudo("mv folders{0}/web_static/* folders{0}/".format(archive_basename))
        sudo("rm -rf folders{}/web_static".format(archive_basename))
        sudo("rm -rf /data/web_static/current")
        sudo("ln -s folders{}/ /data/web_static/current".format(
            archive_basename))
        return True
    except Exception as e:
        return False
