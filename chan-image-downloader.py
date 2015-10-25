import json
import configparser
import os.path
import time
import urllib.request
# get recovery.js path
config = configparser.ConfigParser()
config.read(os.getenv("HOME") + '/.mozilla/firefox/profiles.ini')
profile_val = config.get('Profile0', 'Path')
path_to_recovery_js = os.getenv("HOME") + '/.mozilla/firefox/' + profile_val + '/sessionstore-backups/recovery.js'

# obtain thread url
json_to_sift = json.loads(open(path_to_recovery_js).read())
selected_window_index = json_to_sift['selectedWindow'] - 1
selected_tab_index = json_to_sift['windows'][selected_window_index]['selected'] - 1
last_entry = len(json_to_sift['windows'][selected_window_index]['tabs'][selected_tab_index]['entries']) - 1
thread_url = json_to_sift['windows'][selected_window_index]['tabs'][selected_tab_index]['entries'][last_entry]['url']

# check if 4chan
print(thread_url)
if not (thread_url.startswith('https://boards.4chan.org/') or thread_url.startswith('http://boards.4chan.org/')):
	print('Not a 4chan thread! Exiting script.')
	exit();

#get board name
board_name = thread_url.split('/')[3]

# request to 4chan api shouldn't come more often than every second
time.sleep(1)

# get thread json
thread_url_json = thread_url + '.json'
r = urllib.request.urlopen(thread_url_json)
data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))

#iterate through posts and save images
print('Downloading...')
for posts in data['posts']:
	if 'tim' in posts:
		url = 'https://i.4cdn.org/' + board_name + "/" + str(posts['tim']) + posts['ext']
		img = urllib.request.urlretrieve(url, str(posts['tim']) + posts['ext'])
print('Done!')

