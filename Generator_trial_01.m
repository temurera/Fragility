N=1000;
a=rand(1,N);
b=mean(a);
c=std(a);

mean_Fyiso=125/0.835;       %kN cinsinden
COV_Fyiso=0.2;
sigma_Fyiso=mean_Fyiso*COV_Fyiso;

Uni_dist=a;
Distr=norminv(Uni_dist,mean_Fyiso,sigma_Fyiso);

b=mean(Distr);
c=std(Distr);

%x_Fyiso=[-3:0.001:3].*sigma_Fyiso+mean_Fyiso;
%y_Fyiso=normcdf(x_Fyiso,mean_Fyiso,sigma_Fyiso);



figure('name','Fyiso - normal','NumberTitle','off');
subplot(3,1,1);
plot(Distr,'bx');
subplot(3,1,2);
hist(Distr,50);
subplot(3,1,3);
plot(x_Fyiso,y_Fyiso,'b');
grid on
grid minor
