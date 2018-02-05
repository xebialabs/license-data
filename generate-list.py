import json
from collections import defaultdict
from os import listdir
from os.path import isfile, isdir, join
import sys

lib_version = {}

if len(sys.argv) < 2 or not isdir(sys.argv[1]):
    print("Usage 'python %s <lib directory of XL tool>'" % sys.argv[0])
    exit(1)

for f in [f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1], f))]:
    lib_name = '.'.join(f.strip().split('.')[0:-1])
    parts = lib_name.strip().split('-')
    lib_version['-'.join(parts[0:-1])] = parts[-1]

art_ga = defaultdict(list)
ga_license = defaultdict(list)

with open('src/main/resources/license-data.json', 'r') as f:
    d = json.load(f)
    arts = d['artifacts']
    for k, v in arts.items():
        a = k.split(':')[1] if ':' in k else k
        if a in art_ga:
            print("WARN: DUPLICATE '%s' FOUND for %s and %s" % (a, k, art_ga[a]), file=sys.stderr)
        art_ga[a].append(k)
        ga_license[k].append(v["license"])
        if 'additionalLicenses' in v:
            additionalLicenses = v['additionalLicenses']
            if type(additionalLicenses) is list:
                for l in additionalLicenses:
                    ga_license[k].append(l)
            else:
                ga_license[k].append(additionalLicenses)

for lib in sorted(lib_version.keys()):
    version = lib_version[lib]
    group_artifacts = art_ga[lib]
    unknown = len(group_artifacts) > 1
    for ga in group_artifacts:
        licenses = ga_license[ga]
        s = ""
        if unknown:
            s += "POTENTIAL MATCH: "
        s += "%s: %s licensed under: %s" % (ga, version, ', '.join(licenses))
        print(s)
