# -*- coding: utf-8 -*-

from project.settings.production import *

try:
    from project.settings.local import *
except:
    pass

