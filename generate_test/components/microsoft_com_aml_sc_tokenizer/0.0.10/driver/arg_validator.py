# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
""" The module provides features to validate arguments."""
import os
import re
import traceback

from score_module import ScoreModule
from logger import get_user_error_logger


class ArgValidator:
    """ The class validates arguments used in the driver."""

    def __init__(self, args):
        self.args = args

    def validate(self):
        """ Validate the args."""
        if self.args.input_tabular_datasets and (self.args.input_file_datasets or self.args.inputs):
            raise Exception("Cannot mix FileDatasets and TabularDatasets as inputs")

        if not self.args.input_tabular_datasets and not self.args.input_file_datasets and not self.args.inputs:
            raise Exception("Missing inputs. The inputs should either be FileDatasets or TabularDatasets")

        self.check_pathname_valid(self.args.output, self.args.append_row_file_name)

        try:
            module = ScoreModule(self.args.scoring_module_name)
            module.import_module()  # Try to import the module to validate it.
        except BaseException as exc:
            e_logger = get_user_error_logger()
            e_logger.error(f"Entry script validation failed for {exc}. Details {traceback.format_exc()}")
            raise exc

    def check_pathname_valid(self, folder, filename):
        """ Validate filename argument"""
        full_path = os.path.join(os.path.join(folder, filename))
        regexp = re.compile(r'[~"#%&*:<>?/\\{|}]+')
        if len(full_path) > 260 or regexp.search(filename):
            raise ValueError(
                f"append_row_file_name must be a valid UNIX file name. The path {full_path} is either too long or contains invalid characters"
            )
