#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time

import json
import requests
import subprocess
import functools

CRATE_URL = "https://crates.io/api/v1/crates/{crate_name}"
AUTHOR_URL = "https://crates.io/api/v1/crates/{crate_name}/{crate_ver}/authors"

def res_cmd(cmd):
  return subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True,universal_newlines=True).communicate()[0]

def get_license(crate_name):
    req = requests.get(CRATE_URL.format(crate_name=crate_name))
    if req.status_code == requests.codes.ok:
        try:
            j = req.json()
            crate = j['crate']
            license = crate['license']
            return license
        except KeyError:
            return None
        except ValueError:
            return None
    return None

def get_authors(crate_name,crate_ver):
    req = requests.get(AUTHOR_URL.format(crate_name=crate_name,crate_ver=crate_ver))
    if req.status_code == requests.codes.ok:
        try:
            j = req.json()
            meta = j['meta']
            names = meta['names']
            return names
        except KeyError:
            return None
        except ValueError:
            return None
    return None


def main():
    # get_license("libc")
    deps = json.loads(res_cmd("cargo metadata --no-deps"))
    deps = [d
            for p in deps['packages']
            for d in p['dependencies']]
    deps = [(p['name'],p['req'].lstrip('^')) for p in deps]
    print("| name | version | licence | authors |")
    print("|:-----|:--------|:--------|:--------|")
    deps.sort()
    for (c,v) in deps:
        url = "https://crates.io/crates/{}".format(c)
        licence = get_license(c)        
        authors = get_authors(c,v)
        if authors:
            authors = functools.reduce(lambda x,y : "{},{}".format(x,y),authors)
        else:
            authors = ""
        print("| [{name}]({url}) | {version} | {licence} | {authors} |".format(name=c,url=url,version=v,licence=licence,authors=authors))
    pass

if __name__ == '__main__':
    main()

