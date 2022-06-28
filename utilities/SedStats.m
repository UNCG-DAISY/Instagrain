function [d_vals] = SedStats(phi,type,per)
%SEDSTATS computes the mean, median, skewness and kurtosis of a sediment
%sample, then plots a histogram and a cumulative sand size distribution
%
%  [phi_mean,phi50,phi_skew,phi_kurt] = SEDSTATS(phi,type,per)
%
%  ------------------------------------------------------------
%  --------------- INPUT DESCRIPTIONS -------------------------
%  ------------------------------------------------------------
%
%     phi -  ARRAY containing the phi values of the sample
%
%  'type' -  STRING specifying the type of values
%            contained in the array, per. There are 2 valid 
%            values for 'type':
%            
%              'weight' means that the values in the input
%              variable, per, are the corresponding weights
%
%              'percent' means the values in the input
%              variable, per, are the corresponding percent of 
%              sample values
%
%     per -  ARRAY containing the values consistent with the 
%            parameter entered for 'type', which correspond to
%            their respective phi values. If 'type' equals
%            'percent', the percentage values should be > 1
%            (i.e. 20% would be 20, NOT 0.2).
%
%  ------------------------------------------------------------
%  --------------- OUTPUT VARIABLES ---------------------------
%  ------------------------------------------------------------
%
%  phi_mean - mean phi size of sediment sample
%
%     phi50 - median grain size in phi units of sample
%
%  phi_skew - skewness of sample
%
%  phi_kurt - kurtosis of sample
%


% Parse/validate user input
p = inputParser;
expectedTypes = {'weight','percent'};

addRequired(p,'phi',@isnumeric);
addRequired(p,'type',@(type) any(validatestring(type,expectedTypes)));
addRequired(p,'c',@isnumeric);

parse(p,phi,type,per);





if strcmp(type,'weight')
  % Compute percentages of total weight
    per = (per/sum(per))*100
elseif strcmp(type,'percent')
  % Ensure values are greater than 1 if 'percent' was specified
    if max(per) < 1
        per = per*100;
    end
end

% Sort from smallest to largest
tmp = zeros(length(phi),2);
tmp(:,1) = phi;
tmp(:,2) = per;
tmp = sortrows(tmp,1);  % sort values in both columns together, based on values in column 1, in descending order
phi = tmp(:,1)';
per = tmp(:,2)';

% Compute statistics
phi_mean = sum(per.*phi/100);  % 1st moment, mean
phi_std = sqrt(sum(per.*(phi - phi_mean).^2)/100);  % sqrt(2nd moment), std dev
phi_skew = sum((per.*(phi - phi_mean).^3)/(phi_std^3*100));  % 3rd moment, skewness
phi_kurt = 3*phi_std^4;  % 4th moment, kurtosis

% Compute CDF
cdf = cumsum(per);

% Compute estimate of median by linerly interpolating
% between the first points above and below the 50th
% percentile in the CDF
ct = 1;
while cdf(ct) < 50
    ct = ct + 1;
end
m = (cdf(ct) - cdf(ct - 1))/(phi(ct) - phi(ct - 1));  % slope

%y2 = ["d2", "d5", "d10", "d16", "d25", "d50", "d75", "d84", "d90", "d95", "d98"];

phi98= 2^-(interp1(cdf,phi,2));
phi95 = 2^-(interp1(cdf,phi,5));
phi90 = 2^-(interp1(cdf,phi,10));
phi84 = 2^-(interp1(cdf,phi,16));
phi75 = 2^-(interp1(cdf,phi,25));
phi50 = 2^-(interp1(cdf,phi,50));
phi25 = 2^-(interp1(cdf,phi,75));
phi16 = 2^-(interp1(cdf,phi,84));
phi10 = 2^-(interp1(cdf,phi,90));
phi5 = 2^-(interp1(cdf,phi,95));
phi2 = 2^-(interp1(cdf,phi,98));

d_vals = [phi2, phi5, phi10, phi16, phi25, phi50, phi75, phi84, phi90, phi95, phi98];

phi98= interp1(cdf,phi,2);
phi95 = interp1(cdf,phi,5);
phi90 = interp1(cdf,phi,10);
phi84 = interp1(cdf,phi,16);
phi75 = interp1(cdf,phi,25);
phi50 = interp1(cdf,phi,50);
phi25 = interp1(cdf,phi,75);
phi16 = interp1(cdf,phi,84);
phi10 = interp1(cdf,phi,90);
phi5 = interp1(cdf,phi,95);
phi2 = interp1(cdf,phi,98);

d_vals_phi = [phi2, phi5, phi10, phi16, phi25, phi50, phi75, phi84, phi90, phi95, phi98]

% median, computed from point-slope formula

% If you're reading this, Jack, I realize I could have used
%   >> phi50 = interp1(cdf,phi,50);
% but sometimes I enjoy re-inventing the wheel a bit. :)




% phi_mean = (interp1(cdf,phi,84) + interp1(cdf,phi,50) + interp1(cdf,phi,16))/3; 
% phi_std = (interp1(cdf,phi,84) - interp1(cdf,phi,16))/2;
% phi_median = interp1(cdf,phi,50);
% phi_skew = (phi_mean - phi_median)/phi_std;
% phi_kurt = ((interp1(cdf,phi,16) - interp1(cdf,phi,5)) + ((interp1(cdf,phi,95) - interp1(cdf,phi,84))))/(2*phi_std);






% Plot PDF and CDF with stats (similar to Figure 5.3 in Masselink and
% Hughes book)
% fig = figure('units','normalized','position',[0.25 0.3 0.5 0.35]);
%   ax1 = axes('position',[0.07 0.14 0.4 0.8],'parent',fig,'fontsize',12);
%     box(ax1,'on');
%   ax2 = axes('position',[0.57 0.14 0.4 0.8],'parent',fig,'fontsize',12,'xtick',-2.5:0.5:2.5);
%     box(ax2,'on');
%     hold(ax2,'on');
% 
% 
% % Plot Histogram, phi
%   bar(phi,per,'parent',ax1,'facecolor','k')
%     xlabel('Grain Size, \phi','parent',ax1)
%     ylabel('Frequency (%)','parent',ax1)
%   
% % Plot Cumulative Distribution, phi
%   plot(phi,cdf,'parent',ax2,'color','k','linewidth',2)
%     xlabel('Grain Size, \phi','parent',ax2)
%     ylabel('Cumulative Frequency (%)','parent',ax2)
%   % Plot phi50 lines
%   plot([min(phi) phi50],[50 50],'parent',ax2,'linewidth',2,'linestyle',':','color','k')
%   plot([phi50 phi50],[50 0],'parent',ax2,'linewidth',2,'linestyle',':','color','k')
%     axis tight
%     ylim(ax2,[0 100])
%     
% % Annotations
% annotation('textbox','position',[0.08 0.75 0.22 0.18],'string',{['Mean = ' num2str(phi_mean,'%.2f')];['Skewness = ' num2str(phi_skew,'%.2f')];['Kurtosis = ' num2str(phi_kurt,'%.2f')]},'fontsize',10,'edgecolor','none','backgroundcolor','white');
% annotation('textbox','position',[0.58 0.825 0.1 0.07],'string',['\phi_5_0 = ' num2str(phi50,'%.2f')],'fontsize',10,'edgecolor','none','backgroundcolor','none')
% annotation('textbox','position',[0.65 0.55 0.25 0.07],'string','50^t^h Percentile','fontsize',10,'edgecolor','none','backgroundcolor','none')
% 
% % return
% %
% % FOR PART (b) OF 2.7 IN D&D...
% %
% 
% % Compute normal distribution
% x = -2:0.1:4;
% pdf_norm = normpdf(x,phi_mean,phi_std);
% 
% figure;
%   plot(phi,per,'k','linewidth',2)
%     hold on
%   plot(x,pdf_norm*(max(per)/max(pdf_norm)),':k','linewidth',2)
%   set(gca,'fontsize',12)
%   xlabel('Grain Size, \phi','fontsize',12)
%   ylabel('Frequency (%)','fontsize',12)
%   legend('Data','Normal Distribution','location','northwest')



end







% % Compute d and d50 (mm) from phi values, for plotting in semilogx
% d = 2.^-phi;
% d50 = 2^-phi50;
% % Plot Histogram, d (mm)
%   bar(d,per,'parent',ax1,'xscale','log')
%     xlabel('Grain Diameter, d (mm)','parent',ax1)
%     ylabel('Frequency (%)','parent',ax1)
%   
% % Plot Cumulative Distribution, d (mm)
%   semilogx(d,cdf,'parent',ax2)
%     xlabel('Grain Diameter, d (mm)','parent',ax2)
%     ylabel('Cumulative Frequency (%)','parent',ax2)
%     grid(sub2,'on');




