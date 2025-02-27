#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of
   the web_static folder of your AirBnB Clone repo, using the function
   do_pack.
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """Archive all the contents of web_static folder"""
    # Create the versions directory if it doesn't exist
    local("mkdir -p versions")

    # Get the current date and time
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
