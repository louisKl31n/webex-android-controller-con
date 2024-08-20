from csv import writer
import requests
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import PatternFill
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
redFill = PatternFill(start_color= "FF0000", end_color= "FF0000", fill_type="solid")
greenFill = PatternFill(start_color= "00FF00", end_color= "00FF00", fill_type="solid")

class Tests :
    #login
    def MNCQUALIF_10966_in(deviceName,email,token) :
        step1 = requests.post(web_server+'/log-in-bis', json={
            'deviceName': deviceName,
            'email': email,
            'password': '1Sac2billes!',
            'token': token,
            })
        return step1.status_code == 200

    #logout
    def MNCQUALIF_10966_out(deviceName,token) :
        step1 = requests.post(web_server+'/log-out', json={
            'deviceName': deviceName,
            'token': token,
            })
        return step1.status_code == 200 

    #check new IM
    def MNCQUALIF_10998() :
        step1 = requests.post(web_server+'/send-im', json={
        "deviceName" : deviceName2,
        "token" : token2,
        "targetMail" : "qlan3webex@gmail.com",
        "instantMessage" : "Ouais"
        })
        time.sleep(10)
        step2 = requests.post(web_server+'/check-new-im', json={
        'deviceName': deviceName1,
        'token': token1,
        'convName': "qRen001 webex"
        })
        return (step1.status_code == 200 and step2.status_code == 200)

    #check new GIM
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
            'deviceName': deviceName1,
            'token': token1,
            'convName': "Test 10999"
            })
        return (step1.status_code == 200 and step2.status_code == 200)

    #delete IM  
    def MNCQUALIF_11000() :
        step1 = requests.post(web_server+'/delete-im', json={
            'deviceName': deviceName1,
            'token': token1,
            'convName': "qRen001 webex"
            })
        return(step1.status_code == 200)
    
    #delete GIM
    def MNCQUALIF_11001() :
        step1 = requests.post(web_server+'/delete-gim', json={
            'deviceName': deviceName1,
            'token': token1,
            'convName': "Test 10999"
            })
        return(step1.status_code == 200)
    
    #delete call
    def MNCQUALIF_11004_a() :
        step1 = requests.post(web_server+'/delete-call', json={
            'deviceName': deviceName1,
            'token': token1,
            })
        return(step1.status_code == 200)
    
    #delete all call
    def MNCQUALIF_11004_b() :
        step1 = requests.post(web_server+'/delete-all-call', json={
            'deviceName': deviceName1,
            'token': token1,
            })
        return(step1.status_code == 200)

    #call from logs
    def MNCQUALIF_11005() :
        step1 = requests.post(web_server+'/call-from-logs', json={
            'deviceName': deviceName1,
            'token': token1,
            })
        time.sleep(5)
        step2 = requests.post(web_server+'/answer', json={
            'deviceName': deviceName2,
            'token': token2,
            'incomingNumber': phoneNumberWebexBeta1
            })
        time.sleep(5)
        step3 = requests.post(web_server+'/hang-up', json={
            'deviceName': device_name1,
            'token': token1,
            })
        return(step1.status_code == 200 and step2.status_code == 200 and step3.status_code == 200)

    #call normally
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

    #call on hold
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

    #video call
    def MNCQUALIF_11012() :
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

        step3 = requests.post(web_server+'/video-call', json={
            'deviceName': deviceName1,
            'token': token1
            })
        return(step1.status_code == 200)

    #blind transfer
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
            'token': token2,
            'transfertTarget' : transfertTarget
            })
        step4 = requests.post(web_server+'/hang-up', json={
            'deviceName': deviceName1,
            'token': token1,
            })
        return(step1.status_code == 200 and step2.status_code == 200 and step3.status_code == 200 and step4.status_code == 200)

    #supervised transfer
    def MNCQUALIF_11014() :
        step1 = requests.post(web_server+'/call', json={
            'deviceName': deviceName1,
            'token': token1,
            'incomingNumber': phoneNumberWebexBeta2
            })
        step2 = requests.post(web_server+'/answer', json={
            'deviceName': deviceName2,
            'token': token2,
            'incomingNumber': phoneNumberWebexBeta1
            })
        time.sleep(5)
        step3 = requests.post(web_server+'/supervised-transfert', json={
            'deviceName': deviceName2,
            'token': token2,
            'transfertTarget' : transfertTarget
            })
        step4 = requests.post(web_server+'/hang-up', json={
            'deviceName': deviceName1,
            'token': token1,
            })
        return(step1.status_code == 200 and step2.status_code == 200 and step3.status_code == 200 and step4.status_code == 200)


if __name__ == '__main__' :

    currentTime = datetime.now().time()
    filename = "CampagneBeta-"+str(currentTime)+".xlsx"
    wb = Workbook()
    sheet = wb.active

    response = requests.post(web_server+'/connect', json={'deviceName': deviceName1})
    token1 = response.json()['token']
    response = requests.post(web_server+'/connect', json={'deviceName': deviceName2})
    token2 = response.json()['token']

    """ MNCQUALIF-10996 """

    if Tests.MNCQUALIF_10966_in(deviceName2, email2, token2) :
        sheet.append(("MNCQUALIF-10996 login", "OK"))
        for cell in sheet[sheet.max_row] :
            cell.fill = greenFill
    else :
        sheet.append(("MNCQUALIF-10996 login", "KO"))
        for cell in sheet[sheet.max_row] :
            cell.fill = redFill
    if Tests.MNCQUALIF_10966_out(deviceName2, token2) :
        sheet.append(("MNCQUALIF-10996 logout", "OK"))
        for cell in sheet[sheet.max_row] :
            cell.fill = greenFill
    else :
        sheet.append(("MNCQUALIF-10996 logout", "KO"))
        for cell in sheet[sheet.max_row] :
            cell.fill = redFill



    Tests.MNCQUALIF_10966_in(deviceName1, email1, token1)
    Tests.MNCQUALIF_10966_in(deviceName2, email2, token2)

    time.sleep(2)
    """ MNCQUALIF-10998 """

    if Tests.MNCQUALIF_10998() :
        sheet.append(("MNCQUALIF-10998", "OK"))
        for cell in sheet[sheet.max_row] :
            cell.fill = greenFill
    else :
        sheet.append(("MNCQUALIF-10998", "KO"))
        for cell in sheet[sheet.max_row] :
            cell.fill = redFill
    time.sleep(2)
    """ MNCQUALIF-10999 """

    if Tests.MNCQUALIF_10999() :
        sheet.append(("MNCQUALIF-10999", "OK"))
        for cell in sheet[sheet.max_row] :
            cell.fill = greenFill
    else :
        sheet.append(("MNCQUALIF-10999", "KO"))
        for cell in sheet[sheet.max_row] :
            cell.fill = redFill
    time.sleep(2)
    """ MNCQUALIF-11000 """

    if Tests.MNCQUALIF_11000() :
        sheet.append(("MNCQUALIF-11000", "OK"))
        for cell in sheet[sheet.max_row] :
            cell.fill = greenFill
    else :
        sheet.append(("MNCQUALIF-11000", "KO"))
        for cell in sheet[sheet.max_row] :
            cell.fill = redFill
    time.sleep(2)
    """ MNCQUALIF-11001 """

    if Tests.MNCQUALIF_11001() :
        sheet.append(("MNCQUALIF-11001", "OK"))
        for cell in sheet[sheet.max_row] :
            cell.fill = greenFill
    else :
        sheet.append(("MNCQUALIF-11001", "KO"))
        for cell in sheet[sheet.max_row] :
            cell.fill = redFill
    time.sleep(2)
    """ MNCQUALIF-11009 """

    # if Tests.MNCQUALIF_11009() :
    #     sheet.append(("MNCQUALIF-11009", "OK"))
    #     for cell in sheet[sheet.max_row] :
    #         cell.fill = greenFill
    # else :
    #     sheet.append(("MNCQUALIF-11009", "KO"))
    #     for cell in sheet[sheet.max_row] :
    #         cell.fill = redFill
    # time.sleep(2)
    # """ MNCQUALIF-11005 """

    # if Tests.MNCQUALIF_11005() :
    #     sheet.append(("MNCQUALIF-11005", "OK"))
    #     for cell in sheet[sheet.max_row] :
    #         cell.fill = greenFill
    # else :
    #     sheet.append(("MNCQUALIF-11005", "KO"))
    #     for cell in sheet[sheet.max_row] :
    #         cell.fill = redFill
    # time.sleep(2)
    # """ MNCQUALIF-11005 """

    # if Tests.MNCQUALIF_11005() :
    #     sheet.append(("MNCQUALIF-11005", "OK"))
    #     for cell in sheet[sheet.max_row] :
    #         cell.fill = greenFill
    # else :
    #     sheet.append(("MNCQUALIF-11005", "KO"))
    #     for cell in sheet[sheet.max_row] :
    #         cell.fill = redFill
    # time.sleep(2)
    # """ MNCQUALIF-11004 """

    # if Tests.MNCQUALIF_11004_a() :
    #     sheet.append(("MNCQUALIF-11004 one deletion", "OK"))
    #     for cell in sheet[sheet.max_row] :
    #         cell.fill = greenFill
    # else :
    #     sheet.append(("MNCQUALIF-11004 one deletion", "KO"))
    #     for cell in sheet[sheet.max_row] :
    #         cell.fill = redFill
    # if Tests.MNCQUALIF_11004_b() :
    #     sheet.append(("MNCQUALIF-11004 all deletion", "OK"))
    #     for cell in sheet[sheet.max_row] :
    #         cell.fill = greenFill
    # else :
    #     sheet.append(("MNCQUALIF-11004 all deletion", "KO"))
    #     for cell in sheet[sheet.max_row] :
    #         cell.fill = redFill
    # time.sleep(2)
    # """ MNCQUALIF-11011 """

    # if Tests.MNCQUALIF_11005() :
    #     sheet.append(("MNCQUALIF-11011", "OK"))
    #     for cell in sheet[sheet.max_row] :
    #         cell.fill = greenFill
    # else :
    #     sheet.append(("MNCQUALIF-11011", "KO"))
    #     for cell in sheet[sheet.max_row] :
    #         cell.fill = redFill
            
    wb.save(filename=filename)