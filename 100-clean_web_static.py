#!/usr/bin/python3
""" Function that deploys """
from fabric.api import *


env.hosts = ["54.146.14.173", "54.158.218.254"]
env.user = "ubuntu"


def do_clean(num=0):
    """
    cleans
    """

    num = int(num)

    if num == 0:
        nums = 1
    else:
        nums = num

    local('cd versions ; ls -t | head -n -{} | xargs rm -rf'.format(nums))
    path = '/data/web_static/releases'
    run('cd {} ; ls -t | head -n -{} | xargs rm -rf'.format(path, nums))
