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
        self.InitToolBar()
        self.InitPanel()

        self.SetSize((600, 400))
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
        
    def InitToolBar(self):
        frameSizer = wx.BoxSizer(wx.VERTICAL)
        tools = wx.ToolBar(self)
        tools.AddLabelTool(wx.ID_ANY, 'line', wx.Bitmap('icon.png'))
        tools.AddLabelTool(wx.ID_ANY, 'rectangle', wx.Bitmap('icon.png'))
        tools.AddLabelTool(wx.ID_ANY, 'erase', wx.Bitmap('icon.png'))
        tools.Realize()
        
        colors = wx.ToolBar(self)
        colors.AddLabelTool(wx.ID_ANY, 'COLOR1', wx.Bitmap('icon.png'))
        colors.AddLabelTool(wx.ID_ANY, 'COLOR2', wx.Bitmap('icon.png'))
        colors.AddLabelTool(wx.ID_ANY, 'COLOR3', wx.Bitmap('icon.png'))
        colors.Realize()
        
        frameSizer.Add(tools, 0, wx.EXPAND)
        frameSizer.Add(colors, 0, wx.EXPAND)
        
        self.SetSizer(frameSizer)
        
    def InitPanel(self):
        frameSizer = self.GetSizer()
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('#C0C0C0') #light grey
        self.panel.SetSizer(panelSizer)
        
        frameSizer.Add(self.panel, 1, wx.EXPAND)

    def OnNew(self, e):
        dlg = ScaleSettingDialog(self)
        dlg.ShowModal()
        dlg.Destroy()
        self.column = dlg.GetColumn()
        self.row = dlg.GetRow()
        self.InitDesign()
    def OnQuit(self, e):
        self.Close()
    def OnSave(self, e):
        pass
    def OnLoad(self, e):
        pass
    def OnPrint(self, e):
        pass
        
    def InitDesign(self):
    # button size (25, 25)
        canvasCol = self.column + 1
        canvasRow = self.row + 1
        colPixel = canvasCol * 30
        rowPixel = canvasRow * 30
        self.canvas = wx.Panel(self.panel, size=(rowPixel, colPixel))
        self.canvas.SetBackgroundColour(wx.RED)
        
        canvasSizer = wx.GridBagSizer(5, 5)
        
        spacer = wx.StaticText(self.canvas, size = (25, 25), style=wx.ALIGN_BOTTOM|wx.ALIGN_CENTRE)
        canvasSizer.Add(spacer, pos = (0, 0), span = (1, 1), flag = wx.EXPAND)
        
        for i in range(1, self.column+1):
            text = wx.StaticText(self.canvas, label = str(i), size = (25, 25), style=wx.ALIGN_BOTTOM|wx.ALIGN_CENTRE)
            canvasSizer.Add(text, pos = (0, i), span = (1, 1), flag = wx.EXPAND)
            
        for i in range(1, self.row+1):
            text = wx.StaticText(self.canvas, label = str(i), size = (25, 25), style=wx.ALIGN_BOTTOM|wx.ALIGN_CENTRE)
            canvasSizer.Add(text, pos = (i, 0), span = (1, 1), flag = wx.EXPAND)
            
        for i in range(1, self.row+1):
            for j in range(1, self.column+1):
                btn = wx.Button(self.canvas, size = (25, 25), style=wx.ALIGN_BOTTOM|wx.ALIGN_CENTRE)
                canvasSizer.Add(btn, pos = (i, j), span = (1, 1), flag = wx.EXPAND)

        self.canvas.SetSizerAndFit(canvasSizer)

        self.canvas.Centre()
        self.canvas.Show(True)

def main():
    
    ex = wx.App()
    WeaverFrame(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()