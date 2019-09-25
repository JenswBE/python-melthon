"""This module glues all components together"""

import logging
import os
import sys
import distutils.dir_util as dir_util

from melthon.middleware import MWLoader
from melthon.middleware import MWStep
from melthon.data import get_yml_data
from melthon.template import render_templates


def main(middleware_dir, data_dir, templates_dir, static_dir, output_dir):
    # Add current directory to path.
    # This is required to be able to load the middlewares
    sys.path.append(os.getcwd())

    # Load middlewares
    mws = MWLoader(middleware_dir)

    # Initial context
    context = {
        'data': get_yml_data(data_dir)
    }

    # Delete and recreate output folder
    dir_util.remove_tree(output_dir)
    dir_util.mkpath(output_dir)

    # Execute middlewares "before" step
    context = mws.execute_chain(MWStep.BEFORE, context)
    logging.debug('Context after middlewares "before" step: %s', repr(context))

    # Render pages
    render_templates(templates_dir, output_dir, context)

    # Copy static assets to output
    dir_util.copy_tree(static_dir, output_dir, update=True)

    # Execute middlewares "after" step
    context = mws.execute_chain(MWStep.AFTER, context)
    logging.debug('Context after middlewares "after" step: %s', repr(context))
