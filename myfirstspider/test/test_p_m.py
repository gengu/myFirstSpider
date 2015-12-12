__author__ = 'genxiaogu'

import re

p = re.compile(r'^/cars/[\w\d]+/[\w\d]+$');
c = "/cars/brands/q7"

m = p.match(c)

if(m):
    print m.group()