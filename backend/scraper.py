from selenium_imports import *
from typing import Dict,Callable,Union
from colorama import Fore
import logging
import inspect
import time

w=Fore.WHITE
c=Fore.CYAN

logger=logging.getLogger('scraper_logger')
logger.setLevel(logging.DEBUG)

file_handler_formatter=logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
console_handler_formatter=logging.Formatter('%(asctime)s | %(message)s')

file_handler=logging.FileHandler('logs/scraper.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_handler_formatter)

console_handler=logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(console_handler_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

class Navigator:
    def __init__(self,web_url:str='https://google.com',headless:bool=False)->None:
        self.web_url=web_url
        self.actions_list=[]

        options=webdriver.ChromeOptions()
        service=Service(ChromeDriverManager().install())

        headmodeArgs=['--ingore-certificate-errors','--disable-notifications']
        headlessArgs=['--headless','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--enable-unsafe-swiftshader']+headmodeArgs

        args=headlessArgs if headless else headmodeArgs

        for arg in args:
            options.add_argument(arg)
        options.add_experimental_option('detach',True)
        
        self.driver=webdriver.Chrome(options=options,service=service)

    def action(self,action:str='',attribute:str='',timeout:int=30,sleep:int=0,input_value:str='',message:str='',function:Callable[[],None]=None)->None:
        self.actions_list.append({key:value for key,value in locals().items() if key !='self'})

    def action_executer(self,action):
        def click():
            element=WebDriverWait(self.driver,action['timeout']).until(EC.element_to_be_clickable((By.XPATH,f'//*[@{action['attribute']}]')))
            element.click()
        
        def write():
            element=WebDriverWait(self.driver,action['timeout']).until(EC.presence_of_element_located((By.XPATH,f'//*[@{action['attribute']}]')))
            element.send_keys(action['input_value'])
        
        def send():
            element=WebDriverWait(self.driver,action['timeout']).until(EC.presence_of_element_located((By.XPATH,f'//*[@{action['attribute']}]')))
            element.send_keys(action['input_value']+Keys.RETURN)

        def function():
            action['function']()
        
        def execute_action(action_action):
            time.sleep(action['sleep'])
            action_action()

            if action['message']!='':
                logger.info(action['message'])

        action_hash_map={
            'click':lambda:click(),
            'write':lambda:write(),
            'send':lambda:send(),
            'function':lambda:function()
        }
        execute_action(action_hash_map[action['action']])

    def start(self):
        self.driver.get(self.web_url)
        logger.info(f'{c}navigating to {self.web_url}...{w}')
        
        for action in self.actions_list:
            self.action_executer(action)