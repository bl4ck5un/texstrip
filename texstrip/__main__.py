"""
texstrip sanitizes LaTeX sources for submission.

Usage:
  texstrip [options] <main> [<extra> ...]

Options:
  -h --help                 Show this screen.
  --version                 Show version.
  --outdir=<outdir>         The output directory (relative to the main file) [default: stripped].
  --keep                    Keep intermediate files for debugging.
  -b,--build                Build after stripping.
  -v,--verbose              Print debug messages.
"""

import logging
import os
import shutil
import subprocess

import chromalog
from docopt import docopt
from strip_comments import strip_comments_from_files


def check_exe_available(exe):
    if shutil.which(exe) is None:
        raise Exception("{} not available".format(exe))


def main():
    # check dependencies are available
    check_exe_available('latexpand')

    # setup docopt and logging
    args = docopt(__doc__, version='texstrip v0.0.2')

    logger_format = '%(asctime)s [%(levelname)s] - %(message)s'
    chromalog.basicConfig(level=logging.DEBUG if args['--verbose'] else logging.INFO, format=logger_format)
    logger = logging.getLogger('texstrip')

    # disable parser logger
    logging.getLogger('strip_comments').setLevel(logging.INFO)

    # the main TeX input file
    main_file = args['<main>']
    logger.info('using {} as the main file'.format(main_file))

    # create the target dir
    output_dir = os.path.join(os.getcwd(), args['--outdir'])
    os.makedirs(output_dir, exist_ok=True)

    logger.info("using {} as the output dir".format(output_dir))

    # 1) expand the main file
    target_main_file = os.path.join(output_dir, os.path.basename(main_file))
    # names for intermediate files
    expanded_main_file = os.path.join(output_dir, 'expanded.tex.strip')
    stripped_main_file = os.path.join(output_dir, 'stripped.tex.strip')

    if target_main_file == main_file:
        raise Exception('target main file is the same as the source')

    cmd = 'latexpand --empty-comments -o {} {}'.format(expanded_main_file, main_file)
    subprocess.run(cmd, shell=True, check=True)
    logger.debug('Finished: {}'.format(cmd))

    if args['<extra>']:
        cp_cmd = "cp -rf {} {}".format(" ".join(args['<extra>']), output_dir)
        subprocess.run(cp_cmd, shell=True, check=True)
        logger.debug("Finished: {}".format(cp_cmd))

    # 2) remove comments
    strip_comments_from_files(expanded_main_file, stripped_main_file)

    # 3) clean up
    shutil.copyfile(stripped_main_file, target_main_file)
    # remove intermediate files unless --keep
    if not args['--keep']:
        os.remove(expanded_main_file)
        os.remove(stripped_main_file)

    if args['--build']:
        os.chdir(output_dir)
        build_cmd = "latexmk -pdf {}".format(target_main_file)
        subprocess.run(build_cmd, shell=True, check=True)

    from chromalog.mark.helpers.simple import success, important

    logger.info("%s The stripped version is at %s" % (success("Done!"), important(target_main_file)))


if __name__ == '__main__':
    main()