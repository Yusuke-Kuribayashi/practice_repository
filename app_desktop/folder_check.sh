#!/bin/bash

CURRENT_DIR=$(pwd)
WORK_PATH="/kaitou/第1回"
PYTHON_DIR="/python_dir"

# mkdir ${CURRENT_DIR}${WORK_PATH}${PYTHON_DIR}
# echo "${CURRENT_DIR}${WORK_PATH}"

# for file in "${CURRENT_DIR}${WORK_PATH}"/*; do
#     if [ -d "$file" ]; then
#         echo 
#     echo "$file"
# done

# cd ${CURRENT_DIR}${WORK_PATH}

# ディレクトリを再帰的に探索する関数
function change_folder {
    echo $1

    for file in "$1"/*; do
        if [ -d "$file" ]; then
            change_folder ${file}
        else
            echo "$file"
            # jupyter nbconvert --to python "$file"
        fi
    done
 
}
cd ${CURRENT_DIR}${WORK_PATH}

change_folder .

