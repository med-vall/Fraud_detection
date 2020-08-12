
from django.shortcuts import render,redirect
import pandas as pd
from django_pandas.io import read_frame
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import datetime
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import datetime
import time
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage

# Imaginary function to handle an uploaded file.

listBN = []
def homeuplo(request):
    posts=datfr('/home/vall/Documents/cv.pdf')
    posts["DATEOPERATION"] = pd.to_datetime(posts["DATEOPERATION"])
    posts["DATEVALEUR"] = pd.to_datetime(posts["DATEVALEUR"])
    delai = posts["DATEOPERATION"] - posts["DATEVALEUR"]

    fraud = []

    for d in delai:
        if d.days > 7:
            fraud.append(1)

        else:
            fraud.append(0)
    posts["fraude"] = fraud
    post='hi me'
    return render(request, 'help.html',{'cv':posts,'pst':post}  )

def upload(request):
    if request.method=='POST':
        uploas_ffile=request.FILES['doc']
        fs=FileSystemStorage()
        name=fs.save(uploas_ffile.name ,uploas_ffile)
        url=fs.url(name)
        print(url)
        return redirect('uploa')


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print ('hhhiiiii')
        if form.is_valid()==False:
            uploas_ffile = request.FILES['doc']
            fs = FileSystemStorage()
            name = fs.save(uploas_ffile.name, uploas_ffile)
            url = fs.url(name)
            url = '/home/Videos/version4/fraudDetection' + url
            url.replace("b", '')
            posts = datfr(url)
            posts["DATEOPERATION"] = pd.to_datetime(posts["DATEOPERATION"])
            posts["DATEVALEUR"] = pd.to_datetime(posts["DATEVALEUR"])
            delai = posts["DATEOPERATION"] - posts["DATEVALEUR"]

            taille = 0
            for index, row in posts.iterrows():
                taille = taille + 1
            print('taille de votre dataset ---> ', taille)

            fraud = []
            fr = 0
            frN = 0
            for d in delai:
                if d.days > 7:
                    fraud.append(1)
                    fr = fr + 1

                else:
                    fraud.append(0)
                    frN = frN + 1
            posts["fraude"] = fraud
            Pfr = fr / taille
            Pfr = Pfr * 100
            IPfr = int(Pfr)

            PfrN = frN / taille
            PfrN = PfrN * 100
            IPfrN = int(PfrN)

            Pfr = str(Pfr)
            Pfr = Pfr[0:5]
            PfrN = str(PfrN)
            PfrN = PfrN[0:5]

            sr = 0
            frRef = ''
            for index, row in posts.iterrows():
                for ind, raw in posts.iterrows():
                    if row["REFERENCEMan "] == raw["REFERENCEMan "] and row["REFERENCEAuto"] != raw["REFERENCEAuto"] and \
                            row[
                                "DATEOPERATION"] == raw["DATEOPERATION"]:
                        sr = sr + 1
                        m = 'une fraude liée au réfférence de manuel ->'
                        frRef = frRef + m + str(row["REFERENCEMan "]) + '  /  ' + str(row["DATEVALEUR"]) + '\n'
                        print('une fraude liée au réfférence de manuel ->', row["REFERENCEMan "], row["DATEVALEUR"])
            if frRef == '':
                frRef = 'aucune Fraude de réfference!'
            else:
                print('fraudes liée au réfference ---> ', sr)

            print(frRef)

            print('***************Montant**************')

            frdMt = 0
            frMnt = ''
            for index, row in posts.iterrows():
                for ind, raw in posts.iterrows():
                    if row["REFERENCEMan "] == raw["REFERENCEMan "] and row["REFERENCEAuto"] != raw["REFERENCEAuto"] and \
                            row["MONTANT"] == raw["MONTANT"]:
                        frdMt = frdMt + 1
                        m = 'MEMES MONTANTS CONSTATES SUCCESSIVEMENT sur un même compte. ->'
                        frMnt = frMnt + m + row["REFERENCEMan "] + ' <---> ' + row["MONTANT"]
                        print('MEMES MONTANTS CONSTATES SUCCESSIVEMENT sur un même compte. ->', row["REFERENCEMan "],
                              row["MONTANT"])

            if frMnt == '':
                frMnt = 'aucune fraudes liées au montant !'
                print('aucune fraudes liées au montant !')
            else:
                print('les fraudes liées au montant ---> ', frdMt)
            print('***************LES MONTANTS SUP 10000**************')

            posts["TIME"] = pd.to_datetime(posts["TIME"])
            posts['TIMES'] = posts["TIME"].dt.time
            time2 = datetime.time(18, 00, 00)
            time1 = datetime.time(7, 00, 00)
            frMntTime = ''
            tcount = 0

            for index, row in posts.iterrows():
                for ind, raw in posts.iterrows():
                    if int(row["MONTANT"]) > 10000 and row["REFERENCEAuto"] != raw["REFERENCEAuto"] and row[
                        "REFERENCEMan "] == raw["REFERENCEMan "] and posts['TIMES'] < time1:
                        tcount = tcount + 1
                        m = "le temps de cette transaction est avant le temps  d'ouverture "
                        frMntTime = frMntTime + m + row["REFERENCEMan "] + ' <---> ' + row["MONTANT"]
                        print ('MEMES MONTANTS CONSTATES SUCCESSIVEMENT sur un même compte. ->', row["REFERENCEMan "],
                               row["MONTANT"])
                    elif int(row["MONTANT"]) > 10000 and row["REFERENCEAuto"] != raw["REFERENCEAuto"] and row[
                        "REFERENCEMan "] == raw["REFERENCEMan "] and posts['TIMES'] > time2:
                        tcount = tcount + 1
                        m = "le temps de cette transaction est aprés le temps  de fermeture --> "
                        frMntTime = frMntTime + m + row["REFERENCEMan "] + ' <---> ' + row["MONTANT"]
                        print ('MEMES MONTANTS CONSTATES SUCCESSIVEMENT sur un même compte. ->', row["REFERENCEMan "],
                               row["MONTANT"])
            if frMntTime == '':
                frMntTime = 'aucune fraude  aprés/avant le temps de travail !'
                print('aucune fraude  aprés/avant le temps de travail  !')
            else:
                print('les fraudes liées au montant ---> ', frdMt)

            frMntReg = ''
            Regcount = 0
            print('****************Réglementation de change***************')

            for index, row in posts.iterrows():
                if row["TRANSCODEDESC "] == 'Credit':
                    for ind, raw in posts.iterrows():
                        if row["REFERENCEAuto"] != raw["REFERENCEAuto"] and int(row["MONTANT"]) == int(
                                raw["MONTANT"]) * (
                                -1) and raw["TRANSCODEDESC "] == 'Debit' and row["CURRENCCY"] != raw["CURRENCCY"]:
                            Regcount = Regcount + 1
                            m = "\n Réglementation de change. "
                            frMntReg = frMntReg + m + row["BN "] + ' <---> ' + row["MONTANT"]
                            print('Réglementation de change. ->', row["REFERENCEMan "], row["MONTANT"])
                elif row["TRANSCODEDESC "] == 'Debit':
                    for ind, raw in posts.iterrows():
                        if row["REFERENCEAuto"] != raw["REFERENCEAuto"] and int(row["MONTANT"]) == int(
                                raw["MONTANT"]) * (
                                -1) and raw["TRANSCODEDESC "] == 'Debit' and row["CURRENCCY"] != raw["CURRENCCY"]:
                            Regcount = Regcount + 1
                            m = "\n Réglementation de change. "
                            frMntReg = frMntReg + m + row["BN "] + ' <---> ' + row["MONTANT"]
                            print('Réglementation de change. ->', row["REFERENCEMan "], row["MONTANT"])
            if frMntReg == '':
                frMntReg = 'aucune fraude de Réglementation de change !'
                print('aRéglementation de change  !')
            else:
                print('les fraudes liées au montant ---> ', frdMt)

            d = 0
            c = 0
            for index, row in posts.iterrows():

                if row["TRANSCODEDESC "] == "Debit":
                    d = d + int(row["MONTANT"])
                    print('debit de ---> ', d)
                elif row["TRANSCODEDESC "] == "Credit":
                    c = c + int(row["MONTANT"])
                    print('credit de  ---> ', c)

            difCD = c + d
            print('TOTAL DES ECRITURES PAR REFERENCE AUTOMATIQUE Crée par le Système = ', difCD)

            if difCD == 0:
                tepr = 'une fraude TOTAL DES ECRITURES PAR REFERENCE AUTOMATIQUE Crée par le Système.'
            else:
                tepr = 'aucune fraude TOTAL DES ECRITURES PAR REFERENCE AUTOMATIQUE Crée par le Système (:'

            GBY = posts.groupby("USER")["APPLICATION"].nunique().to_frame()
            GBY = GBY.APPLICATION

            print(GBY)
            stj = 0
            frtj = ''

            for index, row in posts.iterrows():
                if int(row["BN"]) > 699999:
                    for ind, raw in posts.iterrows():
                        if row["BN"] == raw["BN"] and row["DATEOPERATION"] == raw["DATEOPERATION"]:
                            stj = stj + int(raw["MONTANT"])
                    if stj != 0:
                        if test(row["BN"]) == False:
                            m = 'totale de journée de compte interne est différent de zero. ->'
                            frtj = frtj, row["BN"], '/'
                            listBN.append(row["BN"])

            print('***********LES BN**********')

            print(listBN)
            taiBN = len(listBN)

            if frtj == '':
                frtj = 'aucune fraude liée au totale de journée de compte interne'
            else:
                m = 'totale de journée de compte interne est différent de zero. ->'
                frtj = m + str(listBN)

            return render(request, 'index.html',
                          {'Pfr': Pfr, 'GBY': GBY, 'frtj': frtj, 'taiBN': taiBN, 'frRef': frRef, 'difCD': difCD,
                           'tepr': tepr, 'tcount': tcount, 'IPfr': IPfr, 'IPfrN': IPfrN, 'Regcount': Regcount,
                           'frMntReg': frMntReg, 'sr': sr, 'frMntTime': frMntTime, 'PfrN': PfrN, 'fr': fr,
                           'frdMt': frdMt, 'frMnt': frMnt, 'frN': frN})

    else:
        print ('yoooooo')
        form = UploadFileForm()
    return render(request, 'uplod.html', {'form': form})



def fraude(request):
    posts = datfr('/home/vall/Documents/cv.pdf')
    posts["DATEOPERATION"] = pd.to_datetime(posts["DATEOPERATION"])
    posts["DATEVALEUR"] = pd.to_datetime(posts["DATEVALEUR"])
    delai = posts["DATEOPERATION"] - posts["DATEVALEUR"]

    taille = 0
    for index, row in posts.iterrows():
        taille = taille + 1
    print('taille de votre dataset ---> ', taille)

    fraud = []
    fr = 0
    frN = 0
    for d in delai:
        if d.days > 7:
            fraud.append(1)
            fr = fr + 1

        else:
            fraud.append(0)
            frN = frN + 1
    posts["fraude"] = fraud
    Pfr = fr / taille
    Pfr=Pfr*100
    IPfr=int(Pfr)

    PfrN = frN / taille
    PfrN=PfrN*100
    IPfrN=int(PfrN)

    Pfr=str(Pfr)
    Pfr=Pfr[0:5]
    PfrN=str(PfrN)
    PfrN = PfrN[0:5]

    sr = 0
    frRef = ''
    for index, row in posts.iterrows():
        for ind, raw in posts.iterrows():
            if row["REFERENCEMan "] == raw["REFERENCEMan "] and row["REFERENCEAuto"] != raw["REFERENCEAuto"] and row[
                "DATEOPERATION"] == raw["DATEOPERATION"]:
                sr = sr + 1
                m = 'une fraude liée au réfférence de manuel ->'
                frRef = frRef + m + str(row["REFERENCEMan "]) + '  /  ' + str(row["DATEVALEUR"]) + '\n'
                print('une fraude liée au réfférence de manuel ->', row["REFERENCEMan "], row["DATEVALEUR"])
    if frRef=='':
        frRef='aucune Fraude de réfference!'
    else:
        print('fraudes liée au réfference ---> ', sr)


    print(frRef)

    print('***************Montant**************')

    frdMt = 0
    frMnt = ''
    for index, row in posts.iterrows():
        for ind, raw in posts.iterrows():
            if row["REFERENCEMan "] == raw["REFERENCEMan "] and row["REFERENCEAuto"] != raw["REFERENCEAuto"] and row["MONTANT"] == raw["MONTANT"]:
                frdMt = frdMt + 1
                m = 'MEMES MONTANTS CONSTATES SUCCESSIVEMENT sur un même compte. ->'
                frMnt = frMnt + m + row["REFERENCEMan "] + ' <---> ' + row["MONTANT"]
                print('MEMES MONTANTS CONSTATES SUCCESSIVEMENT sur un même compte. ->', row["REFERENCEMan "],row["MONTANT"])

    if frMnt == '':
        frMnt = 'aucune fraudes liées au montant !'
        print('aucune fraudes liées au montant !')
    else:
        print('les fraudes liées au montant ---> ', frdMt)
    print('***************LES MONTANTS SUP 10000**************')

    posts["TIME"] = pd.to_datetime(posts["TIME"])
    posts['TIMES'] = posts["TIME"].dt.time
    time2= datetime.time(18,00,00)
    time1= datetime.time(7,00,00)
    frMntTime = ''
    tcount=0

    for index, row in posts.iterrows():
        for ind, raw in posts.iterrows():
            if int(row["MONTANT"])>10000 and row["REFERENCEAuto"]!=raw["REFERENCEAuto"] and row["REFERENCEMan "]==raw["REFERENCEMan "] and posts['TIMES']<time1:
                tcount=tcount+1
                m = "le temps de cette transaction est avant le temps  d'ouverture "
                frMntTime = frMntTime + m + row["REFERENCEMan "] + ' <---> ' + row["MONTANT"]
                print ('MEMES MONTANTS CONSTATES SUCCESSIVEMENT sur un même compte. ->',row["REFERENCEMan "], row["MONTANT"])
            elif int(row["MONTANT"])>10000 and row["REFERENCEAuto"]!=raw["REFERENCEAuto"] and row["REFERENCEMan "]==raw["REFERENCEMan "] and posts['TIMES']>time2:
                tcount = tcount + 1
                m = "le temps de cette transaction est aprés le temps  de fermeture --> "
                frMntTime = frMntTime + m + row["REFERENCEMan "] + ' <---> ' + row["MONTANT"]
                print ('MEMES MONTANTS CONSTATES SUCCESSIVEMENT sur un même compte. ->',row["REFERENCEMan "], row["MONTANT"])
    if frMntTime == '':
        frMntTime = 'aucune fraude  aprés/avant le temps de travail !'
        print('aucune fraude  aprés/avant le temps de travail  !')
    else:
        print('les fraudes liées au montant ---> ', frdMt)

    frMntReg = ''
    Regcount = 0
    print('****************Réglementation de change***************')

    for index, row in posts.iterrows():
        if row["TRANSCODEDESC "] == 'Credit':
            for ind, raw in posts.iterrows():
                if row["REFERENCEAuto"] != raw["REFERENCEAuto"] and int(row["MONTANT"]) == int(raw["MONTANT"]) * (
                -1) and raw["TRANSCODEDESC "] == 'Debit' and row["CURRENCCY"] != raw["CURRENCCY"]:
                    Regcount = Regcount + 1
                    m = "\n Réglementation de change. "
                    frMntReg = frMntReg + m + row["BN "] + ' <---> ' + row["MONTANT"]
                    print('Réglementation de change. ->', row["REFERENCEMan "], row["MONTANT"])
        elif row["TRANSCODEDESC "] == 'Debit':
            for ind, raw in posts.iterrows():
                if row["REFERENCEAuto"] != raw["REFERENCEAuto"] and int(row["MONTANT"]) == int(raw["MONTANT"]) * (
                -1) and raw["TRANSCODEDESC "] == 'Debit' and row["CURRENCCY"] != raw["CURRENCCY"]:
                    Regcount = Regcount + 1
                    m = "\n Réglementation de change. "
                    frMntReg = frMntReg + m + row["BN "] + ' <---> ' + row["MONTANT"]
                    print('Réglementation de change. ->', row["REFERENCEMan "], row["MONTANT"])
    if frMntReg == '':
        frMntReg = 'aucune fraude de Réglementation de change !'
        print('aRéglementation de change  !')
    else:
        print('les fraudes liées au montant ---> ', frdMt)

    d = 0
    c = 0
    for index, row in posts.iterrows():

        if row["TRANSCODEDESC "] == "Debit":
            d = d + int(row["MONTANT"])
            print('debit de ---> ', d)
        elif row["TRANSCODEDESC "] == "Credit":
            c = c + int(row["MONTANT"])
            print('credit de  ---> ', c)

    difCD = c + d
    print('TOTAL DES ECRITURES PAR REFERENCE AUTOMATIQUE Crée par le Système = ', difCD)

    if difCD == 0:
        tepr = 'une fraude TOTAL DES ECRITURES PAR REFERENCE AUTOMATIQUE Crée par le Système.'
    else:
        tepr = 'aucune fraude TOTAL DES ECRITURES PAR REFERENCE AUTOMATIQUE Crée par le Système (:'

    GBY = posts.groupby("USER")["APPLICATION"].nunique().to_frame()
    GBY=GBY.APPLICATION

    print(GBY)
    return render(request, 'index.html', {'Pfr': Pfr,'GBY':GBY,'frRef':frRef,'difCD':difCD,'tepr':tepr,'tcount':tcount,'IPfr':IPfr,'IPfrN':IPfrN,'Regcount':Regcount,'frMntReg':frMntReg,'sr':sr,'frMntTime':frMntTime, 'PfrN': PfrN, 'fr':fr, 'frdMt':frdMt,'frMnt':frMnt,'frN':frN})



def DifFraude(request):
    posts = datfr('/home/vall/Documents/cv.pdf')
    d = 0
    c = 0
    for index, row in posts.iterrows():

        if row["TRANSCODEDESC "] == "Debit":
            d = d + int(row["MONTANT"])
            print('debit de ---> ', d)
        elif row["TRANSCODEDESC "] == "Credit":
            c = c + int(row["MONTANT"])
            print('credit de  ---> ', c)

    difCD = c + d
    print('TOTAL DES ECRITURES PAR REFERENCE AUTOMATIQUE Crée par le Système = ', difCD)
    print('une fraude a été détécté !')
    frd = "n'exite pas une fraude liée au réfference"
    if difCD == 0:
        frd = 'une fraude a été détécté au niveau de credit / débit'
        return render(request, 'help.html', {'cv': frd})
    d=difCD/100
    return render(request, 'help.html', {'cvtail': d})
def datfr(path):
    df = pd.read_csv(path)
    return df
def test(a):

    for l in listBN:
        if a==l:
            return True

    return False