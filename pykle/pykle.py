#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from jinja2 import Template, FileSystemLoader, Environment
import imp

working_dir = os.getcwd()


def open_file(fname):
  with open(fname) as f:
      content = f.read()
      return content


def open_file_json(fname):
  return json.loads(open_file(fname))


def create_file(fname, contents):
  if not os.path.exists(os.path.dirname(fname)):
      os.makedirs(os.path.dirname(fname))
  with open(fname, "w") as f:
      f.write(contents)  


def find_files():
  file_list = []
  for root, dirs, files in os.walk(os.getcwd()):
    for f in files:
      dist = os.path.join(root, f)
      dist = dist.replace(working_dir, os.path.join(working_dir, "dist"))
      file_list.append({
        "file": os.path.join(root, f),
        "dist": dist,
      })
  return file_list

file_list = find_files()

for f in file_list:
  current_file = f["file"]
  if current_file.endswith("__run.py"):
    module = imp.load_source('module.name', current_file)
    module.do()

file_list = find_files()

# Build a helper dict.
file_dict = {}
for f in file_list:
  file_dict[f["file"]] = file    
  
for f in file_list:
  current_file = f["file"]
  dist_file = f["dist"]
  if "dist" in current_file:
    continue

  if "__skip" in current_file:
    print "Processing file: %s" % (current_file,)
    print "- Skipping."
    print "- Format: %s" % current_file_ext
    continue
  current_file_ext = current_file.split(".")[-1]

  if current_file_ext == "html" or current_file_ext == "fill_data":
    print "Processing file: %s" % (current_file,)
    print "- Format: %s" % current_file_ext    

  if "__copy" in current_file:
    contents = open_file(current_file)
    dist_file = dist_file.replace("__copy", "")
    create_file(dist_file, contents)
  elif current_file_ext == "html":
    env  = Environment(loader=FileSystemLoader(''))
    template = env.get_template(current_file.replace(working_dir+"/", ""))
    data = {}
    if (current_file + ".data") in file_dict:
      data = open_file_json(current_file + ".data")
    rendered = template.render(data=data)
    create_file(dist_file, rendered)
  elif current_file_ext == "fill_data":
    env  = Environment(loader=FileSystemLoader(''))
    djson_data = open_file_json(current_file)
    template = env.get_template(djson_data["template"])
    rendered = template.render(data=djson_data["data"])
    current_dir = "/".join(dist_file.split("/")[0:-1])
    create_file(current_dir+"/"+djson_data["dist"], rendered)