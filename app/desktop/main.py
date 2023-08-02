import sys
import socket
import requests
import threading
import functools
import numpy as np
import pandas as pd
import configparser
import tkinter as tk
import urllib.request
from tkinter import *
import haversine as hs
import tkinter.filedialog
from PIL import ImageTk, Image
from tkinter import messagebox
import matplotlib.pyplot as plt
from exif import Image as ex_img
from matplotlib.figure import Figure
from geopy.geocoders import Nominatim
from tkintermapview import TkinterMapView
from tkinter.ttk import Progressbar, Style
from tkinter.filedialog import askopenfile
from math import radians, cos, sin, asin, sqrt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
        
        if len(username)==0 or len(password)==0:
            messagebox.showerror("Signup Failed", "All entries are not filled")
        
        elif username not in config["Users"]:
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
        super().__init__(background="#2E2E2E")
        self.master = master
        self.screen_width = screen_w
        self.screen_height = screen_h
        self.exit_command = exit_command
        self.create_widgets()
        self.check_and_display_conn_result()

    def create_widgets(self):
        self.server_label = Label(self, text="Server Link", bg="#2E2E2E", fg="#ffffff",
                                    font=("yu gothic ui", 13, "bold"))
        self.server_label.place(x=self.screen_width*0.1, y=self.screen_height*0.1)

        self.server_entry = Entry(self, highlightthickness=2, highlightbackground="#ffffff", relief=FLAT, bg="#454545", fg="#ffffff",
                                    font=("yu gothic ui ", 12, "bold"), width=70, insertbackground = '#6b6a69')

        self.server_entry.place(x=self.screen_width*0.18, y=self.screen_height*0.1)

        self.image_label = Label(self, text="Image(jpg,png)", bg="#454545", font=('yu gothic ui', 25, "bold"), highlightbackground="#ffffff", highlightthickness=2)
        self.image_label.place(x=self.screen_width*0.1, y=self.screen_height*0.2, width=self.screen_width//2, height=self.screen_height//2)

        
        self.show_image = Button(self, text="Upload Image", command=self.upload_image)
        self.show_image.place(x=self.screen_width*0.1,y=self.screen_height*0.725)

        self.predict_image = Button(self, text="Run Prediction", command=self.run_prediction)
        self.predict_image.place(x=self.screen_width*0.535,y=self.screen_height*0.725)

        self.progress_style = Style()
        self.progress_style.theme_use('default')  
        self.progress_style.configure("Custom.Horizontal.TProgressbar", thickness=20, troughcolor='green', background='black')
        self.pb = Progressbar(
                        self,
                        orient='horizontal',
                        mode='indeterminate',
                        length=100,
                    )
        self.info_label10 = Label(self, text="Plastic Counts :", bg="#2E2E2E", fg="white", font=('yu gothic ui', 15, "bold"))
        self.info_label10.place(x=(self.screen_width*0.12 + self.screen_width//2), y=self.screen_height*0.2)

        self.info_label11 = Label(self, text="NA", bg="#2E2E2E", fg="white", font=('yu gothic ui', 15, "bold"))
        self.info_label11.place(x=(self.screen_width*0.28 + self.screen_width//2), y=self.screen_height*0.2)

        self.info_label20 = Label(self, text="Coordinates :", bg="#2E2E2E", fg="white", font=('yu gothic ui', 15, "bold"))
        self.info_label20.place(x=(self.screen_width*0.12 + self.screen_width//2), y=self.screen_height*0.28)

        self.info_label21 = Label(self, text="NA", bg="#2E2E2E", fg="white", font=('yu gothic ui', 15, "bold"))
        self.info_label21.place(x=(self.screen_width*0.28 + self.screen_width//2), y=self.screen_height*0.28)

        self.info_label30 = Label(self, text="City :", bg="#2E2E2E", fg="white", font=('yu gothic ui', 15, "bold"))
        self.info_label30.place(x=(self.screen_width*0.12 + self.screen_width//2), y=self.screen_height*0.36)

        self.info_label31 = Label(self, text="NA", bg="#2E2E2E", fg="white", font=('yu gothic ui', 15, "bold"))
        self.info_label31.place(x=(self.screen_width*0.28 + self.screen_width//2), y=self.screen_height*0.36)

        self.info_label40 = Label(self, text="Postal code :", bg="#2E2E2E", fg="white", font=('yu gothic ui', 15, "bold"))
        self.info_label40.place(x=(self.screen_width*0.12 + self.screen_width//2), y=self.screen_height*0.44)

        self.info_label41 = Label(self, text="NA", bg="#2E2E2E", fg="white", font=('yu gothic ui', 15, "bold"))
        self.info_label41.place(x=(self.screen_width*0.28 + self.screen_width//2), y=self.screen_height*0.44)

        self.info_label50 = Label(self, text="State :", bg="#2E2E2E", fg="white", font=('yu gothic ui', 15, "bold"))
        self.info_label50.place(x=(self.screen_width*0.12 + self.screen_width//2), y=self.screen_height*0.52)

        self.info_label51 = Label(self, text="NA", bg="#2E2E2E", fg="white", font=('yu gothic ui', 15, "bold"))
        self.info_label51.place(x=(self.screen_width*0.28 + self.screen_width//2), y=self.screen_height*0.52)

        self.info_label60 = Label(self, text="Country :", bg="#2E2E2E", fg="white", font=('yu gothic ui', 15, "bold"))
        self.info_label60.place(x=(self.screen_width*0.12 + self.screen_width//2), y=self.screen_height*0.60)

        self.info_label61 = Label(self, text="NA", bg="#2E2E2E", fg="white", font=('yu gothic ui', 15, "bold"))
        self.info_label61.place(x=(self.screen_width*0.28 + self.screen_width//2), y=self.screen_height*0.60)

        self.back_btn = Button(self, text="Back", command=self.back)
        self.back_btn.place(x=(self.screen_width*0.12 + self.screen_width//2), y=self.screen_height*0.725)

    def upload_image(self):
        self.image_path = tkinter.filedialog.askopenfilename(filetypes=[('Jpg Files', '*.jpg'),('PNG Files','*.png')])
        if self.image_path:
            self.up_image = Image.open(self.image_path)
            self.res_image = self.up_image.resize((1024, 1024), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(self.res_image)
            self.image_label.config(text="", image=self.photo)
            self.image_label.image = self.photo

    def perform_prediction(self):
        self.lat, self.long = get_coordinates(self.image_path)
        self.info = get_info_from_coordinates(self.lat, self.long) 
        
        if self.info is not None:
            self.city, self.postal_code, self.state, self.country = self.info
            self.info_label21.config(text=f"{self.lat:.4f}° N, {self.long:.4f}° E", font=('yu gothic ui', 15, "bold"))
            if self.city.strip()!="":
                self.info_label31.config(text=f"{self.city}")
            if self.postal_code.strip()!="":
                self.info_label41.config(text=f"{self.postal_code}")
            if self.state.strip()!="":
                self.info_label51.config(text=f"{self.state}")
            if self.country.strip()!="":
                self.info_label61.config(text=f"{self.country}")

            self.info_label11.config(text="")

        self.server_link = self.server_entry.get()
        if self.server_link.strip()=="":
            messagebox.showerror("Prediction Failed", "Provide Server Link")

        else:
            if self.server_link[-1:]!="/":
                self.server_link+="/"

            self.url = f"{self.server_link}predict/"
            self.resp = requests.post(url=self.url, files=[('files', open(self.image_path, 'rb'))], verify=False)
            self.result = self.resp.json()
            count = self.result['file'][0]['PRED_CT']
            geo_tag_url = self.result['file'][0]['GEO_TAG_URL']
            self.info_label11.config(text=f"{count}")
            print(count, geo_tag_url)

        self.after(0, self.stop_progress)

    
    def run_prediction(self):
        if self.image_path:
            self.pb.pack(pady=20)
            self.after(0, self.update_progress)  # Use after() to call update_progress() after 0 milliseconds

            # Perform the prediction in a separate thread
            prediction_thread = threading.Thread(target=self.perform_prediction)
            prediction_thread.start()
            
        else:
            messagebox.showerror("Process Failed", "No image selected!")

    def update_progress(self):
        self.pb.start()

    def stop_progress(self):
        self.pb.stop()
        self.pb.pack_forget() 

    def back(self):
        dashboard= Dashboard(self, self.screen_width, self.screen_height, self.exit_command)
        dashboard.pack(fill=BOTH, expand=True)
        self.destroy()

    def check_internet_connection(self):
        try:
            socket.create_connection(("1.1.1.1", 53))
            return True
        except:
            return False
    
    def check_and_display_conn_result(self):
        if not self.check_internet_connection():
            messagebox.showerror("Error", "No internet connection!")
        
        self.after(5000, self.check_and_display_conn_result)


class NearbyPage(Frame):
    def __init__(self, master, screen_w, screen_h, exit_command):
        super().__init__(background="#2E2E2E")
        self.master = master
        self.screen_width = screen_w
        self.screen_height = screen_h
        self.exit_command = exit_command
        self.coords = pd.read_csv("resources/coords.csv")
        self.create_widgets()
        self.check_and_display_conn_result()

    def create_widgets(self):
        self.address_label = Label(self, text="Address: ", bg="#2E2E2E", fg="#ffffff",
                                    font=("yu gothic ui", 13, "bold"))
        self.address_label.place(x=self.screen_width*0.1, y=self.screen_height*0.1)

        self.address_entry = Entry(self, highlightthickness=2, highlightbackground="#ffffff", relief=FLAT, bg="#454545", fg="#ffffff",
                                    font=("yu gothic ui ", 12, "bold"), width=70, insertbackground = '#6b6a69')
        
        self.address_entry.place(x=self.screen_width*0.18, y=self.screen_height*0.1)

        self.search_btn = Button(self, text="Search", command=self.search)
        self.search_btn.place(x=self.screen_width*0.6, y=self.screen_height*0.1)

        self.back_btn = Button(self, text="Back", command=self.back)
        self.back_btn.place(x=self.screen_width*0.65, y=self.screen_height*0.1)

        note = "Note: Thank you for using our app! To find the nearest polluted river, please search for the location you're interested in. Our app will then provide you with information about the nearest polluted river based on our database. Let's work together to protect our environment!"
        self.note_label = Label(self, text=note, bg="#000000", fg="#ffffff",
                                    font=("yu gothic ui", 13, "bold"), wraplength=self.screen_width*0.8, anchor=W, justify=LEFT, highlightthickness=2)
        self.note_label.place(x=self.screen_width*0.1, y=self.screen_height*0.15)

        self.map_widget = TkinterMapView(self, width=self.screen_width*0.8, height=self.screen_height*0.6, corner_radius=2)
        self.map_widget.place(x=self.screen_width*0.1, y=self.screen_height*0.3)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        self.map_widget.set_address("Delhi, India", marker=True)


    def back(self):
        dashboard= Dashboard(self, self.screen_width, self.screen_height, self.exit_command)
        dashboard.pack(fill=BOTH, expand=True)
        self.destroy()

    def check_internet_connection(self):
        try:
            socket.create_connection(("1.1.1.1", 53))
            return True
        except:
            return False
    
    def check_and_display_conn_result(self):
        if not self.check_internet_connection():
            messagebox.showerror("Error", "No internet connection!")
        
        self.after(5000, self.check_and_display_conn_result)

    def get_user_location_by_address(self):
        self.address = self.address_entry.get()
        geolocator = Nominatim(user_agent='myGeocoder')
        location = geolocator.geocode(self.address)
        if location:
            return location.latitude, location.longitude
        else:
            return None
        
    def get_nearby_locations(self):
        in_lat, in_long = self.get_user_location_by_address()
        loc1 = (in_lat, in_long)
        min_distance = np.inf
        req_lat = 0.0
        req_long = 0.0
        for lat, long in zip(self.coords['LAT'].values, self.coords['LONG'].values):
            dis_km = hs.haversine(loc1, (lat, long))
            if dis_km < min_distance:
                min_distance, req_lat, req_long = dis_km, lat, long

        return req_lat, req_long, min_distance

    def search(self):
        lat, long, distance = self.get_nearby_locations()
        city, _ , state, country = get_info_from_coordinates(lat, long)
        self.map_widget.set_address(f"{city},{state},{country}", marker=True)
   

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
        self.check_and_display_conn_result()

    def show_login_page(self):
        login_page = LoginPage(self, self.screen_width, self.screen_height, self.exit_command)
        login_page.pack(fill=tk.BOTH, expand=True)

    def exit_command(self):
        exit_command = messagebox.askyesno("Confirm Exit?")
        if exit_command > 0:
            self.destroy()

    def check_internet_connection(self):
        try:
            socket.create_connection(("1.1.1.1", 53))
            return True
        except:
            return False
    
    def check_and_display_conn_result(self):
        if not self.check_internet_connection():
            messagebox.showerror("Error", "No internet connection!")
        
        self.after(5000, self.check_and_display_conn_result)


def get_info_from_coordinates(latitude, longitude):
        geolocator = Nominatim(user_agent="myGeocoder")
        location = geolocator.reverse((latitude, longitude), exactly_one=True)

        if location is not None:
            address = location.raw['address']
            city = address.get('city', '')
            postal_code = address.get('postcode', '')
            state = address.get('state', '')
            country = address.get('country', '')
            return city, postal_code, state, country

        return None


def get_coordinates(image_path):
    my_image = ex_img(image_path)
    lat = my_image.gps_latitude[0] + (my_image.gps_latitude[1]/60) + (my_image.gps_latitude[2]/3600)
    long = my_image.gps_longitude[0] + (my_image.gps_longitude[1]/60) + (my_image.gps_longitude[2]/3600)

    return lat, long


if __name__ == '__main__':
    app = App()
    app.mainloop()

