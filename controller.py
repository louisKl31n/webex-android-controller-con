from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.common import AppiumOptions
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
import time
import re
import os
import subprocess

class Controller:
    device_name = 'default'
    driver = 'default'
    appium_server_ip = 'default'
    timer_until_detection_timeout = 2 # Timeout timer in s
    frequency = 8 # Frequency of checks in Hz
    display_log = False

    def __init__(self,device_name):
        Controller.device_name = device_name
        print(device_name)

    def swipe_vertical(self,px) :
        """
        swipe_vertical swipes the screen up the given number of pixel

        :param px: number of pixel to swipe        
        """

        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(500, 1000)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(500, 1000-px)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    def print_log(self,str) :
        if self.display_log == True :
            print(str)

    def find_by_XPATH(self,XPATH) :
        """
        find_by_od function detects specified element with its XPATH. if element isn't found , throws an excpetion

        :param XPATH: appium XPATH of the element to search        
        """
        
        self.print_log('find_by_XPATH : '+XPATH)
        local_timer = self.timer_until_detection_timeout
        element =""
        while True:
            try :
                element = self.driver.find_element(by=AppiumBy.XPATH, value=XPATH)
            except :
                time.sleep(1/self.frequency)
                self.print_log('.')
                local_timer = local_timer - 1/self.frequency
                if local_timer <= 0 :
                    raise Exception('Couldn\'t find element :'+XPATH)
            else :
                self.print_log(' > Found')
                return element
            
    def find_by_id(self,id) :
        """
        find_by_od function detects specified element with its id. if element isn't found , throws an excpetion

        :param id: appium id of the element to search        
        """
        
        self.print_log('find_by_id : '+id)
        local_timer = self.timer_until_detection_timeout
        element =""
        while True:
            try :
                element = self.driver.find_element(by=AppiumBy.ID, value=id)
            except :
                time.sleep(1/self.frequency)
                self.print_log('.')
                local_timer = local_timer - 1/self.frequency
                if local_timer <= 0 :
                    raise Exception('Couldn\'t find element :'+id)
            else :
                self.print_log(' > Found')
                return element
            
    def find_by_XPATH_inside_parent(self,parent,XPATH) :
        """
        find_by_XPATH_inside_parent function detects specified element with its XPATH in the specified parent context. If element isn't found , throws an excpetion

        :param parent: appium parent to search in
        :param XPATH: appium XPATH of the element to search        
        """
        
        self.print_log('find_by_XPATH_inside_parent : '+XPATH)
        local_timer = self.timer_until_detection_timeout
        element =""
        while True:
            try :
                element = parent.find_element(by=AppiumBy.XPATH, value=XPATH)
            except :
                time.sleep(1/self.frequency)
                self.print_log('.')
                local_timer = local_timer - 1/self.frequency
                if local_timer <= 0 :
                    raise Exception('Couldn\'t find element :'+XPATH+' inside parent element')
            else :
                self.print_log(' > Found')
                return element
        
    def wait_until_element_is_displayed(self,XPATH,timeout) :
        """
        wait_until_element_is_displayed function waits until specified element with its XPATH is displayed before specified timeout. If element isn't found , throws an excpetion

        :param XPATH: appium XPATH of the element to search
        :param timeout: time period before throwing an exception        
        """ 
        self.print_log('wait_until_element_is_displayed : '+XPATH)
        while True:
            try :
                element = self.driver.find_element(by=AppiumBy.XPATH, value=XPATH)
            except :
                time.sleep(1/self.frequency)
                self.print_log('.')
                timeout = timeout - 1/self.frequency
                if timeout <= 0 :
                    raise Exception('Couldn\'t find element :'+XPATH+' until timeout')
            else :
                self.print_log(' > Displayed')
                return
            
    def wait_until_element_is_displayed_id(self,id,timeout) :
        """
        wait_until_element_is_displayed_id function waits until specified element with its XPATH is displayed before specified timeout. If element isn't found , throws an excpetion

        :param id: appium id of the element to search
        :param timeout: time period before throwing an exception        
        """

        self.print_log('wait_until_element_is_displayed : '+id)
        while True:
            try :
                element = self.driver.find_element(by=AppiumBy.ID, value=id)
            except :
                time.sleep(1/self.frequency)
                self.print_log('.')
                timeout = timeout - 1/self.frequency
                if timeout <= 0 :
                    raise Exception('Couldn\'t find element :'+id+' until timeout')
            else :
                self.print_log(' > Displayed')
                return

    def webex_launch_app(self,appium_server) :
        """
        launch_app launches a fresh inctance of the webex app
        """

        self.appium_server_ip = appium_server
        capabilities = {
            'udid' : self.device_name,
            'automationName' : 'UiAutomator2',
            'platformName' : 'Android',
            'platformVersion' : '13',
            'appPackage': 'com.cisco.wx2.android',
            'appActivity': 'com.webex.teams.WebexLauncherActivity',
            'autoGrantPermissions': True,
            'newCommandTimeout': 300
        }
        appium_options = AppiumOptions()
        appium_options.load_capabilities(capabilities)
        # Start appium server
        self.driver = webdriver.Remote(self.appium_server_ip,options=appium_options)
        return True

    def webex_log_in(self,email,password) :
        """
        webex_log_in function does the whole process of login in 

        :param email: is the email used through the process
        :param password: is the password used through the process
        """
        
        # Connection process inside the Webex application
        connection_button = self.find_by_XPATH('//android.widget.ScrollView/android.view.View[3]/android.widget.Button')
        connection_button.click()
        email_address_field = self.find_by_XPATH('//android.widget.TextView[@text="Adresse électronique"]/../..')
        email_address_field.send_keys(email)
        next_button = self.find_by_XPATH('//android.widget.ScrollView/android.view.View/android.widget.Button')
        next_button.click()
        # Connection process inside the Orange webview
        self.wait_until_element_is_displayed('//android.webkit.WebView[@text="Authentication B2B"]',10)
        orange_portal_webview = self.find_by_XPATH('//android.webkit.WebView[@text="Authentication B2B"]')
        orange_portal_id = self.find_by_XPATH_inside_parent(orange_portal_webview,'//android.widget.EditText')
        orange_portal_id.send_keys(email)
            # in order to have the connection button visible we need swipe
        self.swipe_vertical(300)
        orange_portal_next = self.find_by_XPATH_inside_parent(orange_portal_webview,'//android.widget.Button[@text="Suivant"]')
        orange_portal_next.click()
            # wait until the page loads to password view
        self.wait_until_element_is_displayed('//android.view.View[@text="Saisissez votre mot de passe"]',10)
        self.swipe_vertical(500)
        orange_portal_webview = self.find_by_XPATH('//android.webkit.WebView[@text="Authentication B2B"]')
        orange_portal_password = self.find_by_XPATH_inside_parent(orange_portal_webview,'//android.widget.EditText')
        orange_portal_password.send_keys(password)
            # in order to have the connection button visible we need swipe
        orange_portal_connect = self.find_by_XPATH_inside_parent(orange_portal_webview,'//android.widget.Button[@text="Se connecter"]')
        orange_portal_connect.click()
        # Check for a toasts from the application and accept it
        try :   
            self.wait_until_element_is_displayed('(//android.widget.ImageView[@resource-id="com.cisco.wx2.android:id/avatarBackground"])[1]',10)
        except :
            pass
        print('=> webex_log_in() success')

    def webex_log_out(self) :
        """
        log_out function logs out current user
        """

        webex_activity = {
            'intentAction':'android.intent.action.MAIN',
            'intentFlags': ['FLAG_ACTIVITY_CLEAR_TOP','FLAG_ACTIVITY_NEW_TASK'],
            'component':f'{"com.cisco.wx2.android"}/{"com.webex.teams.TeamsActivity"}'
        }
        self.driver.execute_script('mobile:startActivity',webex_activity)
        try : self.find_by_XPATH('//android.view.View[@content-desc="retour"]').click()
        except : pass
        print('mobile:startActivity DONE')
        avatar_icon = self.find_by_XPATH('(//android.widget.ImageView[@resource-id="com.cisco.wx2.android:id/avatarBackground"])[1]')
        avatar_icon.click()
        disconnect_button = self.find_by_XPATH('//android.widget.TextView[@resource-id="com.cisco.wx2.android:id/settingLabel" and @text="Déconnexion"]')
        disconnect_button.click()
        disconnect_toast_disconnect_button = self.find_by_XPATH('//android.widget.Button[@resource-id="android:id/button1"]')
        disconnect_toast_disconnect_button.click()
        try :
            self.wait_until_element_is_displayed('//android.view.View[@resource-id="onboarding_startScreen_joinAMeeting"]',10)
        except :
            print('=> webex_log_out() failed')
        print('=> webex_log_out() success')

    def webex_call(self,destinationNumber) :
        """
        call function calls specified Number
        
        :param destinationNumber: the phone number to call
        """

        webex_activity = {
            'intentAction':'android.intent.action.MAIN',
            'intentFlags': ['FLAG_ACTIVITY_CLEAR_TOP','FLAG_ACTIVITY_NEW_TASK'],
            'component':f'{"com.cisco.wx2.android"}/{"com.webex.teams.TeamsActivity"}'
        }
        self.driver.execute_script('mobile:startActivity',webex_activity)
        search_bar = self.find_by_id('com.cisco.wx2.android:id/searchIcon')
        search_bar.click()
        search_text = self.find_by_XPATH('//android.widget.EditText')
        search_text.send_keys(destinationNumber)
        call_button = self.find_by_id('com.cisco.wx2.android:id/callButton')
        call_button.click()
        # Check for a calling service unavailability
        try :
            self.find_by_XPATH('//android.widget.TextView[@resource-id="com.cisco.wx2.android:id/alertTitle"]')
            return 503
        except  :
            pass

        orange_phone_call_button = self.find_by_id('com.orange.phone:id/dialpad_floating_action_button')
        orange_phone_call_button.click()
        print('=> webex_call() success')
        return 200

    def wbex_call_from_logs(self) :
        webex_activity = {
            'intentAction':'android.intent.action.MAIN',
            'intentFlags': ['FLAG_ACTIVITY_CLEAR_TOP','FLAG_ACTIVITY_NEW_TASK'],
            'component':f'{"com.cisco.wx2.android"}/{"com.webex.teams.TeamsActivity"}'
        }
        self.driver.execute_script('mobile:startActivity',webex_activity)
        calls = self.find_by_XPATH('//android.widget.TextView[@text="Appels"]')
        calls.click()
        call_parent = self.find_by_XPATH('//androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[1]')
        call_icon = self.find_by_XPATH_inside_parent(call_parent,'//androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.widget.Button')
        call_icon.click()
        orange_phone_call_button = self.find_by_id('com.orange.phone:id/dialpad_floating_action_button')
        orange_phone_call_button.click()
        print('=> webex_call() success')
        return 200


    def webex_cancel(self) :
        """
        cancel function refuses incomming call
        """

        end_call_action_button = self.find_by_id('com.orange.phone:id/floating_end_call_action_button')
        end_call_action_button.click()
        print('=> webex_cancel() success')
    
    def webex_hang_up(self) :
        """
        hang_up function hangs up current call
        """

        end_call_action_button = self.find_by_id('com.orange.phone:id/floating_end_call_action_button')
        end_call_action_button.click()
        print('=> webex_hang_up() success')

    def webex_dtmf(self,dtmf_sequence):
        """
        dtmf function plays a dtmf sequence during a call 
        
        :param dtmf_sequence: the dtmf sequence to play during the call 
        """

        diaplpad_button = self.find_by_id('com.orange.phone:id/dialpadButton')
        diaplpad_button.click()
        dtmf_elements_id = {
                    '1':'com.orange.phone:id/dialpad_key_1',
                    '2':'com.orange.phone:id/dialpad_key_2',
                    '3':'com.orange.phone:id/dialpad_key_3',
                    '4':'com.orange.phone:id/dialpad_key_4',
                    '5':'com.orange.phone:id/dialpad_key_5',
                    '6':'com.orange.phone:id/dialpad_key_6',
                    '7':'com.orange.phone:id/dialpad_key_7',
                    '8':'com.orange.phone:id/dialpad_key_8',
                    '9':'com.orange.phone:id/dialpad_key_9',
                    '0':'com.orange.phone:id/dialpad_key_0',
                    '*':'com.orange.phone:id/dialpad_key_star',
                    '#':'com.orange.phone:id/dialpad_key_hash'
                }
        print(dtmf_sequence)
        print(len(dtmf_sequence))
        for index in range( len(dtmf_sequence) ) :
            time.sleep(0.5)
            dtmf = dtmf_sequence[index]
            print(dtmf)
            try :
                print(dtmf_elements_id[dtmf])
                dtmf_key = self.find_by_id(dtmf_elements_id[dtmf])
                dtmf_key.click()
            except:
                pass
        diaplpad_button.click()

    def webex_hold(self):
        """
        hold function puts on hold a call
        """

        more_button = self.find_by_id('com.orange.phone:id/call_screen_more_id')
        more_button.click()
        hold_button = self.find_by_XPATH('(//android.widget.LinearLayout[@resource-id="com.orange.phone:id/content"])[1]')
        hold_button.click()

    def webex_resume(self):
        """
        resume function resumes a call put on hold 
        """

        more_button = self.find_by_id('com.orange.phone:id/call_screen_more_id')
        more_button.click()
        hold_button = self.find_by_XPATH('(//android.widget.LinearLayout[@resource-id="com.orange.phone:id/content"])[1]')
        hold_button.click()

    def webex_mute(self):
        """
        mute function mutes the microphone during a call
        """
        
        mute_button = self.find_by_id('com.orange.phone:id/muteButton')
        mute_button.click()

    def webex_unmute(self):
        """
        unmute function unmutes the microphone during a call
        """

        unmute_button = self.find_by_id('com.orange.phone:id/muteButton')
        unmute_button.click()

    def webex_answer(self, incoming_number):
        """
        answer function answers the call from the incoming_number
        
        :param incoming_number: phone number of the caller
        """

        print('Before regex : '+incoming_number)
        regex = r'((\+\d{1,3})|(0)(?P<number>\d+))'
        number = re.search(regex, incoming_number).group('number')
        print('After regex : '+number)
        self.wait_until_element_is_displayed_id('com.orange.phone:id/answer_button',10)
        number_found_in_sys = self.driver.execute_script('mobile: shell',{'command' : 'dumpsys telephony.registry | grep mCallI'})
        print('Dumpsys : '+number_found_in_sys)
        if number not in number_found_in_sys :
            return 503
        self.driver.execute_script('mobile: shell',{'command' : 'input keyevent KEYCODE_CALL'})
        return 200

    def webex_play_audio(self) :
        """
        This function plays an audio file to simulate a conversation during a call. Call should be ongoing before using this function
        """
        escaped_path = "/Stockage interne/Music/Appium/Monologue.mp3"
        subprocess.run(["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", "file:///Stockage\\ interne/Music/Appium/Monologue.mp3", "-t", "audio/mp3"])
        # os.system(f'adb shell am start -a android.intent.action.VIEW -d "file:///Stockage\\ interne/Music/Appium/Monologue.mp3" -t audio/mp3')

    def webex_decline(self, incoming_number):
        """
        decline function declines the call from the incoming_number
        
        :param incoming_number: phone number of the caller
        """

        print('Before regex : '+incoming_number)
        regex = r'((\+\d{1,3})|(0)(?P<number>\d+))'
        number = re.search(regex, incoming_number).group('number')
        print('After regex : '+number)
        self.wait_until_element_is_displayed_id('com.orange.phone:id/answer_button',10)
        number_found_in_sys = self.driver.execute_script('mobile: shell',{'command' : 'dumpsys telephony.registry | grep mCallI'})
        print('Dumpsys  : '+number_found_in_sys) 
        if number not in number_found_in_sys :
            return 503
        self.driver.execute_script('mobile: shell',{'command' : 'input keyevent KEYCODE_ENDCALL'})
        return 200

    def webex_send_im(self, target_mail, message) :
        """
        send_im function creates a conv with the target_mail user and sends an instant message

        :param target_mail: the mail to use to retreive the member to add
        :param instant_message: the instant message to send
        """
         #Go to instant message creation menu
        messages_menu = self.find_by_id('com.cisco.wx2.android:id/fab_menu_button')
        messages_menu.click()
        instant_message = self.find_by_id('com.cisco.wx2.android:id/send_message_menu_item')
        instant_message.click()
        #Go to select person menu 
        add_person =  self.find_by_id('com.cisco.wx2.android:id/addPersonText')
        add_person.click()
        search_person= self.find_by_id('com.cisco.wx2.android:id/recipients')
        search_person.send_keys(target_mail)
        #try to create conversation (only works if target_mail user is found )
        try :
            select_person= self.find_by_id('com.cisco.wx2.android:id/addPeopleRow')
            select_person.click()
            create_conversation = self.find_by_XPATH('//android.widget.Button[@resource-id="com.cisco.wx2.android:id/createSpaceButton"]')
            create_conversation.click()
            #send instant message in conv
            print('=> trying to write')
            message_text = self.find_by_id('com.cisco.wx2.android:id/message')
            message_text.send_keys(message)
            send_button = self.find_by_id('com.cisco.wx2.android:id/send')
            send_button.click()
            back_button = self.find_by_XPATH('//android.widget.ImageButton[@content-desc="retour"]')
            back_button.click()
            return 200
        except : 
            print('=> user not found ')
            return 404
       
    def webex_check_if_im_received(self, conv_name) :
        try :
        #self.wait_until_element_is_displayed('//android.widget.LinearLayout[@content-desc="qRen001 webex, ,Nouveaux messages"]',3)
            message_tab = self.find_by_XPATH('//android.widget.TextView[@text="Messages"]')
            message_tab.click()
            new_message = self.find_by_XPATH('//android.widget.LinearLayout[@content-desc="' + conv_name + ', ,Nouveaux messages"]')
            new_message.click()
            back_button = self.find_by_XPATH('//android.widget.ImageButton[@content-desc="retour"]')
            back_button.click()
            return 200
        except :
            return 503

    def webex_send_group_im(self, group_name, target_mail, message) :
        """
        send_group_im function creates a group conv with the target_mail user and sends an group message
        
        :param group_name: the name of the group conversation
        :param target_mail: the mail to use to retreive the member to add
        :param message: the instant message to send 
        """
        #Go to group message creation menu
        messages_menu = self.find_by_id('com.cisco.wx2.android:id/fab_menu_button')
        messages_menu.click()
        instant_message = self.find_by_id('com.cisco.wx2.android:id/create_space_menu_item')
        instant_message.click()
        #Go to adding person menu 
        add_person =  self.find_by_id('com.cisco.wx2.android:id/add_person_text')
        add_person.click()
        search_person= self.find_by_id('com.cisco.wx2.android:id/recipients')
        search_person.send_keys(target_mail)
        #try to search and add target_mail user
        try :
            select_person= self.find_by_id('com.cisco.wx2.android:id/addPeopleRow')
            select_person.click()
            confirm_button = self.find_by_id('com.cisco.wx2.android:id/ok')
            confirm_button.click()
            #name the group 
            name_group = self.find_by_XPATH('//android.widget.EditText')
            name_group.send_keys(group_name)
            #create the conv
            create_conversation = self.find_by_id('com.cisco.wx2.android:id/createSpaceButton')
            create_conversation.click()
            #send instant_message in conv 
            message_text = self.find_by_id('com.cisco.wx2.android:id/message')
            message_text.send_keys(message)
            send_button = self.find_by_id('com.cisco.wx2.android:id/send')
            send_button.click()
            back_button = self.find_by_XPATH('//android.widget.ImageButton[@content-desc="retour"]')
            back_button.click()
            return 200
        except : 
            print('=> user not found ')
            return 404

    def webex_power_up(self) :
        """
        powerup function does the whole process of transitionning from dialer call to webex call
        Webex call overlay must be activated and a call ongoing
        This function will use the notification feature
        """
        print('=> opening notification bar')
        self.driver.open_notifications()
        print('=> notification bar opened')
        webex_notification= self.find_by_XPATH('//android.widget.TextView[@resource-id="android:id/title" and @text="Gérer cet appel avec Webex"]')
        webex_notification.click()

    def webex_video_call(self) :
        """
        video_call function does the process of transitionning from powered up call to webex video call
        The call must be ongoing and powered up (on both sides)
        """
        
        video_call = self.find_by_XPATH('//androidx.compose.ui.platform.ComposeView[@resource-id="com.cisco.wx2.android:id/call_control_view"]/android.view.View/android.view.View/android.view.View[4]/android.widget.Button')
        video_call.click()

    def webex_blind_transfert(self,transfert_target) :
        """
        blind_transfert does the whole process of blind transfering the call to target number 
        This function needs the power up state 
        
        :param transfert_target: the phone number the call should be transferted to
        """
        #Open transfert menu
        transfert_button = self.find_by_XPATH('//android.view.View[@content-desc="Transfert"]')
        transfert_button.click()
        #Specify target number
        target= self.find_by_XPATH('//android.widget.EditText[@resource-id="com.cisco.wx2.android:id/recipients"]')
        target.send_keys(transfert_target)
        #Initiate transfert
        call= self.find_by_XPATH('//android.widget.ImageView[@content-desc="Appeler directement"]')
        call.click()
        #chose blind transfert
        blind_transfert= self.find_by_XPATH('//android.widget.TextView[@text="Transfert"]')
        blind_transfert.click()
    
    def webex_supervised_transfert(self,transfert_target) :
        """
        supervised_transfert does the whole process of doing a supervised transfert to target number 
        This function needs the power up state 
        
        :param transfert_target: the phone number the call should be transferted to 
        """
        #Open transfert menu
        transfert_button = self.find_by_XPATH('//android.view.View[@content-desc="Transfert"]')
        transfert_button.click()
        #Specify target number
        target= self.find_by_XPATH('//android.widget.EditText[@resource-id="com.cisco.wx2.android:id/recipients"]')
        target.send_keys(transfert_target)
        #Initiate transfert
        call= self.find_by_XPATH('//android.widget.ImageView[@content-desc="Appeler directement"]')
        call.click()
        #chose supervised transfert
        blind_transfert= self.find_by_XPATH('//android.widget.TextView[@text="Consulter en premier"]')
        blind_transfert.click()
        #start call to transfert 
        call= self.find_by_XPATH('//android.widget.ImageButton[@content-desc="Appeler"]')
        call.click()
        #wait pick up then power up the temp call
        #todo : multhread to pick up during this function 
        time.sleep(20)
        print("=> powering up temp call")
        self.webex_power_up()
        #finish transfert
        transfert_button= self.find_by_XPATH('//android.widget.TextView[@text="Transfert"]')
        transfert_button.click()       

    def webex_configure_CFNA(self,forward_target) :
        """
        configure_CFNA configures a call forward no answer using the advanced call options on webex android 
        
        :param forward_target: the phone number to which calls should be forwarded
        """

        self.wait_until_element_is_displayed('(//android.widget.ImageView[@resource-id="com.cisco.wx2.android:id/avatarBackground"])[1]',5)
        #open user menu
        user_menu = self.find_by_XPATH('(//android.widget.ImageView[@resource-id="com.cisco.wx2.android:id/avatarBackground"])[1]')
        user_menu.click()
        #open call params
        parameters = self.find_by_XPATH('//android.view.ViewGroup[@content-desc="Bouton Paramètres"]')
        parameters.click()
        call_options = self.find_by_XPATH('//android.view.ViewGroup[@content-desc="Bouton Appels"]')
        call_options.click()
        advanced_call_options = self.find_by_XPATH('//androidx.recyclerview.widget.RecyclerView[@resource-id="com.cisco.wx2.android:id/calling_settings_list"]/android.widget.LinearLayout[1]')
        advanced_call_options.click()
        #todo : check if already opened
        #open incoming call options
        self.wait_until_element_is_displayed('//android.view.View[@text="Appels entrants"]',10)
        incoming_call = self.find_by_XPATH('//android.view.View[@text="Appels entrants"]')
        incoming_call.click()
        #open call forward config
        call_forward = self.find_by_XPATH('//android.widget.TextView[@text="Renvoi d \'appel"]')
        call_forward.click()
        no_answer_activation = self.find_by_XPATH('//android.webkit.WebView[@text="BWCallSettingsWeb"]/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View[3]/android.view.View[2]/android.view.View[1]/android.view.View[2]/android.view.View/android.view.View/android.widget.ToggleButton')
        #todo : check if already checked 
        no_answer_activation.click()
        forward_section= self.find_by_XPATH('//android.webkit.WebView[@text="BWCallSettingsWeb"]/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View[3]/android.view.View[2]/android.view.View[2]/android.view.View/android.view.View[1]')
        forward_number= self.find_by_XPATH_inside_parent(forward_section,'//android.widget.EditText')
        forward_number.send_keys(forward_target)
        forward_number.click()
        self.driver.press_keycode(66)
        time.sleep(2)
        try: 
            print('=> checking if activation worked')
            activation= self.find_by_XPATH('//android.widget.TextView[@text="Activé"]')
            #returning to main menu
            back_button = self.find_by_XPATH('(//android.widget.ImageButton[@content-desc="retour"])[1]')
            back_button.click()
            back_button = self.find_by_XPATH('(//android.widget.ImageButton[@content-desc="retour"])[2]')
            back_button.click()
            back_button = self.find_by_XPATH('//android.widget.ImageButton[@content-desc="retour"]')
            back_button.click()
            return 200
        except :
            try: 
                error= self.find_by_XPATH_inside_parent(forward_section,'//android.view.View[@text="Impossible de mettre à jour les données. Réessayez ou contactez l\'administrateur. Code: (400)"]')
                return 400
            except:
                pass

    def webex_configure_CFBusy(self,forward_target) :
        """
         configure_CFBusy configures a call forward busy using the advanced call options on webex android 
        
        :param forward_target: the phone number to which calls should be forwarded
        """

        self.wait_until_element_is_displayed('(//android.widget.ImageView[@resource-id="com.cisco.wx2.android:id/avatarBackground"])[1]',5)
        #open user menu
        user_menu = self.find_by_XPATH('(//android.widget.ImageView[@resource-id="com.cisco.wx2.android:id/avatarBackground"])[1]')
        user_menu.click()
        #open call params
        parameters = self.find_by_XPATH('//android.view.ViewGroup[@content-desc="Bouton Paramètres"]')
        parameters.click()
        call_options = self.find_by_XPATH('//android.view.ViewGroup[@content-desc="Bouton Appels"]')
        call_options.click()
        advanced_call_options = self.find_by_XPATH('//androidx.recyclerview.widget.RecyclerView[@resource-id="com.cisco.wx2.android:id/calling_settings_list"]/android.widget.LinearLayout[1]')
        advanced_call_options.click()
        #todo : check if already opened
        #open incoming call options
        incoming_call = self.find_by_XPATH('//android.view.View[@text="Appels entrants"]')
        incoming_call.click()
        #open call forward config
        call_forward = self.find_by_XPATH('//android.widget.TextView[@text="Renvoi d \'appel"]')
        call_forward.click()
        busy_activation = self.find_by_XPATH('//android.webkit.WebView[@text="BWCallSettingsWeb"]/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View[3]/android.view.View[2]/android.view.View[2]/android.view.View[2]/android.view.View/android.view.View/android.widget.ToggleButton')
        #todo : check if already checked 
        busy_activation.click()
        forward_section= self.find_by_XPATH('//android.webkit.WebView[@text="BWCallSettingsWeb"]/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View[3]/android.view.View[2]/android.view.View[3]/android.view.View')
        forward_number= self.find_by_XPATH_inside_parent(forward_section,'//android.widget.EditText')
        forward_number.send_keys(forward_target)
        forward_number.click()
        self.driver.press_keycode(66)
        time.sleep(2)
        try: 
            print('=> checking if activation worked')
            activation= self.find_by_XPATH('//android.widget.TextView[@text="Activé"]')
            #returning to main menu
            back_button = self.find_by_XPATH('(//android.widget.ImageButton[@content-desc="retour"])[1]')
            back_button.click()
            back_button = self.find_by_XPATH('(//android.widget.ImageButton[@content-desc="retour"])[2]')
            back_button.click()
            back_button = self.find_by_XPATH('//android.widget.ImageButton[@content-desc="retour"]')
            back_button.click()
            return 200
        except :
            print('=> Aïe')
            try: 
                error= self.find_by_XPATH_inside_parent(forward_section,'//android.view.View[@text="Impossible de mettre à jour les données. Réessayez ou contactez l\'administrateur. Code: (400)"]')
                print('=> Oula')
                return 400
            except:
                pass
        
    def webex_configure_CFNR(self,forward_target) :
        """
        configure_CFNR configure a call forward not reachable using the advanced call options on webex android 
        
        :param forward_target: the phone number to which calls should be forwarded
        """

        self.wait_until_element_is_displayed('(//android.widget.ImageView[@resource-id="com.cisco.wx2.android:id/avatarBackground"])[1]',5)
        #open user menu
        user_menu = self.find_by_XPATH('(//android.widget.ImageView[@resource-id="com.cisco.wx2.android:id/avatarBackground"])[1]')
        user_menu.click()
        #open call params
        parameters = self.find_by_XPATH('//android.view.ViewGroup[@content-desc="Bouton Paramètres"]')
        parameters.click()
        call_options = self.find_by_XPATH('//android.view.ViewGroup[@content-desc="Bouton Appels"]')
        call_options.click()
        advanced_call_options = self.find_by_XPATH('//androidx.recyclerview.widget.RecyclerView[@resource-id="com.cisco.wx2.android:id/calling_settings_list"]/android.widget.LinearLayout[1]')
        advanced_call_options.click()
        #todo : check if already opened
        #open incoming call options
        incoming_call = self.find_by_XPATH('//android.view.View[@text="Appels entrants"]')
        incoming_call.click()
        #open call forward config
        call_forward = self.find_by_XPATH('//android.widget.TextView[@text="Renvoi d \'appel"]')
        call_forward()
        not_reachable_activation = self.find_by_XPATH('//android.webkit.WebView[@text="BWCallSettingsWeb"]/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View[3]/android.view.View[2]/android.view.View[4]/android.view.View[2]/android.view.View/android.view.View/android.widget.ToggleButton')
        #todo : check if already checked 
        not_reachable_activation
        forward_section= self.find_by_XPATH('//android.webkit.WebView[@text="BWCallSettingsWeb"]/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View[3]/android.view.View[2]/android.view.View[4]/android.view.View')
        forward_number= self.find_by_XPATH_inside_parent(forward_section,'//android.widget.EditText')
        forward_number.send_keys(forward_target)
        forward_number.click()
        self.driver.press_keycode(66)
        time.sleep(2)
        try: 
            print('=> checking if activation worked')
            activation= self.find_by_XPATH('//android.widget.TextView[@text="Activé"]')
            #returning to main menu
            back_button = self.find_by_XPATH('(//android.widget.ImageButton[@content-desc="retour"])[1]')
            back_button.click()
            back_button = self.find_by_XPATH('(//android.widget.ImageButton[@content-desc="retour"])[2]')
            back_button.click()
            back_button = self.find_by_XPATH('//android.widget.ImageButton[@content-desc="retour"]')
            back_button.click()
            return 200
        except :
            try: 
                error= self.find_by_XPATH_inside_parent(forward_section,'//android.view.View[@text="Impossible de mettre à jour les données. Réessayez ou contactez l\'administrateur. Code: (400)"]')
                return 400
            except:
                pass

    def webex_join_callcenter(self) :
        # Open menu 
        self.wait_until_element_is_displayed('(//android.widget.ImageView[@resource-id="com.cisco.wx2.android:id/avatarBackground"])[1]',5)
        menu = self.find_by_XPATH('(//android.widget.ImageView[@resource-id="com.cisco.wx2.android:id/avatarBackground"])[1]')
        menu.click()
        # Open call center settings
        ccSettings = self.find_by_XPATH('//android.widget.TextView[@resource-id="com.cisco.wx2.android:id/settingLabel" and @text="Files d’attente d’appels"]')
        ccSettings.click()
        # Change agent status
        status = self.find_by_XPATH('//android.widget.TextView[@resource-id="com.cisco.wx2.android:id/agentStatus"]')
        if status.get_attribute('text') != "Disponible(s)" :
            status.click()
            # Select "Available"
            available = self.find_by_XPATH('//android.widget.TextView[@resource-id="com.cisco.wx2.android:id/acd_status_title" and @text="Disponible(s)"]')
            available.click()
            #back to main screen
            back_button= self.find_by_XPATH('//android.widget.ImageButton[@content-desc="retour"]')
            back_button.click()
            back_button= self.find_by_XPATH('//android.widget.ImageButton[@content-desc="retour"]')
            back_button.click()
        else :
            back_button= self.find_by_XPATH('//android.widget.ImageButton[@content-desc="retour"]')
            back_button.click()     

    def webex_leave_callcenter(self) :
        # Open menu 
        self.wait_until_element_is_displayed('(//android.widget.ImageView[@resource-id="com.cisco.wx2.android:id/avatarBackground"])[1]',5)
        menu = self.find_by_XPATH('(//android.widget.ImageView[@resource-id="com.cisco.wx2.android:id/avatarBackground"])[1]')
        menu.click()
        # Open call center settings
        ccSettings = self.find_by_XPATH('//android.widget.TextView[@resource-id="com.cisco.wx2.android:id/settingLabel" and @text="Files d’attente d’appels"]')
        ccSettings.click()
        # Change agent status
        status = self.find_by_XPATH('//android.widget.TextView[@resource-id="com.cisco.wx2.android:id/agentStatus"]')
        status.click()
        # Select "Available"
        disconnected = self.find_by_XPATH('//android.widget.TextView[@resource-id="com.cisco.wx2.android:id/acd_status_title" and @text="Déconnecté"]')
        disconnected.click()
        #back to main screen
        back_button= self.find_by_XPATH('//android.widget.ImageButton[@content-desc="retour"]')
        back_button.click()
        back_button= self.find_by_XPATH('//android.widget.ImageButton[@content-desc="retour"]')
        back_button.click()

    def webex_open_widget(self) :
        widget = self.find_by_XPATH('//android.appwidget.AppWidgetHostView[@content-desc="Paramètres d’appel"]')
        open_settings = self.find_by_XPATH_inside_parent(widget,'//android.widget.ImageView[@content-desc="Paramètres"]')
        open_settings.click()
        try :
            self.find_by_id('com.cisco.wx2.android:id/teams_activity_first_pane')
            return 200
        except :
            return 404

    def driver_quit(self) :
        self.driver.quit()


    def webex_delete_im(self, conv_name) :
        try : 
            actions = ActionChains(self.driver)
            message_tab = self.find_by_XPATH('//android.widget.TextView[@text="Messages"]')
            message_tab.click()
            message = self.find_by_XPATH('//android.widget.LinearLayout[@content-desc="'+ conv_name + ', ,"]')
            actions.click_and_hold(message).pause(2).release().perform()
            delete_button = self.find_by_XPATH('//android.widget.TextView[@content-desc="bouton Quitter"]')
            delete_button.click()
            return 200
        except :
            return 503
        
    def webex_delete_call(self) :
        try : 
            actions = ActionChains(self.driver)
            message_tab = self.find_by_XPATH('//android.widget.TextView[@text="Appels"]')
            message_tab.click()
            call = self.find_by_XPATH('//androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[1]')
            actions.click_and_hold(call).pause(2).release().perform()
            delete_button = self.find_by_XPATH('//android.widget.TextView[@resource-id="com.cisco.wx2.android:id/primary_text" and @text="Supprimer"]')
            delete_button.click()
            return 200
        except :
            return 503

    def webex_delete_call(self) :
        try : 
            actions = ActionChains(self.driver)
            message_tab = self.find_by_XPATH('//android.widget.TextView[@text="Appels"]')
            message_tab.click()
            call = self.find_by_XPATH('//androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[1]')
            actions.click_and_hold(call).pause(2).release().perform()
            selectPlus_button = self.find_by_XPATH('//android.widget.TextView[@resource-id="com.cisco.wx2.android:id/primary_text" and @text="Sélectionner plus"]')
            selectPlus_button.click()
            selectAll_button = self.find_by_XPATH('//android.widget.TextView[@text="Tout sélectionner"]')
            selectAll_button.click()
            delete_button = self.find_by_XPATH('//android.widget.TextView[@text="Supprimer"]')
            delete_button.click()
            return 200
        except :
            return 503

    def webex_log_in_bis(self,email,password) :
        """
        webex_log_in_bis function does the whole process of login in a bis case (TM Qualif Vo-Wi-Fi)

        :param email: is the email used through the process
        :param password: is the password used through the process
        """
        
        # Connection process inside the Webex application
        connection_button = self.find_by_XPATH('//android.widget.ScrollView/android.view.View[3]/android.widget.Button')
        connection_button.click()
        email_address_field = self.find_by_XPATH('//android.widget.TextView[@text="Adresse électronique"]/../..')
        email_address_field.send_keys(email)
        next_button = self.find_by_XPATH('//android.widget.ScrollView/android.view.View/android.widget.Button')
        next_button.click()
        # Connection process inside the Orange B2B webview
        self.wait_until_element_is_displayed('//android.webkit.WebView[@text="Authentication B2B"]',5)
        orange_portal_webview = self.find_by_XPATH('//android.webkit.WebView[@text="Authentication B2B"]')
        orange_portal_id = self.find_by_XPATH_inside_parent(orange_portal_webview,'//android.widget.EditText')
        orange_portal_id.send_keys(email)
        self.swipe_vertical(500)
            # in order to have the connection button visible we need swipe
        orange_portal_next = self.find_by_XPATH_inside_parent(orange_portal_webview,'//android.widget.Button[@text="Suivant"]')
        orange_portal_next.click()
            # wait until the page loads to password view
        self.wait_until_element_is_displayed('//android.view.View[@text="Saisissez votre mot de passe"]',10)
        self.swipe_vertical(500)
        orange_portal_webview = self.find_by_XPATH('//android.webkit.WebView[@text="Authentication B2B"]')
        orange_portal_password = self.find_by_XPATH_inside_parent(orange_portal_webview,'//android.widget.EditText')
        orange_portal_password.send_keys(password)
        orange_portal_connect = self.find_by_XPATH_inside_parent(orange_portal_webview,'//android.widget.Button[@text="Se connecter"]')
        orange_portal_connect.click()
       
        time.sleep(3)
        #expect login, catch rollback 
        try :
            self.wait_until_element_is_displayed('(//android.widget.ImageView[@resource-id="com.cisco.wx2.android:id/avatarBackground"])[1]',5)
        except :
        # First B2B rollback
            print('=> entering B2B rollback handling')
                # wait until the page loads to login view
            self.wait_until_element_is_displayed('//android.webkit.WebView[@text="Authentication B2B"]',10)
            orange_portal_webview = self.find_by_XPATH('//android.webkit.WebView[@text="Authentication B2B"]')
            orange_portal_id = self.find_by_XPATH_inside_parent(orange_portal_webview,'//android.widget.EditText')
            orange_portal_id.send_keys(email)
            self.swipe_vertical(500)
            orange_portal_next = self.find_by_XPATH_inside_parent(orange_portal_webview,'//android.widget.Button[@text="Suivant"]')
            orange_portal_next.click()
                # wait until the page loads to password view
            self.wait_until_element_is_displayed('//android.view.View[@text="Saisissez votre mot de passe"]',10)
            self.swipe_vertical(500)
            orange_portal_webview = self.find_by_XPATH('//android.webkit.WebView[@text="Authentication B2B"]')
            orange_portal_password = self.find_by_XPATH_inside_parent(orange_portal_webview,'//android.widget.EditText')
            orange_portal_password.send_keys(password)
            orange_portal_connect = self.find_by_XPATH_inside_parent(orange_portal_webview,'//android.widget.Button[@text="Se connecter"]')
            orange_portal_connect.click()

                #Close error page 
            time.sleep(5)
            close_web_form_button = self.find_by_id('com.android.chrome:id/close_button')
            close_web_form_button.click()
            time.sleep(5)

        # Second B2B rollback
            #Handling rollback
            next_button = self.find_by_XPATH('//android.widget.ScrollView/android.view.View/android.widget.Button')
            next_button.click()
                # wait until the page loads to login view
            self.wait_until_element_is_displayed('//android.webkit.WebView[@text="Authentication B2B"]',10)
            orange_portal_webview = self.find_by_XPATH('//android.webkit.WebView[@text="Authentication B2B"]')
            orange_portal_id = self.find_by_XPATH_inside_parent(orange_portal_webview,'//android.widget.EditText')
            orange_portal_id.send_keys(email)
            self.swipe_vertical(500)
            orange_portal_next = self.find_by_XPATH_inside_parent(orange_portal_webview,'//android.widget.Button[@text="Suivant"]')
            orange_portal_next.click()
                # wait until the page loads to password view
            self.wait_until_element_is_displayed('//android.view.View[@text="Saisissez votre mot de passe"]',10)
            self.swipe_vertical(500)
            orange_portal_webview = self.find_by_XPATH('//android.webkit.WebView[@text="Authentication B2B"]')
            orange_portal_password = self.find_by_XPATH_inside_parent(orange_portal_webview,'//android.widget.EditText')
            orange_portal_password.send_keys(password)
            orange_portal_connect = self.find_by_XPATH_inside_parent(orange_portal_webview,'//android.widget.Button[@text="Se connecter"]')
            orange_portal_connect.click()
            time.sleep(5)
            try :   
                self.wait_until_element_is_displayed('(//android.widget.ImageView[@resource-id="com.cisco.wx2.android:id/avatarBackground"])[1]',5)
            except :
                pass
            print('=> webex_log_in() success with B2B roll back')
        print('=> webex_log_in() success in one go ')