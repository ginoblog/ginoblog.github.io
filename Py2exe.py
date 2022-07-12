#需要安装tkinter, pywin32, pyinstaller
#里面注释打*的需要自行调整路径

from tkinter import ttk
import threading
import tkinter,time
import glob
import shutil
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os,pywintypes,pythoncom

#文件路径
#pyinstaller默认放在scripts文件夹而不是site-packages下面
#编译时默认编译到运行位置
#在cmd里运行时在pyinstaller.exe的文件夹下面

PATH,nameq=os.path.split(__file__)
root=Tk()
root.title="Python to exe v2.0.0"
root.geometry("500x500")
sh=[]

if not "C:\\Users\\gino\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python39\\Scripts\\" in os.environ["PATH"]:
    #设置环境变量
    ### *路径自行调整
    os.system(f"PATH={os.environ['PATH']};C:\\Users\\gino\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python39\\Scripts")


btn2=Button(root,text="Compile All to",anchor="center",state="disabled",width=20)
btn4=Button(root,text="Delete last",anchor="center",state="disabled",width=20)
btn3=Button(root,text="Delete All",anchor="center",state="disabled",width=20)
tmp=[]

#函数
def q(event=""):  #退出
    root.quit()

def cfile():   #选择文件
    #cav.delete(a)
    
    tmpw=filedialog.askopenfilename(parent=root,filetypes=[('Python File', '*.py'),("Python File (No Console)", "*.pyw"),("All Files","*.*")],initialdir="C:/",title='Choose a python file')
    
    if tmp.count(tmpw)>0:
        messagebox.showwarning("ERROR","filesys.repeatedfileerror: Repeated File")
    elif len(tmpw)!=0 and tmpw!=None:
        tmp.append(tmpw)
        w=cav.create_text(len(tmp[len(tmp)-1])*2.5+60,20*len(tmp),text=tmp[len(tmp)-1],fill="black")
        sh.append(w)
    
    if len(tmp)>0:
        btn3.config(state="active")
        btn2.config(state="active")
        btn4.config(state="active")



def reset():       #删除所有文件
    
    if (len(sh)==0):
        messagebox.showerror("ERROR","compiler.fileerror: empty file list")
        return 0    
    t=len(sh)
    for i in range(0,t):
        cav.delete(sh[i])
    tmp.clear()
    sh.clear()
    if len(tmp)<=0:
        btn3.config(state="disabled")
        btn2.config(state="disabled")
        btn4.config(state="disabled")
        
        
         
def delast():      #删除最后一个文件
    
    if (len(sh)==0):
        messagebox.showerror("ERROR","compiler.fileerror: empty file list")
        return 0
    cav.delete(sh[len(sh)-1])
    if len(sh):
        sh.pop()
        tmp.pop()
    if len(sh)<=0:
        btn3.config(state="disabled")
        btn2.config(state="disabled")
        btn4.config(state="disabled") 
    
    
    
def cato():      #编译所有文件
    if (len(sh)==0):
        messagebox.showerror("ERROR","compiler.fileerror: empty file list")
        return 0    
    #os.system("cd C:\\Users\\gino\\")
    tmpw=filedialog.askdirectory()
    progressbarOne = ttk.Progressbar(root, length=200, mode='indeterminate', orient=tkinter.HORIZONTAL)
    progressbarOne.pack(padx=5,pady=5)    
    def wr(tmpw):
        t1=time.time()
        for i in tmp:
            if " " in i:
                messagebox.showerror("ERROR","filesys.readfileerror: Space in filename")
                continue
            os.system(f"C:\\Users\\gino\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python39\\Scripts\\pyinstaller.exe -F -w {i}") 
            ###  *路径自行调整，默认只需调整用户名"gino"
        filelist=glob.glob(f"{PATH}\\dist\*")
        dflist=glob.glob(f"{PATH}\\*.spec")
        for f in filelist:
            fpath,fname=os.path.split(f)
            shutil.move(f,tmpw+"\\"+fname)
        for f in dflist:
            os.remove(f)
        t2=time.time()
        progressbarOne.stop()
        messagebox.showinfo("INFO",f"EXE build of total {len(sh)} finished in {t2-t1} sec")
        progressbarOne.destroy()
    
    tw1=threading.Thread(target=progressbarOne.start,args=())
    tw2=threading.Thread(target=wr,args=(tmpw,))
    tw1.setDaemon(daemonic=tw2)
    tw1.start()
    tw2.start()
    
#菜单
menubar = Menu(root,activeborderwidth=3,tearoff=False)
menubar.add_command(label="Choose...",command=cfile)
menubar.add_command(label="Delete All",command=reset)
menubar.add_command(label="Delete Last file",command=delast)
menubar.add_command(label="Compile All...",command=cato)
menubar.add_command(label="Quit",command=q)

def xShowMenu(event):
    menubar.post(event.x_root, event.y_root)   

root.bind("<Button-3>", xShowMenu)
root.bind("<Control-Q>",q)
root.bind("<Control-q>",q)

btn3.config(command=reset)
btn4.config(command=delast)
btn2.config(command=cato)
btn=Button(root,text="Choose a python file",anchor="center",command=cfile,width=20)

#文件显示区
frame = Frame(root, bd=4, relief=SUNKEN,background="white")
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
yscroll = Scrollbar(frame)
yscroll.grid(row=0, column=1, sticky=N+S)
cav = Canvas(frame, bd=0, yscrollcommand=yscroll.set,cursor="circle")
cav.grid(row=0, column=0, sticky=N+S+E+W)
yscroll.config(command=cav.yview)
frame.pack(fill=BOTH,expand=1)

#启动
cav.pack
btn.pack()
btn4.pack()
btn3.pack()
btn2.pack()   
root.mainloop()