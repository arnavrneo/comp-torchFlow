import sys
import functools
import pandas as pd
import tkinter as tk
from tkinter import *
import configparser
from tkinter import messagebox
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# from tkinter import filedialog

class LoginPage(Frame):
    def __init__(self, master, screen_w, screen_h, exit_command):
        super().__init__()
        self.master = master
        self.screen_width = screen_w
        self.screen_height = screen_h
        self.exit_command = exit_command
        # ========================================================================
        # ============================background image============================
        # ========================================================================
        self.bg_frame = Image.open('resources/background1.png').resize((self.screen_width, self.screen_height))
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')
        # ====== Login Frame =========================
        self.lgn_frame = Frame(self, bg='#040405', width=1024, height=724)
        x = (self.screen_width//2)-(1024//2)
        y = (self.screen_height//2)-(724//2)
        self.lgn_frame.place(x=x, y=y)

        # ========================================================================
        # ========================================================
        # ========================================================================
        self.txt = "WELCOME"
        self.heading = Label(self.lgn_frame, text=self.txt, font=('yu gothic ui', 25, "bold"), bg="#040405",
                             fg='white',
                             bd=5,
                             relief=FLAT)
        self.heading.place(x=80, y=30, width=300, height=30)

        # ========================================================================
        # ============ Left Side Image ================================================
        # ========================================================================
        self.side_image = Image.open('resources/login.png').resize((468, 512))
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.side_image_label.image = photo
        self.side_image_label.pack(fill='both', expand='yes')
        self.side_image_label.place(x=50, y=150)

        # ========================================================================
        # ============ Sign In Image =============================================
        # ========================================================================
        self.sign_in_image = Image.open('resources/hyy.png')
        photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.sign_in_image_label.image = photo
        self.sign_in_image_label.place(x=620, y=130)

        # ========================================================================
        # ============ Sign In label =============================================
        # ========================================================================
        self.sign_in_label = Label(self.lgn_frame, text="Sign In", bg="#040405", fg="white",
                                    font=("yu gothic ui", 17, "bold"))
        self.sign_in_label.place(x=650, y=240)

        # ========================================================================
        # ============================username====================================
        # ========================================================================
        self.username_label = Label(self.lgn_frame, text="Username", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=300)

        self.username_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui ", 12, "bold"), insertbackground = '#6b6a69')
        self.username_entry.place(x=580, y=335, width=270)

        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=359)
        # ===== Username icon =========
        self.username_icon = Image.open('resources/username_icon.png')
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=332)

        # ========================================================================
        # ============================password====================================
        # ========================================================================
        self.password_label = Label(self.lgn_frame, text="Password", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=550, y=380)

        self.password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui", 12, "bold"), show="*", insertbackground = '#6b6a69')
        self.password_entry.place(x=580, y=416, width=244)

        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=440)
        # ======== Password icon ================
        self.password_icon = Image.open('resources/password_icon.png')
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=550, y=414)
        # ========= show/hide password ==================================================================
        self.show_icon = Image.open("resources/show.png") 
        self.show_image = ImageTk.PhotoImage(self.show_icon)
        self.hide_icon = Image.open("resources/hide.png")
        self.hide_image = ImageTk.PhotoImage(self.hide_icon)

        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)

        # ========================================================================
        # ============================login button================================
        # ========================================================================
        self.lgn_button = Image.open('resources/btn1.png')
        photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.lgn_button_label.image = photo
        self.lgn_button_label.place(x=550, y=450)
        self.login = Button(self.lgn_button_label, text='LOGIN', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=functools.partial(self.on_click_login, self.username_entry, self.password_entry))
        self.login.place(x=20, y=10)

        # =========== Sign Up ==================================================
        self.sign_label = Label(self.lgn_frame, text='No account yet?', font=("yu gothic ui", 11, "bold"),
                                relief=FLAT, borderwidth=0, background="#040405", fg='white')
        self.sign_label.place(x=550, y=560)

        self.signup_img = ImageTk.PhotoImage(file='resources/register.png')
        self.signup_button_label = Button(self.lgn_frame, image=self.signup_img, bg='#98a65d', cursor="hand2",
                                          borderwidth=0, background="#040405", activebackground="#040405",command=functools.partial(self.on_click_signup, self.username_entry, self.password_entry))
        self.signup_button_label.place(x=700, y=555, width=111, height=35)


    def show(self):
        self.hide_button = Button(self.lgn_frame, image=self.hide_image, command=self.hide, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.hide_button.place(x=860, y=420)
        self.password_entry.config(show='')

    def hide(self):
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)
        self.password_entry.config(show='*')

    def load_login_data(self):
        config = configparser.ConfigParser()
        try:
            config.read("login.ini")
        except:
            with open("login.ini", "w") as config_file:
                config.write(config_file)
        
        return config

    def on_click_login(self, username_entry, password_entry):
        username = username_entry.get()
        password = password_entry.get()

        config = self.load_login_data()
        if "Users" not in config:
            config["Users"] = {}

        if username in config["Users"] and config["Users"][username] == password:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.pack_forget() 
            self.main_page = Dashboard(self, self.screen_width, self.screen_height, self.exit_command)
            self.main_page.pack(fill=BOTH, expand=True)


        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")


    def on_click_signup(self, username_entry, password_entry):
        username = username_entry.get()
        password = password_entry.get()

        config = self.load_login_data()

        if "Users" not in config:
            config["Users"] = {}
        
        if username not in config["Users"]:
            config["Users"][username] = password
            with open("login.ini", "w") as config_file:
                config.write(config_file)
            messagebox.showinfo("Signup Successful", "Account created successfully!")
        else:
            messagebox.showerror("Signup Failed", "Username already exists")


class Dashboard(Frame):
    def __init__(self, master, screen_w, screen_h, exit_command):
        super().__init__()
        self.master = master
        self.screen_width = screen_w
        self.screen_height = screen_h
        self.exit_command = exit_command

        data = pd.read_csv("resources/results.csv")
        data.columns = data.columns.str.strip()

        preds = pd.read_csv("resources/preds.csv")
        
        #=======================LEFT FRAME========================
        side_frame = Frame(self, bg="#4C2A85")
        side_frame.pack(side="left", fill="y", ipadx=15)

        label = Label(side_frame, text="Dashboard", bg="#4C2A85", fg="#FFF", font=('yu gothic ui', 25, "bold"))
        label.pack(pady=50, padx=50)

        label = Button(side_frame, text="Predict", command=self.predict, relief=FLAT, activebackground="#5c2a85", font=('yu gothic ui', 15, "bold"),
                        borderwidth=0, background="#4C2A85", cursor="hand2", fg="white", highlightbackground="black",bd=3)
        label.pack(pady=(20,0), fill='x', ipady=5)
        
        label = Button(side_frame, text="Nearby", command=self.nearby, relief=FLAT, activebackground="#5c2a85", font=('yu gothic ui', 15, "bold"),
                        borderwidth=0, background="#4C2A85", cursor="hand2", fg="white", highlightbackground="black",bd=3)
        label.pack(fill='x', ipady=5)

        label = Button(side_frame, text="Back", command=self.back, relief=FLAT, activebackground="#5c2a85", font=('yu gothic ui', 15, "bold"),
                        borderwidth=0, background="#4C2A85", cursor="hand2", fg="white", highlightbackground="black",bd=3)
        label.pack(fill='x', ipady=5)
        

        label = Button(side_frame, text="Exit", command=self.exit_command, relief=FLAT, activebackground="#5c2a85", font=('yu gothic ui', 15, "bold"),
                        borderwidth=0, background="#4C2A85", cursor="hand2", fg="white", highlightbackground="black",bd=3)
        label.pack(fill='x', ipady=5)
        

        # ===================Plastic Density in Test Set===========

        fig0 = Figure(figsize=(16,6))  
        gs = fig0.add_gridspec(1, 3, wspace=0.3)

        bar_width = 0.35
        ax0 = fig0.add_subplot(gs[0])
        ax0.bar(preds.index - bar_width/2, preds["ACTUAL_CT"], bar_width, label="Actual Count")
        ax0.bar(preds.index - bar_width/2, preds["PRED_CT"], bar_width, label="Predicted Count")
        ax0.set_title("Plastic Density")
        ax0.set_xlabel("Images")
        ax0.set_ylabel("Counts")
        ax0.legend()

        #================mAP50/mAP50-95============================
        plt.rcParams["axes.prop_cycle"] = plt.cycler(
        color=["#4C2A85", "#BE96FF", "#957DAD", "#5E366E", "#A98CCC"])

        ax1 = fig0.add_subplot(gs[1])
        ax1.plot(data["epoch"], data["metrics/mAP50(B)"], label="mAP50", marker="o")
        ax1.plot(data["epoch"], data["metrics/mAP50-95(B)"], label="mAP50-95", marker="x")
        ax1.set_title("mAP50/mAP50-95")
        ax1.set_xlabel("Epochs")
        ax1.set_ylabel("mAP")
        ax1.legend()

        #================Precision/Recall Curve============================
        data['TPR'] = data['metrics/recall(B)']
        data['FPR'] = 1 - data['metrics/precision(B)']
        ax2 = fig0.add_subplot(gs[2])
        ax2.plot(data['FPR'], data['TPR'], marker='o', linestyle='-', color='r')
        ax2.set_title("ROC Curve")
        ax2.set_xlabel("FPR")
        ax2.set_ylabel("TPR")

        # #================Losses============================

        fig1 = Figure(figsize=(16,6))  
        gs = fig1.add_gridspec(1, 3, wspace=0.3)

        ax3 = fig1.add_subplot(gs[0])
        ax3.plot(data["epoch"], data["train/dfl_loss"], label="train", marker="o")
        ax3.plot(data["epoch"], data["val/dfl_loss"], label="val", marker="s")
        ax3.set_title("Detection Focal Loss")
        ax3.set_xlabel("Epochs")
        ax3.set_ylabel("Loss")
        ax3.legend()

        ax4 = fig1.add_subplot(gs[1])
        ax4.plot(data["epoch"], data["train/box_loss"], label="train", marker="o")
        ax4.plot(data["epoch"], data["val/box_loss"], label="val", marker="s")
        ax4.set_title("Box Loss")
        ax4.set_xlabel("Epochs")
        ax4.set_ylabel("Loss")
        ax4.legend()

        ax5 = fig1.add_subplot(gs[2])
        ax5.plot(data["epoch"], data["train/cls_loss"], label="train", marker="o")
        ax5.plot(data["epoch"], data["val/cls_loss"], label="val", marker="s")
        ax5.set_title("Classification Loss")
        ax5.set_xlabel("Epochs")
        ax5.set_ylabel("Loss")
        ax5.legend()

        charts_frame = Frame(self)
        charts_frame.pack()

        upper_frame = Frame(charts_frame)
        upper_frame.pack(fill="both", expand=True)

        canvas0 = FigureCanvasTkAgg(fig0, upper_frame)
        canvas0.draw()
        canvas0.get_tk_widget().pack(side="left", fill="both", expand=True)

        lower_frame = Frame(charts_frame)
        lower_frame.pack(fill="both", expand=True)

        canvas1 = FigureCanvasTkAgg(fig1, lower_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

        
    def predict(self):
        login_page = PredictPage(self, self.screen_width, self.screen_height, self.exit_command)
        login_page.pack(fill=tk.BOTH, expand=True)
        self.destroy()

    def nearby(self):
        login_page = NearbyPage(self, self.screen_width, self.screen_height, self.exit_command)
        login_page.pack(fill=tk.BOTH, expand=True)
        self.destroy()

    def back(self):
        login_page= LoginPage(self, self.screen_width, self.screen_height, self.exit_command)
        login_page.pack(fill=BOTH, expand=True)
        self.destroy()


class PredictPage(Frame):
    def __init__(self, master, screen_w, screen_h, exit_command):
        super().__init__()
        self.master = master
        self.screen_width = screen_w
        self.screen_height = screen_h
        self.exit_command = exit_command
        print("Predict")

class NearbyPage(Frame):
    def __init__(self, master, screen_w, screen_h, exit_command):
        super().__init__()
        self.master = master
        self.screen_width = screen_w
        self.screen_height = screen_h
        self.exit_command = exit_command
        print("Nearby")
   

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1190x718')
        self.resizable(0, 0)
        self.platform = sys.platform
        if self.platform=="linux":
            self.attributes('-zoomed', True) # for linux

        else:
            self.state('zoomed') # if mac or window

        self.title('torchFlow')
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.show_login_page()

    def show_login_page(self):
        login_page = LoginPage(self, self.screen_width, self.screen_height, self.exit_command)
        login_page.pack(fill=tk.BOTH, expand=True)

    def exit_command(self):
        exit_command = messagebox.askyesno("Confirm Exit?")
        if exit_command > 0:
            self.destroy()

if __name__ == '__main__':
    app = App()
    app.mainloop()
