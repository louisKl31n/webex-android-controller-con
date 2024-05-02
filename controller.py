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

    def webex_cancel(self) :
        end_call_action_button = self.find_by_id('com.orange.phone:id/floating_end_call_action_button')
        end_call_action_button.click()
        print('=> webex_cancel() success')
    
    def webex_hang_up(self) :
        end_call_action_button = self.find_by_id('com.orange.phone:id/floating_end_call_action_button')
        end_call_action_button.click()
        print('=> webex_hang_up() success')

    def webex_dtmf(self,dtmf_sequence):
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
        more_button = self.find_by_id('com.orange.phone:id/call_screen_more_id')
        more_button.click()
        hold_button = self.find_by_XPATH('(//android.widget.LinearLayout[@resource-id="com.orange.phone:id/content"])[1]')
        hold_button.click()

    def webex_resume(self):
        more_button = self.find_by_id('com.orange.phone:id/call_screen_more_id')
        more_button.click()
        hold_button = self.find_by_XPATH('(//android.widget.LinearLayout[@resource-id="com.orange.phone:id/content"])[1]')
        hold_button.click()

    def webex_mute(self):
        mute_button = self.find_by_id('com.orange.phone:id/muteButton')
        mute_button.click()

    def webex_unmute(self):
        unmute_button = self.find_by_id('com.orange.phone:id/muteButton')
        unmute_button.click()

    def webex_answer(self, incoming_number):
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

    def webex_decline(self, incoming_number):
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

    def driver_quit(self) :
        self.driver.quit()



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
            self.swipe_vertical(300)
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
            self.swipe_vertical(300)
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