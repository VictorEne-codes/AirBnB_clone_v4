#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py)
"""
import time
import os
from fabric.api import *
from fabric.operations import run, put


env.hosts = ['54.146.14.173', '54.158.218.254'] 
env.user = 'ubuntu'


def do_pack():
    """generates a .tgz archive"""
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{:s}.tgz web_static/".
              format(time.strftime("%Y%m%d%H%M%S")))
        return "versions/web_static_{:s}.tgz".\
            format(time.strftime("%Y%m%d%H%M%S"))
    except BaseException:
        return None


def do_deploy(archive_path):
    """distributes an archive to my web servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')

        # Create a target dir without the file extension
        timestamp = time.strftime("%Y%m%d%H%M%S")
        run(
            'sudo mkdir -p /data/web_static/releases/web_static_{:s}/'.
            format(timestamp))

        # will uncompress archive to the targed dir
        run('sudo tar xzvf /tmp/web_static_{:s}.tgz --directory\
            /data/web_static/releases/web_static_{:s}/'.
            format(timestamp, timestamp))

        # deletes archive from the web server
        run('sudo rm /tmp/web_static_{:s}.tgz'.format(timestamp))

        # moves the contents into host web_static
        run('sudo mv /data/web_static/releases/web_static_{:s}/web_static/*\
            /data/web_static/releases/web_static_{}/'.format(
            timestamp, timestamp))

        # will remove irrelevant web_static dir
        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'.
            format(timestamp))

        # will delete the initial symbolic link from the web server
        run('sudo rm -rf /data/web_static/current')

        # a new symbolic link
        run('sudo ln -s /data/web_static/releases/web_static_{:s}/ \
            /data/web_static/current'.format(
            timestamp))
    except BaseException:
        return False
    # if all that succeeded, return True
    return True
