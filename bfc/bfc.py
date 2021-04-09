#
# ANTs N4BiasFieldCorrection ds ChRIS plugin app
#
# (c) 2021 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

from chrisapp.base import ChrisApp
from os import path
import os
from glob import glob
from concurrent.futures import ThreadPoolExecutor
import logging
import ants


Gstr_title = r"""
  ___   _   _ _____     _   _   ___  ______ _            ______ _      _     _   _____                          _   _
 / _ \ | \ | |_   _|   | \ | | /   | | ___ (_)           |  ___(_)    | |   | | /  __ \                        | | (_)
/ /_\ \|  \| | | |___  |  \| |/ /| | | |_/ /_  __ _ ___  | |_   _  ___| | __| | | /  \/ ___  _ __ _ __ ___  ___| |_ _  ___  _ __
|  _  || . ` | | / __| | . ` / /_| | | ___ \ |/ _` / __| |  _| | |/ _ \ |/ _` | | |    / _ \| '__| '__/ _ \/ __| __| |/ _ \| '_ \
| | | || |\  | | \__ \ | |\  \___  | | |_/ / | (_| \__ \ | |   | |  __/ | (_| | | \__/\ (_) | |  | | |  __/ (__| |_| | (_) | | | |
\_| |_/\_| \_/ \_/___/ \_| \_/   |_/ \____/|_|\__,_|___/ \_|   |_|\___|_|\__,_|  \____/\___/|_|  |_|  \___|\___|\__|_|\___/|_| |_|
"""


class ConvergenceInputParseError(Exception):
    pass


class N4BiasFieldCorrection(ChrisApp):
    """
    N4 is a variant of the popular N3 (nonparameteric nonuniform normalization) retrospective bias correction algorithm.
    """
    PACKAGE                 = 'ants_n4biasfieldcorrection'
    TITLE                   = 'ANTs N4 Bias Field Correction'
    CATEGORY                = 'Registration'
    TYPE                    = 'ds'
    ICON                    = ''   # url of an icon image
    MIN_NUMBER_OF_WORKERS   = 1    # Override with the minimum number of workers as int
    MAX_NUMBER_OF_WORKERS   = 1    # Override with the maximum number of workers as int
    MIN_CPU_LIMIT           = 1000 # Override with millicore value as int (1000 millicores == 1 CPU core)
    MIN_MEMORY_LIMIT        = 200  # Override with memory MegaByte (MB) limit as int
    MIN_GPU_LIMIT           = 0    # Override with the minimum number of GPUs as int
    MAX_GPU_LIMIT           = 0    # Override with the maximum number of GPUs as int

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        self.add_argument(
            '-p', '--inputPathFilter',
            dest='inputPathFilter',
            help='selection (glob) for which files to evaluate',
            default='*.nii',
            type=str,
            optional=True
        )
        self.add_argument(
            '-s', '--shrink-factor',
            dest='shrink_factor',
            type=int,
            default=3,
            optional=True
        )
        self.add_argument(
            '-c', '--convergence',
            dest='convergence',
            type=str,
            default='[400x400x400,0.00]',
            optional=True
        )

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """

        input_files = glob(path.join(options.inputdir, options.inputPathFilter))

        try:
            conv = self.parse_convergence(options.convergence)
        except ConvergenceInputParseError as e:
            print(e)
            sys.exit(1)

        print(Gstr_title, flush=True)
        logging.getLogger().setLevel(logging.INFO)

        def process(filename: str) -> str:
            img = ants.image_read(filename)
            img = ants.n4_bias_field_correction(img, shrink_factor=options.shrink_factor, convergence=conv)

            output = path.join(options.outputdir, path.basename(filename))
            img.to_file(output)
            logging.info(output)
            return output

        with ThreadPoolExecutor(max_workers=len(os.sched_getaffinity(0))) as pool:
            pool.map(process, input_files)

    @staticmethod
    def parse_convergence(input: str) -> dict:
        start = input.index('[')
        if start < 0:
            raise ConvergenceInputParseError("Missing '['")
        comma = input.index(',')
        if comma < 0:
            raise ConvergenceInputParseError("Missing ','")
        end = input.index(']')
        if end < 0:
            raise ConvergenceInputParseError("Missing ']'")

        return {
            'iters': [int(i) for i in input[start+1:comma].split('x')],
            'tol': float(input[comma+1:end])
        }

    def show_man_page(self):
        self.print_help()
