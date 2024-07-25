# -*- coding:utf-8 -*-
import json
import os
import sys
import requests
import threading
import ast
import multiprocessing
import wx
from pyperclip3 import copy
from Taowa_wx import *
get_list_data = []

ItemName_matched_items_p = []
ItemName_matched_items_c = []
ItemName_matched_items_content = []
get_can_place_on_matched_items_p = []
get_can_place_on_matched_items_c = []
get_can_place_on_matched_items_content = []
get_can_destroy_matched_items_p = []
get_can_destroy_matched_items_c = []
get_can_destroy_matched_items_content = []

get_can_place_on_list = []
get_can_destroy_auto_list = []
get_json = {}
get_requests_json = {}
can_place_on_json = {"can_place_on":{"blocks":[]}}
can_destroy_json = {"can_destroy":{"blocks":[]}}

#重连次数
requests.adapters.DEFAULT_RETRIES = 5
#获取当前执行exe的路径
pathx_pyinstaller = os.path.dirname(os.path.realpath(sys.argv[0]))
#获取当前path路径
pathx = os.path.dirname(os.path.realpath(sys.argv[0]))
#忽略证书警告
requests.packages.urllib3.disable_warnings()
#请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
}

class Frame(wx_Frame):
    def __init__(self):
        wx_Frame.__init__(self, None, title='Minecraft物品指令NBT编辑器', size=(1725, 923),name='frame',style=541072384)
        self.启动窗口 = wx_Panel(self)
        self.Centre()
        self.标签1 = wx_StaticTextL(self.启动窗口,size=(80, 24),pos=(13, 18),label='搜索物品/方块:',name='staticText',style=0)
        self.find_items_block = wx_TextCtrl(self.启动窗口,size=(1003, 22),pos=(112, 20),value='',name='text',style=0)
        self.find_items_block.Bind(wx.EVT_TEXT,self.find_items_block_内容被改变)
        self.超级列表框1 = wx_ListCtrl(self.启动窗口,size=(1102, 265),pos=(13, 55),name='listCtrl',style=8227)
        self.超级列表框1.AppendColumn('序号', 0,168)
        self.超级列表框1.AppendColumn('类型', 0,159)
        self.超级列表框1.AppendColumn('名称', 0,365)
        self.超级列表框1.AppendColumn('英文id', 0,394)
        self.item_death = wx_CheckBox(self.启动窗口,size=(114, 24),pos=(13, 560),name='check',label='物品死亡不掉落',style=16384)
        self.itemName = wx_TextCtrl(self.启动窗口,size=(562, 22),pos=(78, 332),value='',name='text',style=0)
        self.标签4 = wx_StaticTextL(self.启动窗口,size=(58, 24),pos=(13, 330),label='物品名称:',name='staticText',style=0)
        self.itemName_auto = wx_ComboBox(self.启动窗口,value='',pos=(652, 332),name='comboBox',choices=[],style=16)
        self.itemName_auto.SetSize((461, 22))
        self.itemName_auto.Bind(wx.EVT_COMBOBOX,self.itemName_auto_选中列表项)
        self.itemName_auto.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.itemName_auto_弹出列表项_thread)
        self.标签5 = wx_StaticTextL(self.启动窗口,size=(58, 24),pos=(13, 372),label='物品数量:',name='staticText',style=1)
        self.item_number = wx_SpinCtrl(self.启动窗口,size=(60, 24),pos=(72, 372),name='wxSpinCtrl',min=1,max=32767,initial=1,style=0)
        self.item_number.SetBase(10)
        self.标签6 = wx_StaticTextL(self.启动窗口,size=(58, 24),pos=(148, 372),label='物品id:',name='staticText',style=0)
        self.item_data = wx_SpinCtrl(self.启动窗口,size=(60, 24),pos=(192, 372),name='wxSpinCtrl',min=0,max=32767,initial=0,style=0)
        self.item_data.SetBase(10)
        self.item_lock = wx_CheckBox(self.启动窗口,size=(114, 24),pos=(13, 585),name='check',label='锁定物品',style=16384)
        self.item_lock.Bind(wx.EVT_CHECKBOX,self.item_lock_狀态被改变)
        self.item_lock_mode = wx_RadioBox(self.启动窗口,size=(770, 84),pos=(13, 615),label='锁定模式',choices=['阻止该物品被从玩家的物品栏移除、丢弃或用于合成', '阻止该物品被从玩家物品栏的该槽位移动、移除、丢弃或用于合成'],majorDimension=0,name='radioBox',style=8)
        self.select_can_place_on = wx_CheckBox(self.启动窗口,size=(123, 24),pos=(13, 412),name='check',label='可放置在方块类型:',style=16384)
        self.select_can_place_on.Bind(wx.EVT_CHECKBOX,self.select_can_place_on_狀态被改变)
        self.get_can_place_on = wx_TextCtrl(self.启动窗口,size=(516, 22),pos=(140, 414),value='',name='text',style=0)
        self.add_can_place_on = wx_Button(self.启动窗口,size=(138, 32),pos=(13, 445),label='添加可放置在方块类型',name='button')
        self.add_can_place_on.Bind(wx.EVT_BUTTON,self.add_can_place_on_按钮被单击)
        self.get_can_place_on_auto = wx_ComboBox(self.启动窗口,value='',pos=(663, 414),name='comboBox',choices=[],style=16)
        self.get_can_place_on_auto.SetSize((450, 22))
        self.get_can_place_on_auto.Bind(wx.EVT_COMBOBOX,self.get_can_place_on_auto_选中列表项)
        self.get_can_place_on_auto.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.get_can_place_on_auto_弹出列表项_thread)
        self.select_can_destroy = wx_CheckBox(self.启动窗口,size=(123, 24),pos=(13, 488),name='check',label='可破坏方块类型:',style=16384)
        self.select_can_destroy.Bind(wx.EVT_CHECKBOX,self.select_can_destroy_狀态被改变)
        self.add_destroy = wx_Button(self.启动窗口,size=(138, 32),pos=(13, 519),label='添加可破坏方块类型',name='button')
        self.add_destroy.Bind(wx.EVT_BUTTON,self.add_destroy_按钮被单击)
        self.get_can_destroy = wx_TextCtrl(self.启动窗口,size=(516, 22),pos=(140, 490),value='',name='text',style=0)
        self.get_can_destroy_auto = wx_ComboBox(self.启动窗口,value='',pos=(663, 490),name='comboBox',choices=[],style=16)
        self.get_can_destroy_auto.SetSize((450, 22))
        self.get_can_destroy_auto.Bind(wx.EVT_COMBOBOX,self.get_can_destroy_auto_选中列表项)
        self.get_can_destroy_auto.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.get_can_destroy_auto_弹出列表项_thread)
        self.标签7 = wx_StaticTextL(self.启动窗口,size=(105, 24),pos=(13, 708),label='当前放置方块列表:',name='staticText',style=1)
        self.列表框2 = wx_ListBox(self.启动窗口,size=(971, 51),pos=(133, 708),name='listBox',choices=[],style=32)
        self.标签8 = wx_StaticTextL(self.启动窗口,size=(130, 24),pos=(13, 765),label='当前可破坏方块列表:',name='staticText',style=1)
        self.列表框3 = wx_ListBox(self.启动窗口,size=(971, 51),pos=(133, 765),name='listBox',choices=[],style=32)
        self.标签9 = wx_StaticTextL(self.启动窗口,size=(299, 24),pos=(1130, 18),label='当前生成物品代码(需添加give命令后其他):',name='staticText',style=1)
        self.generate_code = wx_Button(self.启动窗口,size=(80, 32),pos=(1130, 784),label='生成代码',name='button')
        self.generate_code.Bind(wx.EVT_BUTTON,self.generate_code_按钮被单击)
        self.generate_code_text = wx_TextCtrl(self.启动窗口,size=(564, 22),pos=(1130, 55),value='',name='text',style=0)
        self.copy_generate_code = wx_Button(self.启动窗口,size=(119, 32),pos=(1130, 97),label='复制物品代码',name='button')
        self.copy_generate_code.Bind(wx.EVT_BUTTON,self.copy_generate_code_按钮被单击)
        self.flush_api = wx_Button(self.启动窗口,size=(80, 32),pos=(1130, 288),label='刷新api',name='button')
        self.flush_api.Bind(wx.EVT_BUTTON,self.flush_api_按钮被单击)
        self.标签10 = wx_StaticTextL(self.启动窗口,size=(122, 24),pos=(1130, 150),label='导入物品代码:',name='staticText',style=1)
        self.编辑框6 = wx_TextCtrl(self.启动窗口,size=(564, 22),pos=(1130, 184),value='',name='text',style=0)
        self.load_code = wx_Button(self.启动窗口,size=(80, 32),pos=(1130, 222),label='导入',name='button')
        self.load_code.Bind(wx.EVT_BUTTON,self.load_code_按钮被单击)

        self.列表框2.Bind(wx.EVT_RIGHT_DOWN, self.on_right_click)
        self.列表框3.Bind(wx.EVT_RIGHT_DOWN, self.on_right_click_1)
        self.超级列表框1.Bind(wx.EVT_RIGHT_DOWN, self.on_right_click_2)

        self.popup_menu = wx.Menu()
        delete_item = self.popup_menu.Append(-1, '删除')
        self.Bind(wx.EVT_MENU, self.delete_content_can_place_on, delete_item)
        self.popup_menu_1 = wx.Menu()
        delete_item_1 = self.popup_menu_1.Append(-1, '删除')
        self.Bind(wx.EVT_MENU, self.delete_content_can_destroy, delete_item_1)
        self.popup_menu_2 = wx.Menu()
        copy_item = self.popup_menu_2.Append(-1,'复制英文ID')
        copy_item_1 = self.popup_menu_2.Append(-1,'复制中文ID')
        self.Bind(wx.EVT_MENU, self.copy_en, copy_item)
        self.Bind(wx.EVT_MENU, self.copy_zh, copy_item_1)
        self.get_can_place_on.Disable()
        self.get_can_place_on_auto.Disable()
        self.add_can_place_on.Disable()
        self.get_can_destroy_auto.Disable()
        self.get_can_destroy.Disable()
        self.add_destroy.Disable()
        self.flush_list_def()
        self.item_lock_mode.Disable()
    def copy_en(self, event):
        copy(self.超级列表框1.GetItem(self.超级列表框1.GetFirstSelected(),3).GetText())
        self.message_info(f"复制成功,复制内容:{self.超级列表框1.GetItem(self.超级列表框1.GetFirstSelected(),3).GetText()}\n此内容中文ID:{self.超级列表框1.GetItem(self.超级列表框1.GetFirstSelected(),2).GetText()}")
    def copy_zh(self, event):
        copy(self.超级列表框1.GetItem(self.超级列表框1.GetFirstSelected(), 2).GetText())
        self.message_info(f"复制成功,复制内容:{self.超级列表框1.GetItem(self.超级列表框1.GetFirstSelected(), 2).GetText()}\n此内容英文ID:{self.超级列表框1.GetItem(self.超级列表框1.GetFirstSelected(), 3).GetText()}")
    def message_info(self,text:str):
        message = wx.MessageDialog(None, caption="info",message=f"{text}",style=wx.OK | wx.ICON_INFORMATION)
        if message.ShowModal() == wx.ID_OK:
            pass
    def message_error(self,text:str):
        message = wx.MessageDialog(None, caption="error",message=f"{text}",style=wx.OK | wx.ICON_ERROR)
        if message.ShowModal() == wx.ID_OK:
            pass
    def delete_content_can_destroy(self,event):
        try:
            can_destroy_json['can_destroy']['blocks'].remove(can_destroy_json['can_destroy']['blocks'][self.列表框3.GetSelection()])
        except Exception:
            pass
        self.flush_destroy_place_on_ListCtrl()
    def delete_content_can_place_on(self,event):
        try:
            can_place_on_json['can_place_on']['blocks'].remove(can_place_on_json['can_place_on']['blocks'][self.列表框2.GetSelection()])
        except Exception:
            pass
        self.flush_destroy_place_on_ListCtrl()
    def flush_list_def(self):
        global get_requests_json
        self.find_items_block.SetLabel("")
        get_requests_json = json.loads(requests.get(f"https://ca.projectxero.top/idlist/data/beta/vanilla.json",headers=headers,verify=False).text)
        get_sum = 1
        self.超级列表框1.DeleteAllItems()
        """for i, j in get_requests_json['enums']['block'].items():
            self.超级列表框1.Append([f'{str(get_sum)}', '方块', f'{str(j)}', f'{str(i)}'])
            get_sum += 1"""
        for p,c in get_requests_json['enums']['item'].items():
            self.超级列表框1.Append([f'{str(get_sum)}', '物品', f'{str(c)}', f'{str(p)}'])
            get_sum += 1
        get_sum -= 1
        for index in range(self.超级列表框1.GetItemCount()):
            item_data = []
            for column in range(self.超级列表框1.GetColumnCount()):
                item_data.append(self.超级列表框1.GetItem(index, column).GetText())
            get_list_data.append(tuple(item_data))
        """for i, j in get_requests_json['enums']['block'].items():
            self.itemName_auto.AppendItems(f"方块:{str(j)}-{str(i)}")
        for p,c in get_requests_json['enums']['item'].items():
            self.itemName_auto.AppendItems(f"物品:{str(c)}-{str(p)}")"""

    def find_items_block_内容被改变(self,event):
        # 获取输入框中的内容
        keyword = self.find_items_block.GetValue()
        # 如果输入框内容为空，则调用populate_list函数
        if not keyword:
            self.populate_list()
            return

        # 创建一个空列表，用于存放匹配的项
        matched_items = []
        # 遍历get_list_data列表
        for item in get_list_data:
            # 判断输入框中的关键字是否在列表中的值中，如果有，则添加到matched_items列表中
            if any(keyword.lower() in value.lower() for value in item):
                matched_items.append(item)

        # 删除所有项目
        self.超级列表框1.DeleteAllItems()
        # 遍历matched_items列表
        for row, item in enumerate(matched_items):
            # 在列表中插入项目
            self.超级列表框1.InsertItem(row, item[0])
            # 遍历列表中的剩余项
            for col, value in enumerate(item[1:]):
                # 在列表中设置剩余项的值
                self.超级列表框1.SetItem(row, col + 1, value)
    def populate_list(self):
        # 删除所有项目
        self.超级列表框1.DeleteAllItems()
        # 遍历get_list_data列表
        for row, item in enumerate(get_list_data):
            # 在列表中插入项目
            self.超级列表框1.InsertItem(row, item[0])
            # 遍历列表中的剩余项
            for col, value in enumerate(item[1:]):
                # 在列表中设置剩余项的值
                self.超级列表框1.SetItem(row, col+1, value)


    def itemName_auto_弹出列表项(self):
        # 获取输入框中的关键词
        keyword = self.itemName.GetValue()
        # 如果关键词为空，清空匹配的物品列表
        if keyword == "":
            ItemName_matched_items_c.clear()
            ItemName_matched_items_p.clear()
            ItemName_matched_items_content.clear()
            self.itemName_auto.Clear()
            return
        # 清空匹配的物品列表
        self.itemName_auto.Clear()
        ItemName_matched_items_c.clear()
        ItemName_matched_items_p.clear()
        ItemName_matched_items_content.clear()
        # 遍历物品json文件，如果关键词在物品名称或英文名称中，则添加到匹配的物品列表中
        for p, c in get_requests_json['enums']['item'].items():
            if keyword.lower() in c.lower() or keyword.lower() in p.lower():
                ItemName_matched_items_p.append(p)
                ItemName_matched_items_c.append(c)
                ItemName_matched_items_content.append(f"物品:{c}-{p}")
        # 设置匹配的物品列表
        self.itemName_auto.SetItems(ItemName_matched_items_content)
    def itemName_auto_弹出列表项_thread(self,event):
        # 在新线程中执行itemName_auto_弹出列表项函数
        threading.Thread(target=self.itemName_auto_弹出列表项).start()


    def itemName_auto_选中列表项(self,event):
        self.itemName.SetLabel(ItemName_matched_items_p[self.itemName_auto.GetSelection()])

    def get_can_place_on_auto_弹出列表项(self):
        keyword = self.get_can_place_on.GetValue()
        if keyword == "":
            get_can_place_on_matched_items_c.clear()
            get_can_place_on_matched_items_p.clear()
            get_can_place_on_matched_items_content.clear()
            self.get_can_place_on_auto.Clear()
            return
        self.get_can_place_on_auto.Clear()
        get_can_place_on_matched_items_c.clear()
        get_can_place_on_matched_items_p.clear()
        get_can_place_on_matched_items_content.clear()
        for p, c in get_requests_json['enums']['block'].items():
            if keyword.lower() in c.lower() or keyword.lower() in p.lower():
                get_can_place_on_matched_items_p.append(p)
                get_can_place_on_matched_items_c.append(c)
                get_can_place_on_matched_items_content.append(f"方块:{c}-{p}")
        self.get_can_place_on_auto.SetItems(get_can_place_on_matched_items_content)

    def get_can_place_on_auto_选中列表项(self,event):
        self.get_can_place_on.SetLabel(get_can_place_on_matched_items_p[self.get_can_place_on_auto.GetSelection()])
    def get_can_place_on_auto_弹出列表项_thread(self,event):
        threading.Thread(target=self.get_can_place_on_auto_弹出列表项).start()
    def add_can_place_on_按钮被单击(self,event):
        can_place_on_json['can_place_on']['blocks'].append(self.get_can_place_on.GetValue())
        self.flush_destroy_place_on_ListCtrl()

    def add_destroy_按钮被单击(self,event):
        can_destroy_json['can_destroy']['blocks'].append(self.get_can_destroy.GetValue())
        self.flush_destroy_place_on_ListCtrl()


    def get_can_destroy_auto_弹出列表项(self):
        keyword = self.get_can_destroy.GetValue()
        if keyword == "":
            get_can_destroy_matched_items_p.clear()
            get_can_destroy_matched_items_c.clear()
            get_can_destroy_matched_items_content.clear()
            self.get_can_destroy_auto.Clear()
            return
        self.get_can_destroy_auto.Clear()
        get_can_destroy_matched_items_p.clear()
        get_can_destroy_matched_items_c.clear()
        get_can_destroy_matched_items_content.clear()

        for p, c in get_requests_json['enums']['block'].items():
            if keyword.lower() in c.lower() or keyword.lower() in p.lower():
                get_can_destroy_matched_items_p.append(p)
                get_can_destroy_matched_items_c.append(c)
                get_can_destroy_matched_items_content.append(f"方块:{c}-{p}")
        self.get_can_destroy_auto.SetItems(get_can_destroy_matched_items_content)

    def get_can_destroy_auto_弹出列表项_thread(self,event):
        threading.Thread(target=self.get_can_destroy_auto_弹出列表项).start()


    def get_can_destroy_auto_选中列表项(self,event):
        self.get_can_destroy.SetLabel(get_can_destroy_matched_items_p[self.get_can_destroy_auto.GetSelection()])


    def generate_code_按钮被单击(self,event):
        get_json = {}
        if self.itemName.GetValue() == "":
            self.message_error("物品名称不能为空")
            return
        if self.select_can_place_on.GetValue() == True:
            get_json.update(can_place_on_json)
        if self.select_can_destroy.GetValue() == True:
            get_json.update(can_destroy_json)
        if self.item_death.GetValue() == True:
            get_json.update({"keep_on_death":{}})
        if self.item_lock.GetValue() == True:
            if self.item_lock_mode.GetSelection() == 0:
                get_json.update({"item_lock":{"mode":"lock_in_inventory"}})
            elif self.item_lock_mode.GetSelection() == 1:
                get_json.update({"item_lock":{"mode":"lock_in_slot"}})
        if get_json == {}:
            self.generate_code_text.SetLabel(f"{str(self.itemName.GetValue())} {str(self.item_number.GetValue())} {str(self.item_data.GetValue())}")
        else:
            self.generate_code_text.SetLabel(f"{str(self.itemName.GetValue())} {str(self.item_number.GetValue())} {str(self.item_data.GetValue())} {json.dumps(ast.literal_eval(str(get_json)), ensure_ascii=False)}")
        self.message_info("生成完毕")

    def copy_generate_code_按钮被单击(self,event):
        copy(self.generate_code_text.GetValue())
        self.message_info("复制成功")


    def flush_api_按钮被单击(self,event):
        self.flush_list_def()
        self.message_info("刷新完毕")


    def load_code_按钮被单击(self,event):
        # 获取编辑框中的值，并将其分割
        global can_place_on_json
        global can_destroy_json
        get_part = str(self.编辑框6.GetValue()).split(" ")
        try:
            # 设置物品名称
            self.itemName.SetLabel(get_part[0])
            # 设置物品数量
            self.item_number.SetValue(get_part[1])
            # 设置物品数据
            self.item_data.SetValue(get_part[2])
            try:
                # 将分割后的值转换为json格式
                get_json_load = json.loads(' '.join(get_part[3:]))
                # 如果json格式中包含keep_on_death，则设置物品死亡属性
                if "keep_on_death" in get_json_load:
                    self.item_death.SetValue(True)
                # 如果json格式中包含item_lock，则设置物品锁定属性
                if "item_lock" in get_json_load:
                    self.item_lock.SetValue(True)
                    # 如果锁定模式为lock_in_inventory，则设置锁定模式为0
                    if get_json_load['item_lock']['mode'] == "lock_in_inventory":
                        self.item_lock_mode.SetSelection(0)
                    # 如果锁定模式为lock_in_slot，则设置锁定模式为1
                    elif get_json_load['item_lock']['mode'] == "lock_in_slot":
                        self.item_lock_mode.SetSelection(1)
                    # 启用锁定模式下拉框
                    self.item_lock_mode.Enable()
                # 如果json格式中包含can_place_on，则设置可以放置的方块属性
                if "can_place_on" in get_json_load:
                    can_place_on_json['can_place_on']['blocks'] = get_json_load['can_place_on']['blocks']
                    # 设置可以放置的方块属性为True
                    self.select_can_place_on.SetValue(True)
                    # 启用获取可以放置的方块的按钮
                    self.get_can_place_on.Enable()
                    # 启用获取可以放置的方块的自动添加按钮
                    self.get_can_place_on_auto.Enable()
                    # 启用添加可以放置的方块的按钮
                    self.add_can_place_on.Enable()
                # 如果json格式中包含can_destroy，则设置可以破坏的方块属性
                if "can_destroy" in get_json_load:
                    can_destroy_json['can_destroy']['blocks'] = get_json_load['can_destroy']['blocks']
                    # 设置可以破坏的方块属性为True
                    self.select_can_destroy.SetValue(True)
                    # 启用获取可以破坏的方块的自动添加按钮
                    self.get_can_destroy_auto.Enable()
                    # 启用获取可以破坏的方块的按钮
                    self.get_can_destroy.Enable()
                    # 启用添加可以破坏的方块的按钮
                    self.add_destroy.Enable()
                # 刷新可以放置和可以破坏的方块列表
                self.flush_destroy_place_on_ListCtrl()
                # 提示导入完成
                self.message_info("导入完成")
            except Exception:
                # 如果导入失败，则设置可以放置和可以破坏的方块属性为False
                self.select_can_place_on.SetValue(False)
                self.select_can_destroy.SetValue(False)
                self.item_death.SetValue(False)
                self.item_lock.SetValue(False)
                # 提示导入完成
                self.message_info("导入完成")
                return


        except Exception as e:
            pass

    def select_can_destroy_狀态被改变(self,event):
        if self.select_can_destroy.GetValue() == True:
            self.get_can_destroy_auto.Enable()
            self.get_can_destroy.Enable()
            self.add_destroy.Enable()
        else:
            self.get_can_destroy_auto.Disable()
            self.get_can_destroy.Disable()
            self.add_destroy.Disable()

    def select_can_place_on_狀态被改变(self,event):
        if self.select_can_place_on.GetValue() == True:
            self.get_can_place_on.Enable()
            self.get_can_place_on_auto.Enable()
            self.add_can_place_on.Enable()
        else:
            self.get_can_place_on.Disable()
            self.get_can_place_on_auto.Disable()
            self.add_can_place_on.Disable()


    def item_lock_狀态被改变(self,event):
        if self.item_lock.GetValue() == True:
            self.item_lock_mode.Enable()
        else:
            self.item_lock_mode.Disable()

    def flush_destroy_place_on_ListCtrl(self):
        self.列表框2.Clear()
        self.列表框3.Clear()
        for i in can_place_on_json['can_place_on']['blocks']:
            self.列表框2.Append(f"可在此方块上放置:{str(i)}")
        for j in can_destroy_json['can_destroy']['blocks']:
            self.列表框3.Append(f"可以破坏此方块:{str(j)}")

    def on_right_click(self,event):
        pos = wx.GetMousePosition()
        pos = self.ScreenToClient(pos)
        self.PopupMenu(self.popup_menu, pos)
    def on_right_click_1(self,event):
        pos = wx.GetMousePosition()
        pos = self.ScreenToClient(pos)
        self.PopupMenu(self.popup_menu_1, pos)
    def on_right_click_2(self,event):
        pos = wx.GetMousePosition()
        pos = self.ScreenToClient(pos)
        self.PopupMenu(self.popup_menu_2, pos)



class myApp(wx.App):
    def  OnInit(self):
        self.frame = Frame()
        self.frame.Show(True)
        return True

if __name__ == '__main__':
    app = myApp()
    app.MainLoop()