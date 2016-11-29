# -*- coding: utf-8 -*-
import os,sys, pkgutil

__path__ = os.path.dirname(__file__)

for importer, package_name, _ in pkgutil.iter_modules([__path__]):
    full_package_name = '%s.%s' % (__path__, package_name)
    if full_package_name not in sys.modules:
        module = importer.find_module(package_name).load_module(full_package_name)