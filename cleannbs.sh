#/usr/bin/env bash
# Run this from the nengo directory
if ls examples/*.ipynb &> /dev/null; then
    for example in examples/*.ipynb; do
        git checkout --theirs $example
        ../devscripts/clearoutputs.py $example
        git add $example
    done
fi

if ls examples/old_api/*.ipynb &> /dev/null; then
    for example in examples/old_api/*.ipynb; do
        git checkout --theirs $example
        ../devscriptbs/clearoutputs.py $example
        git add $example
    done
fi
