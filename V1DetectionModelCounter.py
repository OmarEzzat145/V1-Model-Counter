import requests
import json
import tkinter
from tkinter.ttk import *


def listV1DetectionModels():
    url_path = '/v2.0/xdr/dmm/models'
    token = str(APIKey_entry.get())
    if token == "":
        resultLabel.config(text="API Key is Empty, please enter one")
        return
    if combobox.get() == "":
        resultLabel.config(text="Risk Level is empty, please choose one")
        return
    elif combobox.get() == "All":
        query_params = {"risk": ""}
    else:
        query_params = {"risk": combobox.get()}

    match domaincombobox.get():
        case 'United States':
            url_base = 'https://api.xdr.trendmicro.com'
        case 'Singapore':
            url_base = 'https://api.sg.xdr.trendmicro.com'
        case 'Japan':
            url_base = 'https://api.xdr.trendmicro.co.jp'
        case 'India':
            url_base = 'https://api.in.xdr.trendmicro.com'
        case 'EU':
            url_base = 'https://api.eu.xdr.trendmicro.com'
        case 'Australia':
            url_base = 'https://api.au.xdr.trendmicro.com'
        case "":
            resultLabel.config(text="Regional Domain is empty, please choose one")
            return
    resultLabel.config(text="Requesting Detection Models...")
    headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json;charset=utf-8'}
    r = requests.get(url_base + url_path, params=query_params, headers=headers)

    print(r.status_code)

    if (r.status_code != 200):
        resultLabel.config(text="API Call failed\n" + json.dumps(r.json(), indent=4))
        return
    enabled = 0
    disabled = 0
    if 'application/json' in r.headers.get('Content-Type', ''):
        models = r.json()['data']
        for model in models:
            if (model.get("enabled") == False):
                disabled += 1
            elif (model.get("enabled") == True):
                enabled += 1

            resultLabel.config(
                text=f"Number of {combobox.get()} risk enabled models is {enabled}\n"f"Number of {combobox.get()} risk disabled models is {disabled}")
    else:
        print(r.text)


top = tkinter.Tk()
top.title("Vision One Detection Model counter via API")
top.geometry('600x300')
label = Label(top,
              text="Find out how many Detection Models you have enabled/disabled \n                                          Enter your API key")
label.pack()
frame = Frame(top).pack()
APIKey = tkinter.StringVar()
APIKey_entry = Entry(frame, textvariable=APIKey)
APIKey_entry.pack()

riskLabel = Label(top, text="Choose the Risk Level")
riskLabel.pack()

risk = tkinter.StringVar()
combobox = Combobox(frame, textvariable=risk)
combobox['values'] = ('Critical', 'High', 'Medium', 'Low', 'All')
combobox.pack()

domainlabel = Label(top, text="Choose the Vision One Regional Domain")
domainlabel.pack()

domain = tkinter.StringVar()
domaincombobox = Combobox(frame, textvariable=domainlabel)
domaincombobox['values'] = ('United States', 'Singapore', 'Japan', 'India', 'EU', 'Australia')
domaincombobox.pack()

button = Button(frame, text='Calculate the number of Detection Models', command=listV1DetectionModels).pack()
resultLabel = Label(top, text="")
resultLabel.pack()
top.mainloop()
