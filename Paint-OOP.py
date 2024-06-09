from tkinter import*;
from tkinter import colorchooser;
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image 
import math
import pyautogui as py
import PIL.ImageGrab as ImageGrab;
import cv2
import numpy as np
class Paintapp:
    def __init__(self,width,height,title):
        self.root=Tk();            
        self.root.title("AbdulRahim's Paint");
        self.root.geometry("1100x600");
        self.root.resizable(False,False);
        

        #Variables
        self.stroke_size=IntVar();
        self.stroke_size.set(1);
        self.stroke_color=StringVar();
        self.stroke_color.set("black");
        self.selected_slice=None
        self.selected_image=None
        self.prevPoint=[0,0];
        self.newPoint=[0,0];
        self.shape=None
        self.npolygon=IntVar()

        #Frames
        self.frame1=Frame(self.root,height=150,width=1100); 
        self.frame1.grid(row=0,column=0,sticky=NW);
        self.frame2=Frame(self.root,height=450,width=1100,bg="grey"); 
        self.frame2.grid(row=100,column=0); 
        self.toolsFrame=Frame(self.frame1,height=100,width=100,relief=SUNKEN,borderwidth=3);
        self.toolsFrame.grid(row=0,column=0);
        self.sizeFrame=Frame(self.frame1,height=100,width=100,relief=SUNKEN,borderwidth=3);
        self.sizeFrame.grid(row=0,column=1);
        self.colorBoxFrame=Frame(self.frame1,height=100,width=100,relief=SUNKEN,borderwidth=3);
        self.colorBoxFrame.grid(row=0,column=2);
        self.colorsFrame=Frame(self.frame1,height=100,width=100,relief=SUNKEN,borderwidth=3);
        self.colorsFrame.grid(row=0,column=3);
        self.shapesFrame=Frame(self.frame1,height=100,width=100,relief=SUNKEN,borderwidth=3);
        self.shapesFrame.grid(row=0,column=4);
        self.npolygonFrame=Frame(self.frame1,height=100,width=100,relief=SUNKEN,borderwidth=3);
        self.npolygonFrame.grid(row=0,column=5);
        self.othersFrame=Frame(self.frame1,height=100,width=100,relief=SUNKEN,borderwidth=3);
        self.othersFrame.grid(row=0,column=6);
        self.SaveFrame=Frame(self.frame1,height=100,width=100,relief=SUNKEN,borderwidth=3);
        self.SaveFrame.grid(row=0,column=7);
        #inside sizeframe
        self.resetsizeButton=Button(self.sizeFrame,text="reset",width=10,command=lambda:self.reset());
        self.resetsizeButton.grid(row=0,column=0);
        self.sizeoptions=[1,2,3,4,5,6,7,8,9,10];
        self.sizelist=OptionMenu(self.sizeFrame,self.stroke_size,*self.sizeoptions);
        self.sizelist.grid(row=1,column=0);
        self.sizeLabel=Label(self.sizeFrame,text="Size",width=10);
        self.sizeLabel.grid(row=2,column=0);


        #creating canvas
        self.canvas=Canvas(self.frame2,height=450,width=1100,bg="white");
        self.canvas.grid(row=0,column=0);
        self.canvas.pack()

        #Binding with Pencil
        self.canvas.bind("<B1-Motion>",self.pencil);
        self.canvas.bind("<B3-Motion>",self.dottedline);
        self.canvas.bind("<Button-1>",self.pencil);


        #Buttons
        self.pencilButton=Button(self.toolsFrame,text="Pencil",width=10,command=lambda:self.usePencil());
        self.pencilButton.grid(row=0,column=0);
        self.EraserButton=Button(self.toolsFrame,text="Eraser",width=10,command=lambda:self.useEraser());
        self.EraserButton.grid(row=1,column=0);
        self.ToolsButton=Button(self.toolsFrame,text="Tools",width=10);
        self.ToolsButton.grid(row=2,column=0); 
        self.colorBoxButton=Button(self.colorBoxFrame,text="Select Color",width=10,command=lambda:self.selectColor());
        self.colorBoxButton.grid(row=0,column=0);
        self.EyedroppingcolorButton=Button(self.colorBoxFrame,width=10);
        self.EyedroppingcolorButton.grid(row=1,column=0);
        #Eyedropping color label
        self.EyedroppingcolorLabel=Label(self.colorBoxFrame,text="Eyedropping Color",width=16);
        self.EyedroppingcolorLabel.grid(row=2,column=0);
        #
        self.Savebutton=Button(self.SaveFrame,text="Save",bg="Lime",width=10,command=lambda:self.Save());
        self.Savebutton.grid(row=0,column=0);
        self.clearbutton=Button(self.SaveFrame,text="Clear",bg="tomato",width=10,command=lambda:self.clear());
        self.clearbutton.grid(row=1,column=0);
        self.newcanvasbutton=Button(self.SaveFrame,text="New",bg="dark turquoise",width=10,command=lambda:self.newcanvas());
        self.newcanvasbutton.grid(row=2,column=0);
        self.openbutton=Button(self.SaveFrame,text="Open",bg="mediumseagreen",width=10,command=lambda:self.Open());
        self.openbutton.grid(row=3,column=0);
        self.colorpickerbutton=Button(self.othersFrame,text="Pick Color",width=10,command=lambda:self.pickcolorbuttonpressed());
        self.colorpickerbutton.grid(row=0,column=0);
        self.magnifierbutton=Button(self.othersFrame,text="Magnifier",width=10,command=lambda:self.Magnifierbuttonpressed());
        self.magnifierbutton.grid(row=1,column=0);
        self.selectareabutton=Button(self.othersFrame,text="Select Area",width=10,command=lambda:self.SelectAreabuttonpressed());
        self.selectareabutton.grid(row=2,column=0);
        self.fillcolorbutton=Button(self.othersFrame,text="Fillcolor",width=10,command=lambda:self.FillColorbuttonpressed());
        self.fillcolorbutton.grid(row=3,column=0);




        #colorsButton
        self.redbutton=Button(self.colorsFrame,width=5,bg="red",command=lambda: self.stroke_color.set("red"));
        self.redbutton.grid(row=0,column=0);
        self.bluebutton=Button(self.colorsFrame,bg="blue",width=5,command=lambda: self.stroke_color.set("blue"));
        self.bluebutton.grid(row=1,column=0);
        self.greenbutton=Button(self.colorsFrame,bg="green",width=5,command=lambda: self.stroke_color.set("green"));
        self.greenbutton.grid(row=2,column=0);
        self.yellowbutton=Button(self.colorsFrame,bg="yellow",width=5,command=lambda: self.stroke_color.set("yellow"));
        self.yellowbutton.grid(row=0,column=1);
        self.pinkbutton=Button(self.colorsFrame,bg="pink",width=5,command=lambda: self.stroke_color.set("pink"));
        self.pinkbutton.grid(row=1,column=1);
        self.brownbutton=Button(self.colorsFrame,bg="brown",width=5,command=lambda: self.stroke_color.set("brown"));
        self.brownbutton.grid(row=2,column=1);
        self.purplebutton=Button(self.colorsFrame,bg="purple",width=5,command=lambda: self.stroke_color.set("purple"));
        self.purplebutton.grid(row=0,column=2);
        self.orangebutton=Button(self.colorsFrame,bg="orange",width=5,command=lambda: self.stroke_color.set("orange"));
        self.orangebutton.grid(row=1,column=2);
        self.maroonbutton=Button(self.colorsFrame,bg="maroon",width=5,command=lambda: self.stroke_color.set("maroon"));
        self.maroonbutton.grid(row=2,column=2);
        self.violetbutton=Button(self.colorsFrame,bg="violet",width=5,command=lambda: self.stroke_color.set("violet"));
        self.violetbutton.grid(row=0,column=3);
        self.whitebutton=Button(self.colorsFrame,bg="white",width=5,command=lambda: self.stroke_color.set("white"));
        self.whitebutton.grid(row=1,column=3);
        self.Lightgreenbutton=Button(self.colorsFrame,bg="Lightgreen",width=5,command=lambda: self.stroke_color.set("Lightgreen"));
        self.Lightgreenbutton.grid(row=2,column=3);
        self.circleshapebutton=Button(self.shapesFrame,text="Circle",width=8,command=lambda:self.circlebuttonpressed());
        self.circleshapebutton.grid(row=0,column=0);
        self.squareshapebutton=Button(self.shapesFrame,text="Square",width=8,command=lambda:self.Squarebuttonpressed());
        self.squareshapebutton.grid(row=1,column=0);
        self.rectangleshapebutton=Button(self.shapesFrame,text="Rectangle",width=8,command=lambda:self.Rectanglebuttonpressed());
        self.rectangleshapebutton.grid(row=2,column=0);
        self.lineshapebutton=Button(self.shapesFrame,text="Line",width=8,command=lambda:self.Linebuttonpressed());
        self.lineshapebutton.grid(row=0,column=1);
        self.triangleshapebutton=Button(self.shapesFrame,text="Triangle",width=8,command=lambda:self.Trianglebuttonpressed());
        self.triangleshapebutton.grid(row=1,column=1);
        self.ovalshapebutton=Button(self.shapesFrame,text="Oval",width=8,command=lambda:self.Ovalbuttonpressed());
        self.ovalshapebutton.grid(row=2,column=1);
        self.starshapebutton=Button(self.shapesFrame,text="Star",width=8,command=lambda:self.Starbuttonpressed());
        self.starshapebutton.grid(row=0,column=2);
        self.hexagonshapebutton=Button(self.shapesFrame,text="Hexagon",width=8,command=lambda:self.Hexagonbuttonpressed());
        self.hexagonshapebutton.grid(row=1,column=2);
        self.Pentagonshapebutton=Button(self.shapesFrame,text="Pentagon",width=8,command=lambda:self.Pentagonbuttonpressed());
        self.Pentagonshapebutton.grid(row=2,column=2);
        self.npolygonbutton=Button(self.npolygonFrame,text="N-Polygon",width=10,height=3,command=lambda:self.NPolygonpressed());
        self.npolygonbutton.grid(row=0,column=0);
        self.sizeoptions=[3,4,5,6,7,8,9,10];
        self.sizelist=OptionMenu(self.npolygonFrame,self.npolygon,*self.sizeoptions);
        self.sizelist.grid(row=1,column=0);

        #self.scale = Scale(self.root,from_=3,to=10, orient=HORIZONTAL)
        #self.scale.pack()
    

    def run(self):
        self.root.mainloop()
    def usePencil(self):
        self.canvas.bind("<B1-Motion>",self.pencil);
        self.canvas.bind("<B3-Motion>",self.dottedline);
        self.canvas.bind("<Button-1>",self.pencil);
        self.canvas["cursor"]="arrow";
    def pencil(self,event):
        if(event.type=="4"):
         self.prevPoint=[0,0];
        x=event.x
        y=event.y;
        self.newPoint=[x,y];
        if(self.prevPoint!=[0,0]):
            self.canvas.create_polygon(self.prevPoint[0],self.prevPoint[1],self.newPoint[0],self.newPoint[1],fill=self.stroke_color.get(),outline=self.stroke_color.get(),width=self.stroke_size.get());
        self.prevPoint=[x,y];
    def NPolygonpressed(self):
        self.prevPoint=[0,0]
        self.newPoint=[0,0]
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        if(self.npolygon.get()==3):
            self.canvas.bind("<B1-Motion>",self.DrawTriangle)
        elif(self.npolygon.get()==4):
            self.canvas.bind("<B1-Motion>",self.DrawSquare)
        elif(self.npolygon.get()==5):
            self.canvas.bind("<B1-Motion>",self.DrawPentagon)
        elif(self.npolygon.get()==6):
            self.canvas.bind("<B1-Motion>",self.DrawHexagon)
        elif(self.npolygon.get()==7):
            self.canvas.bind("<Button-1>", self.startdrawingHeptagon)
            self.canvas.bind("<B1-Motion>", self.drawHeptagon)
        elif(self.npolygon.get()==8):
            self.canvas.bind("<Button-1>", self.startdrawingHeptagon)
            self.canvas.bind("<B1-Motion>", self.drawOctagon)
        elif(self.npolygon.get()==9):
            self.canvas.bind("<Button-1>", self.startdrawingNanogon)
            self.canvas.bind("<B1-Motion>", self.drawNanogon)
        elif(self.npolygon.get()==10):
            self.canvas.bind("<Button-1>", self.startdrawingDecagon)
            self.canvas.bind("<B1-Motion>", self.drawDecagon)

        self.canvas.bind("<ButtonRelease-1>",self.DrawShape_end)


    def FillColorbuttonpressed(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<Button-1>",self.FillColor)
    def FillColor(self,event):
        x, y = event.x, event.y
        color = self.stroke_color.get() 
        
        current_color = self.canvas.itemcget(self.canvas.find_closest(x, y), "fill") #pixel color
        
        # Check if the clicked position has a different color than the fill color
        if current_color != color:
            self._flood_fill(x, y, current_color, color)
        self.canvas.unbind("<Button-1>")
    
    def _flood_fill(self, x, y, old_color, new_color):
        if self.isvalidpixel(x, y) and self.canvas.itemcget(self.canvas.find_closest(x, y), "fill")== old_color:
            self.canvas.itemconfig(self.canvas.find_closest(x, y), fill=new_color, outline=new_color, tags=new_color)
            self._flood_fill(x + 1, y, old_color, new_color)  # Fill right pixel
            self._flood_fill(x - 1, y, old_color, new_color)  # Fill left pixel
            self._flood_fill(x, y + 1, old_color, new_color)  # Fill bottom pixel
            self._flood_fill(x, y - 1, old_color, new_color)  # Fill top pixel
    
    def isvalidpixel(self, x, y):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        return 0 <= x < canvas_width and 0 <= y < canvas_height
    def SelectAreabuttonpressed(self):
        self.prevPoint=[0,0]
        self.newPoint=[0,0]
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind('<Button-1>', self.start_selection)
        self.canvas.bind('<B1-Motion>', self.update_selection)
        self.canvas.bind('<ButtonRelease-1>', self.move_slice1)
        
    def start_selection(self, event):
        self.prevPoint[0] = event.x
        self.prevPoint[1] = event.y
        self.selected_slice = self.canvas.create_rectangle(event.x, event.y, event.x, event.y,dash=(3,4),outline="red")
    def update_selection(self, event):
        self.canvas.coords(self.selected_slice, self.prevPoint[0],self.prevPoint[1], event.x, event.y)
    def move_slice1(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.selected_slice)
        x=self.root.winfo_x();
        y=self.root.winfo_y();
        self.selected_image = ImageGrab.grab(bbox=(x+x1+10,y+y1+185,x2+x,y+y2+180))
        self.selected_image.save("image.jpg") 
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')

        self.canvas.bind('<Button-1>', self.select_slice)
        self.canvas.bind('<B1-Motion>', self.move_slice2)
        self.canvas.bind('<ButtonRelease-1>', self.release_slice)

    def select_slice(self, event):
        self.prevPoint[0] = event.x
        self.prevPoint[1] = event.y
        
    def move_slice2(self, event):
        if self.selected_slice:
            self.newPoint[0] = event.x - self.prevPoint[0]
            self.newPoint[1] = event.y - self.prevPoint[1]
            self.canvas.move(self.selected_slice, self.newPoint[0], self.newPoint[1])
            self.prevPoint[0] = event.x
            self.prevPoint[1] = event.y
        
    def release_slice(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.selected_slice)
        x1 += 1  # Adjusting coordinates to capture content inside rectangle
        y1 += 1
        self.selected_image = ImageTk.PhotoImage(file='C:\\Users\\syeda\\Desktop\\image.jpg') # Create PhotoImage object from the saved image
        self.canvas.create_image(x1,y1, image=self.selected_image, anchor="nw")  # Display the saved image on the canvas
        self.canvas.pack()
    def Magnifierbuttonpressed(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<Button-3>")

        self.canvas.bind("<Button-1>",self.Magnify)
        self.canvas.bind("<Button-3>",self.UnMagnify)
    def Magnify(self,event):
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
    def UnMagnify(self,event):
        self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
    def pickcolorbuttonpressed(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")

        self.canvas.bind("<Button-1>",self.pickcolor);
        #self.canvas.bind("<ButtonRelease-1>",self.pickcolor_end())
    def pickcolor(self,event): 
        pos=py.position()
        s=py.screenshot(region=(pos[0]-1,pos[1]-1,1,1))
        a=np.array(s)
        c=tuple(a[0,0])
        c_rgb = c
        d = '#{:02x}{:02x}{:02x}'.format(c_rgb[0], c_rgb[1], c_rgb[2])
        self.stroke_color.set(d)
        self.EyedroppingcolorButton["bg"]=self.stroke_color.get()
        self.EyedroppingcolorButton["command"]=lambda:self.stroke_color.set(d)
        self.usePencil()
        self.pencil(event)
        print(d)
    def pickcolor_end(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<Button-1>",self.pencil)
        self.canvas.bind("<B1-Motion>",self.pencil)
    def reset(self):
        self.stroke_color.set("black");
        self.stroke_size.set(1);
    def useEraser(self):
        self.canvas.bind("<B1-Motion>",self.pencil);
        self.canvas.bind("<B3-Motion>",self.dottedline);
        self.canvas.bind("<Button-1>",self.pencil);
        self.stroke_color.set("white");
        self.canvas["cursor"]=DOTBOX;
    def selectColor(self):
        selectedcolor=colorchooser.askcolor("blue",title="Select Color:");
        if(selectedcolor[1]==None):
            self.stroke_color.set("black");
        else:
            self.stroke_color.set(selectedcolor[1]);
    def Save(self):
        filelocation=filedialog.asksaveasfilename(defaultextension="jpg");
        x=self.root.winfo_x();
        y=self.root.winfo_y();
        img=ImageGrab.grab(bbox=(x+30,y+185,x+1350,y+730))
        if(filelocation):
            showimage=messagebox.askyesno("AbdulRahim's Paint","Do you want to open the image?");
            if(showimage==True):
                img.show();
        img.save(filelocation);
    def Open(self):
        self.filename=filedialog.askopenfilename()
        picture=Image.open(self.filename)
        self.img = ImageTk.PhotoImage(picture)


        self.canvas.create_image(0, 0, anchor=NW, image=self.img)
        self.canvas.pack()
    def clear(self):
        if(messagebox.askyesnocancel("AbdulRahim's Paint","Do you want to clear everything?")):
            self.canvas.delete('all');
    def newcanvas(self):
        if(messagebox.askyesnocancel("AbdulRahim's Paint","Do you want to save before you clear everything?")):
            self.Save()

        self.clear();
    def dottedline(self,event):
        x=event.x;
        y=event.y;
        self.canvas.create_oval(x,y,x+self.stroke_size.get(),y+self.stroke_size.get(),fill=self.stroke_color.get(),outline=self.stroke_color.get(),width=self.stroke_size.get());
    def DrawShape_end(self,event):
        self.prevPoint=[0,0]
        self.newPoint=[0,0]
        self.shape=None
    def circlebuttonpressed(self):
        self.prevPoint=[0,0]
        self.newPoint=[0,0]
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>",self.DrawCircle)
        self.canvas.bind("<ButtonRelease-1>",self.DrawShape_end)
    def DrawCircle(self,event):
        self.canvas.delete(self.shape)
        x=event.x
        y=event.y
        self.newPoint=[x,y]
        if(self.prevPoint==[0,0]):
            prevPoint=[x,y]
        radius=abs(self.prevPoint[0]-self.newPoint[0])+abs(self.prevPoint[1]-self.newPoint[1])
        x1,y1=(self.prevPoint[0]),(self.prevPoint[1])
        x2,y2=(self.prevPoint[0]+radius),(self.prevPoint[1]+radius )
        self.shape=self.canvas.create_oval(x1,y1,x2,y2,width=self.stroke_size.get(),outline=self.stroke_color.get());
    def Squarebuttonpressed(self):
        self.prevPoint=[0,0]
        self.newPoint=[0,0]
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>",self.DrawSquare)
        self.canvas.bind("<ButtonRelease-1>",self.DrawShape_end)
    def DrawSquare(self,event):
        self.canvas.delete(self.shape)
        x=event.x
        y=event.y
        self.newPoint=[x,y]
        if(self.prevPoint==[0,0]):
            self.prevPoint=[x,y]
        radius=abs(self.prevPoint[0]-self.newPoint[0])+abs(self.prevPoint[1]-self.newPoint[1])
        x1,y1=(self.prevPoint[0]),(self.prevPoint[1])
        x2,y2=(self.prevPoint[0]+radius),(self.prevPoint[1]+radius )
        self.shape=self.canvas.create_rectangle(x1,y1,x2,y2,width=self.stroke_size.get(),outline=self.stroke_color.get());
    def Rectanglebuttonpressed(self):
        self.prevPoint=[0,0]
        self.newPoint=[0,0]
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>",self.DrawRectangle)
        self.canvas.bind("<ButtonRelease-1>",self.DrawShape_end)
    def DrawRectangle(self,event):
        self.canvas.delete(self.shape)
        x=event.x
        y=event.y
        self.newPoint=[x,y]
        if(self.prevPoint==[0,0]):
            self.prevPoint=[x,y]
        radius=abs(self.prevPoint[0]-self.newPoint[0])+abs(self.prevPoint[1]-self.newPoint[1])
        x1,y1=(self.prevPoint[0]),(self.prevPoint[1])
        x2,y2=(self.prevPoint[0]+radius*2),(self.prevPoint[1]+radius )
        self.shape=self.canvas.create_rectangle(x1,y1,x2,y2,width=self.stroke_size.get(),outline=self.stroke_color.get());
    def Linebuttonpressed(self):
        self. prevPoint=[0,0]
        self.newPoint=[0,0]
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>",self.DrawLine)
        self.canvas.bind("<ButtonRelease-1>",self.DrawShape_end)
    def DrawLine(self,event):
        self.canvas.delete(self.shape)
        x=event.x
        y=event.y
        self.newPoint=[x,y]
        self.shape=self.canvas.create_line(self.prevPoint[0],self.prevPoint[1],self.newPoint[0],self.newPoint[1],width=self.stroke_size.get(),fill=self.stroke_color.get());
    def Trianglebuttonpressed(self):
        self.prevPoint=[0,0]
        self.newPoint=[0,0]
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>",self.DrawTriangle)
        self.canvas.bind("<ButtonRelease-1>",self.DrawShape_end)
    def DrawTriangle(self,event):
        self.canvas.delete(self.shape)
        x=event.x
        y=event.y
        self.newPoint=[x,y]
        if(self.prevPoint==[0,0]):
            self.prevPoint=[x,y]
        radius=abs(self.prevPoint[0]-self.newPoint[0])+abs(self.prevPoint[1]-self.newPoint[1])
        x1,y1=(self.prevPoint[0]),(self.prevPoint[1])
        x2,y2=(self.prevPoint[0]+radius),(self.prevPoint[1]+radius )
        x3,y3=(self.prevPoint[0]-radius),(self.prevPoint[1]+radius )
        self.shape=self.canvas.create_polygon(x1,y1,x2,y2,x3,y3,width=self.stroke_size.get(),outline=self.stroke_color.get(),fill="white");
    def Ovalbuttonpressed(self):
        self.prevPoint=[0,0]
        self.newPoint=[0,0]
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>",self.DrawOval)
        self.canvas.bind("<ButtonRelease-1>",self.DrawShape_end)
    def DrawOval(self,event):
        self.canvas.delete(self.shape)
        x=event.x
        y=event.y
        self.newPoint=[x,y]
        if(self.prevPoint==[0,0]):
            self.prevPoint=[x,y]
        radius=abs(self.prevPoint[0]-self.newPoint[0])+abs(self.prevPoint[1]-self.newPoint[1])
        x1,y1=(self.prevPoint[0]),(self.prevPoint[1])
        x2,y2=(self.prevPoint[0]+radius),(self.prevPoint[1]+radius/2 )
        self.shape=self.canvas.create_oval(x1,y1,x2,y2,width=self.stroke_size.get(),outline=self.stroke_color.get());
    def Starbuttonpressed(self):
        self.prevPoint=[0,0]
        self.newPoint=[0,0]
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>",self.DrawStar)
        self.canvas.bind("<ButtonRelease-1>",self.  DrawShape_end)
    def DrawStar(self,event):
        self.canvas.delete(self.shape)
        x=event.x
        y=event.y
        self.newPoint=[x,y]
        if(self.prevPoint==[0,0]):
            self.prevPoint=[x,y]
        radius=abs(self.prevPoint[0]-self.newPoint[0])+abs(self.prevPoint[1]-self.newPoint[1])
        x1,y1=(self.prevPoint[0]),(self.prevPoint[1])
        x2,y2=(x1+radius/2),(y1+radius/2)
        x3,y3=(x2+radius),(y2)
        x4,y4=(x3-radius+0.1*radius),(y3+radius/2 )
        x5,y5=(x4+radius/2,y4+radius/1.5)
        x6,y6=(x5-radius,y5-radius/2)
        x7,y7=(x6-radius,y6+radius/2)
        x8,y8=(x7+radius/2,y7-radius/1.5)
        x9,y9=(x8-radius,y8-radius/2)
        x10,y10=(x9+radius,y9)
        self.shape=self.canvas.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7,x8,y8,x9,y9,x10,y10,width=self.stroke_size.get(),outline=self.stroke_color.get(),fill="white");
    def Hexagonbuttonpressed(self):
        self.prevPoint=[0,0]
        self.newPoint=[0,0]
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>",self.DrawHexagon)
        self.canvas.bind("<ButtonRelease-1>",self.DrawShape_end)
    def DrawHexagon(self,event):
        self.canvas.delete(self.shape)
        x=event.x
        y=event.y
        self.newPoint=[x,y]
        if(self.prevPoint==[0,0]):
            self.prevPoint=[x,y]
        radius=abs(self.prevPoint[0]-self.newPoint[0])+abs(self.prevPoint[1]-self.newPoint[1])
        x1,y1=(self.prevPoint[0]),(self.prevPoint[1])
        x2,y2=(x1+radius),(y1)
        x3,y3=(x2+radius/2,y2+radius)
        x4,y4=(x3-radius/2,y3+radius)
        x5,y5=(x4-radius,y4)
        x6,y6=(x5-radius/2,y5-radius)
        self.shape=self.canvas.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,outline=self.stroke_color.get(),width=self.stroke_size.get(),fill="white");
    def Pentagonbuttonpressed(self):
        self.prevPoint=[0,0]
        self.newPoint=[0,0]
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>",self.DrawPentagon)
        self.canvas.bind("<ButtonRelease-1>",self.DrawShape_end)
    def DrawPentagon(self,event):
        self.canvas.delete(self.shape)
        x=event.x
        y=event.y
        self.newPoint=[x,y]
        if(self.prevPoint==[0,0]):
            self.prevPoint=[x,y]
        radius=abs(self.prevPoint[0]-self.newPoint[0])+abs(self.prevPoint[1]-self.newPoint[1])
        x1,y1=(self.prevPoint[0]),(self.prevPoint[1])
        x2,y2=(x1+radius),(y1+radius/2)
        x3,y3=(x2-radius/2),(y2+radius)
        x4,y4=(x3-radius),(y3)
        x5,y5=(x4-radius/2),(y4-radius)
        self.shape=self.canvas.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,outline=self.stroke_color.get(),width=self.stroke_size.get(),fill="white");
    def startdrawingHeptagon(self, event):
        self.prevPoint[0] = event.x
        self.prevPoint[1] = event.y

    def drawHeptagon(self, event):
        self.canvas.delete(self.shape)
        center_x = self.prevPoint[0]
        center_y = self.prevPoint[1]
        radius = abs(event.x - self.prevPoint[0]) 

        heptagon_vertices = self.calculateheptagonvertices(center_x, center_y, radius)
 
        self.shape=self.canvas.create_polygon(heptagon_vertices, outline=self.stroke_color.get(), fill='white', width=self.stroke_size.get())
    def calculateheptagonvertices(self, center_x, center_y, radius):
        vertices = []
        for i in range(7):
            angle_deg = 360 / 7 * i
            angle_rad = angle_deg * (3.14159 / 180)  # Convert angle to radians
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)
            vertices.append((x, y))
        return vertices
    def startdrawingoctagon(self, event):
        self.prevPoint[0] = event.x
        self.prevPoint[1]= event.y

    def drawOctagon(self, event):
        self.canvas.delete(self.shape)
        center_x = self.prevPoint[0]
        center_y = self.prevPoint[1]
        radius = abs(event.x - self.prevPoint[0])  

        octagon_vertices = self.calculateoctagonvertices(center_x, center_y, radius)

        self.shape=self.canvas.create_polygon(octagon_vertices, outline=self.stroke_color.get(), fill='white', width=self.stroke_size.get())
    def calculateoctagonvertices(self, center_x, center_y, radius):
        vertices = []
        for i in range(8):
            angle_deg = 45 + 45 * i
            angle_rad = angle_deg * (3.14159 / 180) 
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)
            vertices.append((x, y))
        return vertices
    def startdrawingNanogon(self, event):
        self.prevPoint[0] = event.x
        self.prevPoint[1] = event.y

    def drawNanogon(self, event):
        self.canvas.delete(self.shape)
        center_x = self.prevPoint[0]
        center_y = self.prevPoint[1]
        radius = abs(event.x - self.prevPoint[0])  

        nanogon_vertices = self.calculatenanogonvertices(center_x, center_y, radius)

        self.shape=self.canvas.create_polygon(nanogon_vertices, outline=self.stroke_color.get(), fill='white', width=self.stroke_size.get())
    def calculatenanogonvertices(self, center_x, center_y, radius):
        vertices = []
        for i in range(9):
            angle_deg = 40 + 40 * i
            angle_rad = angle_deg * (3.14159 / 180)  # Convert angle to radians
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)
            vertices.append((x, y))
        return vertices
    def startdrawingDecagon(self, event):
        self.prevPoint[0] = event.x
        self.prevPoint[1] = event.y

    def drawDecagon(self, event):
        self.canvas.delete(self.shape)
        center_x = self.prevPoint[0]
        center_y = self.prevPoint[1]
        radius = abs(event.x - self.prevPoint[0])  # Use the distance between start_x and current x as radius

        decagon_vertices = self.calculatedecagonvertices(center_x, center_y, radius)

        self.shape=self.canvas.create_polygon(decagon_vertices, outline=self.stroke_color.get(), fill='white', width=self.stroke_size.get())
    def calculatedecagonvertices(self, center_x, center_y, radius):
        vertices = []
        for i in range(10):
            angle_deg = 36 + 36 * i
            angle_rad = angle_deg * (3.14159 / 180)  # Convert angle to radians
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)
            vertices.append((x, y))
        return vertices




Paintapp(1100,600,"AbdulRahim's Paint").run() 

"""""
def circlebuttonpressed():
    prevPoint=[0,0]
    newPoint=[0,0]
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    canvas.unbind("<Button-1>")


    canvas.bind("<Button-1>",DrawCircle)
    canvas.bind("<B1-Motion>",DrawCircle)
    canvas.bind("<ButtonRelease-1>",DrawCircle_end)
def DrawCircle(event):
    global prevPoint
    x=event.x
    y=event.y
    if(prevPoint!=[0,0]):
        prevPoint[0]=x
        prevPoint[1]=y

    radius=abs(prevPoint[0]-x)+abs(prevPoint[1]-y)
    x2,y2=(x+radius),(y+radius )
    canvas.create_oval(x,y ,x2,y2,width=5,outline="red");

def DrawCircle_end(event):
    prevPoint=[0,0]
    """