import wx
import requests
import re
import json
import os
from bs4 import BeautifulSoup
import time
import threading
from cefpython3 import cefpython as cef

number_list = []
is_page = False
folder_name = 'macro'


class CefApp(wx.App):
    def __init__(self, redirect):
        self.timer = None
        self.timer_id = 1
        self.is_initialized = False
        super(CefApp, self).__init__(redirect=redirect)

    def OnPreInit(self):
        super(CefApp, self).OnPreInit()

    def OnInit(self):
        self.initialize()
        return True

    def initialize(self):
        if self.is_initialized:
            return
        self.is_initialized = True
        self.create_timer()
        frame = Dialog3()
        self.SetTopWindow(frame)

    def create_timer(self):
        self.timer = wx.Timer(self, self.timer_id)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.timer.Start(10)  # 10ms timer

    def on_timer(self, _):
        cef.MessageLoopWork()

    def OnExit(self):
        self.timer.Stop()
        return 0


class Dialog3(wx.Dialog):
    def __init__(self):
        self.browser = None
        size = scale_window_size_for_high_dpi(1920, 1080)
        wx.Dialog.__init__(self, parent=None, id=wx.ID_ANY,
                           title='약괴밀', size=size)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.browser_panel = wx.Panel(self, style=wx.WANTS_CHARS)
        self.browser_panel.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.browser_panel.Bind(wx.EVT_SIZE, self.OnSize)
        self.embed_browser()
        self.Show()

    def embed_browser(self):
        window_info = cef.WindowInfo()
        (width, height) = self.browser_panel.GetClientSize().Get()
        assert self.browser_panel.GetHandle(), "Window handle not available"
        window_info.SetAsChild(self.browser_panel.GetHandle(),
                               [0, 0, width, height])
        mgr = cef.CookieManager.GetGlobalManager()
        cookie = cef.Cookie()
        temp = database.cookies()
        key = {'name': '약괴밀', 'value': temp['\354\225\275\352\264\264\353\260\200']}
        cookie.Set(key)
        mgr.SetCookie("http://drugmil.net/2/xgp/game.php", cookie)
        self.browser = cef.CreateBrowserSync(window_info,
                                             url="http://drugmil.net/2/xgp/game.php?")

    def OnSetFocus(self, _):
        if not self.browser:
            return
        cef.WindowUtils.OnSetFocus(self.browser_panel.GetHandle(),
                                   0, 0, 0)
        self.browser.SetFocus(True)

    def OnSize(self, _):
        if not self.browser:
            return
        cef.WindowUtils.OnSize(self.browser_panel.GetHandle(),
                               0, 0, 0)
        self.browser.NotifyMoveOrResizeStarted()

    def OnClose(self, event):
        global is_page
        if not self.browser:
            return
        self.browser.ParentWindowWillClose()
        event.Skip()
        self.clear_browser_references()
        is_page = False
        self.Destroy()

    def clear_browser_references(self):
        self.browser = None


def scale_window_size_for_high_dpi(width, height):
    (_, _, max_width, max_height) = wx.GetClientDisplayRect().Get()
    (width, height) = cef.DpiAware.Scale((width, height))
    if width > max_width:
        width = max_width
    if height > max_height:
        height = max_height
    return width, height


class Database:
    def cookies(self):
        with open(folder_name + '/main.json') as json_file:
            cookies = json.load(json_file)
        return cookies

    def header(self):
        header = {"Host": "drugmil.net", "Connection": "keep-alive",
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
        return header


database = Database()


class Attack:
    def __init__(self):
        self.attack_data = ''
        self.attack_url = ''

    def url(self, attack_url):
        self.attack_url = attack_url

    def data(self, attack_data):
        self.attack_data = attack_data

    def get_attack(self):
        return requests.get(url=self.attack_url, cookies=database.cookies(), headers=database.header(),
                            allow_redirects=False, timeout=30)

    def post_attack(self):
        return requests.post(url=self.attack_url, cookies=database.cookies(), headers=database.header(),
                             data=self.attack_data, allow_redirects=False, timeout=30)

    def soup(self, attack):
        html = attack.content
        soup = BeautifulSoup(html, 'html.parser')
        return soup


def get_filename():
    file_name = os.listdir(folder_name)
    if os.path.isfile(folder_name + '/main.json'):
        file_name.remove('main.json')
    if os.path.isfile(folder_name + '/div_usedfleet.json'):
        file_name.remove('div_usedfleet.json')
    if os.path.isfile(folder_name + '/cus_usedfleet.json'):
        file_name.remove('cus_usedfleet.json')
    if os.path.isfile(folder_name + '/data.json'):
        file_name.remove('data.json')
    return file_name


def get_usedfleet(galaxy, system, planet, galaxyend, systemend, planetend):
    get = Attack()
    get.attack_data = {'galaxy': galaxy, 'system': system, 'planet': planet, 'galaxyend': galaxyend,
                       'systemend': systemend, 'planetend': planetend, 'onsubmit': 'this.submit.disabled = true;'}
    get.attack_url = "http://drugmil.net/2/xgp/game.php?page=fleet1"
    with open(folder_name + '/data.json') as json_file1:
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
    with open(folder_name + '/div_usedfleet.json', 'w', encoding='utf-8') as g:
        json.dump(one_usedfleet, g, indent="\t")
    get.attack_data[keys[1]] = values[1]
    soup1 = get.soup(get.post_attack())
    p_data1 = soup1.find_all('input')
    two_data = p_data1[9]
    two_speed = p_data1[8]
    t1 = re.split('[;"]', str(two_data))
    p1 = re.split('[;"]', str(two_speed))
    two_usedfleet = {'usedfleet': t1[-2], 'speedallsmin': p1[-2]}
    with open(folder_name + '/cus_usedfleet.json', 'w', encoding='utf-8') as g:
        json.dump(two_usedfleet, g, indent="\t")


def get_list():
    get = Attack()
    get.attack_url = "http://drugmil.net/2/xgp/game.php?page=fleet"
    soup0 = get.soup(get.get_attack())
    h_data = soup0.find_all('option')
    counters = 0
    list0 = []
    while counters < len(h_data):
        list0.append(h_data[counters].get_text())
        counters += 1
    global number_list
    counters = 0
    while counters < len(h_data):
        temps = re.split('[;]', str(h_data[counters]))
        number_list.append(temps[2][:-4])
        counters += 1
    return list0


def get_planet_number():
    get = Attack()
    get.attack_url = "http://drugmil.net/2/xgp/game.php?page=fleet"
    soup = get.soup(get.get_attack())
    h_data = soup.find_all('option')
    return h_data


choice = 0
planet_type = 0
choose = []
choose_number = 0
counter = 0


class Dialog1(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, pos=wx.DefaultPosition, size=wx.Size(300, 300))
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
        with open(folder_name + '/data.json', 'w', encoding='utf-8') as g:
            json.dump(data, g, indent="\t")


class Dialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, pos=wx.DefaultPosition, size=wx.Size(300, 200))
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
        url = 'http://drugmil.net/2/xgp/index.php'
        data = {'username': ids, 'password': password, 'submit': '로그인'}
        res = requests.post(url=url, data=data, headers=database.header(), allow_redirects=False)
        t = res.headers.get('Set-cookie')
        t = re.split('[=;]', t)
        name = '\354\225\275\352\264\264\353\260\200'
        value = ''.join(t[1])
        cookie = {
            name: value
        }
        if not (os.path.isdir('macro')):
            os.makedirs('macro')
        with open(folder_name + '/main.json', 'w', encoding='utf-8') as g:
            json.dump(cookie, g, indent="\t")


class Menu(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, size=(460, 720),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX)  # 기본 사이즈 460, 720
        menu_bar = wx.MenuBar()
        file_bar = wx.Menu()
        help_bar = wx.Menu()
        file_bar.Append(101, '&로그인', '약괴밀 홈페이지에 로그인합니다')
        file_bar.Append(103, '&데이터 작성', '광질에 필요한 데이터를 작성합니다')
        file_bar.Append(105, '&macro 폴더 선택', 'macro 폴더를 임의로 선택합니다')
        file_bar.Append(106, '약괴밀 화면', '약괴밀 페이지를 엽니다')
        file_bar.AppendSeparator()  # 구분선 추가
        file_bar.Append(102, '&종료\tCtrl+Q', '닫기')
        help_bar.Append(104, '&정보', '약괴밀 메크로 정보')
        menu_bar.Append(file_bar, '&메인')
        menu_bar.Append(help_bar, '&정보')
        self.SetMenuBar(menu_bar)
        self.CreateStatusBar()  # 상태바 만들기
        self.panel = wx.Panel(self)

        wx.StaticText(self.panel, id=201, label='출발 행성', pos=(35, 10))
        p_list = []
        if os.path.isfile(folder_name + '/main.json'):
            p_list = get_list()
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

        file_list = get_filename()
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
        self.Bind(wx.EVT_MENU, self.open_drugmil, id=106)
        self.Bind(wx.EVT_MENU, self.open_dir, id=105)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def on_quit(self, event):
        self.Close()

    def open_dir(self, event):
        global folder_name
        open_dlg = wx.DirDialog(self, "macro 폴더 선택")
        if open_dlg.ShowModal() == wx.ID_OK:
            folder_name = open_dlg.GetPath()
            self.attack_list.Clear()
            self.listBox.Clear()
            file_list = get_filename()
            self.listBox.AppendItems(file_list)

    def show_custom_dialog(self, event):
        if not os.path.isfile(folder_name + '/main.json'):
            dia = Dialog(self, -1, '로그인')
            dia.ShowModal()
            dia.Destroy()
            wx.Yield()
        else:
            dlg = wx.MessageDialog(self, '이미 로그인되었습니다', '로그인', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def open_drugmil(self, event):
        global is_page
        if not is_page:
            settings = {}
            cef.DpiAware.EnableHighDpiSupport()
            cef.Initialize(settings=settings)
            CefApp(False)
            is_page = True
        else:
            dlg = wx.MessageDialog(self, '이미 켜져있습니다', '약괴밀', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def show_data_dialog(self, event):
        if not os.path.isfile(folder_name + '/data.json'):
            dia1 = Dialog1(self, -1, '데이터 작성')
            dia1.ShowModal()
            dia1.Destroy()
            wx.Yield()
        else:
            dlg = wx.MessageDialog(self, '이미 데이터가 존재합니다', '데이터 작성', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def make_macro(self, event):
        if not os.path.isfile(folder_name + '/main.json'):
            dlg = wx.MessageDialog(self, '메인 - 로그인으로 로그인먼저 해야합니다.', '로그인 필요', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        elif not os.path.isfile(folder_name + '/data.json'):
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
            galaxy_end = str(self.input_galaxy_end.GetValue())
            system_end = str(self.input_system_end.GetValue())
            planet_end = str(self.input_planet_end.GetValue())
            if not os.path.isfile(folder_name + '/cus_usedfleet.json'):
                get_usedfleet(galaxy, system, planet, galaxy_end, system_end, planet_end)
            with open(folder_name + '/data.json') as json_file3:
                temp = json.load(json_file3)
            temp1 = list(temp.keys())
            temp2 = list(temp.values())
            if choice == 0:
                with open(folder_name + '/div_usedfleet.json') as json_file1:
                    usedfleet = json.load(json_file1)
                usedfleet[temp1[0]] = temp2[0]
            elif choice == 1:
                with open(folder_name + '/cus_usedfleet.json') as json_file2:
                    usedfleet = json.load(json_file2)
                usedfleet[temp1[0]] = temp2[0]
                usedfleet[temp1[1]] = temp2[1]
            temp3 = {'thisplanettype': '1'}
            if planet_type == 1:
                temp3['thisplanettype'] = '3'

            data = {'thisgalaxy': galaxy, 'thissystem': system, 'thisplanet': planet, 'galaxy': galaxy_end,
                    'system': system_end, 'planet': planet_end, 'speed': '10', 'mission': '1', 'holdingtime': '0',
                    'planettype': '1'}
            data.update(usedfleet)
            data.update(temp3)
            add_file = galaxy_end + '_' + system_end + '_' + planet_end
            add_list = add_file + '.json'
            with open(folder_name + '/' + add_list, 'w', encoding='utf-8') as make_file:
                json.dump(data, make_file, indent="\t")
            self.listBox.Append(add_list)
            wx.Yield()

    def set_div(self, event):
        global choice
        choice = self.choice.GetSelection()

    def set_type(self, event):
        global planet_type
        planet_type = self.planet_choice.GetSelection()

    def thread(self, event):
        global counter
        if counter == 0:
            t = threading.Thread(target=self.attack)
            t.setDaemon(True)
            t.start()
            counter = 1
        else:
            dlg = wx.MessageDialog(self, '이미 공격이 진행중입니다.', '공격 진행중', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def attack(self):
        global counter
        attack_list = get_filename()
        if not os.path.isfile(folder_name + '/main.json'):
            dlg = wx.MessageDialog(self, '메인 - 로그인으로 로그인먼저 해야합니다.', '로그인 필요', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            counter = 0
            dlg.Destroy()
        elif not os.path.isfile(folder_name + '/data.json'):
            dlg = wx.MessageDialog(self, '메인 - 데이터작성 으로 데이터 작성먼저 해야합니다.', '데이터 작성 필요', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            counter = 0
            dlg.Destroy()
        elif not attack_list:
            dlg = wx.MessageDialog(self, '공격 데이터가 없습니다', '공격 데이터 작성 필요', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            counter = 0
            dlg.Destroy()
        else:
            counter = len(attack_list)
            while counter != 0:
                self.all_attack(attack_list.pop())
                wx.Yield()
                counter -= 1
            dlg = wx.MessageDialog(self, '모든 목표를 공격했습니다', '공격 완료', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            counter = 0
            dlg.Destroy()

    def all_attack(self, point):
        attack = Attack()
        with open(folder_name + '/' + point) as json_file1:
            json_data1 = json.load(json_file1)
        temp = json_data1['thisgalaxy'] + ':' + json_data1['thissystem'] + ':' + json_data1['thisplanet']
        attack_counter = 0
        attack_list = get_list()
        h_data = get_planet_number()
        n = ''
        while attack_counter < len(h_data):
            if temp in attack_list[attack_counter]:
                if json_data1['thisplanettype'] == '3' and str('(묘지)') in attack_list[attack_counter]:
                    n = str(number_list[attack_counter])
                    break
                else:
                    if not str('(묘지)') in attack_list[attack_counter]:
                        n = str(number_list[attack_counter])
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
        time.sleep(1.5)

    def set_planet(self, event):
        global choose, choose_number
        choose = self.box.GetStringSelection()
        choose_number = self.box.GetSelection()

    def ifo(self, event):
        dlg = wx.MessageDialog(self, '약괴밀 메크로 버전 3.1.1\n'
                                     '3.0 : GUI 모드화  3.1 : 실행불가 버그 수정\n'
                                     '3.1.1 : 정보창 추가  3.1.2 : 묘지관련 오류 수정\n'
                                     '3.1.3 : 묘지관련 추가 오류 수정\n'
                                     '3.2 : 쓰레드 기능 구현  3.3 : 약괴밀 화면기능 추가\n'
                                     '3.3.1 : macro폴더 선택기능 추가  3.3.2 : 쓰레드 관련 오류 수정'
                                     '\n제작자 : 마리사라', '정보', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnClose(self, event):
        event.Skip()
        quit(0)


class MyApp(wx.App):
    def OnInit(self):
        frame = Menu(None, -1, '약괴밀 메크로 3.3.2')
        frame.Show(True)
        frame.Centre()
        return True


if not os.path.isdir('macro'):
    os.mkdir('macro')
app = MyApp(0)
app.MainLoop()
