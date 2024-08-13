from csv import writer
import requests
from datetime import datetime
from openpyxl import Workbook
import time

web_server = "http://127.0.0.1:5000"
""" Specifying the différent varibable for the devices """
deviceName1 = 'R3CR405S9DH'
deviceName2 = 'RFCT111C17X'
email1 = 'qlan3webex@gmail.com'
email2 = 'qren1webex@gmail.com'
token1 = 0
token2 = 0
phoneNumberWebexBeta1 = '0789182612'
phoneNumberWebexBeta2 = '0789182614'
transfertTarget = '0789182689'

class Tests :
    def MNCQUALIF_10966_in(deviceName,email,token) :
        step1 = requests.post(web_server+'/log-in-bis', json={
            'deviceName': deviceName,
            'email': email,
            'password': '1Sac2billes!',
            'token': token,
            })
        return step1.status_code == 200

    def MNCQUALIF_10966_out(deviceName,token) :
        step1 = requests.post(web_server+'/log-out', json={
            'deviceName': deviceName,
            'token': token,
            })
        return step1.status_code == 200 

    def MNCQUALIF_10998() :
        step1 = requests.post(web_server+'/send-im', json={
        "deviceName" : deviceName2,
        "token" : token2,
        "targetMail" : "qlan3webex@gmail.com",
        "instantMessage" : "Ouais"
        })
        time.sleep(10)
        step2 = requests.post(web_server+'/check-new-im', json={
        'deviceName': deviceName2,
        'token': token2,
        'convName': "qRen001 webex"
        })
        return (step1.status_code == 200 and step2.status_code == 200)

    def MNCQUALIF_10999() :
        step1 = requests.post(web_server+'/send-gim', json={
            "deviceName" : deviceName2,
            "token" : token2,
            "groupName" : "Test 10999",
            "targetMail" : "qlan3webex@gmail.com",
            "instantMessage" : "Ouais"
            })
        time.sleep(10)
        step2 = requests.post(web_server+'/check-new-im', json={
            'deviceName': deviceName2,
            'token': token2,
            'convName': "Test 10999"
            })
        return (step1.status_code == 200 and step2.status_code == 200)
    
    def MNCQUALIF_11000() :
        step1 = requests.post(web_server+'/delete-im', json={
            'deviceName': deviceName1,
            'token': token1,
            'convName': "qRen001 webex"
            })
        return(step1.status_code == 200)
    
    def MNCQUALIF_11001() :
        step1 = requests.post(web_server+'/delete-im', json={
            'deviceName': deviceName1,
            'token': token1,
            'convName': "Test 10999"
            })
        return(step1.status_code == 200)
    
    def MNCQUALIF_11004_a() :
        step1 = requests.post(web_server+'/delete-call', json={
            'deviceName': deviceName1,
            'token': token1,
            })
        return(step1.status_code == 200)
    
    def MNCQUALIF_11004_b() :
        step1 = requests.post(web_server+'/delete-all-call', json={
            'deviceName': deviceName1,
            'token': token1,
            })
        return(step1.status_code == 200)

    def MNCQUALIF_11005() :
        step1 = requests.post(web_server+'/call-from-logs', json={
            'deviceName': deviceName1,
            'token': token1,
            })
        return(step1.status_code == 200)

    def MNCQUALIF_11009() :    
        step1 = requests.post(web_server+'/call', json={
            'deviceName': deviceName1,
            'token': token1,
            'incomingNumber': phoneNumberWebexBeta2
            })
        time.sleep(5)
        step2 = requests.post(web_server+'/answer', json={
            'deviceName': deviceName2,
            'token': token2,
            'incomingNumber': phoneNumberWebexBeta1
            })
        time.sleep(5)
        step3 = requests.post(web_server+'/hang-up', json={
            'deviceName': deviceName1,
            'token': token1,
            })
        return (step1.status_code == 200 and step2.status_code == 200 and step3.status_code == 200)

    def MNCQUALIF_11011() :
        step1 = requests.post(web_server+'/call', json={
        'deviceName': deviceName1,
        'token': token1,
        'incomingNumber': phoneNumberWebexBeta2
        })
        time.sleep(5)
        step2 = requests.post(web_server+'/answer', json={
            'deviceName': deviceName2,
            'token': token2,
            'incomingNumber': phoneNumberWebexBeta1
            })
        time.sleep(5)
        step3 = requests.post(web_server+'/hold', json={
            'deviceName': deviceName2,
            'token': token2,
            })
        time.sleep(5)
        step4 = requests.post(web_server+'/resume', json={
            'deviceName': device_name2,
            'token': token2,
            })
        time.sleep(5)
        step5 = requests.post(web_server+'/hang-up', json={
            'deviceName': device_name1,
            'token': token1,
            })
        return (step1.status_code == 200 and step2.status_code == 200 and step3.status_code == 200 and step4.status_code == 200 and step5.status_code == 200)

    def MNCQUALIF_11012() :
        step1 = requests.post(web_server+'/video-call', json={
            'deviceName': deviceName1,
            'token': token1
            })
        return(step1.status_code == 200)

    def MNCQUALIF_11013() :
        step1 = requests.post(web_server+'/call', json={
            'deviceName': deviceName1,
            'token': token1,
            'incomingNumber': phoneNumberWebexBeta2
            })
        time.sleep(5)
        step2 = requests.post(web_server+'/answer', json={
            'deviceName': deviceName2,
            'token': token2,
            'incomingNumber': phoneNumberWebexBeta1
            })
        time.sleep(5)
        step3 = requests.post(web_server+'/blind-transfert', json={
            'deviceName': deviceName2,
            'token': token2
            'transfertTarget' : transfertTarget
            })
        step4 = requests.post(web_server+'/hang-up', json={
            'deviceName': deviceName1,
            'token': token1,
            })
        return(step1.status_code == 200 and step2.status_code == 200 and step3.status_code == 200 and step4.status_code == 200)

    def MNCQUALIF_11014() :
        step1 = requests.post(web_server+'/supervised-transfert', json={
            'deviceName': deviceName1,
            'token': token1
            'transfertTarget' : transfertTarget
            })
        return(step1.status_code == 200)


if __name__ == '__main__' :

    currentTime = datetime.now().time()
    wb = Workbook()
    sheet = wb.active

    response = requests.post(web_server+'/connect', json={'deviceName': deviceName1})
    token1 = response.json()['token']
    response = requests.post(web_server+'/connect', json={'deviceName': deviceName2})
    token2 = response.json()['token']

    """ MNCQUALIF-10996 """
    
    # if Tests.MNCQUALIF_10966_in(deviceName1,) :
    #     sheet.append(("MNCQUALIF-10996 login", "OK"))
    # else :
    #     sheet.append(("MNCQUALIF-10996 login", "KO"))

    if Tests.MNCQUALIF_10966_out() :
        sheet.append(("MNCQUALIF-10996 logout", "OK"))
    else :
        sheet.append(("MNCQUALIF-10996 logout", "KO"))

    
    