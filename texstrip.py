"""
Sanitize LaTeX sources for submission. This script removes comments
(both inline ones (i.e., things after %) and comment environments),
copies the supplementary files to a new folder for a clean submission.

Usage:
  texstrip.py [options] <main> [<extra> ...]

Options:
  -h --help                 Show this screen.
  --version                 Show version.
  --comments
  --outdir=<outdir>         The output directory (relative to the main file) [default: stripped].
  -b,--build                   How to build.
  -c,--check                   Check the comments.
"""

from docopt import docopt
import shutil
from distutils import dir_util
from strip_comments import strip_comments_from_files
import logging
import os
import tempfile
import subprocess

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    args = docopt(__doc__, version='texstrip v0.0.1')

    main_file = args['<main>']
    logging.debug('using {} as the main file'.format(main_file))

    # extract target dir
    output_dir = os.path.join(os.getcwd(), args['--outdir'])
    os.makedirs(output_dir, exist_ok=True)

    logging.debug("using {} as the output dir".format(output_dir))

    # expand
    target_main_file = os.path.join(output_dir, os.path.basename(main_file))
    if target_main_file == main_file:
        raise Exception('target main file is the same as the source')

    cmd = 'latexpand --empty-comments -o {} {}'.format(os.path.join(output_dir, 'expanded.tex'), main_file)
    subprocess.run(cmd, shell=True, check=True)
    logging.info('Finished: {}'.format(cmd))

    if args['<extra>']:
        cp_cmd = "cp -rf {} {}".format(" ".join(args['<extra>']), output_dir)
        subprocess.run(cp_cmd, shell=True, check=True)
        logging.info("Finished: {}".format(cp_cmd))

    # 2nd step: strip comments
    strip_comments_from_files(os.path.join(output_dir, 'expanded.tex'),
                              os.path.join(output_dir, 'stripped.tex'))

    # 3rd step: copy
    shutil.copyfile(os.path.join(output_dir, 'stripped.tex'), target_main_file)

    if args['--build']:
        os.chdir(output_dir)
        build_cmd = "latexmk -pdf {}".format(target_main_file)
        subprocess.run(build_cmd, shell=True, check=True)




