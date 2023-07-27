import sys
import functools
import tkinter as tk
from tkinter import *
import configparser
from tkinter import messagebox
from PIL import ImageTk, Image


class LoginPage(Frame):
    def __init__(self, master, screen_w, screen_h):
        super().__init__()
        self.master = master
        self.screen_width = screen_w
        self.screen_height = screen_h
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
        self.lgn_frame.place(x=400, y=150)

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

        if username in config["Users"]:
            if config["Users"][username] == password:
                messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                self.pack_forget() 
                self.main_page = MainPage(self)
                self.main_page.pack(fill=tk.BOTH, expand=True)

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


class MainPage(Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        label = Label(self, text="Welcome to the Main Page!")
        label.pack(pady=20)
   

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
        self.login_page = LoginPage(self, self.screen_width, self.screen_height)
        self.login_page.pack(fill=tk.BOTH, expand=True)



def page():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    page()
    