#!/bin/bash
echo 'Script Working'
dir1='./dataset/'
dataset=https://dl.dropboxusercontent.com/s/2a9jvq1m4vhp8rp/
name1=dataset-original.zip
wget $dataset$name1 -P $dir1 && unzip $dir1$name1 && rm $dir1$name1
dataset256=https://dl.dropboxusercontent.com/s/9bvxp36g13li63w/
name2=dataset-256.zip
wget $dataset256$name2 -P $dir1 && unzip $dir1$name2 && rm $dir$name2
dataset512=https://dl.dropboxusercontent.com/s/q4rdb0g26j107m9/
name3=dataset-512.zip
wget $dataset512$name3 -P $dir1 && unzip $dir1$name3 && rm $dir$name3
dataset1280=https://dl.dropboxusercontent.com/s/9totbwbdnm12jf7/
name4=dataset-1280.zip
wget $dataset1280$name4 -P $dir1 && unzip $dir1$name4 && rm $dir$name4
echo 'Downloading dataset...'
dir2='./models'
url2=https://www.dropbox.com/scl/fi/vqytmc8532x7ov805bu6z/torchFlow-ckpt.onnx?rlkey=2wg8s6x829aaoqed56jj7ug7y&dl=0
echo 'Downloading onnx model...'
wget $url2 -O torchflow-ckpt.onnx
mv torchflow-ckpt.onnx models/
url3=https://dl.dropboxusercontent.com/s/dv916v4t5hn6qpu/torchFlow-ckpt.pt
echo 'Downloading yolo checkpoint...'
wget $url3 -P $dir2
echo "Downloaded!"
