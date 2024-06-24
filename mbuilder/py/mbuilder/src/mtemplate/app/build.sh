#!/bin/bash
# vars :: {"sample_img/latest":"docker_image_tag"}

# parse args #

no_cache=false
if [ "$1" == "--no-cache" ]; then
    no_cache=true
fi

# if ./medium-stack does NOT exist

if [ ! -d "./medium-stack" ]; then
    echo "cloning medium-stack"
    git clone https://github.com/b-rad-c/medium-stack.git

    if [ $? -ne 0 ]; then
        echo "git clone failed"
        exit 1
    fi

fi


# checkout branch templating #

cd medium-stack
git checkout templating

if [ $? -ne 0 ]; then
    echo "could not checkout branch"
    exit 1
fi

cd ..

# run docker build #

if [ "$no_cache" = true ]; then
    docker build . -t sample_img/latest --no-cache
else
    docker build . -t sample_img/latest
fi

exit $?