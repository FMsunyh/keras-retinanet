python ~/RetinaNet/keras_retinanet/bin/train_com2.py --backbone resnet101 --snapshot /home/syh/RetinaNet/snapshots/resn_pascal_04.h5 --gpu 1 pascal /home/syh/train_data/all_train_data
python ~/RetinaNet/keras_retinanet/bin/train_com2.py --snapshot /home/syh/RetinaNet/snapshots/resn_pascal_04.h5 --gpu 1 pascal /home/syh/train_data/all_train_data
python ~/RetinaNet/keras_retinanet/bin/train_com2.py --backbone resnet101 --gpu 1 pascal /home/syh/train_data/all_train_data

python ~/RetinaNet/keras_retinanet/bin/train_com2.py --backbone resnet50 --snapshot /home/syh/RetinaNet/snapshots/resnet50_pascal_04.h5 --gpu 1 pascal /home/syh/train_data/all_train_data

python ~/RetinaNet/keras_retinanet/bin/train_com2.py --backbone resnet101 --batch-size 3 --epochs 200 --steps 25000 --datasets fusion-train_data --multi-gpu 2 --multi-gpu-force pascal /home/syh/train_data/data/all_train_data_resize2/


python ~/RetinaNet/keras_retinanet/bin/train_com2.py --backbone resnet101 --snapshot /home/syh/RetinaNet/snapshots/20180625_resnet101_fusion-train_data_GPUs2_01.h5  --batch-size 3 --epochs 50 --steps 25000  --datasets all --multi-gpu 2 --multi-gpu-force pascal /home/syh/train_data/data/all_train_data_resize2


## 解压
cd /home/syh/RetinaNet/data_processing
python archiving.py -i /data/train_data -o /home/syh/train_data/data/sub_train_data

## 测试图片是否有问题
