#!/usr/bin/python3
"""
Module that generates a .tgz from the contents of web_static
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
        function will return the archive path if archive
        has been correctly gernerated.
    """

    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archived_f_path = "versions/web_static_{}.tgz".format(date)
    t_gzip_archive = local("tar -cvzf {} web_static".format(archived_f_path))

    if t_gzip_archive.succeeded:
        return archived_f_path
    else:
        return None
