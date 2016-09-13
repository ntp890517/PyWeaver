#!/usr/bin/python

import wx

class ScaleSettingDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(ScaleSettingDialog, self).__init__(*args, **kwargs)
        self.Init()
        self.SetSize((300, 200))
        self.SetTitle('New design')
    
    def Init(self):
        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        sb = wx.StaticBox(pnl, label='Scale')
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)        
        
        self.colText = wx.TextCtrl(pnl)
        colBox = wx.BoxSizer(wx.HORIZONTAL)
        colBox.Add(wx.StaticText(pnl, label='Column: '))
        colBox.Add(self.colText, flag=wx.LEFT, border=5)
        self.rowText = wx.TextCtrl(pnl)
        rowBox = wx.BoxSizer(wx.HORIZONTAL)
        rowBox.Add(wx.StaticText(pnl, label='Row: '))
        rowBox.Add(self.rowText, flag=wx.LEFT, border=5)
        sbs.Add(colBox)
        sbs.Add(rowBox)
        
        pnl.SetSizer(sbs)
       
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox3.Add(okButton)
        hbox3.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1, 
            flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox3, 
            flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)
        
        okButton.Bind(wx.EVT_BUTTON, self.OnClose)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
        
    def OnClose(self, e):
        try:
            self.column = int(self.colText.GetValue())
            self.row = int(self.rowText.GetValue())
            self.ValidateColumnAndRow()
            self.Destroy()
        except ValueError:
            dlg = wx.MessageDialog(self, 'Scale should be a positive integer', 'illegal scale', wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()
        
    def GetColumn(self):
        return self.column
    def GetRow(self):
        return self.row
        
    def ValidateColumnAndRow(self):
        if self.column <= 0 or self.row <= 0:
            raise ValueError()     

class WeaverFrame(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(WeaverFrame, self).__init__(*args, **kwargs) 
        self.column = 0
        self.row = 0
        self.Init()
        
    def Init(self):
        self.InitMenuBar()

        self.SetSize((300, 200))
        self.SetTitle('Weaver(Alpha)')
        self.Centre()
        self.Show(True)

    def InitMenuBar(self):
        menubar = wx.MenuBar()
        menubar.Append(self.InitFileMenu(), '&File')
        self.SetMenuBar(menubar)

    def InitFileMenu(self):
        fileMenu = wx.Menu()
        fitem = fileMenu.Append(wx.ID_NEW, 'New', 'New file')
        self.Bind(wx.EVT_MENU, self.OnNew, fitem)
        fitem = fileMenu.Append(wx.ID_SAVE, 'Save', 'Save file')
        self.Bind(wx.EVT_MENU, self.OnSave, fitem)
        fitem = fileMenu.Append(wx.ID_OPEN, 'Load', 'Load file')
        self.Bind(wx.EVT_MENU, self.OnLoad, fitem)
        fitem = fileMenu.Append(wx.ID_PRINT, 'Print', 'Print design')
        self.Bind(wx.EVT_MENU, self.OnPrint, fitem)
        fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)
        return fileMenu

    def OnNew(self, e):
        dlg = ScaleSettingDialog(self)
        dlg.ShowModal()
        dlg.Destroy()
        self.column = dlg.GetColumn()
        self.row = dlg.GetRow()
        print 'Scale: ' + str(self.column) + ', ' + str(self.row)
    def OnQuit(self, e):
        self.Close()
    def OnSave(self, e):
        pass
    def OnLoad(self, e):
        pass
    def OnPrint(self, e):
        pass

def main():
    
    ex = wx.App()
    WeaverFrame(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()