#!/bin/bash

# vars :: {"sample_app/latest":"docker_image_tag"}

git clone https://github.com/b-rad-c/medium-stack.git

# exit if the git clone fails
if [ $? -ne 0 ]; then
    echo "git clone failed"
    exit 1
fi

# checkout branch templating
cd medium-stack
git checkout templating

if [ $? -ne 0 ]; then
    echo "could not checkout branch"
    exit 1
fi

cd ..

docker build . -t sample_app/latest

exit $?