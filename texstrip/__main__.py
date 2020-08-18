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
import pathlib
import sys

import chromalog
from docopt import docopt

try:
    from texstrip import strip_comments
except:
    import strip_comments


def check_exe_available(exe):
    if shutil.which(exe) is None:
        raise Exception("{} not available".format(exe))


def main():
    # check dependencies are available
    check_exe_available('latexpand')

    # setup docopt and logging
    args = docopt(__doc__, version='0.0.3')

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
        for extra in args['<extra>']:
            # detect files outside working tree
            path = pathlib.Path(extra)
            logging.info(path)
            logging.info(path.parent)
            if str(path.relative_to('.')).startswith('..'):
                logging.fatal("can't copy files outside current dir %s", extra)
                sys.exit(1)
            if path.parent == '.':
                shutil.copy(path, output_dir)
            else:
                new_dir = pathlib.Path(output_dir) / path.parent
                new_dir.mkdir(parents=True, exist_ok=True)

                shutil.copy(path, new_dir)

    # 2) remove comments
    strip_comments.strip_comments_from_files(expanded_main_file, stripped_main_file)

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
        build_cmd = "latexmk -C {}".format(target_main_file)
        subprocess.run(build_cmd, shell=True, check=True)

    from chromalog.mark.helpers.simple import success, important

    logger.info("%s The stripped version is at %s" % (success("Done!"), important(target_main_file)))


if __name__ == '__main__':
    main()
