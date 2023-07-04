#!/bin/bash
echo 'Script Working'
# dir1='./dataset'
# url1=https://dl.dropboxusercontent.com/s/x919nszlmp62m3r/
# file='dataset.zip'
# echo 'Downloading dataset...'
# curl -L $url1$file -o $file && unzip -q $file -d $dir1
dir2='./models'
url2=https://dl.dropboxusercontent.com/s/grgwkhv0zddmlrh/8l-1280-3232.onnx
echo 'Downloading onnx model...'
wget $url2 -P $dir2
url3=https://dl.dropboxusercontent.com/s/dv916v4t5hn6qpu/torchFlow-ckpt.pt
echo 'Downloading yolo checkpoint...'
wget $url3 -P $dir2
echo "Downloaded!"
