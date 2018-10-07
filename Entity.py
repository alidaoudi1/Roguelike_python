class Entity : 
    def __init__(self,x,y,char,color):
        self.x=x
        self.y=y
        self.char=char
        self.color=color
    def move(self,dx,dy):
        self.x=self.x+dx
        self.y=self.y+dy