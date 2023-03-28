import requests
import pyttsx3
from datetime import datetime
import time


def check_period():
    now = datetime.now()
    date = now.strftime('%d/%m/%Y')
    midnight = datetime.strptime(f'{date} 00:00:00', '%d/%m/%Y %H:%M:%S')
    miday = datetime.strptime(f'{date} 12:00:00', '%d/%m/%Y %H:%M:%S')
    night = datetime.strptime(f'{date} 18:00:00', '%d/%m/%Y %H:%M:%S')

    if now >= midnight and now < miday:
        period = 'manha'
    elif  now >= miday and now < night:
        period = 'tarde'
    else:
        period = 'noite'  
    return date, period

def weather_forecast():
    url_inmet = 'https://apiprevmet3.inmet.gov.br/previsao/'
    geo_code_campinas = '3509502'
    url_local = f'{url_inmet}{geo_code_campinas}'
    response = requests.get(url_local)
    date, period = check_period()
    
    if response.status_code == 200:
        print(f'Status Code: {response}')
        json = response.json()
        temp_max = json[geo_code_campinas][date][period]["temp_max"]
        temp_min = json[geo_code_campinas][date][period]["temp_min"]
        intensity = json[geo_code_campinas][date][period]["int_vento"]
        resume = json[geo_code_campinas][date][period]["resumo"]

        print(f'Temperatura Maxima: {temp_max}')
        print(f'Temperatura Minima: {temp_min}')
        print(f'Intensidade do Vento: {intensity}')
        print(f'Resumo: {resume}')

        return temp_max, temp_min, intensity, resume, period

def robot_says():
    temp_max, temp_min, intensity, resume, period = weather_forecast()
    username = 'Filipe'
    robot = pyttsx3.init()

    if period == 'manha':
        greeting = 'Bom dia'    
    elif period == 'tarde':
        greeting = 'Boa Tarde'
    else:
        greeting = 'Boa Noite'
    
    robot_msg = f'{greeting} {username}, a temperatura máxima é de: {temp_max} graus, a temperatura mínima é de: {temp_min} graus, a vntensidade dos ventos são: {intensity}, Resumo. {resume} durante a {period}'
    
    robot.say(robot_msg)
    robot.runAndWait()


robot_says()