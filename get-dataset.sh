#!/bin/bash
echo 'Script Working'
dir='./dataset'
url=https://dl.dropboxusercontent.com/s/x919nszlmp62m3r/
file='dataset.zip'
echo 'Downloading dataset...'
curl -L $url$file -o $file && unzip -q $file -d $dir
echo "Downloaded!"