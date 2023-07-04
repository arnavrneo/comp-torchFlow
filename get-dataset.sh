#!/bin/bash
echo 'Script Working'
# dir1='./dataset'
# url1=https://dl.dropboxusercontent.com/s/x919nszlmp62m3r/
# file='dataset.zip'
# echo 'Downloading dataset...'
# curl -L $url1$file -o $file && unzip -q $file -d $dir1
dir2='./models'
url2=https://dl.dropboxusercontent.com/s/grgwkhv0zddmlrh
onnx=/8l-1280-3232.onnx
echo 'Downloading onnx model...'
curl -L $url2$onnx > $dir2$onnx
url3=https://dl.dropboxusercontent.com/s/dv916v4t5hn6qpu
ckpt=/torchFlow-ckpt.pt
echo 'Downloading yolo checkpoint...'
curl -L $url3$ckpt > $dir2$ckpt
echo "Downloaded!"
