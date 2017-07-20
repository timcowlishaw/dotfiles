import json
import os
import os.path as path
import distutils.dir_util as dir_util
import shutil
conf = None
with open("config.json") as f:
    conf = json.load(f)
mapping = conf["mapping"]
base_dir = path.dirname(path.realpath(__file__))

def link_files(files, base_path):
    for key in files:
        source = path.realpath(path.join(base_path, key))
        target = path.expanduser(files[key])
        if not (path.isfile(source) or path.isdir(source) or path.islink(source)):
            print("Source file: %s does not exist. Skipping" % source)
            continue
        if path.isfile(target) or path.isdir(target) or path.islink(target):
            print("Link target: %s already exists. Skipping" % target)
            continue
        dir_util.mkpath(path.dirname(target))
        os.symlink(source, target)

link_files(mapping, base_dir)

secrets_base_dir = path.realpath(path.expanduser(conf["secrets_dir"]))
if path.isdir(secrets_base_dir):
	secrets_conf = None
	with open(path.join(secrets_base_dir, "config.json")) as f:
	    secrets_conf = json.load(f)
	secrets_mapping = secrets_conf["mapping"]
	link_files(secrets_mapping, secrets_base_dir)


