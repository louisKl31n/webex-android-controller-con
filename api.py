import string
import random
from controller import Controller
from flask import Flask, request,jsonify

app = Flask(__name__)
devices = {}
appium_servers ={
    'http://127.0.0.1:4724':'free',
    'http://127.0.0.1:4723':'free'
}


def authenticate_request(request):
    data = request.json
    device_name = data['deviceName']
    token = data['token']
    print(devices)
    for device in devices.values():
        print('device')
        print(device)
        print(device.appium_server_ip)
        print(device.driver)
    if devices[device_name].token == token :
        return devices[device_name]
    else :
        return False

def response(status_code,text) :
    resp = jsonify(text)
    resp.status_code = status_code
    return resp

@app.route('/connect', methods=['POST'])
def api_connect():
    device_name = request.json['deviceName']
    global devices
    global appium_servers
    already_in_use = False
    print(devices)
    for device in devices.values() :
        print(device.device_name)
        if device.device_name == device_name :
            already_in_use = True
    if already_in_use == False :
        new_device = Controller(device_name)
        new_device.token = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
        for appium_server_address, appium_server_status in appium_servers.items() :
            if(appium_server_status=='free'):
                new_device_appium_server_address = appium_server_address
        appium_servers[appium_server_address] = 'used'
        if new_device.webex_launch_app(new_device_appium_server_address):
            devices[device_name] = new_device
            print(devices)
            response = jsonify({
                'token': new_device.token
            })
            response.status_code = 200
    else :
        response = jsonify('Device : '+device_name+' is already in use')
        response.status_code = 401
    return response

@app.route('/log-in', methods=['POST'])
def api_log_in():
    device = authenticate_request(request)
    email = request.json['email']
    password = request.json['password']
    if(device != False) :
        device.webex_log_in(email,password)
        response = jsonify('Log in worked as expected')
        response.status_code = 200
    else :
        response = jsonify('Authentication with deviceName and token failed')
        response.status_code = 401
    return response

@app.route('/call', methods=['POST'])
def api_call():
    device = authenticate_request(request)
    destination_number = request.json['destinationNumber']
    if(device != False) :
        try :
            if (device.webex_call(destination_number) == 503) :
                response = jsonify('Webex telephony services unavailable')
                response.status_code = 503
            else :
                response = jsonify('Call worked as expected')
                response.status_code = 200
        except :
            response = jsonify('Call function failed')
            response.status_code = 503
        
    else :
        response = jsonify('Authentication with deviceName and token failed')
        response.status_code = 401
    return response

@app.route('/log-out', methods=['POST'])
def api_log_out():
    device = authenticate_request(request)
    if(device != False) :
        try :
            device.webex_log_out()
            response = jsonify('Log out worked as expected')
            response.status_code = 200
        except Exception as error:
            print(error)
            response = jsonify('Log out function failed')
            response.status_code = 503
        
    else :
        response = jsonify('Authentication with deviceName and token failed')
        response.status_code = 401
    return response

@app.route('/disconnect', methods=['POST'])
def api_disconnect():
    device = authenticate_request(request)
    device_name = request.json['deviceName']
    if(device != False) :
        appium_servers[device.appium_server_ip]='free'
        device.driver_quit()
        devices.pop(device_name)
        response = jsonify('Disconnection worked as expected')
        response.status_code = 200
    else :
        response = jsonify('Authentication with deviceName and token failed')
        response.status_code = 401
    return response

@app.route('/cancel', methods=['POST'])
def api_cancel():
    device = authenticate_request(request)
    if(device != False) :
        try :
            device.webex_cancel()
            resp = response(200,'Cancel function worked as expected')
        except : resp = response(503,'Call function failed')
    else : resp = response(401,'Authentication with deviceName and token failed')
    return resp

@app.route('/hang-up', methods=['POST'])
def api_hang_up():
    device = authenticate_request(request)
    if(device != False) :
        try :
            device.webex_hang_up()
            resp = response(200,'Hang up function worked as expected')
        except : resp = response(503,'Hang up function failed')
    else : resp = response(401,'Authentication with deviceName and token failed')
    return resp

@app.route('/dtmf', methods=['POST'])
def api_dtmf():
    device = authenticate_request(request)
    dtmf_sequence = request.json['dtmfSequence']
    if(device != False) :
        try :
            device.webex_dtmf(dtmf_sequence)
            resp = response(200,'DTMF function worked as expected')
        except : resp = response(503,'DTMF function failed')
    else : resp = resp(401,'Authentication with deviceName and token failed')
    return resp
 
@app.route('/hold', methods=['POST'])
def api_hold():
    device = authenticate_request(request)
    if(device != False) :
        try :
            device.webex_hold()
            resp = response(200,'Hold function worked as expected')
        except : resp = response(503,'Hold function failed')
    else : resp = response(401,'Authentication with deviceName and token failed')
    return resp

@app.route('/resume', methods=['POST'])
def api_resume():
    device = authenticate_request(request)
    if(device != False) :
        try :
            device.webex_hold()
            resp = response(200,'Resume function worked as expected')
        except : resp = response(503,'Resume function failed')
    else : resp = response(401,'Authentication with deviceName and token failed')
    return resp

@app.route('/mute', methods=['POST'])
def api_mute():
    device = authenticate_request(request)
    if(device != False) :
        try :
            device.webex_mute()
            resp = response(200,'Mute function worked as expected')
        except : resp = response(503,'Mute function failed')
    else : resp = response(401,'Authentication with deviceName and token failed')
    return resp

@app.route('/unmute', methods=['POST'])
def api_unmute():
    device = authenticate_request(request)
    if(device != False) :
        try :
            device.webex_unmute()
            resp = response(200,'Unmute function worked as expected')
        except : resp = response(503,'Unmute function failed')
    else : resp = response(401,'Authentication with deviceName and token failed')
    return resp

@app.route('/answer', methods=['POST'])
def api_answer():
    device = authenticate_request(request)
    incoming_number = request.json['incomingNumber']
    if(device != False) :
        try :
            if device.webex_answer(incoming_number) == 200 : response(200,'Call function worked as expected')
            else : resp = response(503,'Number dispayed doesn\'t match expected number')
        except : resp = response(503,'Answer function failed')
    else : resp = response(401,'Authentication with deviceName and token failed')
    return resp

@app.route('/decline', methods=['POST'])
def api_decline():
    device = authenticate_request(request)
    incoming_number = request.json['incomingNumber']
    if(device != False) :
        try :
            if device.webex_decline(incoming_number) == 200 : response(200,'Call function worked as expected')
            else : resp = response(503,'Number dispayed doesn\'t match expected number')
        except : resp = response(503,'Decline function failed')
    else : resp = response(401,'Authentication with deviceName and token failed')
    return resp

if __name__ == '__main__' :
    app.run(debug=True) 

    