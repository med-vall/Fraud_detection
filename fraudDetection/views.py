
from django.shortcuts import render
import pandas as pd
from django_pandas.io import read_frame


def homeuplo(request):
    posts=datfr('/home/vall/Documents/cv.pdf')
    names = list(posts.columns)
    fields = [field.name for field in [MODEL_NAME]._meta.get_fields()]
    return render(request, 'fieldmatching.html', {'fields': fields, 'path_name': path_name, 'names': names})

    return render(request, 'help.html',{'cv':posts})

def datfr(path):
    df = pd.read_csv("/home/vall/Downloads/Documents/stage/tutos/2/data/2.csv")
    return df
