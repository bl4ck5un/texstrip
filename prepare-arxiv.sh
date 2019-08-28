#!/usr/bin/env bash

set -ex

command -v latexpand > /dev/null 2>&1 || {
    echo "latexpand is required. Please refer to README.md"
}

LATEX_ROOT_DIR="../paralysis-proofs-paper"
MAIN_ORIGINAL_FILE=main.tex

TARGET_DIR=$(mktemp -d -p $(pwd) arxiv.XXXXXX)
MAIN_TARGET_FILE=${TARGET_DIR}/${MAIN_ORIGINAL_FILE}

# clear the target directory if any
rm -rf ${TARGET_DIR} && mkdir -p ${TARGET_DIR}

pushd ${LATEX_ROOT_DIR} > /dev/null

# copy bib files
cp -rf *.bib data ${TARGET_DIR}

# expand into a single file with line comments removed (but not comment environment)
latexpand --empty-comments ${MAIN_ORIGINAL_FILE} | \
    sed '/^\s*%/d' > ${TARGET_DIR}/tmp.tex # remove lines with only %
popd > /dev/null

# for some reason latexpand can't remove \begin{comment} .. \end{comment} (which it claims to do),
# so this script is used (taken from https://gist.github.com/amerberg/a273ca1e579ab573b499)
python strip_comments.py -o ${MAIN_TARGET_FILE} ${TARGET_DIR}/tmp.tex

# rm -rf ${TARGET_DIR}/tmp.tex

# copy over the sanity check script
cp -rf .check_comments.sh ${TARGET_DIR}/check_comments.sh

echo "Done! Enter ${TARGET_DIR} and compile."
