# Underexposed Photo Enhancement Using Deep Illumination Estimation

[Ruixing Wang](http://appsrv.cse.cuhk.edu.hk/~rxwang/)<sup>1</sup>, [Qing Zhang](http://zhangqing-home.net)<sup>2</sup>, [Chi-Wing Fu](https://www.cse.cuhk.edu.hk/~cwfu/)<sup>1</sup>, [Xiaoyong Shen](http://xiaoyongshen.me/)<sup>3</sup>, [Wei-Shi Zheng](https://sites.google.com/site/sunnyweishi/)<sup>2</sup>, [Jiaya Jia](http://jiaya.me/)<sup>1,3</sup>

<sup>1</sup>The chinese university of hong kong <sup>2</sup>Sun Yat-sen University <sup>3</sup>Tencent Youtu Lab

### [Paper](https://drive.google.com/file/d/1CCd0NVEy0yM2ulcrx44B1bRPDmyrgNYH/view?usp=sharing), [Errata](https://drive.google.com/file/d/1fJ7MQfm6NuCMtfQzLM0Y6LNU9XyQb6Ho/view?usp=sharing)
### Usage

1. Clone the repository:

   ```shell
   git clone https://github.com/wangruixing/DeepUPE.git
   ```
2. Install the Python dependencies, run:
    ```shell
    cd main
    pip install -r requirements.txt
    make
    ```
3. Evaluation:
The test set can be downloaded in https://drive.google.com/open?id=1FrlMdnwiUfHthtw0jHdp40IbOVXfsoZJ. It includes 500 pair images from MIT-Adobe FiveK 4500-5000. You can download this and run:
```shell
    python main/run.py checkpoints <input file path> <output file path>
```    
PSNR evaluation code is in avg_psnr.m. Modify the related paths in 'avg_psnr.m', and run it.

### Errata
We recently found an implementation bug in calculating PSNR. Fortunately, this bug doesn't affect any of the conclusions in our paper, we have corrected this bug in the Matlab code and updated the corresponding values in the revised paper. We apologize for the confusion to readers.


# Bibtex
```
@InProceedings{Wang_2019_CVPR,
author = {Wang, Ruixing and Zhang, Qing and Fu, Chi-Wing and Shen, Xiaoyong and Zheng, Wei-Shi and Jia, Jiaya},
title = {Underexposed Photo Enhancement Using Deep Illumination Estimation},
booktitle = {The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
month = {June},
year = {2019}
}
```
