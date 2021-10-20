# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import argparse
from azureml.studio.core.logger import module_logger as logger
from azureml.studio.core.io.data_frame_directory import load_data_frame_from_directory, save_data_frame_to_directory

PACKAGE_NAME = 'azureml-designer-tutorial-modules'
VERSION = '0.0.2'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--input-path',
        help='The input directory.',
    )
    parser.add_argument(
        '--input-path-1',
        help='The input directory.',
    )
    parser.add_argument(
        '--input-path-2',
        help='The input directory.',
    )
    parser.add_argument(
        '--input-path-3',
        help='The input directory.',
    )
    parser.add_argument(
        '--input-path-4',
        help='The input directory.',
    )
    parser.add_argument(
        '--output-path',
        help='The output directory.',
    )

    args, _ = parser.parse_known_args()

    logger.info(f"Hello world from {PACKAGE_NAME} {VERSION}")

    logger.debug(f"Input path: {args.input_path}")
    data_frame_directory = load_data_frame_from_directory(args.input_path)

    logger.debug(f"Shape of loaded DataFrame: {data_frame_directory.data.shape}")

    logger.debug(f"Output path: {args.output_path}")
    save_data_frame_to_directory(args.output_path, data_frame_directory.data)
