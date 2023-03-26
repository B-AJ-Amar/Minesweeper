from header import *
from test2 import *

# TODO :====================================================
# time 
# leaderboed
# options
# resetbutton
# remove debug lines
# css

# Classes :=================================================
class ResetButton(QPushButton):
    def __init__(self):
        super().__init__()
    
        self.setIcon(QIcon('./icons/characters/TechGeeks.png'))
        
        self.setIconSize(QtCore.QSize(60, 26.2))
        self.clicked.connect( self.Reset)
    
    def Reset(self):
        for y in range(window.sizeY):
            for x in range(window.sizeX):
                window.items[x][y].SetVal(None)
                window.items[x][y].setText(" ")
                window.items[x][y].setEnabled(True)
                window.items[x][y].Flag(0)
        
        window.FirstMove = 1
        window.ingame = 1 
        window.BombRest = window.sizeX*window.sizeX-window.sizeBomb
        window.FlagRest = window.sizeBomb
        window.DispBomb.display(window.FlagRest)
        window.ClearBombs()
        window.DispTime.reset()
        self.setIcon(QIcon('./icons/characters/TechGeeks.png'))
        
    def win(self):
        self.setIcon(QIcon('./icons/win/win5.png'))
        # self.setIconSize(QtCore.QSize(51.2, 45.8))
    def lose(self):
        self.setIcon(QIcon('./icons/characters/TechGeeks_Lose.png'))
        
        
        
        
    
class lcd(QLCDNumber):
    def __init__(self):
        super().__init__()
        
class timer(lcd): 
    def __init__(self):
        super().__init__()
        self.__counter=0
               
    def reset(self):
        self.display(0)
        self.__counter = 0
    def GetScore(self):
        return self.__counter   
    def inc(self):
        while (not window.FirstMove) and window.ingame:
            sleep(1)
            self.__counter+=1
            self.display(self.__counter)
            
    
class btn(QPushButton):
    def __init__(self,x,y):
        super().__init__()
        self.__value=None
        self.__flag=0
        self.x,self.y=x,y
        
        self.setText(" ")
        self.setEnabled(True)  # en/desabled
        self.setFixedSize(25,25)
        
    
    def mousePressEvent(self, event):
        if window.ingame:   
            if event.button() == Qt.MouseButton.LeftButton:
                window.rec_reveal(self.x,self.y,1)

            elif event.button() == Qt.MouseButton.RightButton:
                # self.setText("RIGHT")
                if not self.__flag:
                    window.FlagRest-=1
                    window.DispBomb.display(window.FlagRest)
                    self.Flag(1)
                else:
                    window.FlagRest+=1
                    window.DispBomb.display(window.FlagRest)
                    self.Flag(0)
    
    def Flag(self,b):
        if b:
            self.__flag=1
            self.setText("")
            self.setIcon(QIcon('./icons/flags/flag1.png'))
            self.setIconSize(QtCore.QSize(20, 20))
        else:
            self.__flag=0
            self.setText(" ")
            self.setIcon(QIcon(''))
                              
    def GetFlag(self):
        return self.__flag 
      
    def SetVal(self,val): 
        print(f"SetVal : ({self.x};{self.y}) = {val}")      
        self.__value=val
        
    def GetVal(self):       
        return self.__value
        


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Vars :==================================================================
        self.FirstMove=1
        self.ingame=1
        
        self.sizeX,self.sizeY=10,10
        self.sizeBomb = 10
        self.BombRest = self.sizeX*self.sizeX-self.sizeBomb
        self.FlagRest = self.sizeBomb
        
        
        self.items=[[btn(x,y) for x in range(self.sizeX)] for y in range(self.sizeY)]
        self.__bombs=[]
        
        
        self.setFixedSize(QSize())
        self.setWindowTitle("Minesweeper")
        self.setWindowIcon(QIcon("./icons/bombs/mine1.png"))
        self.setObjectName("Main")
        with open("./style.css","r") as fh:
            self.setStyleSheet(fh.read())
        # layouts :================================================================
        # layout 1
        self.DispTime = timer()
        self.MButton= ResetButton()
        
        
        self.DispBomb = lcd()
        self.DispBomb.display(str(self.FlagRest))
        
        self.spacer1 = QSpacerItem(20, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.spacer2 = QSpacerItem(20, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
        layout1 = QGridLayout()
        layout1.addWidget(self.DispTime,0,0)
        layout1.addWidget(self.MButton,0,2)
        layout1.addWidget(self.DispBomb,0,4)
        
        layout1.addItem(self.spacer1,0,1)
        layout1.addItem(self.spacer2,0,3)
        
        # layout 2
        layout2 = QGridLayout()
        layout2.setSpacing(0)
        layout2.setContentsMargins(0,0,0,0)
        
        for x in range(self.sizeX):
            for y in range(self.sizeY):
                layout2.addWidget(self.items[y][x], y+1, x+1)
        
        # layout 3
        MainLayout = QVBoxLayout()
        MainLayout.addLayout(layout1)
        MainLayout.addLayout(layout2)
        
        widget = QWidget()
        widget.setLayout(MainLayout)
        self.setCentralWidget(widget)
        
    # Functions :==========================================================
    def rec_reveal(self,x=0,y=0,first_call=0):
  
        if self.FirstMove:
            self.FirstMove=0
            self.MakeBombs(x,y)
            self.SetValues()
            ThTime = threading.Thread(target=self.DispTime.inc).start()
      
        if self.items[y][x].GetFlag() :
            return 
        
        if self.items[y][x].GetVal()=="*":
            if first_call: self.lose()
            return 
        
        if self.items[y][x].text()!=" " :
            return 
        
        elif int(self.items[y][x].GetVal())>0:
            self.items[y][x].setText( str(self.items[y][x].GetVal()) )
            self.items[y][x].setEnabled(False)
            window.BombRest-=1
            if not window.BombRest: self.win()
            return 
            
        elif self.items[y][x].GetVal()==0 :
            self.items[y][x].setText( "  " )
            self.items[y][x].setEnabled(False)
            window.BombRest-=1
            if not window.BombRest: self.win()
            
            if (x+1<self.sizeX): self.rec_reveal(x+1,y)
            if (x-1>=0): self.rec_reveal(x-1,y)
            if (y+1<self.sizeY): self.rec_reveal(x,y+1)
            if (y-1>=0): self.rec_reveal(x,y-1)

            if (x-1>=0 and y-1>=0): self.rec_reveal(x-1,y-1)
            if (x+1<self.sizeX and y+1<self.sizeY): self.rec_reveal(x+1,y+1)
            if (x-1>=0 and y+1<self.sizeY): self.rec_reveal(x-1,y+1)
            if (x+1<self.sizeX and y-1>=0): self.rec_reveal(x+1,y-1)
       
        
    def SetValues(self):    
        for y in range(self.sizeY):
            for x in range(self.sizeX):
                
                if( self.items[y][x].GetVal()=="*"):continue
                count=0
                
                if( y>=1 and x>=1 and self.items[y-1][x-1].GetVal()=="*"): count+=1
                
                if( y>=1 and self.items[y-1][x].GetVal()=="*"): count+=1
                
                if( y>=1 and (x+1)<self.sizeX and self.items[y-1][x+1].GetVal()=="*"): count+=1
                
                # =================================================
                 
                if( (y+1)<self.sizeY and x>=1 and self.items[y+1][x-1].GetVal()=="*"): count+=1
                
                if( (y+1)<self.sizeY and self.items[y+1][x].GetVal()=="*"): count+=1
                
                if( (y+1)<self.sizeY and (x+1)<self.sizeX and self.items[y+1][x+1].GetVal()=="*"): count+=1
                
                # =================================================
                 
                if( x>=1 and self.items[y][x-1].GetVal()=="*"): count+=1
                                 
                if( (x+1)<self.sizeX and self.items[y][x+1].GetVal()=="*"): count+=1
                
                self.items[y][x].SetVal(count)
                
                
    def MakeBombs(self,x,y):
        c = self.sizeBomb
        while c:     
            tempx,tempy=randint(0,self.sizeX-1),randint(0,self.sizeY-1)
            if(abs(tempy-y)<=1 and abs(tempx-x)<=1): continue
            if self.items[tempy][tempx].GetVal()!="*":
                # print(f"bomeb[{c}] ({tempy};{tempx})")
                self.items[tempy][tempx].SetVal("*")
                self.__bombs.append([tempy,tempx])
                c-=1
    def ClearBombs(self):
        window.__bombs.clear()
           
    

    
    def lose(self):
        self.ingame=0
        for x in self.__bombs:
            window.items[x[0]][x[1]].setText("")
            window.items[x[0]][x[1]].setIcon(QIcon('./icons/bombs/mine1.png'))
            window.items[x[0]][x[1]].setIconSize(QtCore.QSize(16, 16))
        self.MButton.lose()
    
    def win(self):
        self.ingame=0
        for x in self.__bombs:
            self.DispBomb.display(0)
            window.items[x[0]][x[1]].setText("")
            window.items[x[0]][x[1]].setIcon(QIcon('./icons/flags/flag1.png'))
            window.items[x[0]][x[1]].setIconSize(QtCore.QSize(20, 20))
            self.MButton.win()
# Main :===============================================================

app = QApplication([])
window = MainWindow()
window.show()
app.exec()   
