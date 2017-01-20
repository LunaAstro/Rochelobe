# Drawing the Roche potential distribution of a binary system
#!/usr/bin/env pythonw

import wx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from wx.lib.masked import NumCtrl
from pymouse import PyMouse


class MyWindow(wx.Frame):
    """This program will show Roche Potential of binary system"""
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,500))
        self.CreateStatusBar()
        
        # Create grid and sizers
        grid = wx.GridBagSizer(hgap=5, vgap=10)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Set up the title
        self.title = wx.StaticText(self, label="Roche Potential of Binary System ")
        self.fontt = wx.Font(24, wx.DECORATIVE, wx.ITALIC, wx.BOLD)
        self.title.SetFont(self.fontt)
        grid.Add(self.title, pos=(1,0))
        
        # Setting labels for getting input values
        
        ## input the masses of two stars
        self.label1 = wx.StaticText(self, label="The mass of the first star (M1):")
        self.fontl1 = wx.Font(16, wx.ROMAN, wx.NORMAL, wx.LIGHT)
        self.label1.SetFont(self.fontl1)
        grid.Add(self.label1, pos=(3,0))
        
        self.label2 = wx.StaticText(self, label="The mass of the second star (M2):")
        self.fontl2 = wx.Font(16, wx.ROMAN, wx.NORMAL, wx.LIGHT)
        self.label2.SetFont(self.fontl2)
        grid.Add(self.label2, pos=(4,0))
        
        ## input the distance of two stars
        self.label3 = wx.StaticText(self, label="The distance of two stars (D):")
        self.fontl3 = wx.Font(16, wx.ROMAN, wx.NORMAL, wx.LIGHT)
        self.label3.SetFont(self.fontl3)
        grid.Add(self.label3, pos=(5,0))
        
        ## input the position of the label curve you want
        self.label4 = wx.StaticText(self, label="The x position of a level curve:")
        self.fontl4 = wx.Font(16, wx.ROMAN, wx.NORMAL, wx.LIGHT)
        self.label4.SetFont(self.fontl4)
        grid.Add(self.label4, pos=(8,0))
        
        self.label5 = wx.StaticText(self, label="The y position of a level curve:")
        self.fontl5 = wx.Font(16, wx.ROMAN, wx.NORMAL, wx.LIGHT)
        self.label5.SetFont(self.fontl5)
        grid.Add(self.label5, pos=(9,0))
        
        ## textboxes
        self.mass1 = wx.lib.masked.NumCtrl(self, autoSize=False, fractionWidth=2, value=1.0)
        grid.Add(self.mass1, pos=(3,1))
        self.mass2 = wx.lib.masked.NumCtrl(self, autoSize=False, fractionWidth=2, value=2.0)
        grid.Add(self.mass2, pos=(4,1))
        self.distance = wx.lib.masked.NumCtrl(self, autoSize=False, fractionWidth=2, value=2.0)
        grid.Add(self.distance, pos=(5,1))
        self.xpos = wx.lib.masked.NumCtrl(self, autoSize=False, fractionWidth=2)
        grid.Add(self.xpos, pos=(8,1))
        self.ypos = wx.lib.masked.NumCtrl(self, autoSize=False, fractionWidth=2)
        grid.Add(self.ypos, pos=(9,1))


        self.label6 = wx.StaticText(self, label="How many levels do you want ?")
        self.fontl6 = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL)
        self.label6.SetFont(self.fontl6)
        grid.Add(self.label6, pos=(7,0))
        self.lev = wx.lib.masked.NumCtrl(self, autoSize=False, fractionWidth=2)
        grid.Add(self.lev, pos=(7,1))

        # add a spacer to the sizer
        grid.Add((10, 40), pos=(6,0))
        grid.Add((10, 40), pos=(10,0))
    
        # Create buttons
        ## button 1 for plotting
        self.button1 =wx.Button(self, label="Plot") #, size(100,30))
    
        # Sizer
        hSizer.Add(grid, 0, wx.ALL, 5)
        mainSizer.Add(hSizer, 0, wx.ALL, 5)
        mainSizer.Add(self.button1, 0, wx.CENTER)
        self.SetSizerAndFit(mainSizer)
        
        # Menus
        ## Setting up the menus
        filemenu=wx.Menu()
        helpmenu=wx.Menu()
        
        ## Giving names to the following things
        menuExit= filemenu.Append(wx.ID_EXIT,"&Exit", "Terminate this program")
        filemenu.AppendSeparator()
        menuAbout= helpmenu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        
        ## Creating the menubar
        menuBar=wx.MenuBar()
        menuBar.Append(filemenu,"&File") # adding the "filename" to the...
        menuBar.Append(helpmenu, "&Help") # adding the MenuBar for the Frame content
        self.SetMenuBar(menuBar)
        
        ## Setting events
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_BUTTON, self.OnClickPlot, self.button1)
    
    # set the plot connection
    def OnClickPlot(self, e):
        #get values from input
        m1 = self.mass1.GetValue()
        m2 = self.mass2.GetValue()
        d = self.distance.GetValue()
        #get position values of a particular point on the image
        j = self.xpos.GetValue()
        k = self.ypos.GetValue()
        lev = self.lev.GetValue()
        
        # draw a figure
        ax = plt.subplot(111)
        
        t=(np.arange(1000)/999.-0.5)*20
        X, Y =np.meshgrid(t,t) #create x and y values and change them into matrix
        
        G = 1
        a = d * m2 / (m1 + m2)
        b = d * m1 / (m1 + m2)
        r1 = ( (X + a)**2 + Y**2 + 1e-6 )**0.5  ##"1e-6" is to make sure the r1 won't be 0.
        r2 = ( (X - b)**2 + Y**2 + 1e-6 )**0.5
        z = - G*m1/r1 - G*m2/r2 - (X**2 + Y**2)/2  #potential energy of the a binary system
        
        # calculate the potential at the giving point
        r11 = ( (j + a)**2 + k**2 + 1e-6 )**0.5
        r22 = ( (j - b)**2 + k**2 + 1e-6 )**0.5
        zz = - G*m1/r11 - G*m2/r22 - (j**2 + k**2)/2
        
        # put the potential value of the point into the level curve
        if lev == 0:
            levels=[-10,-8,-6,-5.5,-5.3,-4.8,-4.6,-4.3,-4,-3.8,-3.6,-3.4,-3.2,-3,-2.0,-1.0]
            levels.append(zz)
            levels.sort()  #make the levels in order

        else:
            levels=[-10]
            i = 0
            q = 10/lev
            p=-10
            while i < q:
                p = p + lev
                levels.append(p)
                i = i + 1


        #plot a contour figure of the potential field
        cp = plt.contour(X, Y, z, levels=levels, cmap=cm.coolwarm, origin='lower', linewidths=2)
        plt.colorbar(cp, shrink=0.8, extend='both')  #make a colorbar
        plt.clabel(cp, fontsize=9, inline=1)
        plt.title('Roche potential distribution of a binary system', fontsize=16)
        ax.set_xlabel('X')
        ax.set_xlim(-1.5*d,1.5*d)
        ax.set_ylabel('Y')
        ax.set_ylim(-1.5*d,1.5*d)
        #show the figure
        plt.show()

    def OnAbout(self,e):
        dlg = wx.MessageDialog(self, "Roche potential of binary stars", "About Rochelobe", wx.OK)
        dlg.ShowModal()  # show it
        dlg.Destroy()  # close window when finished

    def OnExit(self,e):
        self.Close(True) # close the frame

app = wx.App(False)
frame = MyWindow(None, 'Rochelobe')
frame.Show()
app.MainLoop()
