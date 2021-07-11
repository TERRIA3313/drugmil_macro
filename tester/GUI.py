import wx
import requests
import re
import json
import os
from bs4 import BeautifulSoup
import time
import threading
import sys


class Database:
    def cookies(self):
        with open(global_data.folder_name + '/main.json') as json_file:
            cookies = json.load(json_file)
        return cookies

    def header(self):
        header = {"Host": "drugmil.net", "Connection": "keep-alive",
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
        return header


class Global_data:
    def __init__(self):
        self.choice = 0
        self.planet_type_data = 0
        self.choose = []
        self.choose_number = 0
        self.counter = 0
        self.number_list_data = []
        self.folder_name = 'macro'
        self.beetle = 0

    def add_number_list(self, list_data):
        self.number_list_data.append(list_data)

    def number_list(self):
        return self.number_list_data

    def folder_name(self):
        return self.folder_name

    def change_folder_name(self, name):
        self.folder_name = name

    def planet_type(self):
        return self.planet_type_data

    def change_planet_type(self, data):
        self.planet_type_data = data

    def choice(self):
        return self.choice

    def change_choice(self, data):
        self.choice = data

    def choose(self):
        return self.choose

    def change_choose(self, data):
        self.choose = data

    def choose_number(self):
        return self.choose_number

    def change_choose_number(self, data):
        self.choose_number = data

    def counter(self):
        return self.counter

    def change_counter(self, data):
        self.counter = data

    def change_beetle(self, data):
        self.beetle = data


global_data = Global_data()


class Attack:
    def __init__(self):
        self.attack_data = ''
        self.attack_url = ''

    def url(self, attack_url):
        self.attack_url = attack_url

    def data(self, attack_data):
        self.attack_data = attack_data

    def get_attack(self):
        return requests.get(url=self.attack_url, cookies=Database().cookies(), headers=Database().header(),
                            allow_redirects=False, timeout=30)

    def post_attack(self):
        return requests.post(url=self.attack_url, cookies=Database().cookies(), headers=Database().header(),
                             data=self.attack_data, allow_redirects=False, timeout=30)

    def login_attack(self):
        return requests.post(url=self.attack_url, headers=Database().header(),
                             data=self.attack_data, allow_redirects=False, timeout=30)

    def soup(self, attack):
        html = attack.content
        soup = BeautifulSoup(html, 'html.parser')
        return soup


class Get_data:
    def __init__(self):
        if not os.path.isdir(global_data.folder_name):
            os.mkdir(global_data.folder_name)
        self.file_name = os.listdir(global_data.folder_name)
        self.answer_list = []

    def get_filename(self):
        self.file_name = os.listdir(global_data.folder_name)
        if os.path.isfile(global_data.folder_name + '/main.json'):
            self.file_name.remove('main.json')
        if os.path.isfile(global_data.folder_name + '/div_usedfleet.json'):
            self.file_name.remove('div_usedfleet.json')
        if os.path.isfile(global_data.folder_name + '/cus_usedfleet.json'):
            self.file_name.remove('cus_usedfleet.json')
        if os.path.isfile(global_data.folder_name + '/data.json'):
            self.file_name.remove('data.json')
        return self.file_name

    def get_usedfleet(self, galaxy, system, planet, galaxyend, systemend, planetend):
        get = Attack()
        get.attack_data = {'galaxy': galaxy, 'system': system, 'planet': planet, 'galaxyend': galaxyend,
                           'systemend': systemend, 'planetend': planetend, 'onsubmit': 'this.submit.disabled = true;'}
        get.attack_url = "http://drugmil.net/2/xgp/game.php?page=fleet1"
        with open(global_data.folder_name + '/data.json') as json_file1:
            json_data1 = json.load(json_file1)
        keys = list(json_data1.keys())
        values = list(json_data1.values())
        get.attack_data[keys[0]] = values[0]
        soup = get.soup(get.post_attack())
        p_data = soup.find_all('input')
        one_data = p_data[5]
        one_speed = p_data[4]
        t = re.split('[;"]', str(one_data))
        p = re.split('[;"]', str(one_speed))
        one_usedfleet = {'usedfleet': t[-2], 'speedallsmin': p[-2]}
        with open(global_data.folder_name + '/div_usedfleet.json', 'w', encoding='utf-8') as g:
            json.dump(one_usedfleet, g, indent="\t")
        get.attack_data[keys[1]] = values[1]
        soup1 = get.soup(get.post_attack())
        p_data1 = soup1.find_all('input')
        two_data = p_data1[9]
        two_speed = p_data1[8]
        t1 = re.split('[;"]', str(two_data))
        p1 = re.split('[;"]', str(two_speed))
        two_usedfleet = {'usedfleet': t1[-2], 'speedallsmin': p1[-2]}
        with open(global_data.folder_name + '/cus_usedfleet.json', 'w', encoding='utf-8') as g:
            json.dump(two_usedfleet, g, indent="\t")

    def get_list(self):
        get = Attack()
        get.attack_url = "http://drugmil.net/2/xgp/game.php?page=fleet"
        get_list_soup = get.soup(get.get_attack())
        h_data = get_list_soup.find_all('option')
        counters = 0
        while counters < len(h_data):
            self.answer_list.append(h_data[counters].get_text())
            counters += 1
        counters = 0
        while counters < len(h_data):
            temps = re.split('[;]', str(h_data[counters]))
            global_data.add_number_list(temps[2][:-4])
            counters += 1
        return self.answer_list

    def get_planet_number(self):
        get = Attack()
        get.attack_url = "http://drugmil.net/2/xgp/game.php?page=fleet"
        soup = get.soup(get.get_attack())
        h_data = soup.find_all('option')
        return h_data

    def answer(self):
        return self.answer_list


get_data = Get_data()


class make_data(wx.Dialog):
    def __init__(self, parent, make_data_id, title):
        wx.Dialog.__init__(self, parent, make_data_id, title, pos=wx.DefaultPosition, size=wx.Size(300, 300))
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.text_division = wx.StaticText(self, 2001, u"항공전대 갯수",
                                           wx.DefaultPosition, wx.Size(300, -1), wx.ALIGN_CENTRE)
        self.text_division.Wrap(-1)
        sizer1.Add(self.text_division, 0, wx.ALL, 5)
        self.m_textCtrl1 = wx.TextCtrl(self, 2002, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1), 0)
        sizer1.Add(self.m_textCtrl1, 0, wx.ALL, 5)
        self.text_number = wx.StaticText(self, 2003, u"클광용 번호(중뇌장형 : 219 ,린 : 250)",
                                         wx.DefaultPosition, wx.Size(300, -1), wx.ALIGN_CENTRE)
        self.text_number.Wrap(-1)
        sizer1.Add(self.text_number, 0, wx.ALL, 5)
        self.m_textCtrl2 = wx.TextCtrl(self, 2004, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1), 0)
        sizer1.Add(self.m_textCtrl2, 0, wx.ALL, 5)
        self.text_password = wx.StaticText(self, 2003, u"클광용 유닛 갯수", wx.DefaultPosition,
                                           wx.Size(300, -1), wx.ALIGN_CENTRE)
        self.text_password.Wrap(-1)
        sizer1.Add(self.text_password, 0, wx.ALL, 5)
        self.m_textCtrl3 = wx.TextCtrl(self, 2004, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1), 0)
        sizer1.Add(self.m_textCtrl3, 0, wx.ALL, 5)
        self.make_button = wx.Button(self, 2006, u"생성", wx.DefaultPosition, wx.Size(300, -1), 0)
        sizer1.Add(self.make_button, 0, wx.ALL, 5)
        self.SetSizer(sizer1)
        self.Layout()
        self.Centre(wx.BOTH)
        self.Bind(wx.EVT_BUTTON, self.dia_quit, id=2006)  # 생성 버튼을 diaQuit에 바인드

    def dia_quit(self, event):
        self.make()
        self.EndModal(1)

    def make(self):
        div = str(self.m_textCtrl1.GetValue())
        custom_number = str(self.m_textCtrl2.GetValue())
        custom_many = str(self.m_textCtrl3.GetValue())
        data = {'ship221': div, 'ship' + custom_number: custom_many}
        with open(global_data.folder_name + '/data.json', 'w', encoding='utf-8') as g:
            json.dump(data, g, indent="\t")


class login_dialog(wx.Dialog):
    def __init__(self, parent, login_dialog_id, title):
        wx.Dialog.__init__(self, parent, login_dialog_id, title, pos=wx.DefaultPosition, size=wx.Size(300, 200))
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.text_id = wx.StaticText(self, 1001, u"아이디", wx.DefaultPosition, wx.Size(300, -1), wx.ALIGN_CENTRE)
        self.text_id.Wrap(-1)
        sizer1.Add(self.text_id, 0, wx.ALL, 5)
        self.m_textCtrl1 = wx.TextCtrl(self, 1002, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1), 0)
        sizer1.Add(self.m_textCtrl1, 0, wx.ALL, 5)
        self.text_password = wx.StaticText(self, 1003, u"비밀번호", wx.DefaultPosition, wx.Size(300, -1), wx.ALIGN_CENTRE)
        self.text_password.Wrap(-1)
        sizer1.Add(self.text_password, 0, wx.ALL, 5)
        self.m_textCtrl2 = wx.TextCtrl(self, 1004, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1), wx.TE_PASSWORD)
        sizer1.Add(self.m_textCtrl2, 0, wx.ALL, 5)
        self.login_button = wx.Button(self, 1006, u"로그인", wx.DefaultPosition, wx.Size(300, -1), 0)
        sizer1.Add(self.login_button, 0, wx.ALL, 5)
        self.SetSizer(sizer1)
        self.Layout()
        self.Centre(wx.BOTH)
        self.Bind(wx.EVT_BUTTON, self.dia_quit, id=1006)  # 로그인 버튼을 diaQuit에 바인드

    def dia_quit(self, event):
        self.login()
        self.EndModal(1)

    def login(self):
        ids = str(self.m_textCtrl1.GetValue())
        password = str(self.m_textCtrl2.GetValue())
        login = Attack()
        login.attack_url = 'http://drugmil.net/2/xgp/index.php'
        login.attack_data = {'username': ids, 'password': password, 'submit': '로그인'}
        res = login.login_attack()
        t = res.headers.get('Set-cookie')
        t = re.split('[=;]', t)
        name = '\354\225\275\352\264\264\353\260\200'
        value = ''.join(t[1])
        cookie = {
            name: value
        }
        if not (os.path.isdir('macro')):
            os.makedirs('macro')
        with open(global_data.folder_name + '/main.json', 'w', encoding='utf-8') as g:
            json.dump(cookie, g, indent="\t")


class Fairy_attack(wx.Dialog):
    def __init__(self, parent, fairy_attack_id, title):
        wx.Dialog.__init__(self, parent, fairy_attack_id, title, pos=wx.DefaultPosition, size=wx.Size(300, 400))
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.text_counter = wx.StaticText(self, 1, u"원하는 요정 수", wx.DefaultPosition, wx.Size(100, -1), wx.ALIGN_CENTRE)
        self.text_counter.Wrap(-1)
        sizer1.Add(self.text_counter, 0, wx.ALL, 5)
        self.m_textCtrl1 = wx.TextCtrl(self, 2, wx.EmptyString, wx.DefaultPosition, wx.Size(100, -1), 0)
        sizer1.Add(self.m_textCtrl1, 0, wx.ALL, 5)
        self.button = wx.Button(self, 3, u"공격", wx.DefaultPosition, wx.Size(100, -1), 0)
        sizer1.Add(self.button, 0, wx.ALL, 5)
        self.attack_list_data = []
        self.attack_list = wx.ListBox(self, -1, (130, 5), (150, 350), self.attack_list_data, wx.LB_SINGLE)
        self.SetSizer(sizer1)
        self.Layout()
        self.Centre(wx.BOTH)
        self.Bind(wx.EVT_BUTTON, self.thread, id=3)
        self.count = 0

    def thread(self, event):
        if self.count == 0:
            t1 = threading.Thread(target=self.attack)
            t1.setDaemon(True)
            self.count = 1
            t1.start()
        else:
            dlg = wx.MessageDialog(self, '이미 요정 공격중입니다', '요정 공격중', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def attack(self):
        fairy_counter = int(self.m_textCtrl1.GetValue())
        while fairy_counter != 0:
            self.fairy_attack()
            wx.Yield()
            fairy_counter -= 1
        dlg = wx.MessageDialog(self, '공격 완료!', '공격완료', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        self.count = 0

    def fairy_attack(self):
        attack = Attack()
        attack.attack_url = "http://drugmil.net/2/xgp/pack_bonus14.php?mode=pack1"
        breaker = '0'
        while not breaker == '1':
            time.sleep(0.5)
            soup = attack.soup(attack.get_attack())
            p_data = soup.find_all('td')
            data = p_data[0].get_text()
            if data == '\n':
                data = ' 아이템 발견'
            self.attack_list.Append('현재 위치 : ' + data)
            if data == ' 무너진 고성':
                self.attack_list.Append('요정 발견!')
                time.sleep(0.8)
                attack.attack_url = 'http://drugmil.net/2/xgp/pack_bonus15.php?mode=pack2'
                while not breaker == '1':
                    y_soup = attack.soup(attack.get_attack())
                    helper = y_soup.find('a', 'button')
                    self.attack_list.Append("요정 공격!")
                    time.sleep(0.8)
                    if 'achatbonus14.php' in helper['href']:
                        self.attack_list.Append("요청 처치 완료")
                        breaker = '1'


class Enemy_attack(wx.Dialog):
    def __init__(self, parent, enemy_attack_id, title):
        wx.Dialog.__init__(self, parent, enemy_attack_id, title, pos=wx.DefaultPosition, size=wx.Size(300, 400))
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.text_counter = wx.StaticText(self, 1, u"원하는 강적 수", wx.DefaultPosition, wx.Size(100, -1), wx.ALIGN_CENTRE)
        self.text_counter.Wrap(-1)
        sizer1.Add(self.text_counter, 0, wx.ALL, 5)
        self.m_textCtrl1 = wx.TextCtrl(self, 2, wx.EmptyString, wx.DefaultPosition, wx.Size(100, -1), 0)
        sizer1.Add(self.m_textCtrl1, 0, wx.ALL, 5)
        self.button = wx.Button(self, 3, u"공격", wx.DefaultPosition, wx.Size(100, -1), 0)
        sizer1.Add(self.button, 0, wx.ALL, 5)
        self.stop = wx.Button(self, 4, u"중지", wx.DefaultPosition, wx.Size(100, -1), 0)
        sizer1.Add(self.stop, 0, wx.ALL, 5)
        self.attack_list_data = []
        self.attack_list = wx.ListBox(self, -1, (130, 5), (150, 350), self.attack_list_data, wx.LB_SINGLE)
        self.SetSizer(sizer1)
        self.Layout()
        self.Centre(wx.BOTH)
        self.Bind(wx.EVT_BUTTON, self.thread, id=3)
        self.Bind(wx.EVT_BUTTON, self.stopper, id=4)
        self.count = 0

    def thread(self, event):
        if self.count == 0:
            self.t1 = threading.Thread(target=self.attack_counter)
            self.t1.setDaemon(True)
            self.count = 1
            self.t1.start()
        else:
            dlg = wx.MessageDialog(self, '이미 요정 강적중입니다', '강적 공격중', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def attack_counter(self):
        self.enemy_counter = int(self.m_textCtrl1.GetValue())
        while self.enemy_counter != 0:
            self.attacker()
            wx.Yield()
            self.enemy_counter -= 1
            if self.count == 0:
                break
        dlg = wx.MessageDialog(self, '공격 완료!', '공격완료', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        self.count = 0

    def attacker(self):
        attack = Attack()
        attack.attack_url = "http://drugmil.net/2/xgp/pack_bonus14.php?mode=pack1"
        breaker = '0'
        search_counter = 8
        while not breaker == '1':
            time.sleep(0.5)
            soup = attack.soup(attack.get_attack())
            p_data = soup.find_all('td')
            data = p_data[0].get_text()
            if not data == ' 미로의 초원':
                if data == '\n':
                    data = ' 아이템 발견'
                self.attack_list.Append('현재 위치 : ' + data)
                search_counter -= 1
            if search_counter == 0:
                self.attack_list.Append('이미 나왔는지 점검중')
                time.sleep(0.3)
                search = Attack()
                search.attack_url = 'http://drugmil.net/2/xgp/achatbonus15.php'
                p_soup = search.soup(search.get_attack())
                phelper = p_soup.find_all('td', 'c')
                plier = phelper[2].get_text()
                if not plier[-4:-1] == '미출현':
                    data = ' 미로의 초원'
                search_counter = 8
            if data == ' 미로의 초원':
                self.attack_list.Append('강적 발견!')
                time.sleep(0.5)
                attack.attack_url = 'http://drugmil.net/2/xgp/pack_bonus15.php?mode=pack1'
                while not breaker == '1':
                    y_soup = attack.soup(attack.get_attack())
                    helper = y_soup.find('a', 'button')
                    self.attack_list.Append("강적 공격!")
                    time.sleep(0.5)
                    if 'achatbonus14.php' in helper['href']:
                        self.attack_list.Append("강적 처치 완료")
                        breaker = '1'
            if self.count == 0:
                break

    def stopper(self, event):
        self.enemy_counter = 0
        self.count = 0


class card_pack(wx.Dialog):
    def __init__(self, parent, card_pack_id, title):
        wx.Dialog.__init__(self, parent, card_pack_id, title, pos=wx.DefaultPosition, size=wx.Size(350, 400))
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.text_counter = wx.StaticText(self, 1, u"카드팩 이름", wx.DefaultPosition, wx.Size(100, -1), wx.ALIGN_CENTRE)
        self.text_counter.Wrap(-1)
        sizer1.Add(self.text_counter, 0, wx.ALL, 5)
        self.m_textCtrl1 = wx.TextCtrl(self, 2, wx.EmptyString, wx.DefaultPosition, wx.Size(100, -1), 0)
        sizer1.Add(self.m_textCtrl1, 0, wx.ALL, 5)
        self.button = wx.Button(self, 3, u"교환", wx.DefaultPosition, wx.Size(100, -1), 0)
        sizer1.Add(self.button, 0, wx.ALL, 5)
        self.exchange_list_data = []
        self.exchange_list = wx.ListBox(self, -1, (130, 5), (200, 350), self.exchange_list_data, wx.LB_SINGLE)
        self.SetSizer(sizer1)
        self.Layout()
        self.Centre(wx.BOTH)
        self.Bind(wx.EVT_BUTTON, self.thread, id=3)
        self.count = 0

    def thread(self, event):
        if self.count == 0:
            t1 = threading.Thread(target=self.card)
            t1.setDaemon(True)
            self.count = 1
            t1.start()
        else:
            dlg = wx.MessageDialog(self, '교환이 이미 진행중입니다', '교환 공격중', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def card(self):
        self.card_exchange(str(self.m_textCtrl1.GetValue()))
        wx.Yield()
        dlg = wx.MessageDialog(self, '교환 완료!', '교환완료', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        self.count = 0

    def card_exchange(self, name):
        doroshi = Attack()
        doroshi.attack_url = 'http://drugmil.net/2/xgp/pack_bonus21.php?mode=pack2'
        doroshi.attack_data = {'bc': name}
        text = ''
        while not text == '원하는 카드팩 이름과 행동력을 확인해주시기 바랍니다.':
            p_soup = doroshi.soup(doroshi.post_attack())
            text = p_soup.find('th', 'errormessage').get_text()
            if not text == '원하는 카드팩 이름과 행동력을 확인해주시기 바랍니다.':
                self.exchange_list.Append(text)
        wx.Yield()
        time.sleep(0.3)


class beetle_macro(wx.Dialog):
    def __init__(self, parent, beetle_macro_id, title):
        wx.Dialog.__init__(self, parent, beetle_macro_id, title, pos=wx.DefaultPosition, size=wx.Size(350, 400))
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.text_counter = wx.StaticText(self, 1, u"카드 이름", wx.DefaultPosition, wx.Size(100, -1), wx.ALIGN_CENTRE)
        self.text_counter.Wrap(-1)
        self.m_textCtrl1 = wx.TextCtrl(self, 2, wx.EmptyString, wx.DefaultPosition, wx.Size(100, -1), 0)
        self.button = wx.Button(self, 3, u"교환", wx.DefaultPosition, wx.Size(100, -1), 0)
        self.stopper = wx.Button(self, 4, u"중지", wx.DefaultPosition, wx.Size(100, -1), 0)
        self.count_list = wx.RadioBox(self, 501, "교환 갯수", wx.DefaultPosition, wx.DefaultSize,
                                         ['1개', '100개'], 2, wx.RA_SPECIFY_COLS)

        sizer1.Add(self.text_counter, 0, wx.ALL, 5)
        sizer1.Add(self.m_textCtrl1, 0, wx.ALL, 5)
        sizer1.Add(self.count_list, 0, wx.ALL, 5)
        sizer1.Add(self.button, 0, wx.ALL, 5)
        sizer1.Add(self.stopper, 0, wx.ALL, 5)

        self.beetle_list_data = []
        self.beetle_list = wx.ListBox(self, -1, (130, 5), (200, 350), self.beetle_list_data, wx.LB_SINGLE)
        self.SetSizer(sizer1)
        self.Layout()
        self.Centre(wx.BOTH)

        self.Bind(wx.EVT_BUTTON, self.thread, id=3)
        self.Bind(wx.EVT_BUTTON, self.stop, id=4)
        self.Bind(wx.EVT_RADIOBOX, self.change, self.count_list)

        self.count = 0

    def thread(self, event):
        if self.count == 0:
            t1 = threading.Thread(target=self.exchange)
            t1.setDaemon(True)
            self.count = 1
            t1.start()
        else:
            dlg = wx.MessageDialog(self, '교환이 이미 진행중입니다', '교환 공격중', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def exchange(self):
        if global_data.beetle == 0:
            self.beetle_exchange(str(self.m_textCtrl1.GetValue()))
        else:
            self.beetle_100_exchange(str(self.m_textCtrl1.GetValue()))
        wx.Yield()
        dlg = wx.MessageDialog(self, '교환 완료!', '교환완료', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        self.count = 0

    def beetle_exchange(self, name):
        beetle = Attack()
        beetle.attack_url = "http://drugmil.net/2/xgp/pack_bonus17.php?mode=pack1000"
        beetle.attack_data = {'bc': name}
        answer = ''
        while not ('만능풍뎅이' in answer or '최대 레벨' in answer):
            soup = beetle.soup(beetle.post_attack())
            answer = soup.find('th', 'errormessage').get_text()
            if not ('만능풍뎅이' in answer or '최대 레벨' in answer):
                self.beetle_list.Append(answer)
            wx.Yield()
            time.sleep(0.4)
            if self.count != 1:
                break

    def beetle_100_exchange(self, name):
        beetle = Attack()
        beetle.attack_url = "http://drugmil.net/2/xgp/pack_bonus17.php?mode=pack1001"
        beetle.attack_data = {'bc': name}
        answer = ''
        while not ('만능풍뎅이' in answer or '최대 레벨' in answer):
            soup = beetle.soup(beetle.post_attack())
            answer = soup.find('th', 'errormessage').get_text()
            if not ('만능풍뎅이' in answer or '최대 레벨' in answer):
                self.beetle_list.Append(answer)
            wx.Yield()
            time.sleep(0.4)
            break

    def change(self, event):
        global_data.change_beetle(self.count_list.GetSelection())
        print(global_data.beetle)

    def stop(self, event):
        self.count = 0


class build(wx.Dialog):
    def __init__(self, parent, build_id, title):
        wx.Dialog.__init__(self, parent, build_id, title, pos=wx.DefaultPosition, size=wx.Size(800, 350))
        wx.StaticText(self, id=1, label='건설 행성', pos=(35, 10))
        a_list, p_list = [], []
        if os.path.isfile(global_data.folder_name + '/main.json'):
            a_list = get_data.answer()
            for i in a_list:
                if '(묘지)' not in i:
                    p_list.append(i)
        self.box = wx.ComboBox(self, id=2, pos=(10, 32), size=(140, 22), choices=p_list)
        self.choose_number = 0
        self.n = global_data.number_list()
        data = Attack()
        data.attack_url = "http://drugmil.net/2/xgp/game.php?page=buildings&" + self.n[self.choose_number]
        soup = data.soup(data.get_attack())
        red = soup.find_all('fieldset')

        bank_data = Attack()
        bank_data.attack_url = "http://drugmil.net/2/xgp/bank.php"
        bank_soup = bank_data.soup(bank_data.get_attack())
        bank_account = bank_soup.find_all('font', {'color': 'lime'})
        bank_account = int(bank_account[1].get_text().replace(',', ''))

        black = red[0].get_text().replace('  ', ' ').replace('.', '').split(' ')[2:-1]
        black[0], black[1] = int(black[0]), int(black[1])
        green = red[1].get_text().replace('  ', ' ').replace('.', '').split(' ')[2:-1]
        green[0], green[1] = int(green[0]), int(green[1])
        corn = red[2].get_text().replace('  ', ' ').replace('.', '').split(' ')[2:-1]
        corn[0], corn[1] = int(corn[0]), int(corn[1])
        have = soup.find_all('td', {'width': '90'})
        self.have_resource = [int(have[0].get_text().replace('.', '')), int(have[1].get_text().replace('.', '')),
                              int(have[2].get_text().replace('.', ''))]
        wx.StaticText(self, id=3, label=u'보유 홍차', pos=(5, 60))
        self.black_tea = wx.StaticText(self, id=4, label=format(self.have_resource[0], ','), pos=(5, 80))
        wx.StaticText(self, id=5, label=u'보유 녹차', pos=(100, 60))
        self.green_tea = wx.StaticText(self, id=6, label=format(self.have_resource[1], ','), pos=(100, 80))
        wx.StaticText(self, id=7, label=u'보유 옥수수', pos=(190, 60))
        self.corn = wx.StaticText(self, id=8, label=format(self.have_resource[2], ','), pos=(190, 80))
        wx.StaticText(self, id=9, label=u'은행 옥수수', pos=(280, 60))
        self.bank_corn = wx.StaticText(self, id=10, label=format(bank_account, ','), pos=(280, 80))
        self.deposit_button = wx.Button(self, id=11, label=u"자원 전체\n 입금", pos=(370, 60), size=(60, 40))

        wx.StaticText(self, id=101, label=u'홍차밭 요구사항', pos=(5, 160))
        self.make_black_tea_1 = wx.StaticText(self, id=102, label=format(black[0], ','), pos=(5, 180))
        self.make_black_tea_2 = wx.StaticText(self, id=103, label=format(black[1], ','), pos=(100, 180))
        wx.StaticText(self, id=104, label=u'녹차밭 요구사항', pos=(5, 210))
        self.make_green_tea_1 = wx.StaticText(self, id=105, label=format(green[0], ','), pos=(5, 230))
        self.make_green_tea_2 = wx.StaticText(self, id=1066, label=format(green[1], ','), pos=(100, 230))
        wx.StaticText(self, id=107, label=u'옥수수밭 요구사항', pos=(5, 260))
        self.make_corn_1 = wx.StaticText(self, id=108, label=format(corn[0], ','), pos=(5, 280))
        self.make_corn_2 = wx.StaticText(self, id=109, label=format(corn[1], ','), pos=(100, 280))

        wx.StaticText(self, id=201, label=u'홍차밭 부족사항', pos=(200, 160))
        if self.have_resource[0] >= black[0]:
            self.if_black_tea_1 = wx.StaticText(self, id=202, label=u'가능', pos=(200, 180))
        else:
            self.if_black_tea_1 = wx.StaticText(self, id=202, label='-' + format(black[0] - self.have_resource[0], ','),
                                                pos=(200, 180))
        if self.have_resource[1] >= black[1]:
            self.if_black_tea_2 = wx.StaticText(self, id=203, label=u'가능', pos=(300, 180))
        else:
            self.if_black_tea_2 = wx.StaticText(self, id=203, label='-' + format(black[1] - self.have_resource[1], ','),
                                                pos=(300, 180))
        wx.StaticText(self, id=204, label=u'녹차밭 부족사항', pos=(200, 210))
        if self.have_resource[0] >= green[0]:
            self.if_green_tea_1 = wx.StaticText(self, id=204, label=u'가능', pos=(200, 230))
        else:
            self.if_green_tea_1 = wx.StaticText(self, id=204, label='-' + format(green[0] - self.have_resource[0], ','),
                                                pos=(200, 230))
        if self.have_resource[1] >= green[1]:
            self.if_green_tea_2 = wx.StaticText(self, id=205, label=u'가능', pos=(300, 230))
        else:
            self.if_green_tea_2 = wx.StaticText(self, id=205, label='-' + format(green[1] - self.have_resource[1], ','),
                                                pos=(300, 230))
        wx.StaticText(self, id=206, label=u'옥수수밭 부족사항', pos=(200, 260))
        if self.have_resource[0] >= corn[0]:
            self.if_corn_1 = wx.StaticText(self, id=207, label=u'가능', pos=(200, 280))
        else:
            self.if_corn_1 = wx.StaticText(self, id=207, label='-' + format(corn[0] - self.have_resource[0], ','),
                                           pos=(200, 280))
        if self.have_resource[1] >= corn[1]:
            self.if_corn_2 = wx.StaticText(self, id=208, label=u'가능', pos=(300, 280))
        else:
            self.if_corn_2 = wx.StaticText(self, id=208, label='-' + format(corn[1] - self.have_resource[1], ','),
                                           pos=(300, 280))

        wx.StaticText(self, id=301, label=u'환전으로 가능 여부', pos=(400, 160))
        if self.have_resource[0] / 4 + self.have_resource[1] / 2 + self.have_resource[2] >= black[0] / 4 + black[1] / 2:
            self.if_exchange_black_1 = wx.StaticText(self, id=302, label=u'가능', pos=(400, 180))
        else:
            self.if_exchange_black_1 = wx.StaticText(self, id=302, label=u'불가능', pos=(400, 180))
        wx.StaticText(self, id=303, label=u'환전으로 가능 여부', pos=(400, 210))
        if self.have_resource[0] / 4 + self.have_resource[1] / 2 + self.have_resource[2] >= green[0] / 4 + green[1] / 2:
            self.if_exchange_green_1 = wx.StaticText(self, id=304, label=u'가능', pos=(400, 230))
        else:
            self.if_exchange_green_1 = wx.StaticText(self, id=304, label=u'불가능', pos=(400, 230))
        wx.StaticText(self, id=305, label=u'환전으로 가능 여부', pos=(400, 260))
        if self.have_resource[0] / 4 + self.have_resource[1] / 2 + self.have_resource[2] >= corn[0] / 4 + corn[1] / 2:
            self.if_exchange_corn_1 = wx.StaticText(self, id=306, label=u'가능', pos=(400, 280))
        else:
            self.if_exchange_corn_1 = wx.StaticText(self, id=306, label=u'불가능', pos=(400, 280))
        self.have_corn = self.have_resource[0] / 4 + self.have_resource[1] / 2 + self.have_resource[2]
        wx.StaticText(self, id=401, label=u'은행으로 가능 여부', pos=(550, 160))
        if self.have_corn + bank_account >= black[0] / 4 + black[1] / 2:
            self.if_withdrawal_black_1 = wx.StaticText(self, id=402, label=u'가능', pos=(550, 180))
        else:
            self.if_withdrawal_black_1 = wx.StaticText(self, id=402, label=u'불가능', pos=(550, 180))
        wx.StaticText(self, id=403, label=u'은행으로 가능 여부', pos=(550, 210))
        if self.have_corn + bank_account >= green[0] / 4 + green[1] / 2:
            self.if_withdrawal_green_1 = wx.StaticText(self, id=404, label=u'가능', pos=(550, 230))
        else:
            self.if_withdrawal_green_1 = wx.StaticText(self, id=404, label=u'불가능', pos=(550, 230))
        wx.StaticText(self, id=405, label=u'은행으로 가능 여부', pos=(550, 260))
        if self.have_corn + bank_account >= corn[0] / 4 + corn[1] / 2:
            self.if_withdrawal_corn_1 = wx.StaticText(self, id=406, label=u'가능', pos=(550, 280))
        else:
            self.if_withdrawal_corn_1 = wx.StaticText(self, id=406, label=u'불가능', pos=(550, 280))

        self.build_black_button = wx.Button(self, id=1001, label=u"건설", pos=(660, 155), size=(50, 30))
        self.bank_black_button = wx.Button(self, id=10001, label=u"은행\n건설", pos=(720, 155), size=(50, 30))
        self.build_green_button = wx.Button(self, id=1002, label=u"건설", pos=(660, 210), size=(50, 30))
        self.bank_green_button = wx.Button(self, id=10002, label=u"은행\n건설", pos=(720, 210), size=(50, 30))
        self.build_corn_button = wx.Button(self, id=1003, label=u"건설", pos=(660, 260), size=(50, 30))
        self.bank_corn_button = wx.Button(self, id=10003, label=u"은행\n건설", pos=(720, 260), size=(50, 30))
        self.Layout()
        self.Centre(wx.BOTH)
        self.count = 0

        self.Bind(wx.EVT_COMBOBOX, self.set_planet, self.box)
        self.Bind(wx.EVT_BUTTON, self.build_black, id=1001)
        self.Bind(wx.EVT_BUTTON, self.build_green, id=1002)
        self.Bind(wx.EVT_BUTTON, self.build_corn, id=1003)
        self.Bind(wx.EVT_BUTTON, self.banked_black, id=10001)
        self.Bind(wx.EVT_BUTTON, self.banked_green, id=10002)
        self.Bind(wx.EVT_BUTTON, self.banked_corn, id=10003)
        self.Bind(wx.EVT_BUTTON, self.deposit, id=11)

    def set_planet(self, event):
        self.choose_number = self.box.GetSelection()
        wx.Yield()
        self.show_resource()

    def show_resource(self):
        planet_list = get_data.answer()
        count = 0
        self.new_number = []
        for i in planet_list:
            if '(묘지)' not in i:
                self.new_number.append(self.n[count])
            count += 1
        data = Attack()
        data.attack_url = "http://drugmil.net/2/xgp/game.php?page=buildings&" + self.new_number[self.choose_number]
        soup = data.soup(data.get_attack())
        red = soup.find_all('fieldset')

        black = red[0].get_text().replace('  ', ' ').replace('.', '').split(' ')[2:-1]
        black[0], black[1] = int(black[0]), int(black[1])
        green = red[1].get_text().replace('  ', ' ').replace('.', '').split(' ')[2:-1]
        green[0], green[1] = int(green[0]), int(green[1])
        corn = red[2].get_text().replace('  ', ' ').replace('.', '').split(' ')[2:-1]
        corn[0], corn[1] = int(corn[0]), int(corn[1])
        have = soup.find_all('td', {'width': '90'})
        self.have_resource = [int(have[0].get_text().replace('.', '')), int(have[1].get_text().replace('.', '')),
                              int(have[2].get_text().replace('.', ''))]
        self.black_tea.SetLabel(format(self.have_resource[0], ','))
        self.green_tea.SetLabel(format(self.have_resource[1], ','))
        self.corn.SetLabel(format(self.have_resource[2], ','))

        self.make_black_tea_1.SetLabel(format(black[0], ','))
        self.make_black_tea_2.SetLabel(format(black[1], ','))
        self.make_green_tea_1.SetLabel(format(green[0], ','))
        self.make_green_tea_2.SetLabel(format(green[1], ','))
        self.make_corn_1.SetLabel(format(corn[0], ','))
        self.make_corn_2.SetLabel(format(corn[0], ','))

        if self.have_resource[0] >= black[0]:
            self.if_black_tea_1.SetLabel(u'가능')
        else:
            self.if_black_tea_1.SetLabel('-' + format(black[0] - self.have_resource[0], ','))
        if self.have_resource[1] >= black[1]:
            self.if_black_tea_2.SetLabel(u'가능')
        else:
            self.if_black_tea_2.SetLabel('-' + format(black[1] - self.have_resource[1], ','))
        if self.have_resource[0] >= green[0]:
            self.if_green_tea_1.SetLabel(u'가능')
        else:
            self.if_green_tea_1.SetLabel('-' + format(green[0] - self.have_resource[0], ','))
        if self.have_resource[1] >= green[1]:
            self.if_green_tea_2.SetLabel(u'가능')
        else:
            self.if_green_tea_2.SetLabel('-' + format(green[1] - self.have_resource[1], ','))
        if self.have_resource[0] >= corn[0]:
            self.if_corn_1.SetLabel(u'가능')
        else:
            self.if_corn_1.SetLabel('-' + format(corn[0] - self.have_resource[0], ','))
        if self.have_resource[1] >= corn[1]:
            self.if_corn_2.SetLabel(u'가능')
        else:
            self.if_corn_2.SetLabel('-' + format(corn[1] - self.have_resource[1], ','))

        wx.StaticText(self, id=7, label=u'환전으로 가능 여부', pos=(400, 160))
        if self.have_resource[0] / 4 + self.have_resource[1] / 2 + self.have_resource[2] > black[0] / 4 + black[1] / 2:
            self.if_exchange_black_1.SetLabel(u'가능')
        else:
            self.if_exchange_black_1.SetLabel(u'불가능')
        wx.StaticText(self, id=7, label=u'환전으로 가능 여부', pos=(400, 210))
        if self.have_resource[0] / 4 + self.have_resource[1] / 2 + self.have_resource[2] > green[0] / 4 + green[1] / 2:
            self.if_exchange_green_1.SetLabel(u'가능')
        else:
            self.if_exchange_green_1.SetLabel(u'불가능')
        wx.StaticText(self, id=7, label=u'환전으로 가능 여부', pos=(400, 260))
        if self.have_resource[0] / 4 + self.have_resource[1] / 2 + self.have_resource[2] > corn[0] / 4 + corn[1] / 2:
            self.if_exchange_corn_1.SetLabel(u'가능')
        else:
            self.if_exchange_corn_1.SetLabel(u'불가능')

        bank_data = Attack()
        bank_data.attack_url = "http://drugmil.net/2/xgp/bank.php"
        bank_soup = bank_data.soup(bank_data.get_attack())
        bank_account = bank_soup.find_all('font', {'color': 'lime'})
        bank_account = int(bank_account[1].get_text().replace(',', ''))

        self.bank_corn.SetLabel(format(bank_account, ','))

    def build_black(self, event):
        if self.if_exchange_black_1.GetLabel() == '불가능':
            dlg = wx.MessageDialog(self, '건설이 불가능 합니다.', '건설 불가', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            self.exchange(self.if_black_tea_1.GetLabel(), self.if_black_tea_2.GetLabel())
            build_black = Attack()
            build_black.attack_url = 'http://drugmil.net/2/xgp/game.php?page=buildings&cmd=insert&building=1&' +\
                                     self.new_number[self.choose_number]
            build_black.get_attack()
            dlg = wx.MessageDialog(self, '건설하였습니다..', '건설', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def build_green(self, event):
        if self.if_exchange_green_1.GetLabel() == '불가능':
            dlg = wx.MessageDialog(self, '건설이 불가능 합니다.', '건설 불가', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            self.exchange(self.if_green_tea_1.GetLabel(), self.if_green_tea_2.GetLabel())
            build_green = Attack()
            build_green.attack_url = 'http://drugmil.net/2/xgp/game.php?page=buildings&cmd=insert&building=2&' +\
                                     self.new_number[self.choose_number]
            build_green.get_attack()
            dlg = wx.MessageDialog(self, '건설하였습니다..', '건설', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def build_corn(self, event):
        if self.if_exchange_corn_1.GetLabel() == '불가능':
            dlg = wx.MessageDialog(self, '건설이 불가능 합니다.', '건설 불가', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            self.exchange(self.if_corn_1.GetLabel(), self.if_corn_2.GetLabel())
            build_corn = Attack()
            build_corn.attack_url = 'http://drugmil.net/2/xgp/game.php?page=buildings&cmd=insert&building=3&' +\
                                    self.new_number[self.choose_number]
            build_corn.get_attack()
            dlg = wx.MessageDialog(self, '건설하였습니다..', '건설', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def deposit(self, event):
        bank = Attack()
        bank.attack_url = 'http://drugmil.net/2/xgp/bank_bonus.php?mode=pack79&' + self.new_number[self.choose_number]
        message = bank.soup(bank.get_attack()).find('th', 'errormessage').get_text()
        dlg = wx.MessageDialog(self, message, '자원 입금', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def exchange(self, label1, label2):
        self.show_resource()
        wx.Yield()
        if label1 == '가능':
            black_tea = 0
        else:
            black_tea = int(label1[1:].replace(',', ''))
        if label2 == '가능':
            green_tea = 0
        else:
            green_tea = int(label2[1:].replace(',', ''))
        exchange = Attack()
        exchange.attack_url = 'http://drugmil.net/2/xgp/game.php?page=trader'
        exchange.attack_data = {'ress': 'deuterium', 'metal': black_tea, 'cristal': green_tea}
        exchange.soup(exchange.post_attack())

    def withdrawal(self, label1, label2):
        if label1 == '가능':
            black_tea = 0
        else:
            black_tea = int(label1[1:].replace(',', ''))
        if label2 == '가능':
            green_tea = 0
        else:
            green_tea = int(label2[1:].replace(',', ''))
        my_corn = self.corn.GetLabel()
        my_corn = int(my_corn.replace(',', ''))
        corn = (my_corn - (((black_tea // 4) + 1) + ((green_tea // 2) + 1))) * -1
        exchange = Attack()
        exchange.attack_url = 'http://drugmil.net/2/xgp/bank_bonus.php?mode=pack2'
        exchange.attack_data = {'bc': corn}
        message = exchange.soup(exchange.post_attack())
        text = message.find('th', 'errormessage')

    def banked_black(self, event):
        if self.if_exchange_black_1.GetLabel() == '가능':
            dlg = wx.MessageDialog(self, '출금없이도 건설이 가능합니다', '건설 오류', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            if self.if_withdrawal_black_1.GetLabel() == '불가능':
                dlg = wx.MessageDialog(self, '건설이 불가능 합니다.', '건설 불가', wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
            else:
                self.withdrawal(self.if_black_tea_1.GetLabel(), self.if_black_tea_2.GetLabel())
                wx.Yield()
                self.show_resource()
                self.exchange(self.if_black_tea_1.GetLabel(), self.if_black_tea_2.GetLabel())
                build_corn = Attack()
                build_corn.attack_url = 'http://drugmil.net/2/xgp/game.php?page=buildings&cmd=insert&building=1&' + \
                                        self.new_number[self.choose_number]
                build_corn.get_attack()
                dlg = wx.MessageDialog(self, '건설하였습니다..', '건설', wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()

    def banked_green(self, event):
        if self.if_exchange_green_1.GetLabel() == '가능':
            dlg = wx.MessageDialog(self, '출금없이도 건설이 가능합니다', '건설 오류', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            if self.if_withdrawal_green_1.GetLabel() == '불가능':
                dlg = wx.MessageDialog(self, '건설이 불가능 합니다.', '건설 불가', wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
            else:
                self.withdrawal(self.if_green_tea_1.GetLabel(), self.if_green_tea_2.GetLabel())
                wx.Yield()
                self.show_resource()
                self.exchange(self.if_green_tea_1.GetLabel(), self.if_green_tea_2.GetLabel())
                build_corn = Attack()
                build_corn.attack_url = 'http://drugmil.net/2/xgp/game.php?page=buildings&cmd=insert&building=2&' + \
                                        self.new_number[self.choose_number]
                build_corn.get_attack()
                dlg = wx.MessageDialog(self, '건설하였습니다..', '건설', wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()

    def banked_corn(self, event):
        if self.if_exchange_corn_1.GetLabel() == '가능':
            dlg = wx.MessageDialog(self, '출금없이도 건설이 가능합니다', '건설 오류', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            if self.if_withdrawal_corn_1.GetLabel() == '불가능':
                dlg = wx.MessageDialog(self, '건설이 불가능 합니다.', '건설 불가', wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
            else:
                self.withdrawal(self.if_corn_1.GetLabel(), self.if_corn_2.GetLabel())
                wx.Yield()
                self.show_resource()
                self.exchange(self.if_corn_1.GetLabel(), self.if_corn_2.GetLabel())
                build_corn = Attack()
                build_corn.attack_url = 'http://drugmil.net/2/xgp/game.php?page=buildings&cmd=insert&building=3&' + \
                                        self.new_number[self.choose_number]
                build_corn.get_attack()
                dlg = wx.MessageDialog(self, '건설하였습니다..', '건설', wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()


class main(wx.Frame):
    def __init__(self, parent, main_id, title):
        wx.Frame.__init__(self, parent, main_id, title, wx.DefaultPosition, size=(460, 720),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX)  # 기본 사이즈 460, 720
        menu_bar = wx.MenuBar()
        file_bar = wx.Menu()
        help_bar = wx.Menu()
        convenience_bar = wx.Menu()
        file_bar.Append(101, '&로그인', '약괴밀 홈페이지에 로그인합니다')
        file_bar.Append(103, '&데이터 작성', '광질에 필요한 데이터를 작성합니다')
        file_bar.Append(105, '&macro 폴더 선택', 'macro 폴더를 임의로 선택합니다')
        file_bar.AppendSeparator()  # 구분선 추가
        file_bar.Append(102, '&종료\tCtrl+Q', '닫기')
        help_bar.Append(104, '&정보', '약괴밀 메크로 정보')
        convenience_bar.Append(107, '출석체크', '약괴밀 출석체크')
        convenience_bar.Append(108, '요정 메크로', '원하는 만큼 요정을 잡습니다')
        convenience_bar.Append(113, '강적 메크로', '원하는 만큼 강적을 잡습니다')
        convenience_bar.Append(110, '카드팩 구매', '행동력으로 카드팩을 구매합니다')
        convenience_bar.Append(111, '만능풍뎅이 사용', '만능풍뎅이로 카드를 레벨업합니다.')
        convenience_bar.Append(112, '건설 도우미', '건물 건설에 필요한 기능들이 있습니다.')
        menu_bar.Append(file_bar, '&메인')
        menu_bar.Append(convenience_bar, '&편의기능')
        menu_bar.Append(help_bar, '&정보')
        self.SetMenuBar(menu_bar)
        self.CreateStatusBar()  # 상태바 만들기
        self.panel = wx.Panel(self)

        wx.StaticText(self.panel, id=201, label='출발 행성', pos=(35, 10))
        p_list = []
        if os.path.isfile(global_data.folder_name + '/main.json'):
            p_list = get_data.get_list()
        self.box = wx.ComboBox(self.panel, id=202, pos=(10, 32), size=(140, 22), choices=p_list)

        wx.StaticText(self.panel, id=211, label='목표 행성', pos=(45, 60))

        self.input_galaxy_end = wx.TextCtrl(self.panel, id=212, pos=(20, 82), size=(30, 22))
        self.input_galaxy_end.SetMaxLength(1)
        self.input_system_end = wx.TextCtrl(self.panel, id=213, pos=(53, 82), size=(45, 22))
        self.input_system_end.SetMaxLength(3)
        self.input_planet_end = wx.TextCtrl(self.panel, id=214, pos=(100, 82), size=(33, 22))
        self.input_planet_end.SetMaxLength(2)

        wx.Button(self.panel, id=215, label="등록", pos=(155, 112), size=(100, 30))

        wx.Button(self.panel, id=219, label="전체 공격", pos=(150, 312), size=(100, 100))

        file_list = get_data.get_filename()
        self.listBox = wx.ListBox(self.panel, -1, (10, 120), (130, 510), file_list, wx.LB_SINGLE)
        self.attack_list = wx.ListBox(self.panel, -1, (280, 30), (150, 600), file_list, wx.LB_SINGLE)
        self.attack_list.Clear()

        planet_list = ['행성', '묘지']
        self.planet_choice = wx.RadioBox(self.panel, 501, "행성", (155, 13), wx.DefaultSize,
                                         planet_list, 2, wx.RA_SPECIFY_COLS)
        radio_list = ['꿀광', '클광']
        self.choice = wx.RadioBox(self.panel, 500, "종류", (155, 58), wx.DefaultSize, radio_list, 2, wx.RA_SPECIFY_COLS)

        self.Layout()
        self.Centre(wx.BOTH)
        self.Bind(wx.EVT_MENU, self.on_quit, id=102)  # 종료에 OnQuit 바인드
        self.Bind(wx.EVT_MENU, self.show_custom_dialog, id=101)  # 로그인에 ShowCustomDialog 바인드
        self.Bind(wx.EVT_MENU, self.show_data_dialog, id=103)  # 데이터 작성에 ShowDataDialog 바인드
        self.Bind(wx.EVT_BUTTON, self.make_macro, id=215)  # 등록 버튼에 바인드
        self.Bind(wx.EVT_BUTTON, self.thread, id=219)  # 전체 공격 버튼에 바인드
        self.Bind(wx.EVT_RADIOBOX, self.set_div, self.choice)
        self.Bind(wx.EVT_RADIOBOX, self.set_type, self.planet_choice)
        self.Bind(wx.EVT_COMBOBOX, self.set_planet, self.box)
        self.Bind(wx.EVT_MENU, self.ifo, id=104)
        self.Bind(wx.EVT_MENU, self.open_dir, id=105)
        self.Bind(wx.EVT_MENU, self.attend, id=107)
        self.Bind(wx.EVT_MENU, self.show_fairy, id=108)
        self.Bind(wx.EVT_MENU, self.exchange_card, id=110)
        self.Bind(wx.EVT_MENU, self.exchange_beetle, id=111)
        self.Bind(wx.EVT_MENU, self.build_menu, id=112)  # 건물도우미
        self.Bind(wx.EVT_MENU, self.show_enemy, id=113)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def on_quit(self, event):
        self.Close()

    def build_menu(self, event):
        if not os.path.isfile(global_data.folder_name + '/main.json'):
            dlg = wx.MessageDialog(self, '메인 - 로그인으로 로그인먼저 해야합니다.', '로그인 필요', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            dia1 = build(self, -1, '건물 건설 도우미')
            dia1.ShowModal()
            dia1.Destroy()
            wx.Yield()

    def exchange_card(self, event):
        if not os.path.isfile(global_data.folder_name + '/main.json'):
            dlg = wx.MessageDialog(self, '메인 - 로그인으로 로그인먼저 해야합니다.', '로그인 필요', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            dia1 = card_pack(self, -1, '카드팩 매크로')
            dia1.ShowModal()
            dia1.Destroy()
            wx.Yield()

    def exchange_beetle(self, event):
        if not os.path.isfile(global_data.folder_name + '/main.json'):
            dlg = wx.MessageDialog(self, '메인 - 로그인으로 로그인먼저 해야합니다.', '로그인 필요', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            dia1 = beetle_macro(self, -1, '만풍교환 매크로')
            dia1.ShowModal()
            dia1.Destroy()
            wx.Yield()

    def attend(self, event):
        attend = Attack()
        attend.attack_url = 'http://drugmil.net/2/xgp/pack_bonus3.php?mode=pack16'
        data = attend.soup(attend.get_attack())
        text = data.find('th', 'errormessage').get_text()
        dlg = wx.MessageDialog(self, text, '출석체크', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def open_dir(self, event):
        open_dlg = wx.DirDialog(self, "macro 폴더 선택")
        if open_dlg.ShowModal() == wx.ID_OK:
            global_data.change_folder_name(open_dlg.GetPath())
            self.attack_list.Clear()
            self.listBox.Clear()
            file_list = get_data.get_filename()
            self.listBox.AppendItems(file_list)

    def show_custom_dialog(self, event):
        if not os.path.isfile(global_data.folder_name + '/main.json'):
            dia = login_dialog(self, -1, '로그인')
            dia.ShowModal()
            dia.Destroy()
            wx.Yield()
        else:
            dlg = wx.MessageDialog(self, '이미 로그인되었습니다', '로그인', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def show_fairy(self, event):
        if not os.path.isfile(global_data.folder_name + '/main.json'):
            dlg = wx.MessageDialog(self, '메인 - 로그인으로 로그인먼저 해야합니다.', '로그인 필요', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            dia1 = Fairy_attack(self, -1, '편의기능')
            dia1.ShowModal()
            dia1.Destroy()
            wx.Yield()

    def show_enemy(self, event):
        if not os.path.isfile(global_data.folder_name + '/main.json'):
            dlg = wx.MessageDialog(self, '메인 - 로그인으로 로그인먼저 해야합니다.', '로그인 필요', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            dia1 = Enemy_attack(self, -1, '편의기능')
            dia1.ShowModal()
            dia1.Destroy()
            wx.Yield()

    def show_data_dialog(self, event):
        if not os.path.isfile(global_data.folder_name + '/data.json'):
            dia1 = make_data(self, -1, '데이터 작성')
            dia1.ShowModal()
            dia1.Destroy()
            wx.Yield()
        else:
            dlg = wx.MessageDialog(self, '이미 데이터가 존재합니다', '데이터 작성', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def make_macro(self, event):
        if not os.path.isfile(global_data.folder_name + '/main.json'):
            dlg = wx.MessageDialog(self, '메인 - 로그인으로 로그인먼저 해야합니다.', '로그인 필요', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        elif not os.path.isfile(global_data.folder_name + '/data.json'):
            dlg = wx.MessageDialog(self, '메인 - 데이터작성 으로 데이터 작성먼저 해야합니다.', '데이터 작성 필요', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            helper = re.split('\xa0', str(global_data.choose))
            tee = helper[1][1:-1]
            end = re.split(':', str(tee))
            galaxy = str(end[0])
            system = str(end[1])
            planet = str(end[2])
            galaxy_end = str(self.input_galaxy_end.GetValue())
            system_end = str(self.input_system_end.GetValue())
            planet_end = str(self.input_planet_end.GetValue())
            if not os.path.isfile(global_data.folder_name + '/cus_usedfleet.json'):
                get_data.get_usedfleet(galaxy, system, planet, galaxy_end, system_end, planet_end)
            with open(global_data.folder_name + '/data.json') as json_file3:
                temp = json.load(json_file3)
            temp1 = list(temp.keys())
            temp2 = list(temp.values())
            if global_data.choice == 0:
                with open(global_data.folder_name + '/div_usedfleet.json') as json_file1:
                    usedfleet = json.load(json_file1)
                usedfleet[temp1[0]] = temp2[0]
            elif global_data.choice == 1:
                with open(global_data.folder_name + '/cus_usedfleet.json') as json_file2:
                    usedfleet = json.load(json_file2)
                usedfleet[temp1[0]] = temp2[0]
                usedfleet[temp1[1]] = temp2[1]
            temp3 = {'thisplanettype': '1'}
            if global_data.planet_type == 1:
                temp3['thisplanettype'] = '3'

            data = {'thisgalaxy': galaxy, 'thissystem': system, 'thisplanet': planet, 'galaxy': galaxy_end,
                    'system': system_end, 'planet': planet_end, 'speed': '10', 'mission': '1', 'holdingtime': '0',
                    'planettype': '1'}
            data.update(usedfleet)
            data.update(temp3)
            add_file = galaxy_end + '_' + system_end + '_' + planet_end
            add_list = add_file + '.json'
            with open(global_data.folder_name + '/' + add_list, 'w', encoding='utf-8') as make_file:
                json.dump(data, make_file, indent="\t")
            self.listBox.Append(add_list)
            wx.Yield()

    def set_div(self, event):
        global_data.change_choice(self.choice.GetSelection())

    def set_type(self, event):
        global_data.change_planet_type(self.planet_choice.GetSelection())

    def thread(self, event):
        if global_data.counter == 0:
            t = threading.Thread(target=self.attack)
            t.setDaemon(True)
            t.start()
            global_data.change_counter(1)
        else:
            dlg = wx.MessageDialog(self, '이미 공격이 진행중입니다.', '공격 진행중', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def attack(self):
        attack_list = get_data.get_filename()
        if not os.path.isfile(global_data.folder_name + '/main.json'):
            dlg = wx.MessageDialog(self, '메인 - 로그인으로 로그인먼저 해야합니다.', '로그인 필요', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            global_data.change_counter(0)
            dlg.Destroy()
        elif not os.path.isfile(global_data.folder_name + '/data.json'):
            dlg = wx.MessageDialog(self, '메인 - 데이터작성 으로 데이터 작성먼저 해야합니다.', '데이터 작성 필요', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            global_data.change_counter(0)
            dlg.Destroy()
        elif not attack_list:
            dlg = wx.MessageDialog(self, '공격 데이터가 없습니다', '공격 데이터 작성 필요', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            global_data.change_counter(0)
            dlg.Destroy()
        else:
            counter = len(attack_list)
            while counter != 0:
                self.all_attack(attack_list.pop())
                wx.Yield()
                counter -= 1
            dlg = wx.MessageDialog(self, '모든 목표를 공격했습니다', '공격 완료', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            global_data.change_counter(0)
            dlg.Destroy()

    def all_attack(self, point):
        attack = Attack()
        with open(global_data.folder_name + '/' + point) as json_file1:
            json_data1 = json.load(json_file1)
        temp = json_data1['thisgalaxy'] + ':' + json_data1['thissystem'] + ':' + json_data1['thisplanet']
        attack_counter = 0
        attack_list = get_data.answer()
        h_data = get_data.get_planet_number()
        n = ''
        while attack_counter < len(h_data):
            if temp in attack_list[attack_counter]:
                if json_data1['thisplanettype'] == '3' and str('(묘지)') in attack_list[attack_counter]:
                    n = str(global_data.number_list()[attack_counter])
                    break
                else:
                    if not str('(묘지)') in attack_list[attack_counter]:
                        n = str(global_data.number_list()[attack_counter])
                        break
            attack_counter += 1
        attack.attack_url = "http://drugmil.net/2/xgp/game.php?page=fleet3&" + n
        attack.attack_data = json_data1
        res = attack.post_attack().status_code
        viewer = point[:-5]
        if not res == 200:
            self.attack_list.Append(viewer + '는 공격하지 못했습니다.')
        else:
            self.attack_list.Append(viewer + '를 공격했습니다.')
        time.sleep(1.0)

    def set_planet(self, event):
        global_data.change_choose(self.box.GetStringSelection())
        global_data.change_choose_number(self.box.GetSelection())

    def ifo(self, event):
        global version
        dlg = wx.MessageDialog(self, '약괴밀 메크로 버전 ' + version + '\n'
                                     '\n제작자 : 마리사라', '정보', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnClose(self, event):
        sys.exit()


class Update(wx.MessageDialog):
    def __init__(self, parent, message, caption, style):
        wx.MessageDialog.__init__(self, parent, message, caption, style)


version = '3.72'


class starter(wx.App):
    def OnInit(self):
        header = {"authority": "drive.google.com", "Connection": "keep-alive",
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
        url = 'https://docs.google.com/spreadsheets/d/1Eq9_C5l5RPVJvPNcHWjcdXXO-tXrcUk3/edit#gid=555607571'
        attack = requests.get(url=url, headers=header, timeout=30)
        html = attack.content
        soup = BeautifulSoup(html, 'html.parser')
        turn = soup.find("td", {"class": "s0"})
        if float(turn.get_text()) <= float(version):
            frame = main(None, -1, '약괴밀 매크로 ' + version)
            frame.Show(True)
            frame.Centre()
            return True
        else:
            update = Update(None, '현재 버전 : ' + version + '\n새 버전 : ' + turn.get_text() +
                            '\n구버전입니다. 업데이트가 필요합니다', '업데이트 필요', wx.OK | wx.ICON_INFORMATION)
            update.ShowModal()
            update.Centre()
            update.Destroy()
            os.system('explorer "https://drive.google.com/u/0/uc?id=17C2mFR77_YSmTY3867zNIJy2kcD9J2dr&export=download"')
            return True


if not os.path.isdir('macro'):
    os.mkdir('macro')
app = starter(0)
app.MainLoop()
