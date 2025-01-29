from scraper import Navigator
from dotenv import load_dotenv
from colorama import Fore
import os

w=Fore.WHITE
g=Fore.GREEN
y=Fore.YELLOW
c=Fore.CYAN
b=Fore.LIGHTBLACK_EX

load_dotenv()
PHONE=os.getenv('PHONE')
PASSWORD=os.getenv('PASSWORD')
mozzart_url='https://www.mozzartbet.co.ke/en#/casino'

mozzart_navigator=Navigator(mozzart_url)
mozzart_navigator.action(action='click',attribute='class="login-link mozzart_ke"',message=f'{c}logging in...{w}')
mozzart_navigator.action(action='write',attribute='placeholder="Mobile number"',input_value=PHONE,message=f'{c}writing phone input...{w}')
mozzart_navigator.action(action='send',attribute='placeholder="Password"',input_value=PASSWORD,message=f'{c}writing password input...{w}')
mozzart_navigator.action(action='click',attribute='alt="Aviator"',message=f'{c}navigating to game engine...{w}',sleep=1)

mozzart_navigator.start()