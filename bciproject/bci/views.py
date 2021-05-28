from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse,JsonResponse
import requests
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control,never_cache
from django.utils.cache import add_never_cache_headers
from .apps import BciConfig
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler, Normalizer   
import joblib
from bci.models import Results
import matplotlib.pyplot as plt
from io import StringIO
def home(request):
    return render(request,'home.html')

def training(request):
    return render(request,'training.html')


#Fast Fourier Transform
def get_fft(snippet):
    Fs = 128.0;  # sampling rate
   
    y = snippet
    n = len(y) # length of the signal
    k = np.arange(n)
    T = n/Fs
    frq = k/T
    frq = frq[range(n//2)]
    
    Y = np.fft.fft(y) 

    z=Y/n
    z = z[range(n//2)]
    return frq,abs(z)


def make_frames(df,frame_duration,overlap):
    Fs = 128.0
    frame_length = Fs*frame_duration
    frames = []
    steps = make_steps(len(df),frame_duration,overlap)
    for i,_ in enumerate(steps):
        frame = []
        if i == 0:
            continue
        else:
            for channel in df.columns:
                snippet = np.array(df.loc[steps[i][0]:steps[i][1],int(channel)])
                #print(snippet)
                f,Y =  get_fft(snippet)
                            
                alpha,lbeta,hbeta = alpha_lbeta_hbeta_averages(f,Y)
                frame.append(alpha)
                frame.append(lbeta)
                frame.append(hbeta)
            
        frames.append(frame)
    return np.array(frames)


def make_steps(samples,frame_duration,overlap):  
    Fs = 128
    i = 0
    intervals = []
    samples_per_frame = Fs * frame_duration
    while i+samples_per_frame <= samples:
        intervals.append((i,i+samples_per_frame-1))
        i = i + samples_per_frame - int(samples_per_frame*overlap)
    return intervals


def alpha_lbeta_hbeta_averages(f,Y):
    alpha_range = (8,12)
    lbeta_range = (12,20)
    hbeta_range = (20,30)
    alpha = Y[(f>alpha_range[0]) & (f<=alpha_range[1])].mean()
    lbeta = Y[(f>lbeta_range[0]) & (f<=lbeta_range[1])].mean()
    hbeta = Y[(f>hbeta_range[0]) & (f<=hbeta_range[1])].mean()
    return alpha,lbeta,hbeta


def make_data_pipeline2(file_names,image_size,frame_duration,overlap):
    
    Fs = 128.0   #sampling rate
    frame_length = Fs * frame_duration 
    for i, file in enumerate(file_names):
        df = pd.read_csv(file, skiprows=1)
        df = df.filter(items=['EEG.AF3', 'EEG.T7', 'EEG.Pz', 'EEG.T8', 'EEG.AF4'])
        scaler = RobustScaler()
        df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
        df.columns = range(df.shape[1])
        frames = make_frames(df,frame_duration,overlap)
        if i == 0:
            X = frames
        else:
            X = np.concatenate((X,frames),axis = 0)
    return X

def testing(request):
    return render(request,'testing.html')


def testing_res(request):
    nb=joblib.load('knn_model.sav')
   
    csv_file = request.FILES["myFile"]
    #file_data = csv_file.read().decode("utf-8")   
    file_names1 = [csv_file]
    image_size = 28
    frame_duration = 1.0
    overlap = 0.5
    X1 = make_data_pipeline2(file_names1,image_size,frame_duration,overlap)
    l = pd.DataFrame.from_records(X1)
    k1=len(l)
    a1=l[0:k1-1]
    l=a1.mean(axis=0)
    l=l.to_numpy()
    l=[l]
    ans1=nb.predict(l)
    alpha1=(l[0][0]+l[0][3]+l[0][6]+l[0][9]+l[0][12])/5
    beta1=(l[0][1]+l[0][4]+l[0][7]+l[0][10]+l[0][13])/5
    if ans1==[0]:
        ans1='relaxed'
    elif ans1==[1]:
        ans1='concentrated'
    else:
        ans1='stress'
 
    result = Results(Alpha=alpha1,Beta=beta1,Mental_state=ans1)
    result.save()
    return render(request,'testing_res.html',{'ans':ans1,'alpha':alpha1,'beta':beta1})


def results(request):
    
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2*np.pi*t)
    plt.xlabel('time (s)')
    plt.ylabel('voltage (mV)')
    plt.title('About as simple as it gets, folks')
    plt.grid(True)
    return render(request,'results.html',context={'plt':plt})
    '''
    result = Results.objects.values()
    a=list(result)  

    if len(a)==0:

        y1 = [0.0]
        x1 = ['0 weeks  1 weeks  2 weeks  3 weeks']
        y2 = [0.0]

        fig = plt.figure()
        plt.plot(x1, y1, color="orange",marker='.',markersize=10,label = 'alpha')
        plt.plot(x1, y2,color="green", marker='.',markersize=10,label ='beta')
        plt.yticks([0.0,0.01,0.02,0.03,0.04])
        plt.title("No file uploaded")
        plt.legend(loc='best')
        imgdata = StringIO()
        fig.savefig(imgdata, format='svg')
        imgdata.seek(0)
        data = imgdata.getvalue()
        #return data
        return render(request,'results.html',context={'data':data})


    elif len(a)==1:

        y1 = [0.0,a[0]['Alpha']]
        x1 = ['0 weeks','1 weeks  2 weeks  3 weeks']
        y2 = [0.0,a[0]['Beta']]
        fig = plt.figure()
        plt.plot(x1, y1, color="orange",marker='.',markersize=10,label = 'alpha')
        plt.plot(x1, y2,color="green", marker='.',markersize=10,label ='beta')
        plt.yticks([0.0,0.01,0.02,0.03,0.04])
        plt.title("subject1")
        plt.legend(loc='best')
        imgdata = StringIO()
        fig.savefig(imgdata, format='svg')
        imgdata.seek(0)
        data = imgdata.getvalue()
        #return data
        return render(request,'results.html',context={'data':data})
    elif len(a)==2:

        y1 = [0.0,a[0]['Alpha'],a[1]['Alpha']]
        x1 = ['0 weeks','1 weeks','2 weeks  3 weeks']
        y2 = [0.0,a[0]['Beta'],a[1]['Beta']]
        fig = plt.figure()
        plt.plot(x1, y1, color="orange",marker='.',markersize=10,label = 'alpha')
        plt.plot(x1, y2,color="green", marker='.',markersize=10,label ='beta')
        plt.yticks([0.0,0.01,0.02,0.03,0.04])
        plt.title("subject1")
        plt.legend(loc='best')
        imgdata = StringIO()
        fig.savefig(imgdata, format='svg')
        imgdata.seek(0)
        data = imgdata.getvalue()
        #return data
        return render(request,'results.html',context={'data':data})
    else:   
        y1 = [0.0,a[0]['Alpha'],a[1]['Alpha'],a[2]['Alpha']]
        x1 = ['0 weeks','1 weeks','2 weeks','3 weeks']
        y2 = [0.0,a[0]['Beta'],a[1]['Beta'],a[2]['Beta']]
        plt.plot(x1, y1, color="orange",marker='.',markersize=10,label = 'alpha')
        plt.plot(x1, y2,color="green", marker='.',markersize=10,label ='beta')
        plt.yticks([0.0,0.01,0.02,0.03,0.04])
        plt.title("subject1")
        plt.legend(loc='best')

        return render(request,'results.html',context={'data':data})'''

   






    