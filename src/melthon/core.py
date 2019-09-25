"""This module glues all components together"""

import logging
import os
import sys
import distutils.dir_util as dir_util
from pathlib import Path

from melthon.middleware import MWLoader
from melthon.middleware import MWStep
from melthon.data import get_yml_data
from melthon.template import render_templates


def clean(output_path: Path):
    """Deletes generated and temporary files"""
    if output_path.is_dir():
        dir_util.remove_tree(output_path)
        logging.debug('Removed output folder "%s"', output_path)
    else:
        logging.info('Output folder "%s" not found. Nothing deleted.', output_path)


def build(templates_path: Path, static_path: Path, data_path: Path, middleware_path: Path, output_path: Path):
    # Check if mandatory templates_path exist
    if not templates_path.is_dir():
        logging.error('Configured templates folder "%s" doesn\'t exist', templates_path)
        exit(1)

    # Initial context
    context = {
        'data': get_yml_data(data_path)
    }

    # Load middlewares
    mws = None
    if middleware_path.is_dir():
        # Add current directory to path.
        # This is required to be able to load the middlewares
        sys.path.append(os.getcwd())

        # Load middlewares
        mws = MWLoader(middleware_path)
    else:
        logging.warning('Configured middleware folder "%s" doesn\'t exist. Skipping middleware execution.', middleware_path)

    # Delete and recreate output folder
    clean(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    # Execute middlewares "before" step
    if mws is not None:
        context = mws.execute_chain(MWStep.BEFORE, context)
        logging.debug('Context after middlewares "before" step: %s', repr(context))

    # Render pages
    render_templates(templates_path, output_path, context)

    # Copy static assets to output
    if static_path.is_dir():
        dir_util.copy_tree(static_path, output_path, update=True)
    else:
        logging.warning('Configured static folder "%s" doesn\'t exist. Skipping copy to output.', static_path)

    # Execute middlewares "after" step
    if mws is not None:
        context = mws.execute_chain(MWStep.AFTER, context)
        logging.debug('Context after middlewares "after" step: %s', repr(context))
