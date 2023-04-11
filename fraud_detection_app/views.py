from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import glob
import os
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler

loaded_model = pickle.load(open('static/wights/model.pkl', 'rb'))

@csrf_exempt
def index(request):
    folder = 'static/input_img/'
    if request.method == "POST" and request.FILES['file']:
        file = request.FILES.get('file')
        url = request.get_host()
        input_img = glob.glob('static/input_img/*')
        for f in input_img:
            os.remove(f)
      
        location = FileSystemStorage(location=folder)
        fn = location.save(file.name, file)
        path = os.path.join('static/input_img/', fn)
        flage, pre_val = detect(path)
        
        if pre_val == 1:
            response = 'Fraud'
        else:
            response = 'Not Fraud'
            
       
       
        if flage == True:
            context = {
                "flag": flage,
                "status": response,
                
            }
        else:
            context = {
                "flag": flage,
                "status": "please send the valid csv file",
            }
        return JsonResponse(context)
    return render(request, 'index.html')


def detect(path):
    flage = False
    pre_val = ''
    try:
        Data = pd.read_csv(path)
        Data['normAmount'] = StandardScaler().fit_transform(Data['Amount'].values.reshape(-1, 1))
        Data1 = Data.drop(['Amount'],axis=1)
        # print(Data1.values)
        predicted= loaded_model.predict(Data1.values)
        print(predicted)
        pre_val = int(predicted[0])
        flage = True
    except:
        pass
    return flage, pre_val
    
