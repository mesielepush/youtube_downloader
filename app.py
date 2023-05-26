import tkinter as tk
import customtkinter as ctk
import pytube
from pytube import YouTube as yt
from PIL import ImageTk, Image
import os
from multiprocessing import Queue

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')
save_path = Queue()

class SaveFolder(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master)
        
        
        self.save_folder_line = ctk.CTkLabel(self, text = 'Set save folder to: ').pack()
        self.save_folder_memory = ctk.StringVar()
        self.save_folder_entry = ctk.CTkEntry(self, textvariable = self.save_folder_memory)
        self.save_folder_entry.pack(padx = (10,10),pady = (10,10))
        self.submit_save_folder = ctk.CTkButton(self, text = 'Submit folder', command = self.submit_save).pack(pady = 10, padx = 10)
        
    def submit_save(self):
        path = self.save_folder_memory.get()
        while not save_path.empty():
            save_path.get() 
        save_path.put(path)
        self.new_path_warning = ctk.CTkLabel(self, text = 'Save to Path set to: \n'+path)
        self.new_path_warning.pack(pady=(15,5))
        self.after(3000, lambda: self.new_path_warning.destroy())
        print(path)
        


class MainCenter(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0,weight = 1)
        self.grid_rowconfigure(1, weight = 2)
        self.grid_rowconfigure(2,weight = 1)
        self.update()
        self.greetings = ctk.CTkLabel(self, text = f"Insert youtube link" , font = ('Impact',18)).grid(row = 0, column = 0)
        self.links_entry = ctk.CTkTextbox(self, width = 450, height = 60, padx = 10, pady=20)
        self.links_entry.grid(row = 1, column = 0)
        self.download = ctk.CTkButton(self, text = 'Download', command = self.start_download).grid(row = 2, column = 0)
        

    def start_download(self):
        if save_path.empty():
            warning_empty = ctk.CTkLabel(self, text = 'NO DOWNLOAD PATH')
            warning_empty.grid()
            self.after(3000, lambda: warning_empty.destroy())
        else:
            
            links = self.links_entry.get(1.0, 'end')
            links = links.split('https://')
            links = ['https://' + x for x in links if len(x)>0]
            self.links_entry.configure(state = 'disable')
            for link in links:
                try:
                    pre_video = yt(link)
                    video = pre_video.streams.get_highest_resolution()
                    video.download(save_path.get(timeout = 5))
                    self.links_entry.delete('start','end')
                    self.links_entry.insert('start','Ready: ' + link )
                    print('DONEEEEEEEE')
                    
                except:
                    self.warning_no = ctk.CTkLabel(self,text = f'{link} Link invalid or something', font = ('Impact',15))
                    self.warning_no.grid(row = 3, column = 0)
                    self.after(3000, self.warning_no.destroy())        
            
            self.links_entry.configure(state = 'normal')
        
        
        
        
                     

class MonitorDownloads(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.files_path = ctk.StringVar()
        
        self.folder_monitor = ctk.CTkTextbox(self, width = 300, height = 200, pady=5, padx = 5)
        self.folder_monitor
        self.folder_monitor.pack()
        self.submit_path = ctk.CTkButton(self, text = 'monitor folder', command = self.monitor_folder)
        self.submit_path.pack()
        self.user_path = ctk.CTkEntry(self, textvariable = self.files_path)
        self.user_path.pack()
        
        
    def monitor_folder(self):
        if len(self.files_path.get()) == 0:
            warning = ctk.CTkLabel(self, text = 'NO FOLDER TO MONITOR')
            warning.pack()
            self.after(3000, lambda: warning.destroy())
        else:
            files = os.listdir(self.files_path.get())
            files = ''.join([file+'\n' for file in files])
            self.folder_monitor.insert("1.0", files)
            print(files)
        
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ico = Image.open(f'assets/icon.png')
        ico = ImageTk.PhotoImage(ico)
        # configure window
        self.title("    YoutubeDownloader")
        self.geometry(f"{1000}x{300}")
        self.after(250, lambda: self.tk.call('wm', 'iconphoto', self._w, ico))
        self.resizable(False,False)
        self.grid_config()
        
        self.save_folder = SaveFolder(master = self)
        self.save_folder.grid(row = 0,
                         column = 0,
                         padx = 20,
                         pady = 20,
                         sticky = 'ns')
        
        self.main_center = MainCenter(master = self)
        self.main_center.grid(row = 0,
                         column = 1,
                         padx = 20,
                         pady = 20,
                         sticky = 'ns')
        self.monitor_right = MonitorDownloads(master = self)
        self.monitor_right.grid(row = 0,
                               column = 2,
                               padx = 15,
                               pady = 15,
                               sticky = 'ns')
    
    def grid_config(self):
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 1)
        self.grid_rowconfigure(0,weight = 2)
        self.grid_rowconfigure(1, weight = 1)

if __name__=='__main__':
    app = App()
    app.mainloop()