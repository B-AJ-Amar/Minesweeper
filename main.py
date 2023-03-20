from header import *


# TODO :====================================================
# bomb empliment

# Classes :=================================================
class btn(QPushButton):
    def __init__(self,x,y):
        self.value=None
        self.x,self.y=x,y
        super().__init__()
        self.setText("")
        self.setEnabled(True)  # en/desabled
        self.setFixedSize(25,25)
        self.clicked.connect(self.reveal)
        
    
    # def flag:
        
    def SetVal(self,val): 
        print(f"SetVal : ({self.x};{self.y}) = {val}")      
        self.value=val
        
    def GetVal(self):       
        return self.value
        
    def flag(sef): # *flag icon
        pass
      
    def reveal(self): # !recursive
        if window.FirstMove:
            window.FirstMove=0
            window.MakeBombs(self.x,self.y)
            window.SetValues()
            window.revealall()
        
        print(self.value)
        self.setText( str(self.value) )
        self.setEnabled(False)
        if self.value=="*": # *bombe icon
            return "lose"
    
        
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Vars :==================================================================
        self.FirstMove=1
        self.sizeX,self.sizeY=10,10
        self.sizeBomb = 50
        self.items=[[btn(x,y) for x in range(self.sizeX)] for y in range(self.sizeY)]
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
    def SetValues(self):    
        for y in range(self.sizeY):
            for x in range(self.sizeX):
                
                print(f"#setting value of ({y};{x})")
                if( self.items[y][x].GetVal()=="*"):continue
                count=0
                if( (y-1)>=0 and (x-1)>=0 and self.items[y-1][x-1].GetVal()=="*"):
                    count+=1
                    print(f"     donne {y-1},{x-1}")
                
                 
                if( (y-1)>=0 and self.items[y-1][x].GetVal()=="*"):
                    count+=1
                    print(f"     donne {y-1},{x}")
                
                 
                if( (y-1)>=0 and (x+1)<window.sizeX and self.items[y-1][x+1].GetVal()=="*"):
                    count+=1
                    print(f"     donne {y-1},{x+1}")
                
                # =================================================
                 
                if( (y+1)<window.sizeY and (x-1)>=0 and self.items[y+1][x-1].GetVal()=="*"):
                    count+=1
                    print(f"     donne {y+1},{x-1}")
                
                 
                if( (y+1)<window.sizeY and self.items[y+1][x].GetVal()=="*"):
                    count+=1
                    print(f"     donne {y+1},{x}")
                
                 
                if( (y+1)<window.sizeY and (x+1)<window.sizeX and self.items[y+1][x+1].GetVal()=="*"):
                    count+=1
                    print(f"     donne {y+1},{x+1}")
                
                # =================================================
                 
                if( (y+1)<window.sizeY and self.items[y][x-1].GetVal()=="*"):
                    count+=1
                    print(f"     donne {y},{x-1}")
                
                
                 
                if( (x+1)<window.sizeX and self.items[y][x+1].GetVal()=="*"):
                    count+=1
                    print(f"     donne {y}{x+1}")
                
                self.items[y][x].SetVal(count)
                

    def MakeBombs(self,x,y):
        c = self.sizeBomb
        while c:     
            tempx,tempy=randint(0,self.sizeX-1),randint(0,self.sizeY-1)
            if(abs(tempy-y)<=1 and abs(tempx-x)<=1): continue
            if self.items[tempy][tempx].value!="*":
                print(f"bomeb[{c}] ({tempy};{tempx})")
                self.items[tempy][tempx].value = "*"
                c-=1
        
    
    def Reset(self):
        for y in range(self.sizeY):
            for x in range(self.sizeX):
                self.items[x][y]=None
                self.items[x][y].setText(" ")
                self.items[x][y].setEnabled(True)
                window.FirstMove = 1
                # reset time
    
    def revealall(self):
        for y in range(self.sizeY):
            for x in range(self.sizeX):
                self.items[x][y].reveal()         
                  
        
    



# Main :===============================================================

app = QApplication([])

window = MainWindow()

window.show()

app.exec()   
