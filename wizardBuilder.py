from tkinter import *
from tkinter import filedialog,messagebox
import json
import pdb

class ConfigWizard:
    def __init__(self,filename):
        file=open(filename,'r')
        self.title = file.readline().rstrip()
        self.page = {}
        self.pool = {}
        cpage=0
        textblock=False
        for i in file.read().splitlines():
            print(i)
            i=i.lstrip().rstrip()
            # Keep reading if contiguous syntax block
            if textblock:
                self.page[cpage]['items'][-1]+=i[1:-1]
                if i[-1] == '"':
                    textblock=False
            # New page
            #pdb.set_trace()
            if i[0] == '@':
                if cpage!=0 and not ('next' in self.page[cpage]):
                    self.page[cpage]['next']=i[1:]
                self.page[i[1:]]={'items':[]}
                cpage=i[1:]
                
            # Text block
            elif i[0] == '"':
                if i[-1] != '"':
                    textblock=True
                    self.page[cpage]['items'].append(i[1:])
                else:
                    self.page[cpage]['items'].append(i[1:-1])
                

            # parse setting
            elif i[0] == '=':
                incantation=i.split(' ')
                self.page[cpage]['items'].append(incantation[:])

            # parse transition
            elif i[0] == '>':
                self.page[cpage]['next']=i[1:]
        self.page[cpage]['next']='END'
        file.close()
        
    def save_config(self):
        root = tkinter()
        root.withdraw()
        config_file = filedialog.asksaveasfilename()
        try:
            with open(config_file, 'w') as f:
                json.dump(self.pool,f,indent=2)
            messagebox.showinfo("Success", f"Configuration saved to {config_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")

if __name__ == "__main__":
    
    t=ConfigWizard('testc.txt')
    #root = Tk()
    #app = ConfigWizard(root)
    #root.mainloop()
