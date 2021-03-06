
% fourierdemo.m

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Note that this code is written for transparency, not speed.
% This code generated Figures 1.8a and 1.8b in the book.
% Simple Fourier transform key variables
% 
% x       signal of N sampled values
% T       length of signal in seconds
% R       sampling rate in samples per second
% N       number of samples in signal
% tvec    vector of N time values in seconds
% nvec   vector of N elements containing values from 0 to 2*pi =
% fundamental frequency
% fmax  maximum frequency in Hz, chosen by user 
% Nyquistfrequency Nyquist frequency= R/2
% dt        interval in seconds between samples  = 1/R
% fmin    lowest frequency in Hz = 1/T
% nfrequencies  number of frequencies in transform
% Cs    vector of nfrequencies cosine coefficients
% Ds    vector of nfrequencies sine coefficients
% As    vector of nfrequencies Fourier amplitudes
% freqs vector of frequency values in Hz
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clear all;

% set testing to 0 or 1.
testing = 0;
fontsize = 15;

if testing % make signal of two sinusoids with known frequencies
    R = 44100; % set sampling rate, samples/s
    frequency = 1000; % Hz
    period = 1/frequency; % in seconds
    
    T = 0.5; % length of signal in seconds
    N = R*T; % number of samples in T seconds
    tvec = 1:N; % time vector of N samples
    tvec = tvec/R; % time vector in units of seconds
    
    % signal in which each interval of period seconds increases by 2*pi.
    x1 = 2*pi*tvec/period;
    
    % signal in which each interval of period seconds increases by 1.5*2*pi.
    x2 = 1.5*x1;
    
    % make sinusoids
    x = sin(x1);
    x = x + 0.5*sin(x2);
    % specify maximum frequency here
fmax = 3000; % Hz

figure(89); plot(x(1:100));

    
else % not testing, use singing voice as signal x.
    
    % set file name where signal is stored
    %load handel.mat;
    fname = 'sebinpubaudiIMG_1563.m4a';
    
    % Read in voice recording.
    [x,R] = audioread(fname); % R = samples/s
    
%      cd '/Users/JimStone/Documents/BOOKS/book_FourierTransform';
%     ffname = 'sebinpubaudiIMG_1563.wav';
% audiowrite(ffname,x,R);

    % choose length of sound segment in seconds.
    segmentseconds = 1;
    N = R * segmentseconds;
    xmin=1; %1024*5;
    xmax=xmin+N-1;
    x=x(xmin:xmax);
    N = length(x); % number of samples.
    T = N/R;% number of seconds in recording
    % make time vector
    tvec = 1:N; % vector of sample numbers in recording.
    tvec= tvec/R; % convert to seconds.
    % specify maximum frequency here
fmax = 1000; % Hz

end

% listen to sound - this may need a mac to function.
if exist('sound') sound(x,R); end

% plot sound wave.
figure(1);
plot(tvec,x,'k');
xlabel('Time (seconds)')
ylabel('Amplitude');
set(gca,'XLim',[0 T]);
% prettify graph.
set(gca,'FontSize',fontsize);
set(gca,'Linewidth',2);
hline = findobj(gcf, 'type', 'line'); 
set(hline,'LineWidth',2);

% make fundamental sinusoidal vector.
nvec = 1:N;
nvec = nvec*2*pi/N; % nvec now spans up to 2pi.
nvec = nvec';

Nyquistfrequency = R/2;
if fmax > Nyquistfrequency
    error('Maximum freqency exceeds Nyquist frequency.');
end

dt = 1/R; % interval between samples.
T = N/R;
fmin = 1/T; % lowest frequency in Hz.
% number of frequencies
nfrequencies = floor( fmax/fmin);

% ensure x is a row vector
if iscolumn(x) x = x'; end

% make storage for Fourier coefficients.
Cs = zeros(1,nfrequencies);
Ds = zeros(1,nfrequencies);
% make storage for Fourier frequencies.
freqs =  zeros(1,nfrequencies);

for n = 1:nfrequencies
    
    % set frequency
    freq = fmin*n;
    freqs(n) = freq;
    
    % make cosine waves at frequency freq.
    cosinewave = cos(nvec*n);
    % find inner product of sound with cosine wave.
    % x is row vector, wave is column vector, so product is a scalar.
    C = x * cosinewave; % equivalent to C=sum( x .* cosinewave)
    Cs(n) = C;
    
    % make sine waves at frequency freq.
    sinewave = sin(nvec*n);
    % find inner product of sound with cosine wave.
    D = x * sinewave;
    Ds(n) = D;
    
end

% get Fourier amplitudes
As = sqrt(Cs.^2 + Ds.^2);

% get phases phasespectrum = atan(Ds./Cs);

figure(2);
plot(freqs,As,'k');
xlabel('Frequency (Hz)')
ylabel('Amplitude');
% prettify graph.
set(gca,'FontSize',fontsize);
set(gca,'Linewidth',2);
hline = findobj(gcf, 'type', 'line'); 
set(hline,'LineWidth',2) 

figure(3);
plot(Cs);



%%%%%%%%%%%%%%%%%%%%%%%%%
% END OF FILE.
%%%%%%%%%%%%%%%%%%%%%%%%%
