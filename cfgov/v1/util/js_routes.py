## Page Specific JS Routes ##
import os, shutil
from django.conf import settings
from . import util

MOLECULE = 'molecules'
ORGANISM = 'organisms'

LOOKUP_TABLE = {
    'Expandable': MOLECULE,
    'ExpandableGroup': ORGANISM
}


def create_route(data):
    type_found = False
    elements = data['elements']
    content = "'use strict';"

    dir_depth = data['slug'].count('/')
    path_depth = ''
    for x in range(0, dir_depth):
        path_depth += '../'

    for idx, element in enumerate(elements):
        class_name = util.to_camel_case(element)

        if class_name in LOOKUP_TABLE:
            type = LOOKUP_TABLE[class_name]
        else:
            type = None

        if type:
            type_found = True
            if type == MOLECULE:
                selector = 'm-'
            elif type == ORGANISM:
                selector = 'o-'

            selector += element.replace('_', '-')

            # Require module.
            content += 'var ' + class_name + '=require(\'' + path_depth + type + '/' + class_name + '\');'
            # Find all instances in page DOM.
            content += 'var a' + str(idx) + '=document.querySelectorAll( \'.' + selector + '\');'
            # Create variable for individual atomic element.
            content += 'var e;'
            # Loop through instances.
            content += 'for(var i=0,l=a' + str(idx) + '.length;i<l;i++) {'
            # Instantiate instance of atomic element.
            content += 'e=new ' + class_name + '(a' + str(idx) + '[i]);'
            # Initialize instance.
            content += 'e.init();'
            # Close loop.
            content += '}'

            # TODO: Remove after Testing
            content += 'console.log(\'Instantiated new ' + class_name + '\');'

    # Write to file path
    if type_found:
        file_path = settings.REPOSITORY_ROOT.child('cfgov', 'unprocessed', 'js', 'routes') \
                    + data['slug'] + 'index.js'

        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        with open(file_path, "w+") as f:
            f.write(content)
            return True

    return type_found


def delete_route(slug):
    path = settings.REPOSITORY_ROOT.child('cfgov', 'unprocessed', 'js', 'routes') \
           + slug

    if os.path.exists(os.path.dirname(path + 'index.js')):
        shutil.rmtree(path)
        return True

    return False
