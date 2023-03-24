from header import *


# TODO :====================================================
# flag r_click
# loose
# win

# Classes :=================================================
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
                    self.__flag=1
                    window.FlagRest-=1
                    self.setText("")
                    self.setIcon(QIcon('./icons/flags/flag1.png'))
                    self.setIconSize(QtCore.QSize(20, 20))
                else:
                    window.FlagRest+=1
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
        
    def flag(sef): # *flag icon
        pass
    
    def reveal(self): 
        self.setText( str(self.__value) )
        self.setEnabled(False)
        if self.__value=="*": # *bombe icon
            return "lose"
      
   

        
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Vars :==================================================================
        self.FirstMove=1
        self.ingame=1
        self.time=0
        
        self.sizeX,self.sizeY=10,10
        self.sizeBomb = 10
        self.BombRest = self.sizeX*self.sizeX-self.sizeBomb
        self.FlagRest = self.sizeBomb
        
        self.items=[[btn(x,y) for x in range(self.sizeX)] for y in range(self.sizeY)]
        self.__bombs=[]
        
        
        self.setWindowTitle("Minesweeper")
        self.setWindowIcon(QIcon("./icons/bombs/mine1.png"))
        # layouts :================================================================
        # layout 1
        
        # layout 2
        layout2 = QGridLayout()
        layout2.setSpacing(0)
        layout2.setContentsMargins(0,0,0,0)
        
        for x in range(self.sizeX):
            for y in range(self.sizeY):
                layout2.addWidget(self.items[y][x], y+1, x+1)
        
        # layout 3
        MainLayout = QHBoxLayout()
        MainLayout.addLayout(layout2)
        
        widget = QWidget()
        widget.setLayout(MainLayout)
        self.setCentralWidget(widget)
        
    # Functions :==========================================================
    def rec_reveal(self,x=0,y=0,first_call=0):
        print("in rec_rev")
        
        if self.FirstMove:
            print("in rec_rev/firstmove")
            self.FirstMove=0
            self.MakeBombs(x,y)
            self.SetValues()
            print("=================================",x,y)
            # self.revealall()
        print("in rec_rev/end firstmove")
        
        print(x,y)
        if self.items[y][x].GetFlag() :
            print("     rec_flag")
            return 0
        
        if self.items[y][x].GetVal()=="*":
            print("     rec2")
            if first_call: self.lose()
            return 0
        
        if self.items[y][x].text()!=" " :
            print("     rec1")
            return 0
        elif int(self.items[y][x].GetVal())>0:
            print("     rec3")
            # self.rec_reveal(self.x,self.y)
            self.items[y][x].setText( str(self.items[y][x].GetVal()) )
            self.items[y][x].setEnabled(False)
            window.BombRest-=1
            if not window.BombRest: self.win()
            return 0
            
        elif self.items[y][x].GetVal()==0 :
            print("     rec3")
            # self.rec_reveal(self.x,self.y)
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
                
                print(f"#setting value of ({y};{x})= '{self.items[y][x].GetVal()}'")
                if( self.items[y][x].GetVal()=="*"):continue
                print(f"       !!! continue")
                count=0
                if( y>=1 and x>=1 and self.items[y-1][x-1].GetVal()=="*"):
                    count+=1
                    print(f"     donne {y-1},{x-1}")
                
                 
                if( y>=1 and self.items[y-1][x].GetVal()=="*"):
                    count+=1
                    print(f"     donne {y-1},{x}")
                
                 
                if( y>=1 and (x+1)<self.sizeX and self.items[y-1][x+1].GetVal()=="*"):
                    count+=1
                    print(f"     donne {y-1},{x+1}")
                
                # =================================================
                 
                if( (y+1)<self.sizeY and x>=1 and self.items[y+1][x-1].GetVal()=="*"):
                    count+=1
                    print(f"     donne {y+1},{x-1}")
                
                 
                if( (y+1)<self.sizeY and self.items[y+1][x].GetVal()=="*"):
                    count+=1
                    print(f"     donne {y+1},{x}")
                
                 
                if( (y+1)<self.sizeY and (x+1)<self.sizeX and self.items[y+1][x+1].GetVal()=="*"):
                    count+=1
                    print(f"     donne {y+1},{x+1}")
                
                # =================================================
                 
                if( x>=1 and self.items[y][x-1].GetVal()=="*"):
                    count+=1
                    print(f"     donne {y},{x-1}")
                
                
                 
                if( (x+1)<self.sizeX and self.items[y][x+1].GetVal()=="*"):
                    count+=1
                    print(f"     donne {y},{x+1}")
                
                self.items[y][x].SetVal(count)
                

    def MakeBombs(self,x,y):
        c = self.sizeBomb
        while c:     
            tempx,tempy=randint(0,self.sizeX-1),randint(0,self.sizeY-1)
            if(abs(tempy-y)<=1 and abs(tempx-x)<=1): continue
            if self.items[tempy][tempx].GetVal()!="*":
                print(f"bomeb[{c}] ({tempy};{tempx})")
                self.items[tempy][tempx].SetVal("*")
                self.__bombs.append([tempy,tempx])
                c-=1
        
    
    def Reset(self):
        for y in range(self.sizeY):
            for x in range(self.sizeX):
                self.items[x][y]=None
                self.items[x][y].setText(" ")
                self.items[x][y].setEnabled(True)
        
        self.time=0
        self.FirstMove = 1
        self.BombRest = self.sizeX*self.sizeX-self.sizeBomb
        self.FlagRest = self.sizeBomb
                # reset time
    
    def lose(self):
        self.ingame=0
        for x in self.__bombs:
            window.items[x[0]][x[1]].setText("")
            window.items[x[0]][x[1]].setIcon(QIcon('./icons/bombs/mine1.png'))
            window.items[x[0]][x[1]].setIconSize(QtCore.QSize(16, 16))
    
    def win(self):
        self.ingame=0
        for x in self.__bombs:
            window.items[x[0]][x[1]].setText("")
            window.items[x[0]][x[1]].setIcon(QIcon('./icons/flags/flag1.png'))
            window.items[x[0]][x[1]].setIconSize(QtCore.QSize(20, 20))
            
            
        
    def revealall(self):
        for y in range(self.sizeY):
            for x in range(self.sizeX):
                self.items[x][y].text(str(self.items[x][y].SetVal()))        
                  
        
    



# Main :===============================================================

app = QApplication([])

window = MainWindow()

window.show()

app.exec()   
