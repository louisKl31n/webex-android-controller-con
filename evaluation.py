from csv import writer
import requests
from datetime import datetime
import time


if __name__ == '__main__' :
    web_server = "http://127.0.0.1:5000"
    device_name1 = 'R3CR405S9DH'
    device_name2 = 'RFCT111C17X'
    emailctr = 0
    emails=[
        'qren5webex@gmail.com',
        'qren6webex@gmail.com',
        'qren7webex@gmail.com',
        'qren8webex@gmail.com',
        'qren1webex@gmail.com',
        'qren2webex@gmail.com',
        'qren4webex@gmail.com',
    ]
    email1 = 'qlan001webexbeta@gmail.com'
    email2 = 'qlan002webexbeta@gmail.com'
    token1 = 0
    token2 = 0
    phoneNumberWebexBeta1 = '0789182610'
    phoneNumberWebexBeta2 = '0789182611'

    while True:
        current_time = datetime.now().time()
        
        
        response = requests.post(web_server+'/connect', json={'deviceName': device_name1})
        token1 = response.json()['token']
        requests.post(web_server+'/log-in-bis', json={
                'deviceName': device_name1,
                'email': email1,
                'password': '1Sac2billes!',
                'token': token1,
        })
        emailctr = emailctr + 1
        response = requests.post(web_server+'/connect', json={'deviceName': device_name2})
        token2 = response.json()['token']
        requests.post(web_server+'/log-in-bis', json={
            'deviceName': device_name2,
            'email': email2,
            'password': '1Sac2billes!',
            'token': token2,
            })
        emailctr = emailctr + 1
        response =requests.post(web_server+'/call', json={
            'deviceName': device_name1,
            'token': token1,
            'destinationNumber': phoneNumberWebexBeta2
            })
        if response.status_code == 200 :
            requests.post(web_server+'/answer', json={
                'deviceName': device_name2,
                'token': token2,
                'incomingNumber': phoneNumberWebexBeta1
                })
            time.sleep(5)
            requests.post(web_server+'/mute', json={
                'deviceName': device_name1,
                'token': token1,
                })
            time.sleep(5)
            requests.post(web_server+'/unmute', json={
                'deviceName': device_name1,
                'token': token1,
                })
            time.sleep(5)
            requests.post(web_server+'/hold', json={
                'deviceName': device_name2,
                'token': token2,
                })
            time.sleep(5)
            requests.post(web_server+'/resume', json={
                'deviceName': device_name2,
                'token': token2,
                })
            requests.post(web_server+'/dtmf', json={
                'deviceName': device_name1,
                'token': token1,
                'dtmfSequence':'1234567890*#'
                })
            time.sleep(5)
            requests.post(web_server+'/hang-up', json={
                'deviceName': device_name1,
                'token': token1,
                })
        requests.post(web_server+'/log-out', json={
            'deviceName': device_name1,
            'token': token1,
            })
        
        requests.post(web_server+'/log-out', json={
            'deviceName': device_name2,
            'token': token2,
            })
        requests.post(web_server+'/disconnect', json={
            'deviceName': device_name1,
            'token': token1,
            })
        requests.post(web_server+'/disconnect', json={
            'deviceName': device_name2,
            'token': token2,
            })
        time.sleep(20)
 