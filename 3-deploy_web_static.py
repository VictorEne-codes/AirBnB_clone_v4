#!/usr/bin/python3i
"""Fabric script (based on the file 1-pack_web_static.py)
"""
import time
import os
from fabric.api import *
from fabric.operations import run, put


env.hosts = ['54.146.14.173', '54.158.218.254']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


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

        timestamp = time.strftime("%Y%m%d%H%M%S")
        run(
            'sudo mkdir -p /data/web_static/releases/web_static_{:s}/'.
            format(timestamp))

        run('sudo tar xzvf /tmp/web_static_{:s}.tgz --directory\
            /data/web_static/releases/web_static_{:s}/'.
            format(timestamp, timestamp))

        run('sudo rm /tmp/web_static_{:s}.tgz'.format(timestamp))

        run('sudo mv /data/web_static/releases/web_static_{:s}/web_static/*\
            /data/web_static/releases/web_static_{}/'.format(
            timestamp, timestamp))

        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'.
            format(timestamp))

        run('sudo rm -rf /data/web_static/current')

        run('sudo ln -s /data/web_static/releases/web_static_{:s}/ \
            /data/web_static/current'.format(
                timestamp))
    except BaseException:
        return False
    return True

def deploy():
    """
    creates and distributes an archive to my web servers
    """
    created_archive = do_pack()
    if not created_archive:
        return False
    return do_deploy(created_archive)
