clc;close all;clear all;addpath(genpath('./'));
file_path = '../test_data_result/';
gt_path = './expertC_testSet/';
path_list = dir(strcat(file_path,'*.png'));
gt_list = dir(strcat(gt_path,'*.jpg'));
img_num = length(path_list);
%calculate psnr
total_psnr = 0;
if img_num > 0 
   for j = 1:img_num 
       image_name = path_list(j).name;
       gt_name = gt_list(j).name;
       input = imread(strcat(file_path,image_name));
       gt = imread(strcat(gt_path, gt_name));
       psnr_val = psnr_rgb(input, gt);
       total_psnr = total_psnr + psnr_val;
       fprintf('%d %f %s\n',j,psnr_val,strcat(file_path,image_name));
   end
end
qm_psnr = total_psnr / img_num;
fprintf('The avgerage psnr is: %f', qm_psnr);