#!/usr/bin/python3
"""
Write a Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers, using the function do_deploy:

Prototype: def do_deploy(archive_path):
Returns False if the file at the path archive_path doesn’t exist
The script should take the following steps:
Upload the archive to the /tmp/ directory of the web server
Uncompress the archive to the folder
/data/web_static/releases/<archive filename without extension>
on the web server
Delete the archive from the web server
Delete the symbolic link /data/web_static/current from the web server
Create a new the symbolic link /data/web_static/current on the web server,
linked to the new version of your code
(/data/web_static/releases/<archive filename without extension>)
All remote commands must be executed on your both web servers
(using env.hosts = ['<IP web-01>', 'IP web-02'] variable in your script)
Returns True if all operations have been done correctly,
otherwise returns False
You must use this script to deploy it on your servers: xx-web-01 and xx-web-02
"""


from fabric.api import local, hosts, put, run, env
from os import path
from datetime import datetime

env.hosts = ['35.231.52.132', '3.91.244.49']


def do_pack():
    """Generates a .tgz archive from the contents
    of the web_static folder of your AirBnB Clone repo"""
    from os import mkdir, path

    now = datetime.now()
    filename = "web_static_{}.tgz".format(now.strftime("%Y%m%d%H%M%S"))
    filepath = "versions/{}".format(filename)

    try:
        mkdir('./versions')
    except FileExistsError:
        pass

    create_file = local("tar -cvzf {} web_static".format(filepath))
    if create_file.failed:
        return None
    return filepath


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""

    if not path.exists(archive_path):
        return False

    filename = archive_path.split('/')[1]
    dest_path = "/data/web_static/releases/{}/".format(filename.split('.')[0])

    try:
        put(archive_path, "/tmp/")
        run('mkdir -p {}'.format(dest_path))
        run('tar -xzf /tmp/{} -C {}'.format(filename, dest_path))
        run('rm /tmp/{}'.format(filename))
        run('mv {}web_static/* {}'.format(dest_path, dest_path))
        run('rm -rf {}web_static'.format(dest_path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(dest_path))
        return True
    except Exception:
        return False
