
import os
import sys
import site
import uuid

from osnap import __application_name__, get_logger
import osnap.util

from jinja2 import Template


LOGGER = get_logger(__application_name__)


def make_pkgproj(application_name, reverse_dns_identifier, pkgproj_path):

    # find Packages project file
    template_file = 'template.pkgproj'
    locations = set()
    for d in site.getsitepackages():
        for r, _, fs in os.walk(d):
            for f in fs:
                if f == template_file:
                    p = os.path.join(r, f)
                    if osnap.util.is_windows():
                        p = p.lower()
                    locations.add(p)
    if len(locations) != 1:
        s = 'error : looking for exactly one %s : found %s' % (template_file, str(locations))
        print(s)
        sys.exit(s)
    template_file_path = locations.pop()

    LOGGER.debug('using %s as template', template_file_path)
    with open(template_file_path) as template_file:
        template = Template(template_file.read())
        with open(pkgproj_path, 'w') as f:
            f.write(template.render(application_name=application_name,
                                    reverse_dns_identifier=reverse_dns_identifier,
                                    uuid=str(uuid.uuid4())))
