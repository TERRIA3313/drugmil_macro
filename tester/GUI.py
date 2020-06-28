import wx
import requests
import re
import json
import os
from bs4 import BeautifulSoup
import time


number_list = []


def main_json():
    with open('macro/main.json') as json_file:
        cookie = json.load(json_file)
    return cookie


def get_filename():
    filename = os.listdir('macro')
    if os.path.isfile('macro/main.json'):
        filename.remove('main.json')
    if os.path.isfile('macro/div_usedfleet.json'):
        filename.remove('div_usedfleet.json')
    if os.path.isfile('macro/cus_usedfleet.json'):
        filename.remove('cus_usedfleet.json')
    if os.path.isfile('macro/data.json'):
        filename.remove('data.json')
    return filename


def get_usedfleet(galaxy, system, planet, galaxyend, systemend, planetend):
    data = {'galaxy': galaxy, 'system': system, 'planet': planet, 'galaxyend': galaxyend, 'systemend': systemend,
            'planetend': planetend, 'onsubmit': 'this.submit.disabled = true;'}
    url = "http://drugmil.net/2/xgp/game.php?page=fleet1"
    header = {"Host": "drugmil.net", "Connection": "keep-alive",
              "Referer": "Http://drugmil.net/2/xgp/game.php?page=fleet"}
    with open('macro/data.json') as json_file1:
        json_data1 = json.load(json_file1)
    cookie = main_json()
    keys = list(json_data1.keys())
    values = list(json_data1.values())
    data[keys[0]] = values[0]
    attack = requests.post(url=url, cookies=cookie, headers=header, data=data, timeout=30)
    html = attack.content
    soup = BeautifulSoup(html, 'html.parser')
    p_data = soup.find_all('input')
    one_data = p_data[5]
    one_speed = p_data[4]
    t = re.split('[;"]', str(one_data))
    p = re.split('[;"]', str(one_speed))
    one_usedfleet = {'usedfleet': t[-2], 'speedallsmin': p[-2]}
    with open('macro/div_usedfleet.json', 'w', encoding='utf-8') as g:
        json.dump(one_usedfleet, g, indent="\t")
    data[keys[1]] = values[1]
    attack = requests.post(url=url, cookies=cookie, headers=header, data=data, timeout=30)
    html1 = attack.content
    soup1 = BeautifulSoup(html1, 'html.parser')
    p_data1 = soup1.find_all('input')
    two_data = p_data1[9]
    two_speed = p_data1[8]
    t1 = re.split('[;"]', str(two_data))
    p1 = re.split('[;"]', str(two_speed))
    two_usedfleet = {'usedfleet': t1[-2], 'speedallsmin': p1[-2]}
    with open('macro/cus_usedfleet.json', 'w', encoding='utf-8') as g:
        json.dump(two_usedfleet, g, indent="\t")


def get_list():
    url0 = "http://drugmil.net/2/xgp/game.php?page=fleet"
    header0 = {"Host": "drugmil.net", "Connection": "keep-alive"}
    cookie0 = main_json()
    attack0 = requests.post(url=url0, cookies=cookie0, headers=header0, timeout=30)
    html0 = attack0.content
    soup0 = BeautifulSoup(html0, 'html.parser')
    h_data = soup0.find_all('option')
    counter = 0
    list0 = []
    while counter < len(h_data):
        list0.append(h_data[counter].get_text())
        counter += 1
    global number_list
    counter = 0
    while counter < len(h_data):
        temps = re.split('[;]', str(h_data[counter]))
        number_list.append(temps[2][:-4])
        counter += 1
    return list0


def get_planet_number():
    url = "http://drugmil.net/2/xgp/game.php?page=fleet"
    header = {"Host": "drugmil.net", "Connection": "keep-alive"}
    cookie = main_json()
    attack = requests.post(url=url, cookies=cookie, headers=header, timeout=30)
    html = attack.content
    soup = BeautifulSoup(html, 'html.parser')
    h_data = soup.find_all('option')
    return h_data


choice = 0
planet_type = 0
choose = []
choose_number = 0


class Dialog1(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, pos=wx.DefaultPosition, size=wx.Size(300, 300))
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        self.text_division = wx.StaticText(self, 2001, u"항공전대 갯수",
                                           wx.DefaultPosition, wx.Size(300, -1), wx.ALIGN_CENTRE)
        self.text_division.Wrap(-1)
        bSizer1.Add(self.text_division, 0, wx.ALL, 5)
        self.m_textCtrl1 = wx.TextCtrl(self, 2002, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1), 0)
        bSizer1.Add(self.m_textCtrl1, 0, wx.ALL, 5)
        self.text_number = wx.StaticText(self, 2003, u"클광용 번호(중뇌장형 : 219 ,린 : 250)",
                                         wx.DefaultPosition, wx.Size(300, -1), wx.ALIGN_CENTRE)
        self.text_number.Wrap(-1)
        bSizer1.Add(self.text_number, 0, wx.ALL, 5)
        self.m_textCtrl2 = wx.TextCtrl(self, 2004, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1), 0)
        bSizer1.Add(self.m_textCtrl2, 0, wx.ALL, 5)
        self.text_password = wx.StaticText(self, 2003, u"클광용 유닛 갯수", wx.DefaultPosition,
                                           wx.Size(300, -1), wx.ALIGN_CENTRE)
        self.text_password.Wrap(-1)
        bSizer1.Add(self.text_password, 0, wx.ALL, 5)
        self.m_textCtrl3 = wx.TextCtrl(self, 2004, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1), 0)
        bSizer1.Add(self.m_textCtrl3, 0, wx.ALL, 5)
        self.make_button = wx.Button(self, 2006, u"생성", wx.DefaultPosition, wx.Size(300, -1), 0)
        bSizer1.Add(self.make_button, 0, wx.ALL, 5)
        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)
        self.Bind(wx.EVT_BUTTON, self.diaQuit, id=2006)  # 생성 버튼을 diaQuit에 바인드

    def diaQuit(self, event):
        self.make()
        self.EndModal(1)

    def make(self):
        divison = str(self.m_textCtrl1.GetValue())
        custom_number = str(self.m_textCtrl2.GetValue())
        custom_many = str(self.m_textCtrl3.GetValue())
        data = {'ship221': divison, 'ship' + custom_number: custom_many}
        with open('macro/data.json', 'w', encoding='utf-8') as g:
            json.dump(data, g, indent="\t")


class Dialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, pos=wx.DefaultPosition, size=wx.Size(300, 200))
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        self.text_id = wx.StaticText(self, 1001, u"아이디", wx.DefaultPosition, wx.Size(300, -1), wx.ALIGN_CENTRE)
        self.text_id.Wrap(-1)
        bSizer1.Add(self.text_id, 0, wx.ALL, 5)
        self.m_textCtrl1 = wx.TextCtrl(self, 1002, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1), 0)
        bSizer1.Add(self.m_textCtrl1, 0, wx.ALL, 5)
        self.text_password = wx.StaticText(self, 1003, u"비밀번호", wx.DefaultPosition, wx.Size(300, -1), wx.ALIGN_CENTRE)
        self.text_password.Wrap(-1)
        bSizer1.Add(self.text_password, 0, wx.ALL, 5)
        self.m_textCtrl2 = wx.TextCtrl(self, 1004, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1), wx.TE_PASSWORD)
        bSizer1.Add(self.m_textCtrl2, 0, wx.ALL, 5)
        self.login_button = wx.Button(self, 1006, u"로그인", wx.DefaultPosition, wx.Size(300, -1), 0)
        bSizer1.Add(self.login_button, 0, wx.ALL, 5)
        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)
        self.Bind(wx.EVT_BUTTON, self.diaQuit, id=1006)  # 로그인 버튼을 diaQuit에 바인드

    def diaQuit(self, event):
        self.login()
        self.EndModal(1)

    def login(self):
        ids = str(self.m_textCtrl1.GetValue())
        password = str(self.m_textCtrl2.GetValue())
        url = 'http://drugmil.net/2/xgp/index.php'
        req_data = {'username': ids, 'password': password, 'submit': '로그인'}
        res = requests.post(url=url, data=req_data, allow_redirects=False)
        t = res.headers.get('Set-cookie')
        t = re.split('[=;]', t)
        name = '\354\225\275\352\264\264\353\260\200'
        value = ''.join(t[1])
        cookie = {
            name: value
        }
        if not (os.path.isdir('macro')):
            os.makedirs('macro')
        with open('macro/main.json', 'w', encoding='utf-8') as g:
            json.dump(cookie, g, indent="\t")


class Menu(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, size=(520, 720), style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX)
        menubar = wx.MenuBar()
        mfile = wx.Menu()
        mhelp = wx.Menu()
        mfile.Append(101, '&로그인', '약괴밀 홈페이지에 로그인합니다')
        mfile.Append(103, '&데이터 작성', '광질에 필요한 데이터를 작성합니다')
        mfile.AppendSeparator()  # 구분선 추가
        mfile.Append(102, '&종료\tCtrl+Q', '닫기')
        menubar.Append(mfile, '&메인')
        menubar.Append(mhelp, '&정보')
        mhelp.Append(104, '&정보', '약괴밀 메크로 정보')
        self.SetMenuBar(menubar)
        self.CreateStatusBar()  # 상태바 만들기
        panel = wx.Panel(self)

        wx.StaticText(panel, id=201, label='출발 행성', pos=(35, 10))
        p_list = []
        if os.path.isfile('macro/main.json'):
            p_list = get_list()
        self.box = wx.ComboBox(panel, id=202, pos=(10, 32), size=(140, 22), choices=p_list)

        wx.StaticText(panel, id=211, label='목표 행성', pos=(45, 60))

        self.input_galaxyend = wx.TextCtrl(panel, id=212, pos=(20, 82), size=(30, 22))
        self.input_galaxyend.SetMaxLength(1)
        self.input_systemend = wx.TextCtrl(panel, id=213, pos=(53, 82), size=(45, 22))
        self.input_systemend.SetMaxLength(3)
        self.input_planetend = wx.TextCtrl(panel, id=214, pos=(100, 82), size=(33, 22))
        self.input_planetend.SetMaxLength(2)

        wx.Button(panel, id=215, label="등록", pos=(155, 112), size=(100, 30))

        wx.Button(panel, id=219, label="전체 공격", pos=(150, 312), size=(100, 100))

        filename = get_filename()
        self.listBox = wx.ListBox(panel, -1, (10, 120), (130, 510), filename, wx.LB_SINGLE)
        self.attacklist = wx.ListBox(panel, -1, (330, 30), (150, 600), filename, wx.LB_SINGLE)
        self.attacklist.Clear()

        planet_list = ['행성', '묘지']
        self.planet_choice = wx.RadioBox(panel, 501, "행성", (155, 13), wx.DefaultSize, planet_list, 2, wx.RA_SPECIFY_COLS)
        radio_list = ['꿀광', '클광']
        self.choice = wx.RadioBox(panel, 500, "종류", (155, 58), wx.DefaultSize, radio_list, 2, wx.RA_SPECIFY_COLS)

        self.Layout()
        self.Centre(wx.BOTH)

        self.Bind(wx.EVT_MENU, self.OnQuit, id=102)  # 종료에 OnQuit 바인드
        self.Bind(wx.EVT_MENU, self.ShowCustomDialog, id=101)  # 로그인에 ShowCustomDialog 바인드
        self.Bind(wx.EVT_MENU, self.ShowDataDialog, id=103)  # 데이터 작성에 ShowDataDialog 바인드
        self.Bind(wx.EVT_BUTTON, self.make_macro, id=215)  # 등록 버튼에 바인드
        self.Bind(wx.EVT_BUTTON, self.attack, id=219)  # 전체 공격 버튼에 바인드
        self.Bind(wx.EVT_RADIOBOX, self.set_div, self.choice)
        self.Bind(wx.EVT_RADIOBOX, self.set_type, self.planet_choice)
        self.Bind(wx.EVT_COMBOBOX, self.set_planet, self.box)
        self.Bind(wx.EVT_MENU, self.ifo, id=104)

    def OnQuit(self, event):
        self.Close()

    def ShowCustomDialog(self, event):
        if not os.path.isfile('macro/main.json'):
            dia = Dialog(self, -1, '로그인')
            dia.ShowModal()
            dia.Destroy()
            wx.Yield()
        else:
            dlg = wx.MessageDialog(self, '이미 로그인되었습니다', '로그인', wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def ShowDataDialog(self, event):
        if not os.path.isfile('macro/data.json'):
            dia1 = Dialog1(self, -1, '데이터 작성')
            dia1.ShowModal()
            dia1.Destroy()
            wx.Yield()
        else:
            dlg = wx.MessageDialog(self, '이미 데이터가 존재합니다', '데이터 작성', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def make_macro(self, event):
        if not os.path.isfile('macro/main.json'):
            dlg = wx.MessageDialog(self, '메인 - 로그인으로 로그인먼저 해야합니다.', '로그인 필요', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        elif not os.path.isfile('macro/data.json'):
            dlg = wx.MessageDialog(self, '메인 - 데이터작성 으로 데이터 작성먼저 해야합니다.', '데이터 작성 필요', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            handler = choose
            helper = re.split('\xa0', str(handler))
            tee = helper[1][1:-1]
            end = re.split(':', str(tee))
            galaxy = str(end[0])
            system = str(end[1])
            planet = str(end[2])
            galaxyend = str(self.input_galaxyend.GetValue())
            systemend = str(self.input_systemend.GetValue())
            planetend = str(self.input_planetend.GetValue())
            if not os.path.isfile('macro/cus_usedfleet.json'):
                get_usedfleet(galaxy, system, planet, galaxyend, systemend, planetend)
            with open('macro/data.json') as json_file3:
                temp = json.load(json_file3)
            temp1 = list(temp.keys())
            temp2 = list(temp.values())
            if choice == 0:
                with open('macro/div_usedfleet.json') as json_file1:
                    usedfleet = json.load(json_file1)
                usedfleet[temp1[0]] = temp2[0]
            elif choice == 1:
                with open('macro/cus_usedfleet.json') as json_file2:
                    usedfleet = json.load(json_file2)
                usedfleet[temp1[0]] = temp2[0]
                usedfleet[temp1[1]] = temp2[1]
            temp3 = {'thisplanettype': '1'}
            if planet_type == 1:
                temp3['thisplanettype'] = '3'

            data = {'thisgalaxy': galaxy, 'thissystem': system, 'thisplanet': planet, 'galaxy': galaxyend,
                    'system': systemend, 'planet': planetend, 'speed': '10', 'mission': '1', 'holdingtime': '0',
                    'planettype': '1'}
            data.update(usedfleet)
            data.update(temp3)
            add_file = galaxyend + '_' + systemend + '_' + planetend
            add_list = add_file + '.json'
            with open('macro/' + add_list, 'w', encoding='utf-8') as make_file:
                json.dump(data, make_file, indent="\t")
            self.listBox.Append(add_list)
            wx.Yield()

    def set_div(self, event):
        global choice
        choice = self.choice.GetSelection()

    def set_type(self, event):
        global planet_type
        planet_type = self.planet_choice.GetSelection()

    def attack(self, event):
        attack_list = get_filename()
        if not os.path.isfile('macro/main.json'):
            dlg = wx.MessageDialog(self, '메인 - 로그인으로 로그인먼저 해야합니다.', '로그인 필요', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        elif not os.path.isfile('macro/data.json'):
            dlg = wx.MessageDialog(self, '메인 - 데이터작성 으로 데이터 작성먼저 해야합니다.', '데이터 작성 필요', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        elif not attack_list:
            dlg = wx.MessageDialog(self, '공격 데이터가 없습니다', '공격 데이터 작성 필요', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            counter = len(attack_list)
            while counter != 0:
                self.all_attack(attack_list.pop())
                wx.Yield()
                counter -= 1
            dlg = wx.MessageDialog(self, '모든 목표를 공격했습니다', '공격 완료', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def all_attack(self, point):
        header = {"Host": "drugmil.net", "Connection": "keep-alive",
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
        with open('macro/' + point) as json_file1:
            json_data1 = json.load(json_file1)
        cookie = main_json()
        temp = json_data1['thisgalaxy'] + ':' + json_data1['thissystem'] + ':' + json_data1['thisplanet']
        counter = 0
        list = get_list()
        h_data = get_planet_number()
        n = ''
        while counter < len(h_data):
            if temp in list[counter]:
                n = str(number_list[counter])
            counter += 1
        url = "http://drugmil.net/2/xgp/game.php?page=fleet3&" + n
        print(url)
        attack = requests.post(url, cookies=cookie, headers=header, data=json_data1, allow_redirects=False, timeout=30)
        res = attack.status_code
        viewer = point[:-5]
        if not res == 200:
            self.attacklist.Append(viewer + '는 공격하지 못했습니다.')
        else:
            self.attacklist.Append(viewer + '를 공격했습니다.')
        time.sleep(1.5)

    def set_planet(self, event):
        global choose, choose_number
        choose = self.box.GetStringSelection()
        choose_number = self.box.GetSelection()

    def ifo(self, event):
        dlg = wx.MessageDialog(self, '약괴밀 메크로 버전 3.1.1\n'
                                     '3.0 : GUI 모드화  3.1 : 실행불가 버그 수정\n'
                                     '3.1.1 : 정보창 추가\n제작자 : 마리사라', '정보', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


class MyApp(wx.App):
    def OnInit(self):
        frame = Menu(None, -1, '약괴밀 메크로 3.1.1')
        frame.Show(True)
        frame.Centre()
        return True


if not os.path.isdir('macro'):
    os.mkdir('macro')
app = MyApp(0)
app.MainLoop()