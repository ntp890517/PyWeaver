#!/usr/bin/python

import wx

class ScaleSettingDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(ScaleSettingDialog, self).__init__(*args, **kwargs)
        self.Init()
        self.SetTitle('New design')
    
    def Init(self):
        gridSizer = wx.GridBagSizer(5, 5)    
        
        self.colText = wx.TextCtrl(self)
        gridSizer.Add(wx.StaticText(self, label='Column: '), pos = (0, 0), span = (1, 1))
        gridSizer.Add(self.colText, pos = (0, 1), span = (1, 1))
        self.rowText = wx.TextCtrl(self)
        gridSizer.Add(wx.StaticText(self, label='Row: '), pos = (1, 0), span = (1, 1))
        gridSizer.Add(self.rowText, pos = (1, 1), span = (1, 1))

        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        gridSizer.Add(okButton, pos = (2, 0), span = (1, 1))
        gridSizer.Add(closeButton, pos = (2, 1), span = (1, 1))
        
        self.SetSizerAndFit(gridSizer)
        
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
    def ValidateColumnAndRow(self):
        if self.column <= 0 or self.row <= 0:
            raise ValueError()  
        
    def GetColumn(self):
        return self.column
    def GetRow(self):
        return self.row


class WeaverFrame(wx.Frame):
    BTN_SIZE = wx.Size(25, 25)
    
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
        toolUndo = tools.AddLabelTool(wx.ID_UNDO, label = 'undo', bitmap = wx.Bitmap('undo.png'))
        toolRedo = tools.AddLabelTool(wx.ID_REDO, label = 'redo', bitmap = wx.Bitmap('redo.png'))
        tools.AddSeparator()
        toolEdit = tools.AddLabelTool(wx.ID_ANY, label = 'edit', bitmap = wx.Bitmap('edit.png'))
        toolRectFill = tools.AddLabelTool(wx.ID_ANY, label = 'rectFill', bitmap = wx.Bitmap('rectFill.png'))
        toolErase = tools.AddLabelTool(wx.ID_ANY, label = 'erase', bitmap = wx.Bitmap('erase.png'))
        tools.Realize()
        
        self.Bind(wx.EVT_TOOL, self.OnUndo, toolUndo)
        self.Bind(wx.EVT_TOOL, self.OnRedo, toolRedo)
        self.Bind(wx.EVT_TOOL, self.OnEdit, toolEdit)
        self.Bind(wx.EVT_TOOL, self.OnRectFill, toolRectFill)
        self.Bind(wx.EVT_TOOL, self.OnErase, toolErase)
        

        colors = wx.ToolBar(self)
        colors.AddLabelTool(wx.ID_ANY, label = 'COLOR1', bitmap = wx.Bitmap('icon.png'))
        colors.AddLabelTool(wx.ID_ANY, label = 'COLOR2', bitmap = wx.Bitmap('icon.png'))
        colors.AddLabelTool(wx.ID_ANY, label = 'COLOR3', bitmap = wx.Bitmap('icon.png'))
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
    def OnUndo(self, e):
        pass
    def OnRedo(self, e):
        pass
    def OnEdit(self, e):
        pass
    def OnRectFill(self, e):
        pass
    def OnErase(self, e):
        pass
        
    def InitDesign(self):
        def InitSpacer():
            spacer = wx.StaticText(self.canvas, size = WeaverFrame.BTN_SIZE, style=wx.ALIGN_BOTTOM|wx.ALIGN_CENTRE)
            canvasSizer = self.canvas.GetSizer()
            canvasSizer.Add(spacer, pos = (0, 0), span = (1, 1), flag = wx.EXPAND)
        def InitColumnIndex():
            canvasSizer = self.canvas.GetSizer()
            for i in range(1, self.column+1):
                text = wx.StaticText(self.canvas, label = str(i), size = WeaverFrame.BTN_SIZE, style=wx.ALIGN_BOTTOM|wx.ALIGN_CENTRE)
                canvasSizer.Add(text, pos = (0, i), span = (1, 1), flag = wx.EXPAND)
        def InitRowIndex():
            canvasSizer = self.canvas.GetSizer()
            for i in range(1, self.row+1):
                text = wx.StaticText(self.canvas, label = str(i), size = WeaverFrame.BTN_SIZE, style=wx.ALIGN_BOTTOM|wx.ALIGN_CENTRE)
                canvasSizer.Add(text, pos = (i, 0), span = (1, 1), flag = wx.EXPAND)
        def InitButtonArray():
            canvasSizer = self.canvas.GetSizer()
            for i in range(1, self.row+1):
                for j in range(1, self.column+1):
                    btn = wx.Button(self.canvas, size = WeaverFrame.BTN_SIZE, style=wx.ALIGN_BOTTOM|wx.ALIGN_CENTRE)
                    canvasSizer.Add(btn, pos = (i, j), span = (1, 1), flag = wx.EXPAND)

        self.canvas = wx.Panel(self.panel)
        self.canvas.SetSizer(wx.GridBagSizer(0, 0))
        self.canvas.SetBackgroundColour(wx.RED)
        
        InitSpacer()
        InitColumnIndex()
        InitRowIndex()
        InitButtonArray()
        
        self.canvas.Fit()
        self.panel.Fit(self.panel.GetSizer()) # Type Error but right layout??

def main():
    
    ex = wx.App()
    WeaverFrame(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()