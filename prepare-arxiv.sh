#!/usr/bin/env bash

set -e

command -v latexpand > /dev/null 2>&1 || {
    echo "latexpand is required. Please refer to README.md"
}

LATEX_ROOT_DIR="$(pwd)/.."
TARGET_DIR=$(pwd)/arkiv-$(git rev-parse --short HEAD)

MAIN_TARGET_FILE=${TARGET_DIR}/paper.tex
MAIN_ORIGINAL_FILE=paper.tex

# clear the target directory if any
rm -rf ${TARGET_DIR} && mkdir -p ${TARGET_DIR}

pushd ${LATEX_ROOT_DIR} > /dev/null

# copy bib files
cp -rf bib Makefile ${TARGET_DIR}

# expand into a single file with line comments removed (but not comment environment)
latexpand --empty-comments ${MAIN_ORIGINAL_FILE} | sed '/^\s*%/d' > ${TARGET_DIR}/tmp.tex
popd > /dev/null

# for some reason latexpand can't remove \begin{comment} .. \end{comment} (which it claims to do),
# so this script is used (taken from https://gist.github.com/amerberg/a273ca1e579ab573b499)
python strip_comments.py -o ${MAIN_TARGET_FILE} ${TARGET_DIR}/tmp.tex

# move pdf graph to the root dir
for pic in $(grep pdf ${MAIN_TARGET_FILE} | sed 's/.*{\(.*\)}/\1/'); do
	new_filename=$(echo $pic | tr '/' '-');
	cp -vrf ../$pic ${TARGET_DIR}/$new_filename
	sed -i "s;$pic;$new_filename;g" ${MAIN_TARGET_FILE}
done

rm -rf ${TARGET_DIR}/tmp.tex

# copy over the sanity check script
cp -rf .check_comments.sh ${TARGET_DIR}/check_comments.sh

pushd ${TARGET_DIR}
	make
	make latexclean
	rm -rf bib
popd

echo "Done!"
