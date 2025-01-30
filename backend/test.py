from scraper import Navigator
from dotenv import load_dotenv
import os

load_dotenv()
PHONE,PASSWORD=os.getenv('PHONE'),os.getenv('PASSWORD')
mozzart_url='https://www.mozzartbet.co.ke/en#/casino'

mozzart_navigator=Navigator(mozzart_url)
mozzart_navigator.action(action='click',attribute='class="login-link mozzart_ke"',message='logging in...')
mozzart_navigator.action(action='write',attribute='placeholder="Mobile number"',input_value=PHONE,message='writing phone input...')
mozzart_navigator.action(action='send',attribute='placeholder="Password"',input_value=PASSWORD,message='writing password input...')
mozzart_navigator.action(action='click',attribute='alt="Aviator"',message='navigating to game engine...',sleep=1)
mozzart_navigator.action(action='monitor',track_item='class="bubble-multiplier"',record_items={'multiplier':'class="bubble-multiplier"','bets':'class="all-bets-block d-flex justify-content-between align-items-center px-2 pb-1"]//div[1]//div[2]'})

mozzart_navigator.start()