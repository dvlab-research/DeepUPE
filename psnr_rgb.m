function [PSNR, MSE, MSE_r, MSE_g, MSE_b] = psnr_rgb(X, Y)
X = double(X);
Y = double(Y);
X_r= X(:,:,1);
X_g= X(:,:,2);
X_b= X(:,:,3);
Y_r= Y(:,:,1);
Y_g= Y(:,:,2);
Y_b= Y(:,:,3);

  if any(size(X_r)~=size(Y_r))
    error('The input size is not equal to each other!');
  end
 Dr = X_r - Y_r;
 Dg = X_g - Y_g;
 Db = X_b - Y_b;

MSE_r = sum(Dr(:).*Dr(:)) / numel(Dr);
MSE_g = sum(Dg(:).*Dg(:)) / numel(Dg);
MSE_b = sum(Db(:).*Db(:)) / numel(Db);
MSE = (MSE_r+ MSE_g + MSE_b)/3;
PSNR = 10*log10(255^2 / MSE);
