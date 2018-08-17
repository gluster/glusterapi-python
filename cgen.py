#!/usr/bin/python

import argparse
import json
import re

HEADER = """
#!/usr/bin/python
# GENERATED FILE -- DO NOT EDIT


API_NAME = 'api_name'
METHOD = 'method'
NAME = 'name'
PATH = 'path'
PATH_VARS = 'path_vars'


class FakeClient:
    def do(self, method, path, data):
        print ('HTTP {} on {} with {}'.format(method, path, data))

""".strip()


def convert_name(name):
    """Convert a camel case name to a python style name."""
    out = []
    for c in name:
        if c == ' ':
            continue
        if len(out) == 0:
            out.append(c.lower())
        elif c.isupper():
            out.append('_')
            out.append(c.lower())
        else:
            out.append(c)
    return ''.join(out)


def fix_path(path):
    """Filter paths to remove unwanted character sequences"""
    # currently the only unusual character sequence that would
    # not work with python string templating is ':.*' in
    # VolfilesGet
    return path.replace(':.*', '')


def path_vars(path):
    """Return a list of path "variable names" extracted from the
    url path patterns."""
    out = []
    for m in re.finditer('\{([a-zA-Z0-9]+)\}', path):
        out.append(m.groups(1)[0])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        'SOURCE',
        help='source json containing enpoints description')
    cli = ap.parse_args()

    with open(cli.SOURCE) as fh:
        endpoints = json.load(fh)

    print (HEADER)
    print ('endpoints = {')
    for entry in endpoints:
        py_name = convert_name(entry['name'])
        path = fix_path(entry['path'])
        pvars = path_vars(path)
        print ('    "%s": {' % py_name)
        print ('        API_NAME: "%s",' % entry['name'])
        print ('        NAME: "%s",' % py_name)
        print ('        METHOD: "%s",' % entry['methods'])
        print ('        PATH: "%s",' % path)
        print ('        PATH_VARS: %s,' % repr(pvars))
        print ('    },')
    print ('}')
    for entry in endpoints:
        py_name = convert_name(entry['name'])
        path = fix_path(entry['path'])
        pvars = path_vars(path)
        print ('')
        print ('')
        if pvars:
            print ('def _%s(client, %s, data=None):' % (
                py_name, ', '.join(pvars)))
            fmtvars = ['%s=%s' % (v, v) for v in pvars]
            print ('    path = "%s".format(%s)' % (
                path, ', '.join(fmtvars)))
        else:
            print ('def _%s(client, data=None):' % (py_name))
            print ('    path = "%s"' % (path))
        print ('    return client.do("%s", path, data)' % (
            entry['methods'].upper()))

    return

if __name__ == '__main__':
    main()
