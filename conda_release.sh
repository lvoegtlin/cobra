#!/bin/bash
# inspired by https://medium.com/@giswqs/building-a-conda-package-and-uploading-it-to-anaconda-cloud-6a3abd1c5c52

# clean up
conda_folder="conda_builds"
rm -rf $conda_folder

# adjust the Python versions you would like to build
array=( 3.5 3.6 3.7 )
echo "Building conda package ..."
# building conda packages
for i in "${array[@]}"
do
	conda-build --python $i .
done

# convert package to other platforms
echo "Convert conda package to all other available plattforms ..."
find $HOME/miniconda3/conda-bld/osx-64/ -name *pocr*.tar.bz2 | while read file
do
    echo $file
    #conda convert --platform all $file  -o $HOME/conda-bld/
    conda convert -p all $file  -o ./$conda_folder/
    rm $file
done
# upload packages to conda
find ./$conda_folder/ -name *.tar.bz2 | while read file
do
    echo $file
    anaconda upload $file
done

# remove the build temps
conda build purge
echo "Building conda package done!"