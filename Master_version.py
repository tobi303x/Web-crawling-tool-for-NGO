import os
import timeit
import redis
from redis import from_url
import tkinter as tk
import tkinter.messagebox
import customtkinter
from tkinter import ttk
from tkinter import scrolledtext
import threading
import subprocess
import csv
import customtkinter
import subprocess
import platform
from PIL import ImageTk,Image
from Crucial_Data_Files.Location_variables import *
from Crucial_Data_Files.Location_2_variables import *
from Crucial_Data_Files.Filters_Variables import *
from MultpleTerminalsExec import run_scrapy_finale 
import tiktoken
from Tokenization import tokenization
import openai 
from API_Request import Chat_GPT_API
import ast
from dotenv import load_dotenv
import os


load_dotenv()

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
redisClient = redis.from_url(os.getenv('REDIS_CLOUD_KEY'))
# Rozpiska Frameów
# Frame1 -> Ekran początkowy
# Frame2 -> Lokalizacja I
# Frame3 -> Wybór rodzaju konkursu
# Frame4 -> Lokalizacja II
# Frame5 -> Aktualne Konkursy Fundusze
# Frame6 -> Aktualne Konkursy Koniec Naboru
# Frame7 -> Aktualne Konkursy Temat I
# Frame8 -> Aktualne Konkursy Temat II
# Frame9 -> Aktualne Konkursy Odbiorcy I
# Frame10 -> Aktualne Konkursy Odbiorcy II
# Frame11 -> Okno wyboru Filtrów Wyniki Konkursów Fundusze
# Frame12 ->  Okno wyboru Filtrów Wyniki Konkursów Koniec Naboru
# Frame14 -> Okno wyboru Filtrów Wyniki Konkursów Temat I
# Frame15 -> Okno wyboru Filtrów Wyniki Konkursów Temat II
# Frame16 -> Okno wyboru Filtrów Archiwum Fundusze
# Frame17 -> Okno wyboru Filtrów Archiwum Temat II
# Frame18 -> Okno wyboru Filtrów Archiwum Temat II
# Frame19 -> Slider procent dofinansowania


# Fundusze -> Wybierz który z funduszy cię interesuje, możesz zaznaczyć dowolną ilość:

# Koniec Naboru -> Wybierz datę końca naboru szukanych ofert:

# Temat -> Wybierz który z tematów cię interesuje, możesz zaznaczyć dowolną ilość:

# Odbiorcy -> Wybierz do jakich odbiorców mają być kierowane oferty, możesz zaznaczyć dowolną ilość:


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Twoje NGO")
        self.geometry(f"{1600}x{900}")
        self.frames = {}
        self.current_frame = None
        self.create_frames()
        self.frames["frame2"].pack_forget()
        self.frames["frame3"].pack_forget()
        self.frames["frame4"].pack_forget()
        self.frames["frame5"].pack_forget()
        self.frames["frame6"].pack_forget()
        self.frames["frame7"].pack_forget()
        self.frames["frame8"].pack_forget()
        self.frames["frame9"].pack_forget()
        self.frames["frame10"].pack_forget()
        self.frames["frame11"].pack_forget()
        self.frames["frame12"].pack_forget()
        self.frames["frame14"].pack_forget()
        self.frames["frame15"].pack_forget()
        self.frames["frame16"].pack_forget()
        self.frames["frame17"].pack_forget()
        self.frames["frame18"].pack_forget()
        self.frames["frame19"].pack_forget()
        self.frames["frame20"].pack_forget()
        self.frames["frame21"].pack_forget()
        self.frames["frame22"].pack_forget()
        self.show_frame("frame1")
        self.configure(bg='black')

        
        
    def create_frames(self):
        #Funkcja generyczna łączenia funkcji
        def combine_funcs(*funcs):
            def combined_func(*args, **kwargs):
                for f in funcs:
                    f(*args, **kwargs)
            return combined_func
        
        def clear_data():
            folder_path = 'User_Link_Files.py'  
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if filename.endswith('.txt') and os.path.isfile(file_path):
                    # Delete the file
                    os.remove(file_path)
        #Tworzymy panel menu
        sidebar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        sidebar_frame.pack(side='left',fill="both", expand=False)

        user_data_frame = customtkinter.CTkFrame(sidebar_frame, corner_radius=10)
        user_data_frame.pack(side='top',fill="both", expand=False,ipadx=10,ipady=10,padx=10,pady=10)
        
        img1=ImageTk.PhotoImage(Image.open("Avatar.png"))
        logo_label = customtkinter.CTkLabel(user_data_frame, image=img1,text="", font=customtkinter.CTkFont(size=20, weight="bold"))
        logo_label.pack(ipadx=10,ipady=10,padx=10,pady=10)
        
        username =customtkinter.CTkLabel(user_data_frame,text="Twoja nazwa", font=customtkinter.CTkFont(size=20, weight="bold"))
        username.pack(ipadx=10,ipady=10,padx=10,pady=10)

        sidebar_button_1 = customtkinter.CTkButton(user_data_frame, text="Wyloguj", hover_color='#a42023')
        sidebar_button_1.pack(padx=10,pady=10)

        

        

        settings =customtkinter.CTkLabel(sidebar_frame,text="Ustawienia", font=customtkinter.CTkFont(size=18))
        settings.pack(ipadx=10,ipady=10,padx=10,pady=10)

        sidebar_button_2 = customtkinter.CTkButton(sidebar_frame, text="Twój Profil")
        sidebar_button_2.pack(padx=10,pady=10)
        
        sidebar_button_3 = customtkinter.CTkButton(sidebar_frame,text="Planer")
        sidebar_button_3.pack(padx=10,pady=10)
        
        appearance_mode_label = customtkinter.CTkLabel(sidebar_frame, text="Wybierz tryb programu:", anchor="w")
        appearance_mode_label.pack(padx=10,pady=10)
        
        radio_var = tkinter.IntVar(value=0)
        radio_button_1 = customtkinter.CTkRadioButton(sidebar_frame,text="Jasny", variable=radio_var, value=1,command=lambda:customtkinter.set_appearance_mode('Light'))
        radio_button_1.pack(pady=10, padx=20)
        radio_button_2 = customtkinter.CTkRadioButton(sidebar_frame,text="Ciemny", variable=radio_var, value=0,command=lambda:customtkinter.set_appearance_mode('Dark'))
        radio_button_2.pack(pady=(10,20), padx=20)
       
        scaling_label = customtkinter.CTkLabel(sidebar_frame, text="Skalowanie ekranu:", anchor="w")
        scaling_label.pack()
        
        scaling_optionemenu = customtkinter.CTkOptionMenu(sidebar_frame, values=["70%","80%","90%","100%", "110%", "120%", "130%"],
                                                               command=self.change_scaling_event)
        scaling_optionemenu.set("100%")
        
        scaling_optionemenu.pack()
        content_frame = tk.Frame(self)
        content_frame.pack(side='right',fill='both', expand=True)
        
    
        # Okno startowe
        frame1 = customtkinter.CTkFrame(content_frame)
        frame1.pack(fill="both", expand=True)

        frame1_header = customtkinter.CTkFrame(frame1,corner_radius=0)
        frame1_header.pack(side='top',fill="both", expand=False)
        frame1_title = customtkinter.CTkLabel(frame1_header, text="Witaj",font=customtkinter.CTkFont(size=45))
        frame1_title.pack(padx=20,pady=(40,30))

        frame1_content = customtkinter.CTkFrame(frame1,corner_radius=0)
        frame1_content.pack(fill="both", expand=True)
        frame1_con = customtkinter.CTkLabel(frame1_content, text="""
        Witaj w narzędziu Twoje NGO. Po lewej stronie ekranu znajdziesz informację o twoim profilu. W lewym dolnym 
        rogu możesz dostosować wygląd aplikacj w tym skalowanie zawartości oraz tryb ciemny. Możliwe ustawiania to 
        dane profilu gdzie możesz zmienić swoje informację dodyczące konta oraz wymagane zgody. Masz również 
        możliwość ustawienia planera tak aby otrzymywać powiadomienia o najnowszych konkursach.

        Na ekranie wyświetlane zostaną potrzebne informację do wyszukania interesujących cię konkursów.
        Postępuj zgodnie z wyświetlanymi instrukcjami.
        
        """,font=customtkinter.CTkFont(size=25))
        frame1_con.pack(pady=(0,20))
        

        frame1_nav = customtkinter.CTkFrame(frame1,corner_radius=0)
        frame1_nav.pack(side='bottom',fill="both", expand=False)


        frame1_nav_button_next = customtkinter.CTkButton(frame1_nav,height= 60,width=180,text="Zaczynajmy!", command=combine_funcs(lambda: self.show_frame("frame2"),clear_data),font=customtkinter.CTkFont(size=20))
        frame1_nav_button_next.pack(side='right',padx=70,pady=10)



        # Okno wyboru typu konkursów
        frame3 = customtkinter.CTkFrame(content_frame)
        

        frame3_header = customtkinter.CTkFrame(frame3,corner_radius=0)
        frame3_header.pack(side='top',fill="both", expand=False)
        frame3_title = customtkinter.CTkLabel(frame3_header, text="Jaki typ konkursów chciałbyś przeglądać?",font=customtkinter.CTkFont(size=45))
        frame3_title.pack(padx=20,pady=(40,30))

        frame3_content = customtkinter.CTkFrame(frame3,corner_radius=0)
        frame3_content.pack(fill="both", expand=True)
        frame3_con = customtkinter.CTkLabel(frame3_content, text="""Zaznacz odpowiedni:""",font=customtkinter.CTkFont(size=25))
        frame3_con.pack(pady=(0,20))
        frame3_radio_var = tkinter.IntVar(value=0)
        frame3_radio_button_1 = customtkinter.CTkRadioButton(frame3_content,text="Aktualne konkursy",width=420, variable=frame3_radio_var, value=0,font=customtkinter.CTkFont(size=25))
        frame3_radio_button_1.pack(pady=(100,30), padx=20)
        frame3_radio_button_2 = customtkinter.CTkRadioButton(frame3_content,text="Wyniki konkursów",width=420, variable=frame3_radio_var, value=1,font=customtkinter.CTkFont(size=25))
        frame3_radio_button_2.pack(pady=30, padx=20)
        frame3_radio_button_3 = customtkinter.CTkRadioButton(frame3_content,text="Archiwum konkursów",width=420, variable=frame3_radio_var, value=2,font=customtkinter.CTkFont(size=25))
        frame3_radio_button_3.pack(pady=(30,20), padx=20)

        # W zależności od wybranych zmiennych funkcja zwraca nam odpowinią nazwe sceny
        def check_variable_frame3():
            if frame3_radio_var.get() == 0:
                with open('User_Link_Files.py/Typ_Konkursu.txt', 'w') as file:
                    file.writelines("https://fundusze.ngo.pl/aktualne?page=1")
                return "frame5"
            if frame3_radio_var.get() == 1:
                with open('User_Link_Files.py/Typ_Konkursu.txt', 'w') as file:
                    file.writelines("https://fundusze.ngo.pl/wyniki?page=1")
                return "frame11"
            if frame3_radio_var.get() == 2:
                with open('User_Link_Files.py/Typ_Konkursu.txt', 'w') as file:
                    file.writelines("https://fundusze.ngo.pl/archiwum?page=1")
                return "frame16"
            
        def check_variable_frame3_bez():
            if frame3_radio_var.get() == 0:
                return "frame5"
            if frame3_radio_var.get() == 1:
                return "frame11"
            if frame3_radio_var.get() == 2:
                return "frame16"

        frame3_nav = customtkinter.CTkFrame(frame3,corner_radius=0)
        frame3_nav.pack(side='bottom',fill="both", expand=False)
        frame3_nav_button_prev = customtkinter.CTkButton(frame3_nav,height= 60,width=180,text="< Poprzedni krok", command=lambda: self.show_frame("frame2"),font=customtkinter.CTkFont(size=20))
        frame3_nav_button_prev.pack(side='left',padx=70,pady=10)

        frame3_nav_button_next = customtkinter.CTkButton(frame3_nav,height= 60,width=180,text="Następny krok >", command=lambda: self.show_frame(check_variable_frame3()),font=customtkinter.CTkFont(size=20))
        frame3_nav_button_next.pack(side='right',padx=70,pady=10)
        frame3.pack(fill="both", expand=True)



        # Okno wyboru Lokalizacji nr.1
        frame2 = customtkinter.CTkFrame(content_frame)
        frame2.pack(fill="both", expand=True)

        frame2_header = customtkinter.CTkFrame(frame2,corner_radius=0)
        frame2_header.pack(side='top',fill="both", expand=False)
        frame2_title = customtkinter.CTkLabel(frame2_header, text="Lokalizacja",font=customtkinter.CTkFont(size=45))
        frame2_title.pack(padx=20,pady=(40,30))

        frame2_content = customtkinter.CTkFrame(frame2,corner_radius=0)
        frame2_content.pack(fill="both", expand=True)
        frame2_con = customtkinter.CTkLabel(frame2_content, text="""
        Wybierz czy chciałbyś aby szukane przez ciebie konkursy były:
        """,font=customtkinter.CTkFont(size=25))
        frame2_con.pack(pady=(0,20))

        frame2_radio_var = tkinter.IntVar(value=0)
        frame2_radio_button_1 = customtkinter.CTkRadioButton(frame2_content,text="Wszystkie",width=420, variable=frame2_radio_var, value=0,font=customtkinter.CTkFont(size=25))
        frame2_radio_button_1.pack(pady=(100,30), padx=20)
        frame2_radio_button_2 = customtkinter.CTkRadioButton(frame2_content,text="Ogólnopolskie",width=420, variable=frame2_radio_var, value=1,font=customtkinter.CTkFont(size=25))
        frame2_radio_button_2.pack(pady=30, padx=20)
        frame2_radio_button_3 = customtkinter.CTkRadioButton(frame2_content,text="Lokalne",width=420, variable=frame2_radio_var, value=2,font=customtkinter.CTkFont(size=25))
        frame2_radio_button_3.pack(pady=(30,20), padx=20)
        
        def check_variable_frame2():
            if frame2_radio_var.get() == 0:
                with open('User_Link_Files.py/Typ_Lokalizacja.txt', 'w') as file:
                    file.writelines("")
                return "frame3"
            elif frame2_radio_var.get() == 1:
                with open('User_Link_Files.py/Typ_Lokalizacja.txt', 'w') as file:
                    file.writelines("&location=country")
                return "frame3"
            elif frame2_radio_var.get() == 2:
                return "frame4"

        frame2_nav = customtkinter.CTkFrame(frame2,corner_radius=0)
        frame2_nav.pack(side='bottom',fill="both", expand=False)


        frame2_nav_button_prev = customtkinter.CTkButton(frame2_nav,height= 60,width=180,text="< Poprzedni krok", command=lambda: self.show_frame("frame1"),font=customtkinter.CTkFont(size=20))
        frame2_nav_button_prev.pack(side='left',padx=70,pady=10)
        frame2_nav_button_next = customtkinter.CTkButton(frame2_nav,height= 60,width=180,text="Następny krok >", command=lambda: self.show_frame(check_variable_frame2()),font=customtkinter.CTkFont(size=20))
        frame2_nav_button_next.pack(side='right',padx=70,pady=10)
        frame2.pack(fill="both", expand=True)


        #Okno wyboru dokładnej lokalizacji
        frame4 = customtkinter.CTkFrame(content_frame)
        frame4.pack(fill="both", expand=True)

        frame4_header = customtkinter.CTkFrame(frame4,corner_radius=0)
        frame4_header.pack(side='top',fill="both", expand=False)
        frame4_title = customtkinter.CTkLabel(frame4_header, text="Lokalizacja Rejonu Polski",font=customtkinter.CTkFont(size=45), anchor="e")
        frame4_title.pack(padx=20,pady=(40,30))

        frame4_content = customtkinter.CTkFrame(frame4,corner_radius=0)
        frame4_content.pack(fill="both", expand=True)
        frame4_con = customtkinter.CTkLabel(frame4_content, text="""Wybierz czy chciałbyś aby szukane przez ciebie konkursy były na obszarze:""",font=customtkinter.CTkFont(size=25), anchor="e")
        frame4_con.pack(pady=(0,20))

        frame4_label1 = customtkinter.CTkLabel(frame4_content, text="""Województwo""",font=customtkinter.CTkFont(size=25), anchor="e")
        frame4_label1.pack(pady=(20,20))
        # create the first filter
        cat_var = tk.StringVar(frame4_content)
        cat_var.set(Województwa[0])  # set default option to 'Wszystkie'
        cat_menu = ttk.OptionMenu(frame4_content, cat_var, *Województwa)
        cat_menu.pack(ipadx=(25), ipady=(10))
        frame4_label2 = customtkinter.CTkLabel(frame4_content, text="""Powiat/miasto""",font=customtkinter.CTkFont(size=25), anchor="e")
        frame4_label2.pack(pady=(20,20))
        # create the second filter
        subcat_var = tk.StringVar(frame4_content)
        subcat_var.set('Wszystkie')  # set default option to 'Wszystkie'
        subcat_menu = ttk.OptionMenu(frame4_content, subcat_var, 'Wszystkie')
        subcat_menu.pack(ipadx=(25), ipady=(10))
        frame4_label3 = customtkinter.CTkLabel(frame4_content, text="""Powiat/Dzielnica""",font=customtkinter.CTkFont(size=25), anchor="e")
        frame4_label3.pack(pady=(20,20))
        # create the third filter
        color_var = tk.StringVar(frame4_content)
        color_var.set('Wszystkie')  # set default option to 'Wszystkie'
        color_menu = ttk.OptionMenu(frame4_content, color_var, 'Wszystkie')
        color_menu.pack(ipadx=(25), ipady=(10))
        



        # update the second and third filters options based on the first filter selection
        def update_Powiat_Miasto(*args):
            # reset Powiat_Miasto and Gmina_Dzielnica filters when category filter is changed
            subcat_var.set('Wszystkie')
            color_var.set('Wszystkie')
            
            if cat_var.get() == 'Wszystkie':
                subcat_menu['menu'].delete(0, 'end')
            else:
                subcat_menu['menu'].delete(0, 'end')
                for subcat in Powiat_Miasto[cat_var.get()]:
                    subcat_menu['menu'].add_command(label=subcat, command=tk._setit(subcat_var, subcat))

        def update_Gmina_Dzielnica(*args):
            # reset Gmina_Dzielnica filter when subcategory filter is changed
            color_var.set('Wszystkie')
            
            if subcat_var.get() == 'Wszystkie':
                color_menu['menu'].delete(0, 'end')
            else:
                color_menu['menu'].delete(0, 'end')
                for color in Gmina_Dzielnica[subcat_var.get()]:
                    color_menu['menu'].add_command(label=color, command=tk._setit(color_var, color))

        # link the update functions to the filters
        cat_var.trace('w', update_Powiat_Miasto)
        subcat_var.trace('w', update_Gmina_Dzielnica)


        frame4_nav = customtkinter.CTkFrame(frame4,corner_radius=0)
        frame4_nav.pack(side='bottom',fill="both", expand=False)


        frame4_nav_button_prev = customtkinter.CTkButton(frame4_nav,height= 60,width=180,text="< Poprzedni krok", command=lambda: self.show_frame("frame2"),font=customtkinter.CTkFont(size=20))
        frame4_nav_button_prev.pack(side='left',padx=70,pady=10)

        #Funkcja zapisująca filtry dokładnej lokalizacji
        def save_filters_location2():
            cat_val = cat_var.get()
            subcat_val = subcat_var.get()
            color_val = color_var.get()
            woj_link = Wojewodztwa_Filter_Dict[cat_val]
            pow_link = Powiat_Miasto_Filter_Dict[subcat_val]
            gmi_link = Gmina_Dzielnica_Dict[color_val] 
            filter_str = f'&terc={woj_link}{pow_link}{gmi_link}'
            with open('User_Link_Files.py/Lokalizacja_Dokladna.txt', 'w') as file:
                file.writelines(filter_str)

               
        frame4_nav_button_next = customtkinter.CTkButton(frame4_nav,height= 60,width=180,text="Następny krok >", command=combine_funcs(lambda: self.show_frame("frame3"),save_filters_location2),font=customtkinter.CTkFont(size=20))
        frame4_nav_button_next.pack(side='right',padx=70,pady=10)
        frame4.pack(fill="both", expand=True)

        cat_menu.tk.call("source", "Azure-ttk-theme/azure.tcl")
        cat_menu.tk.call("set_theme", "dark")      

        # Okno wyboru Filtrów Aktualne Konkursy Fundusze
        frame5 = customtkinter.CTkFrame(content_frame)
        frame5.pack(fill="both", expand=True)



        frame5_header = customtkinter.CTkFrame(frame5,corner_radius=0)
        frame5_header.pack(side='top',fill="both", expand=False)
        frame5_title = customtkinter.CTkLabel(frame5_header, text="Aktualne Konkursy, Fundusze",font=customtkinter.CTkFont(size=45))
        frame5_title.pack(padx=20,pady=(40,30))

        frame5_content = customtkinter.CTkFrame(frame5,corner_radius=0)
        frame5_content.pack(fill="both", expand=True)
        frame5_con = customtkinter.CTkLabel(frame5_content, text="""Wybierz który z funduszy cię interesuje, możesz zaznaczyć dowolną ilość:""",font=customtkinter.CTkFont(size=25))
        frame5_con.pack(padx=20,pady=(0,30))

        def show_checked():
            checked_boxes = []

            if frame5_checkbox1_var.get():
                checked_boxes.append("&cats%5B630%5D=631")
            if frame5_checkbox2_var.get():
                checked_boxes.append("&cats%5B630%5D=632")
            if frame5_checkbox3_var.get():
                checked_boxes.append("&cats%5B630%5D=633")
            if frame5_checkbox4_var.get():
                checked_boxes.append("&cats%5B630%5D=634")
            if frame5_checkbox5_var.get():
                checked_boxes.append("&cats%5B630%5D=635")
            if frame5_checkbox6_var.get():
                checked_boxes.append("&cats%5B630%5D=636")
            if frame5_checkbox7_var.get():
                checked_boxes.append("&cats%5B630%5D=637")
            if frame5_checkbox8_var.get():
                checked_boxes.append("&cats%5B630%5D=638")
            if frame5_checkbox9_var.get():
                checked_boxes.append("&cats%5B630%5D=639")
            if frame5_checkbox10_var.get():
                checked_boxes.append("&cats%5B630%5D=640")
            if frame5_checkbox11_var.get():
                checked_boxes.append("&cats%5B630%5D=3590")
            if frame5_checkbox12_var.get():
                checked_boxes.append("&cats%5B630%5D=642")
            if checked_boxes:
                with open('User_Link_Files.py/AK_Fundusze.txt', 'w') as file:
                    file.writelines(checked_boxes)
            else:
                with open('User_Link_Files.py/AK_Fundusze.txt', 'w') as file:
                    file.writelines("")
        frame5_checkbox1_var = tk.BooleanVar()
        frame5_checkbox2_var = tk.BooleanVar()
        frame5_checkbox3_var = tk.BooleanVar()
        frame5_checkbox4_var = tk.BooleanVar()
        frame5_checkbox5_var = tk.BooleanVar()
        frame5_checkbox6_var = tk.BooleanVar()
        frame5_checkbox7_var = tk.BooleanVar()
        frame5_checkbox8_var = tk.BooleanVar()
        frame5_checkbox9_var = tk.BooleanVar()
        frame5_checkbox10_var = tk.BooleanVar()
        frame5_checkbox11_var = tk.BooleanVar()
        frame5_checkbox12_var = tk.BooleanVar()

        frame5_checkbox_1 = customtkinter.CTkCheckBox(frame5_content, text="Centralny",width=420,font=customtkinter.CTkFont(size=20), variable=frame5_checkbox1_var)
        frame5_checkbox_1.pack(pady=10, padx=20)
        frame5_checkbox_2 = customtkinter.CTkCheckBox(frame5_content, text="Dzielnicowy",width=420,font=customtkinter.CTkFont(size=20), variable=frame5_checkbox2_var)
        frame5_checkbox_2.pack( pady=10, padx=20)
        frame5_checkbox_3 = customtkinter.CTkCheckBox(frame5_content, text="EOG, CH",width=420,font=customtkinter.CTkFont(size=20), variable=frame5_checkbox3_var)
        frame5_checkbox_3.pack(pady=10, padx=20)
        frame5_checkbox_4 = customtkinter.CTkCheckBox(frame5_content, text="Marszałkowski",width=420,font=customtkinter.CTkFont(size=20), variable=frame5_checkbox4_var)
        frame5_checkbox_4.pack(pady=10, padx=20)
        frame5_checkbox_5 = customtkinter.CTkCheckBox(frame5_content, text="Miejsko-gminny",width=420,font=customtkinter.CTkFont(size=20), variable=frame5_checkbox5_var)
        frame5_checkbox_5.pack( pady=10, padx=20)
        frame5_checkbox_6 = customtkinter.CTkCheckBox(frame5_content, text="Powiatowy",width=420,font=customtkinter.CTkFont(size=20), variable=frame5_checkbox6_var)
        frame5_checkbox_6.pack(pady=10, padx=20)
        frame5_checkbox_7 = customtkinter.CTkCheckBox(frame5_content, text="Prywatny",width=420,font=customtkinter.CTkFont(size=20), variable=frame5_checkbox7_var)
        frame5_checkbox_7.pack(pady=10, padx=20)
        frame5_checkbox_8 = customtkinter.CTkCheckBox(frame5_content, text="Strukturalny",width=420,font=customtkinter.CTkFont(size=20), variable=frame5_checkbox8_var)
        frame5_checkbox_8.pack(pady=10, padx=20)
        frame5_checkbox_9 = customtkinter.CTkCheckBox(frame5_content, text="Stypendialny",width=420,font=customtkinter.CTkFont(size=20), variable=frame5_checkbox9_var)
        frame5_checkbox_9.pack(pady=10, padx=20)
        frame5_checkbox_10 = customtkinter.CTkCheckBox(frame5_content, text="Unijny",width=420,font=customtkinter.CTkFont(size=20), variable=frame5_checkbox10_var)
        frame5_checkbox_10.pack(pady=10, padx=20)
        frame5_checkbox_11 = customtkinter.CTkCheckBox(frame5_content, text="Wojewódzki",width=420,font=customtkinter.CTkFont(size=20), variable=frame5_checkbox11_var)
        frame5_checkbox_11.pack(pady=10, padx=20)
        frame5_checkbox_12 = customtkinter.CTkCheckBox(frame5_content, text="Zagraniczny",width=420,font=customtkinter.CTkFont(size=20), variable=frame5_checkbox12_var)
        frame5_checkbox_12.pack(pady=10, padx=20)
             

        frame5_nav = customtkinter.CTkFrame(frame5,corner_radius=0)
        frame5_nav.pack(side='bottom',fill="both", expand=False)


        frame5_nav_button_prev = customtkinter.CTkButton(frame5_nav,height= 60,width=180,text="< Poprzedni krok", command=lambda: self.show_frame("frame3"),font=customtkinter.CTkFont(size=20))
        frame5_nav_button_prev.pack(side='left',padx=70,pady=10)

        frame5_nav_button_next = customtkinter.CTkButton(frame5_nav,height= 60,width=180,text="Następny krok >", command=combine_funcs(lambda: self.show_frame("frame6"),show_checked),font=customtkinter.CTkFont(size=20))
        frame5_nav_button_next.pack(side='right',padx=70,pady=10)
        frame5.pack(fill="both", expand=True)




        # Okno wyboru Filtrów Aktualne Konkursy Koniec Naboru 
        frame6 = customtkinter.CTkFrame(content_frame)
        frame6.pack(fill="both", expand=True)



        frame6_header = customtkinter.CTkFrame(frame6,corner_radius=0)
        frame6_header.pack(side='top',fill="both", expand=False)
        frame6_title = customtkinter.CTkLabel(frame6_header, text="Aktualne Konkursy, Koniec Naboru",font=customtkinter.CTkFont(size=45))
        frame6_title.pack(padx=20,pady=(40,30))

        frame6_content = customtkinter.CTkFrame(frame6,corner_radius=0)
        frame6_content.pack(fill="both", expand=True)
        frame6_con = customtkinter.CTkLabel(frame6_content, text="""Wybierz datę końca naboru szukanych ofert:""",font=customtkinter.CTkFont(size=25))
        frame6_con.pack(padx=20,pady=(0,30))

        def show_checked2():
            checked_boxes2 = []
            if frame6_checkbox1_var.get():
                checked_boxes2.append('&when=ever')
            if frame6_checkbox2_var.get():
                checked_boxes2.append('&when=week')
            if frame6_checkbox3_var.get():
                checked_boxes2.append('&when=month')
            if frame6_checkbox4_var.get():
                checked_boxes2.append('&when=next_month')
            if frame6_checkbox5_var.get():
                checked_boxes2.append('&when=year')
            if frame6_checkbox6_var.get():
                checked_boxes2.append('&when=next_year')
            
            if checked_boxes2:
                with open('User_Link_Files.py/AK_Koniec_Naboru.txt', 'w') as file:
                    file.writelines(checked_boxes2)
            else:
                with open('User_Link_Files.py/AK_Koniec_Naboru.txt', 'w') as file:
                    file.writelines("")

        frame6_checkbox1_var = tk.BooleanVar()
        frame6_checkbox2_var = tk.BooleanVar()
        frame6_checkbox3_var = tk.BooleanVar()
        frame6_checkbox4_var = tk.BooleanVar()
        frame6_checkbox5_var = tk.BooleanVar()
        frame6_checkbox6_var = tk.BooleanVar()
        frame6_checkbox7_var = tk.BooleanVar()
        frame6_checkbox8_var = tk.BooleanVar()
        frame6_checkbox9_var = tk.BooleanVar()
        frame6_checkbox10_var = tk.BooleanVar()
        frame6_checkbox11_var = tk.BooleanVar()
        frame6_checkbox12_var = tk.BooleanVar()

        frame6_checkbox_1 = customtkinter.CTkCheckBox(frame6_content, text="Kiedykolwiek", width=420, font=customtkinter.CTkFont(size=20), variable=frame6_checkbox1_var)
        frame6_checkbox_1.pack(pady=10, padx=20)
        frame6_checkbox_2 = customtkinter.CTkCheckBox(frame6_content, text="W tym tygodniu", width=420, font=customtkinter.CTkFont(size=20), variable=frame6_checkbox2_var)
        frame6_checkbox_2.pack(pady=10, padx=20)
        frame6_checkbox_3 = customtkinter.CTkCheckBox(frame6_content, text="W tym miesiącu", width=420, font=customtkinter.CTkFont(size=20), variable=frame6_checkbox3_var)
        frame6_checkbox_3.pack(pady=10, padx=20)
        frame6_checkbox_4 = customtkinter.CTkCheckBox(frame6_content, text="W następnym miesiącu", width=420, font=customtkinter.CTkFont(size=20), variable=frame6_checkbox4_var)
        frame6_checkbox_4.pack(pady=10, padx=20)
        frame6_checkbox_5 = customtkinter.CTkCheckBox(frame6_content, text="W tym roku", width=420, font=customtkinter.CTkFont(size=20), variable=frame6_checkbox5_var)
        frame6_checkbox_5.pack(pady=10, padx=20)
        frame6_checkbox_6 = customtkinter.CTkCheckBox(frame6_content, text="W przyszłym roku", width=420, font=customtkinter.CTkFont(size=20), variable=frame6_checkbox6_var)
        frame6_checkbox_6.pack(pady=10, padx=20)

             

        frame6_nav = customtkinter.CTkFrame(frame6,corner_radius=0)
        frame6_nav.pack(side='bottom',fill="both", expand=False)


        frame6_nav_button_prev = customtkinter.CTkButton(frame6_nav,height= 60,width=180,text="< Poprzedni krok", command=lambda: self.show_frame("frame5"),font=customtkinter.CTkFont(size=20))
        frame6_nav_button_prev.pack(side='left',padx=70,pady=10)

        frame6_nav_button_next = customtkinter.CTkButton(frame6_nav,height= 60,width=180,text="Następny krok >", command=combine_funcs(lambda: self.show_frame("frame7"),show_checked2),font=customtkinter.CTkFont(size=20))
        frame6_nav_button_next.pack(side='right',padx=70,pady=10)
        frame6.pack(fill="both", expand=True)




        # Okno wyboru Filtrów Aktualne Konkursy Temat 1
        frame7 = customtkinter.CTkFrame(content_frame)
        frame7.pack(fill="both", expand=True)

        frame7_header = customtkinter.CTkFrame(frame7,corner_radius=0)
        frame7_header.pack(side='top',fill="both", expand=False)
        frame7_title = customtkinter.CTkLabel(frame7_header, text="Aktualne Konkursy, Temat I",font=customtkinter.CTkFont(size=45))
        frame7_title.pack(padx=20,pady=(40,30))

        frame7_content = customtkinter.CTkFrame(frame7,corner_radius=0)
        frame7_content.pack(fill="both", expand=True)
        frame7_con = customtkinter.CTkLabel(frame7_content, text="""Wybierz który z tematów cię interesuje, możesz zaznaczyć dowolną ilość:""",font=customtkinter.CTkFont(size=25))
        frame7_con.pack(padx=20,pady=(0,30))

        def show_checked3():
            checked_boxes3 = []
            if frame7_checkbox1_var.get():
                checked_boxes3.append("&cats%5B464%5D=4286")
            if frame7_checkbox2_var.get():
                checked_boxes3.append("&cats%5B464%5D=514")
            if frame7_checkbox3_var.get():
                checked_boxes3.append("&cats%5B464%5D=513")
            if frame7_checkbox4_var.get():
                checked_boxes3.append("&cats%5B464%5D=515")
            if frame7_checkbox5_var.get():
                checked_boxes3.append("&cats%5B464%5D=512")
            if frame7_checkbox6_var.get():
                checked_boxes3.append("&cats%5B464%5D=504")
            if frame7_checkbox7_var.get():
                checked_boxes3.append("&cats%5B464%5D=501")
            if frame7_checkbox8_var.get():
                checked_boxes3.append("&cats%5B464%5D=511")
            if frame7_checkbox9_var.get():
                checked_boxes3.append("&cats%5B464%5D=2895")
            if frame7_checkbox10_var.get():
                checked_boxes3.append("&cats%5B464%5D=516")
            if frame7_checkbox11_var.get():
                checked_boxes3.append("&cats%5B464%5D=490")
            if frame7_checkbox12_var.get():
                checked_boxes3.append("&cats%5B464%5D=491")
            if frame7_checkbox13_var.get():
                checked_boxes3.append("&cats%5B464%5D=507")
            if frame7_checkbox14_var.get():
                checked_boxes3.append("&cats%5B464%5D=492")
            if frame7_checkbox15_var.get():
                checked_boxes3.append("&cats%5B464%5D=509")
            if checked_boxes3:
                with open('User_Link_Files.py/AK_Temat1.txt', 'w') as file:
                    file.writelines(checked_boxes3)
            else:
                with open('User_Link_Files.py/AK_Temat1.txt', 'w') as file:
                    file.writelines("")
        frame7_checkbox1_var = tk.BooleanVar()
        frame7_checkbox2_var = tk.BooleanVar()
        frame7_checkbox3_var = tk.BooleanVar()
        frame7_checkbox4_var = tk.BooleanVar()
        frame7_checkbox5_var = tk.BooleanVar()
        frame7_checkbox6_var = tk.BooleanVar()
        frame7_checkbox7_var = tk.BooleanVar()
        frame7_checkbox8_var = tk.BooleanVar()
        frame7_checkbox9_var = tk.BooleanVar()
        frame7_checkbox10_var = tk.BooleanVar()
        frame7_checkbox11_var = tk.BooleanVar()
        frame7_checkbox12_var = tk.BooleanVar()
        frame7_checkbox13_var = tk.BooleanVar()
        frame7_checkbox14_var = tk.BooleanVar()
        frame7_checkbox15_var = tk.BooleanVar()



        frame7_checkbox_1 = customtkinter.CTkCheckBox(frame7_content, text="Ukraina", width=420, font=customtkinter.CTkFont(size=20), variable=frame7_checkbox1_var)
        frame7_checkbox_1.pack(pady=10, padx=20)
        frame7_checkbox_2 = customtkinter.CTkCheckBox(frame7_content, text="Zarządzanie, księgowość", width=420, font=customtkinter.CTkFont(size=20), variable=frame7_checkbox2_var)
        frame7_checkbox_2.pack(pady=10, padx=20)
        frame7_checkbox_3 = customtkinter.CTkCheckBox(frame7_content, text="Finansowanie", width=420, font=customtkinter.CTkFont(size=20), variable=frame7_checkbox3_var)
        frame7_checkbox_3.pack(pady=10, padx=20)
        frame7_checkbox_4 = customtkinter.CTkCheckBox(frame7_content, text="Prawo i obowiązki", width=420, font=customtkinter.CTkFont(size=20), variable=frame7_checkbox4_var)
        frame7_checkbox_4.pack(pady=10, padx=20)
        frame7_checkbox_5 = customtkinter.CTkCheckBox(frame7_content, text="Pożytek publiczny i (1%) 1,5%", width=420, font=customtkinter.CTkFont(size=20), variable=frame7_checkbox5_var)
        frame7_checkbox_5.pack(pady=10, padx=20)
        frame7_checkbox_6 = customtkinter.CTkCheckBox(frame7_content, text="Promocja, media społecznościowe", width=420, font=customtkinter.CTkFont(size=20), variable=frame7_checkbox6_var)
        frame7_checkbox_6.pack(pady=10, padx=20)
        frame7_checkbox_7 = customtkinter.CTkCheckBox(frame7_content, text="Technologie", width=420, font=customtkinter.CTkFont(size=20), variable=frame7_checkbox7_var)
        frame7_checkbox_7.pack(pady=10, padx=20)
        frame7_checkbox_8 = customtkinter.CTkCheckBox(frame7_content, text="Wzmacnianie III sektora", width=420, font=customtkinter.CTkFont(size=20), variable=frame7_checkbox8_var)
        frame7_checkbox_8.pack(pady=10, padx=20)
        frame7_checkbox_9 = customtkinter.CTkCheckBox(frame7_content, text="Rozwój zawodowy i osobisty", width=420, font=customtkinter.CTkFont(size=20), variable=frame7_checkbox9_var)
        frame7_checkbox_9.pack(pady=10, padx=20)
        frame7_checkbox_11 = customtkinter.CTkCheckBox(frame7_content, text="Aktywność obywatelska", width=420, font=customtkinter.CTkFont(size=20), variable=frame7_checkbox11_var)
        frame7_checkbox_11.pack(pady=10, padx=20)
        frame7_checkbox_12 = customtkinter.CTkCheckBox(frame7_content, text="Prawa człowieka", width=420, font=customtkinter.CTkFont(size=20), variable=frame7_checkbox12_var)
        frame7_checkbox_12.pack(pady=10, padx=20)
        frame7_checkbox_13 = customtkinter.CTkCheckBox(frame7_content, text="Działalność lokalna", width=420, font=customtkinter.CTkFont(size=20), variable=frame7_checkbox13_var)
        frame7_checkbox_13.pack(pady=10, padx=20)
        frame7_checkbox_14 = customtkinter.CTkCheckBox(frame7_content, text="Współpraca z administracją", width=420, font=customtkinter.CTkFont(size=20), variable=frame7_checkbox14_var)
        frame7_checkbox_14.pack(pady=10, padx=20)
        frame7_checkbox_15 = customtkinter.CTkCheckBox(frame7_content, text="Wolontariat", width=420, font=customtkinter.CTkFont(size=20), variable=frame7_checkbox15_var)
        frame7_checkbox_15.pack(pady=10, padx=20)
        
             

        frame7_nav = customtkinter.CTkFrame(frame7,corner_radius=0)
        frame7_nav.pack(side='bottom',fill="both", expand=False)


        frame7_nav_button_prev = customtkinter.CTkButton(frame7_nav,height= 60,width=180,text="< Poprzedni krok", command=lambda: self.show_frame("frame6"),font=customtkinter.CTkFont(size=20))
        frame7_nav_button_prev.pack(side='left',padx=70,pady=10)

        frame7_nav_button_next = customtkinter.CTkButton(frame7_nav,height= 60,width=180,text="Następny krok >", command=combine_funcs(lambda: self.show_frame("frame8"),show_checked3),font=customtkinter.CTkFont(size=20))
        frame7_nav_button_next.pack(side='right',padx=70,pady=10)
        frame7.pack(fill="both", expand=True)



        # Okno wyboru Filtrów Aktualne Konkursy Temat 2
        frame8 = customtkinter.CTkFrame(content_frame)
        frame8.pack(fill="both", expand=True)



        frame8_header = customtkinter.CTkFrame(frame8,corner_radius=0)
        frame8_header.pack(side='top',fill="both", expand=False)
        frame8_title = customtkinter.CTkLabel(frame8_header, text="Aktualne Konkursy, Temat II",font=customtkinter.CTkFont(size=45))
        frame8_title.pack(padx=20,pady=(40,30))

        frame8_content = customtkinter.CTkFrame(frame8,corner_radius=0)
        frame8_content.pack(fill="both", expand=True)
        frame8_con = customtkinter.CTkLabel(frame8_content, text="""Wybierz który z tematów cię interesuje, możesz zaznaczyć dowolną ilość:""",font=customtkinter.CTkFont(size=25))
        frame8_con.pack(padx=20,pady=(0,30))

        def show_checked4():
            checked_boxes4 = []
            if frame8_checkbox16_var.get():
                checked_boxes4.append("&cats%5B464%5D=493")
            if frame8_checkbox17_var.get():
                checked_boxes4.append("&cats%5B464%5D=510")
            if frame8_checkbox18_var.get():
                checked_boxes4.append("&cats%5B464%5D=498")
            if frame8_checkbox19_var.get():
                checked_boxes4.append("&cats%5B464%5D=494")
            if frame8_checkbox20_var.get():
                checked_boxes4.append("&cats%5B464%5D=495")
            if frame8_checkbox21_var.get():
                checked_boxes4.append("&cats%5B464%5D=496")
            if frame8_checkbox22_var.get():
                checked_boxes4.append("&cats%5B464%5D=497")
            if frame8_checkbox23_var.get():
                checked_boxes4.append("&cats%5B464%5D=499")
            if frame8_checkbox24_var.get():
                checked_boxes4.append("&cats%5B464%5D=506")
            if frame8_checkbox25_var.get():
                checked_boxes4.append("&cats%5B464%5D=500")
            if frame8_checkbox26_var.get():
                checked_boxes4.append("&cats%5B464%5D=505")
            if frame8_checkbox27_var.get():
                checked_boxes4.append("&cats%5B464%5D=502")
            if frame8_checkbox28_var.get():
                checked_boxes4.append("&cats%5B464%5D=503")
            if frame8_checkbox29_var.get():
                checked_boxes4.append("&cats%5B464%5D=508")           
            if checked_boxes4:
                with open('User_Link_Files.py/AK_Temat2.txt', 'w') as file:
                    file.writelines(checked_boxes4)
            else:
                with open('User_Link_Files.py/AK_Temat2.txt', 'w') as file:
                    file.writelines("")
        frame8_checkbox16_var = tk.BooleanVar()
        frame8_checkbox17_var = tk.BooleanVar()
        frame8_checkbox18_var = tk.BooleanVar()
        frame8_checkbox19_var = tk.BooleanVar()
        frame8_checkbox20_var = tk.BooleanVar()
        frame8_checkbox21_var = tk.BooleanVar()
        frame8_checkbox22_var = tk.BooleanVar()
        frame8_checkbox23_var = tk.BooleanVar()
        frame8_checkbox24_var = tk.BooleanVar()
        frame8_checkbox25_var = tk.BooleanVar()
        frame8_checkbox26_var = tk.BooleanVar()
        frame8_checkbox27_var = tk.BooleanVar()
        frame8_checkbox28_var = tk.BooleanVar()
        frame8_checkbox29_var = tk.BooleanVar()

        frame8_checkbox_16 = customtkinter.CTkCheckBox(frame8_content, text="Dobroczynność, filantropia", width=420, font=customtkinter.CTkFont(size=20), variable=frame8_checkbox16_var)
        frame8_checkbox_16.pack(pady=10, padx=20)
        frame8_checkbox_17 = customtkinter.CTkCheckBox(frame8_content, text="Współpraca z biznesem, CSR", width=420, font=customtkinter.CTkFont(size=20), variable=frame8_checkbox17_var)
        frame8_checkbox_17.pack(pady=10, padx=20)
        frame8_checkbox_18 = customtkinter.CTkCheckBox(frame8_content, text="Ekonomia, rynek pracy", width=420, font=customtkinter.CTkFont(size=20), variable=frame8_checkbox18_var)
        frame8_checkbox_18.pack(pady=10, padx=20)
        frame8_checkbox_19 = customtkinter.CTkCheckBox(frame8_content, text="Działalność międzynarodowa", width=420, font=customtkinter.CTkFont(size=20), variable=frame8_checkbox19_var)
        frame8_checkbox_19.pack(pady=10, padx=20)
        frame8_checkbox_20 = customtkinter.CTkCheckBox(frame8_content, text="Unia Europejska", width=420, font=customtkinter.CTkFont(size=20), variable=frame8_checkbox20_var)
        frame8_checkbox_20.pack(pady=10, padx=20)
        frame8_checkbox_21 = customtkinter.CTkCheckBox(frame8_content, text="Edukacja i wychowanie", width=420, font=customtkinter.CTkFont(size=20), variable=frame8_checkbox21_var)
        frame8_checkbox_21.pack(pady=10, padx=20)
        frame8_checkbox_22 = customtkinter.CTkCheckBox(frame8_content, text="Ekologia, zwierzęta", width=420, font=customtkinter.CTkFont(size=20), variable=frame8_checkbox22_var)
        frame8_checkbox_22.pack(pady=10, padx=20)
        frame8_checkbox_23 = customtkinter.CTkCheckBox(frame8_content, text="Kultura i tradycja", width=420, font=customtkinter.CTkFont(size=20), variable=frame8_checkbox23_var)
        frame8_checkbox_23.pack(pady=10, padx=20)
        frame8_checkbox_24 = customtkinter.CTkCheckBox(frame8_content, text="Religia", width=420, font=customtkinter.CTkFont(size=20), variable=frame8_checkbox24_var)
        frame8_checkbox_24.pack(pady=10, padx=20)
        frame8_checkbox_25 = customtkinter.CTkCheckBox(frame8_content, text="Nauka i technika", width=420, font=customtkinter.CTkFont(size=20), variable=frame8_checkbox25_var)
        frame8_checkbox_25.pack(pady=10, padx=20)
        frame8_checkbox_26 = customtkinter.CTkCheckBox(frame8_content, text="Polityka społeczna", width=420, font=customtkinter.CTkFont(size=20), variable=frame8_checkbox26_var)
        frame8_checkbox_26.pack(pady=10, padx=20)
        frame8_checkbox_27 = customtkinter.CTkCheckBox(frame8_content, text="Ochrona zdrowia", width=420, font=customtkinter.CTkFont(size=20), variable=frame8_checkbox27_var)
        frame8_checkbox_27.pack(pady=10, padx=20)
        frame8_checkbox_28 = customtkinter.CTkCheckBox(frame8_content, text="Bezpieczeństwo", width=420, font=customtkinter.CTkFont(size=20), variable=frame8_checkbox28_var)
        frame8_checkbox_28.pack(pady=10, padx=20)
        frame8_checkbox_29 = customtkinter.CTkCheckBox(frame8_content, text="Sport, czas wolny", width=420, font=customtkinter.CTkFont(size=20), variable=frame8_checkbox29_var)
        frame8_checkbox_29.pack(pady=10, padx=20)
             

        frame8_nav = customtkinter.CTkFrame(frame8,corner_radius=0)
        frame8_nav.pack(side='bottom',fill="both", expand=False)


        frame8_nav_button_prev = customtkinter.CTkButton(frame8_nav,height= 60,width=180,text="< Poprzedni krok", command=lambda: self.show_frame("frame8"),font=customtkinter.CTkFont(size=20))
        frame8_nav_button_prev.pack(side='left',padx=70,pady=10)

        frame8_nav_button_next = customtkinter.CTkButton(frame8_nav,height= 60,width=180,text="Następny krok >", command=combine_funcs(lambda: self.show_frame("frame9"),show_checked4),font=customtkinter.CTkFont(size=20))
        frame8_nav_button_next.pack(side='right',padx=70,pady=10)
        frame8.pack(fill="both", expand=True)

        # Okno wyboru Filtrów Aktualne Konkursy Odbiorcy 1
        frame9 = customtkinter.CTkFrame(content_frame)
        frame9.pack(fill="both", expand=True)

        frame9_header = customtkinter.CTkFrame(frame9,corner_radius=0)
        frame9_header.pack(side='top',fill="both", expand=False)
        frame9_title = customtkinter.CTkLabel(frame9_header, text="Aktualne Konkursy, Odbiorcy I",font=customtkinter.CTkFont(size=45))
        frame9_title.pack(padx=20,pady=(40,30))

        frame9_content = customtkinter.CTkFrame(frame9,corner_radius=0)
        frame9_content.pack(fill="both", expand=True)
        frame9_con = customtkinter.CTkLabel(frame9_content, text="""Wybierz do jakich odbiorców mają być kierowane oferty, możesz zaznaczyć dowolną ilość:""",font=customtkinter.CTkFont(size=25))
        frame9_con.pack(padx=20,pady=(0,30))

        def show_checked5():
            checked_boxes5 = []
            if frame9_checkbox1_var.get():
                checked_boxes5.append("&cats%5B626%5D=629")
            if frame9_checkbox2_var.get():
                checked_boxes5.append("&cats%5B626%5D=2197")
            if frame9_checkbox3_var.get():
                checked_boxes5.append("&cats%5B626%5D=2198")
            if frame9_checkbox4_var.get():
                checked_boxes5.append("&cats%5B626%5D=2199")
            if frame9_checkbox5_var.get():
                checked_boxes5.append("&cats%5B626%5D=2200")
            if frame9_checkbox6_var.get():
                checked_boxes5.append("&cats%5B626%5D=2201")
            if frame9_checkbox7_var.get():
                checked_boxes5.append("&cats%5B626%5D=2202")
            if frame9_checkbox8_var.get():
                checked_boxes5.append("&cats%5B626%5D=2203")
            if frame9_checkbox9_var.get():
                checked_boxes5.append("&cats%5B626%5D=2204")
            if checked_boxes5:
                with open('User_Link_Files.py/AK_Odbiorcy1.txt', 'w') as file:
                    file.writelines(checked_boxes5)
            else:
                with open('User_Link_Files.py/AK_Odbiorcy1.txt', 'w') as file:
                    file.writelines("")


        frame9_checkbox1_var = tk.BooleanVar()
        frame9_checkbox2_var = tk.BooleanVar()
        frame9_checkbox3_var = tk.BooleanVar()
        frame9_checkbox4_var = tk.BooleanVar()
        frame9_checkbox5_var = tk.BooleanVar()
        frame9_checkbox6_var = tk.BooleanVar()
        frame9_checkbox7_var = tk.BooleanVar()
        frame9_checkbox8_var = tk.BooleanVar()
        frame9_checkbox9_var = tk.BooleanVar()

        frame9_checkbox_1 = customtkinter.CTkCheckBox(frame9_content, text="Chorzy", width=420, font=customtkinter.CTkFont(size=20), variable=frame9_checkbox1_var)
        frame9_checkbox_1.pack(pady=10, padx=20)
        frame9_checkbox_2 = customtkinter.CTkCheckBox(frame9_content, text="Cudzoziemcy, migranci", width=420, font=customtkinter.CTkFont(size=20), variable=frame9_checkbox2_var)
        frame9_checkbox_2.pack(pady=10, padx=20)
        frame9_checkbox_3 = customtkinter.CTkCheckBox(frame9_content, text="Dorośli", width=420, font=customtkinter.CTkFont(size=20), variable=frame9_checkbox3_var)
        frame9_checkbox_3.pack(pady=10, padx=20)
        frame9_checkbox_4 = customtkinter.CTkCheckBox(frame9_content, text="Dzieci", width=420, font=customtkinter.CTkFont(size=20), variable=frame9_checkbox4_var)
        frame9_checkbox_4.pack(pady=10, padx=20)
        frame9_checkbox_5 = customtkinter.CTkCheckBox(frame9_content, text="Kobiety", width=420, font=customtkinter.CTkFont(size=20), variable=frame9_checkbox5_var)
        frame9_checkbox_5.pack(pady=10, padx=20)
        frame9_checkbox_6 = customtkinter.CTkCheckBox(frame9_content, text="Konsumenci", width=420, font=customtkinter.CTkFont(size=20), variable=frame9_checkbox6_var)
        frame9_checkbox_6.pack(pady=10, padx=20)
        frame9_checkbox_7 = customtkinter.CTkCheckBox(frame9_content, text="Mężczyźni", width=420, font=customtkinter.CTkFont(size=20), variable=frame9_checkbox7_var)
        frame9_checkbox_7.pack(pady=10, padx=20)
        frame9_checkbox_8 = customtkinter.CTkCheckBox(frame9_content, text="Młodzież", width=420, font=customtkinter.CTkFont(size=20), variable=frame9_checkbox8_var)
        frame9_checkbox_8.pack(pady=10, padx=20)
        frame9_checkbox_9 = customtkinter.CTkCheckBox(frame9_content, text="Mniejszości narodowe", width=420, font=customtkinter.CTkFont(size=20), variable=frame9_checkbox9_var)
        frame9_checkbox_9.pack(pady=10, padx=20)       
             

        frame9_nav = customtkinter.CTkFrame(frame9,corner_radius=0)
        frame9_nav.pack(side='bottom',fill="both", expand=False)


        frame9_nav_button_prev = customtkinter.CTkButton(frame9_nav,height= 60,width=180,text="< Poprzedni krok", command=lambda: self.show_frame("frame8"),font=customtkinter.CTkFont(size=20))
        frame9_nav_button_prev.pack(side='left',padx=70,pady=10)

        frame9_nav_button_next = customtkinter.CTkButton(frame9_nav,height= 60,width=180,text="Następny krok >", command=combine_funcs(lambda: self.show_frame("frame10"),show_checked5),font=customtkinter.CTkFont(size=20))
        frame9_nav_button_next.pack(side='right',padx=70,pady=10)
        frame9.pack(fill="both", expand=True)


        # Okno wyboru Filtrów Aktualne Konkursy Odbiorcy 2
        frame10 = customtkinter.CTkFrame(content_frame)
        frame10.pack(fill="both", expand=True)

        frame10_header = customtkinter.CTkFrame(frame10,corner_radius=0)
        frame10_header.pack(side='top',fill="both", expand=False)
        frame10_title = customtkinter.CTkLabel(frame10_header, text="Aktualne Konkursy, Odbiorcy II",font=customtkinter.CTkFont(size=45))
        frame10_title.pack(padx=20,pady=(40,30))

        frame10_content = customtkinter.CTkFrame(frame10,corner_radius=0)
        frame10_content.pack(fill="both", expand=True)
        frame10_con = customtkinter.CTkLabel(frame10_content, text="""Wybierz do jakich odbiorców mają być kierowane oferty, możesz zaznaczyć dowolną ilość:""",font=customtkinter.CTkFont(size=25))
        frame10_con.pack(padx=20,pady=(0,30))

        def show_checked6():
            checked_boxes6 = []
            if frame10_checkbox10_var.get():
                checked_boxes6.append("&cats%5B626%5D=2207")
            if frame10_checkbox11_var.get():
                checked_boxes6.append("&cats%5B626%5D=628")
            if frame10_checkbox12_var.get():
                checked_boxes6.append("&cats%5B626%5D=2205")
            if frame10_checkbox13_var.get():
                checked_boxes6.append("&cats%5B626%5D=4142")
            if frame10_checkbox14_var.get():
                checked_boxes6.append("&cats%5B626%5D=627")
            if frame10_checkbox15_var.get():
                checked_boxes6.append("&cats%5B626%5D=2206")
            if frame10_checkbox16_var.get():
                checked_boxes6.append("&cats%5B626%5D=2208")
            if frame10_checkbox17_var.get():
                checked_boxes6.append("&cats%5B626%5D=2209")
            if frame10_checkbox18_var.get():
                checked_boxes6.append("&cats%5B626%5D=2210")
            if checked_boxes6:
                with open('User_Link_Files.py/AK_Odbiorcy2.txt', 'w') as file:
                    file.writelines(checked_boxes6)
            else:
                with open('User_Link_Files.py/AK_Odbiorcy2.txt', 'w') as file:
                    file.writelines("")


        frame10_checkbox10_var = tk.BooleanVar()
        frame10_checkbox11_var = tk.BooleanVar()
        frame10_checkbox12_var = tk.BooleanVar()
        frame10_checkbox13_var = tk.BooleanVar()
        frame10_checkbox14_var = tk.BooleanVar()
        frame10_checkbox15_var = tk.BooleanVar()
        frame10_checkbox16_var = tk.BooleanVar()
        frame10_checkbox17_var = tk.BooleanVar()
        frame10_checkbox18_var = tk.BooleanVar()

        
        frame10_checkbox_10 = customtkinter.CTkCheckBox(frame10_content, text="Organizacje pozarządowe", width=300, font=customtkinter.CTkFont(size=20), variable=frame10_checkbox10_var)
        frame10_checkbox_10.pack(pady=10, padx=20)
        frame10_checkbox_11 = customtkinter.CTkCheckBox(frame10_content, text="Osoby bezrobotne", width=300, font=customtkinter.CTkFont(size=20), variable=frame10_checkbox11_var)
        frame10_checkbox_11.pack(pady=10, padx=20)
        frame10_checkbox_12 = customtkinter.CTkCheckBox(frame10_content, text="Osoby LGBT+", width=300, font=customtkinter.CTkFont(size=20), variable=frame10_checkbox12_var)
        frame10_checkbox_12.pack(pady=10, padx=20)
        frame10_checkbox_13 = customtkinter.CTkCheckBox(frame10_content, text="Osoby uzależnione", width=300, font=customtkinter.CTkFont(size=20), variable=frame10_checkbox13_var)
        frame10_checkbox_13.pack(pady=10, padx=20)
        frame10_checkbox_14 = customtkinter.CTkCheckBox(frame10_content, text="Osoby w kryzysie bezdomności", width=300, font=customtkinter.CTkFont(size=20), variable=frame10_checkbox14_var)
        frame10_checkbox_14.pack(pady=10, padx=20)
        frame10_checkbox_15 = customtkinter.CTkCheckBox(frame10_content, text="Osoby niepełnosprawne", width=300, font=customtkinter.CTkFont(size=20), variable=frame10_checkbox15_var)
        frame10_checkbox_15.pack(pady=10, padx=20)
        frame10_checkbox_16 = customtkinter.CTkCheckBox(frame10_content, text="Rodziny", width=300, font=customtkinter.CTkFont(size=20), variable=frame10_checkbox16_var)
        frame10_checkbox_16.pack(pady=10, padx=20)
        frame10_checkbox_17 = customtkinter.CTkCheckBox(frame10_content, text="Seniorzy", width=300, font=customtkinter.CTkFont(size=20), variable=frame10_checkbox17_var)
        frame10_checkbox_17.pack(pady=10, padx=20)
        frame10_checkbox_18 = customtkinter.CTkCheckBox(frame10_content, text="Wolontariusze", width=300, font=customtkinter.CTkFont(size=20), variable=frame10_checkbox18_var)
        frame10_checkbox_18.pack(pady=10, padx=20)     

        frame10_nav = customtkinter.CTkFrame(frame10,corner_radius=0)
        frame10_nav.pack(side='bottom',fill="both", expand=False)


        frame10_nav_button_prev = customtkinter.CTkButton(frame10_nav,height= 60,width=180,text="< Poprzedni krok", command=lambda: self.show_frame("frame10"),font=customtkinter.CTkFont(size=20))
        frame10_nav_button_prev.pack(side='left',padx=70,pady=10)

        frame10_nav_button_next = customtkinter.CTkButton(frame10_nav,height= 60,width=180,text="Następny krok >", command=combine_funcs(lambda: self.show_frame("frame19"),show_checked6),font=customtkinter.CTkFont(size=20))
        frame10_nav_button_next.pack(side='right',padx=70,pady=10)
        frame10.pack(fill="both", expand=True)

        # Okno wyboru Filtrów Wyniki Konkursów Fundusze
        frame11 = customtkinter.CTkFrame(content_frame)
        frame11.pack(fill="both", expand=True)

        frame11_header = customtkinter.CTkFrame(frame11,corner_radius=0)
        frame11_header.pack(side='top',fill="both", expand=False)
        frame11_title = customtkinter.CTkLabel(frame11_header, text="Wyniki Konkursów, Fundusze",font=customtkinter.CTkFont(size=45))
        frame11_title.pack(padx=20,pady=(40,30))

        frame11_content = customtkinter.CTkFrame(frame11,corner_radius=0)
        frame11_content.pack(fill="both", expand=True)
        frame11_con = customtkinter.CTkLabel(frame11_content, text="""Wybierz do jakich odbiorców mają być kierowane oferty, możesz zaznaczyć dowolną ilość:""",font=customtkinter.CTkFont(size=25))
        frame11_con.pack(padx=20,pady=(0,30))

        def show_checked7():
            checked_boxes7 = []
            if frame11_checkbox1_var.get():
                checked_boxes7.append("&cats%5B630%5D=631")
            if frame11_checkbox2_var.get():
                checked_boxes7.append("&cats%5B630%5D=632")
            if frame11_checkbox3_var.get():
                checked_boxes7.append("&cats%5B630%5D=633")
            if frame11_checkbox4_var.get():
                checked_boxes7.append("&cats%5B630%5D=634")
            if frame11_checkbox5_var.get():
                checked_boxes7.append("&cats%5B630%5D=635")
            if frame11_checkbox6_var.get():
                checked_boxes7.append("&cats%5B630%5D=636")
            if frame11_checkbox7_var.get():
                checked_boxes7.append("&cats%5B630%5D=637")
            if frame11_checkbox8_var.get():
                checked_boxes7.append("&cats%5B630%5D=638")
            if frame11_checkbox9_var.get():
                checked_boxes7.append("&cats%5B630%5D=639")
            if frame11_checkbox10_var.get():
                checked_boxes7.append("&cats%5B630%5D=640")
            if frame11_checkbox11_var.get():
                checked_boxes7.append("&cats%5B630%5D=3590")
            if frame11_checkbox12_var.get():
                checked_boxes7.append("&cats%5B630%5D=642")
            if checked_boxes7:
                with open('User_Link_Files.py/WK_Fundusze.txt', 'w') as file:
                    file.writelines(checked_boxes7)
            else:
                with open('User_Link_Files.py/WK_Fundusze.txt', 'w') as file:
                    file.writelines("")

        frame11_checkbox1_var = tk.BooleanVar()
        frame11_checkbox2_var = tk.BooleanVar()
        frame11_checkbox3_var = tk.BooleanVar()
        frame11_checkbox4_var = tk.BooleanVar()
        frame11_checkbox5_var = tk.BooleanVar()
        frame11_checkbox6_var = tk.BooleanVar()
        frame11_checkbox7_var = tk.BooleanVar()
        frame11_checkbox8_var = tk.BooleanVar()
        frame11_checkbox9_var = tk.BooleanVar()
        frame11_checkbox10_var = tk.BooleanVar()
        frame11_checkbox11_var = tk.BooleanVar()
        frame11_checkbox12_var = tk.BooleanVar()

        frame11_checkbox_1 = customtkinter.CTkCheckBox(frame11_content, text="Centralny", width=420, font=customtkinter.CTkFont(size=20), variable=frame11_checkbox1_var)
        frame11_checkbox_1.pack(pady=10, padx=20)
        frame11_checkbox_2 = customtkinter.CTkCheckBox(frame11_content, text="Dzielnicowy", width=420, font=customtkinter.CTkFont(size=20), variable=frame11_checkbox2_var)
        frame11_checkbox_2.pack(pady=10, padx=20)
        frame11_checkbox_3 = customtkinter.CTkCheckBox(frame11_content, text="EOG, CH", width=420, font=customtkinter.CTkFont(size=20), variable=frame11_checkbox3_var)
        frame11_checkbox_3.pack(pady=10, padx=20)
        frame11_checkbox_4 = customtkinter.CTkCheckBox(frame11_content, text="Marszałkowski", width=420, font=customtkinter.CTkFont(size=20), variable=frame11_checkbox4_var)
        frame11_checkbox_4.pack(pady=10, padx=20)
        frame11_checkbox_5 = customtkinter.CTkCheckBox(frame11_content, text="Miejsko-gminny", width=420, font=customtkinter.CTkFont(size=20), variable=frame11_checkbox5_var)
        frame11_checkbox_5.pack(pady=10, padx=20)
        frame11_checkbox_6 = customtkinter.CTkCheckBox(frame11_content, text="Powiatowy", width=420, font=customtkinter.CTkFont(size=20), variable=frame11_checkbox6_var)
        frame11_checkbox_6.pack(pady=10, padx=20)
        frame11_checkbox_7 = customtkinter.CTkCheckBox(frame11_content, text="Prywatny", width=420, font=customtkinter.CTkFont(size=20), variable=frame11_checkbox7_var)
        frame11_checkbox_7.pack(pady=10, padx=20)
        frame11_checkbox_8 = customtkinter.CTkCheckBox(frame11_content, text="Strukturalny", width=420, font=customtkinter.CTkFont(size=20), variable=frame11_checkbox8_var)
        frame11_checkbox_8.pack(pady=10, padx=20)
        frame11_checkbox_9 = customtkinter.CTkCheckBox(frame11_content, text="Stypendialny", width=420, font=customtkinter.CTkFont(size=20), variable=frame11_checkbox9_var)
        frame11_checkbox_9.pack(pady=10, padx=20)
        frame11_checkbox_10 = customtkinter.CTkCheckBox(frame11_content, text="Unijny", width=420, font=customtkinter.CTkFont(size=20), variable=frame11_checkbox10_var)
        frame11_checkbox_10.pack(pady=10, padx=20)
        frame11_checkbox_11 = customtkinter.CTkCheckBox(frame11_content, text="Wojewódzki", width=420, font=customtkinter.CTkFont(size=20), variable=frame11_checkbox11_var)
        frame11_checkbox_11.pack(pady=10, padx=20)
        frame11_checkbox_12 = customtkinter.CTkCheckBox(frame11_content, text="Zagraniczny", width=420, font=customtkinter.CTkFont(size=20), variable=frame11_checkbox12_var)
        frame11_checkbox_12.pack(pady=10, padx=20)
        
             

        frame11_nav = customtkinter.CTkFrame(frame11,corner_radius=0)
        frame11_nav.pack(side='bottom',fill="both", expand=False)


        frame11_nav_button_prev = customtkinter.CTkButton(frame11_nav,height= 60,width=180,text="< Poprzedni krok", command=lambda: self.show_frame("frame3"),font=customtkinter.CTkFont(size=20))
        frame11_nav_button_prev.pack(side='left',padx=70,pady=10)

        frame11_nav_button_next = customtkinter.CTkButton(frame11_nav,height= 60,width=180,text="Następny krok >", command=combine_funcs(lambda: self.show_frame("frame12"),show_checked7),font=customtkinter.CTkFont(size=20))
        frame11_nav_button_next.pack(side='right',padx=70,pady=10)
        frame11.pack(fill="both", expand=True)

        # Okno wyboru Filtrów Wyniki Konkursów Koniec Naboru
        frame12 = customtkinter.CTkFrame(content_frame)
        frame12.pack(fill="both", expand=True)

        frame12_header = customtkinter.CTkFrame(frame12,corner_radius=0)
        frame12_header.pack(side='top',fill="both", expand=False)
        frame12_title = customtkinter.CTkLabel(frame12_header, text="Wyniki Konkursów, Koniec Naboru",font=customtkinter.CTkFont(size=45))
        frame12_title.pack(padx=20,pady=(40,30))

        frame12_content = customtkinter.CTkFrame(frame12,corner_radius=0)
        frame12_content.pack(fill="both", expand=True)
        frame12_con = customtkinter.CTkLabel(frame12_content, text="""Wybierz datę końca naboru szukanych ofert:""",font=customtkinter.CTkFont(size=25))
        frame12_con.pack(padx=20,pady=(0,30))

        def show_checked8():
            checked_boxes8 = []
            if frame12_checkbox1_var.get():
                checked_boxes8.append("")
            if frame12_checkbox2_var.get():
                checked_boxes8.append("&when=week")
            if frame12_checkbox3_var.get():
                checked_boxes8.append("&when=month")
            if frame12_checkbox4_var.get():
                checked_boxes8.append("&when=next_month")
            if frame12_checkbox5_var.get():
                checked_boxes8.append("&when=year")
            if frame12_checkbox6_var.get():
                checked_boxes8.append("&when=next_year")

            if checked_boxes8:
                with open('User_Link_Files.py/WK_Koniec_Naboru.txt', 'w') as file:
                    file.writelines(checked_boxes8)
            else:
                with open('User_Link_Files.py/WK_Koniec_Naboru.txt', 'w') as file:
                    file.writelines("")

        frame12_checkbox1_var = tk.BooleanVar()
        frame12_checkbox2_var = tk.BooleanVar()
        frame12_checkbox3_var = tk.BooleanVar()
        frame12_checkbox4_var = tk.BooleanVar()
        frame12_checkbox5_var = tk.BooleanVar()
        frame12_checkbox6_var = tk.BooleanVar()


        frame12_checkbox_1 = customtkinter.CTkCheckBox(frame12_content, text="Kiedykolwiek", width=420, font=customtkinter.CTkFont(size=20), variable=frame12_checkbox1_var)
        frame12_checkbox_1.pack(pady=10, padx=20)
        frame12_checkbox_2 = customtkinter.CTkCheckBox(frame12_content, text="W tym tygodniu", width=420, font=customtkinter.CTkFont(size=20), variable=frame12_checkbox2_var)
        frame12_checkbox_2.pack(pady=10, padx=20)
        frame12_checkbox_3 = customtkinter.CTkCheckBox(frame12_content, text="W tym miesiącu", width=420, font=customtkinter.CTkFont(size=20), variable=frame12_checkbox3_var)
        frame12_checkbox_3.pack(pady=10, padx=20)
        frame12_checkbox_4 = customtkinter.CTkCheckBox(frame12_content, text="W następnym miesiącu", width=420, font=customtkinter.CTkFont(size=20), variable=frame12_checkbox4_var)
        frame12_checkbox_4.pack(pady=10, padx=20)
        frame12_checkbox_5 = customtkinter.CTkCheckBox(frame12_content, text="W tym roku", width=420, font=customtkinter.CTkFont(size=20), variable=frame12_checkbox5_var)
        frame12_checkbox_5.pack(pady=10, padx=20)
        frame12_checkbox_6 = customtkinter.CTkCheckBox(frame12_content, text="W przyszłym roku", width=420, font=customtkinter.CTkFont(size=20), variable=frame12_checkbox6_var)
        frame12_checkbox_6.pack(pady=10, padx=20)
        
        
             

        frame12_nav = customtkinter.CTkFrame(frame12,corner_radius=0)
        frame12_nav.pack(side='bottom',fill="both", expand=False)


        frame12_nav_button_prev = customtkinter.CTkButton(frame12_nav,height= 60,width=180,text="< Poprzedni krok", command=lambda: self.show_frame("frame11"),font=customtkinter.CTkFont(size=20))
        frame12_nav_button_prev.pack(side='left',padx=70,pady=10)

        frame12_nav_button_next = customtkinter.CTkButton(frame12_nav,height= 60,width=180,text="Następny krok >", command=combine_funcs(lambda: self.show_frame("frame14"),show_checked8),font=customtkinter.CTkFont(size=20))
        frame12_nav_button_next.pack(side='right',padx=70,pady=10)
        frame12.pack(fill="both", expand=True)

# Okno wyboru Filtrów Wyniki Konkursów Temat 1
        frame14 = customtkinter.CTkFrame(content_frame)
        frame14.pack(fill="both", expand=True)

        frame14_header = customtkinter.CTkFrame(frame14,corner_radius=0)
        frame14_header.pack(side='top',fill="both", expand=False)
        frame14_title = customtkinter.CTkLabel(frame14_header, text="Wyniki Konkursów, Temat I",font=customtkinter.CTkFont(size=45))
        frame14_title.pack(padx=20,pady=(40,30))

        frame14_content = customtkinter.CTkFrame(frame14,corner_radius=0)
        frame14_content.pack(fill="both", expand=True)
        frame14_con = customtkinter.CTkLabel(frame14_content, text="""Wybierz który z tematów cię interesuje, możesz zaznaczyć dowolną ilość:""",font=customtkinter.CTkFont(size=25))
        frame14_con.pack(padx=20,pady=(0,30))

        def show_checked9():
            checked_boxes9 = []
            if frame14_checkbox1_var.get():
                checked_boxes9.append("&cats%5B464%5D=4286")
            if frame14_checkbox2_var.get():
                checked_boxes9.append("&cats%5B464%5D=514")
            if frame14_checkbox3_var.get():
                checked_boxes9.append("&cats%5B464%5D=513")
            if frame14_checkbox4_var.get():
                checked_boxes9.append("&cats%5B464%5D=515")
            if frame14_checkbox5_var.get():
                checked_boxes9.append("&cats%5B464%5D=512")
            if frame14_checkbox6_var.get():
                checked_boxes9.append("&cats%5B464%5D=504")
            if frame14_checkbox7_var.get():
                checked_boxes9.append("&cats%5B464%5D=501")
            if frame14_checkbox8_var.get():
                checked_boxes9.append("&cats%5B464%5D=511")
            if frame14_checkbox9_var.get():
                checked_boxes9.append("&cats%5B464%5D=2895")
            if frame14_checkbox11_var.get():
                checked_boxes9.append("&cats%5B464%5D=490")
            if frame14_checkbox12_var.get():
                checked_boxes9.append("&cats%5B464%5D=491")
            if frame14_checkbox13_var.get():
                checked_boxes9.append("&cats%5B464%5D=507")
            if frame14_checkbox14_var.get():
                checked_boxes9.append("&cats%5B464%5D=492")
            if frame14_checkbox15_var.get():
                checked_boxes9.append("&cats%5B464%5D=509")
            if checked_boxes9:
                with open('User_Link_Files.py/WK_Temat1.txt', 'w') as file:
                    file.writelines(checked_boxes9)
            else:
                with open('User_Link_Files.py/WK_Temat1.txt', 'w') as file:
                    file.writelines("")

        frame14_checkbox1_var = tk.BooleanVar()
        frame14_checkbox2_var = tk.BooleanVar()
        frame14_checkbox3_var = tk.BooleanVar()
        frame14_checkbox4_var = tk.BooleanVar()
        frame14_checkbox5_var = tk.BooleanVar()
        frame14_checkbox6_var = tk.BooleanVar()
        frame14_checkbox7_var = tk.BooleanVar()
        frame14_checkbox8_var = tk.BooleanVar()
        frame14_checkbox9_var = tk.BooleanVar()
        frame14_checkbox11_var = tk.BooleanVar()
        frame14_checkbox12_var = tk.BooleanVar()
        frame14_checkbox13_var = tk.BooleanVar()
        frame14_checkbox14_var = tk.BooleanVar()
        frame14_checkbox15_var = tk.BooleanVar()


        frame14_checkbox_1 = customtkinter.CTkCheckBox(frame14_content, text="Ukraina", width=420, font=customtkinter.CTkFont(size=20), variable=frame14_checkbox1_var)
        frame14_checkbox_1.pack(pady=10, padx=20)
        frame14_checkbox_2 = customtkinter.CTkCheckBox(frame14_content, text="Zarządzanie, księgowość", width=420, font=customtkinter.CTkFont(size=20), variable=frame14_checkbox2_var)
        frame14_checkbox_2.pack(pady=10, padx=20)
        frame14_checkbox_3 = customtkinter.CTkCheckBox(frame14_content, text="Finansowanie", width=420, font=customtkinter.CTkFont(size=20), variable=frame14_checkbox3_var)
        frame14_checkbox_3.pack(pady=10, padx=20)
        frame14_checkbox_4 = customtkinter.CTkCheckBox(frame14_content, text="Prawo i obowiązki", width=420, font=customtkinter.CTkFont(size=20), variable=frame14_checkbox4_var)
        frame14_checkbox_4.pack(pady=10, padx=20)
        frame14_checkbox_5 = customtkinter.CTkCheckBox(frame14_content, text="Pożytek publiczny i (1%) 1,5%", width=420, font=customtkinter.CTkFont(size=20), variable=frame14_checkbox5_var)
        frame14_checkbox_5.pack(pady=10, padx=20)
        frame14_checkbox_6 = customtkinter.CTkCheckBox(frame14_content, text="Promocja, media społecznościowe", width=420, font=customtkinter.CTkFont(size=20), variable=frame14_checkbox6_var)
        frame14_checkbox_6.pack(pady=10, padx=20)
        frame14_checkbox_7 = customtkinter.CTkCheckBox(frame14_content, text="Technologie", width=420, font=customtkinter.CTkFont(size=20), variable=frame14_checkbox7_var)
        frame14_checkbox_7.pack(pady=10, padx=20)
        frame14_checkbox_8 = customtkinter.CTkCheckBox(frame14_content, text="Wzmacnianie III sektora", width=420, font=customtkinter.CTkFont(size=20), variable=frame14_checkbox8_var)
        frame14_checkbox_8.pack(pady=10, padx=20)
        frame14_checkbox_9 = customtkinter.CTkCheckBox(frame14_content, text="Rozwój zawodowy i osobisty", width=420, font=customtkinter.CTkFont(size=20), variable=frame14_checkbox9_var)
        frame14_checkbox_9.pack(pady=10, padx=20)
        frame14_checkbox_11 = customtkinter.CTkCheckBox(frame14_content, text="Aktywność obywatelska", width=420, font=customtkinter.CTkFont(size=20), variable=frame14_checkbox11_var)
        frame14_checkbox_11.pack(pady=10, padx=20)
        frame14_checkbox_12 = customtkinter.CTkCheckBox(frame14_content, text="Prawa człowieka", width=420, font=customtkinter.CTkFont(size=20), variable=frame14_checkbox12_var)
        frame14_checkbox_12.pack(pady=10, padx=20)
        frame14_checkbox_13 = customtkinter.CTkCheckBox(frame14_content, text="Działalność lokalna", width=420, font=customtkinter.CTkFont(size=20), variable=frame14_checkbox13_var)
        frame14_checkbox_13.pack(pady=10, padx=20)
        frame14_checkbox_14 = customtkinter.CTkCheckBox(frame14_content, text="Współpraca z administracją", width=420, font=customtkinter.CTkFont(size=20), variable=frame14_checkbox14_var)
        frame14_checkbox_14.pack(pady=10, padx=20)
        frame14_checkbox_15 = customtkinter.CTkCheckBox(frame14_content, text="Wolontariat", width=420, font=customtkinter.CTkFont(size=20), variable=frame14_checkbox15_var)
        frame14_checkbox_15.pack(pady=10, padx=20)
             

        frame14_nav = customtkinter.CTkFrame(frame14,corner_radius=0)
        frame14_nav.pack(side='bottom',fill="both", expand=False)


        frame14_nav_button_prev = customtkinter.CTkButton(frame14_nav,height= 60,width=180,text="< Poprzedni krok", command=lambda: self.show_frame("frame12"),font=customtkinter.CTkFont(size=20))
        frame14_nav_button_prev.pack(side='left',padx=70,pady=10)

        frame14_nav_button_next = customtkinter.CTkButton(frame14_nav,height= 60,width=180,text="Następny krok >", command=combine_funcs(lambda: self.show_frame("frame15"),show_checked9),font=customtkinter.CTkFont(size=20))
        frame14_nav_button_next.pack(side='right',padx=70,pady=10)
        frame14.pack(fill="both", expand=True)

        # Okno wyboru Filtrów Wyniki Konkursów Temat 2
        frame15 = customtkinter.CTkFrame(content_frame)
        frame15.pack(fill="both", expand=True)

        frame15_header = customtkinter.CTkFrame(frame15,corner_radius=0)
        frame15_header.pack(side='top',fill="both", expand=False)
        frame15_title = customtkinter.CTkLabel(frame15_header, text="Okno wyboru Filtrów Wyniki Konkursów Temat II",font=customtkinter.CTkFont(size=45))
        frame15_title.pack(padx=20,pady=(40,30))

        frame15_content = customtkinter.CTkFrame(frame15,corner_radius=0)
        frame15_content.pack(fill="both", expand=True)
        frame15_con = customtkinter.CTkLabel(frame15_content, text="""Wybierz który z tematów cię interesuje, możesz zaznaczyć dowolną ilość:""",font=customtkinter.CTkFont(size=25))
        frame15_con.pack(padx=20,pady=(0,30))

        def show_checked10():
            checked_boxes10 = []
            if frame15_checkbox16_var.get():
                checked_boxes10.append("&cats%5B464%5D=493")
            if frame15_checkbox17_var.get():
                checked_boxes10.append("&cats%5B464%5D=510")
            if frame15_checkbox18_var.get():
                checked_boxes10.append("&cats%5B464%5D=498")
            if frame15_checkbox19_var.get():
                checked_boxes10.append("&cats%5B464%5D=494")
            if frame15_checkbox20_var.get():
                checked_boxes10.append("&cats%5B464%5D=495")
            if frame15_checkbox21_var.get():
                checked_boxes10.append("&cats%5B464%5D=496")
            if frame15_checkbox22_var.get():
                checked_boxes10.append("&cats%5B464%5D=497")
            if frame15_checkbox23_var.get():
                checked_boxes10.append("&cats%5B464%5D=499")
            if frame15_checkbox24_var.get():
                checked_boxes10.append("&cats%5B464%5D=506")
            if frame15_checkbox25_var.get():
                checked_boxes10.append("&cats%5B464%5D=500")
            if frame15_checkbox26_var.get():
                checked_boxes10.append("&cats%5B464%5D=505")
            if frame15_checkbox27_var.get():
                checked_boxes10.append("&cats%5B464%5D=502")
            if frame15_checkbox28_var.get():
                checked_boxes10.append("&cats%5B464%5D=503")
            if frame15_checkbox29_var.get():
                checked_boxes10.append("&cats%5B464%5D=508")
            if checked_boxes10:
                with open('User_Link_Files.py/WK_Temat2.txt', 'w') as file:
                    file.writelines(checked_boxes10)
            else:
                with open('User_Link_Files.py/WK_Temat2.txt', 'w') as file:
                    file.writelines("")


        frame15_checkbox16_var = tk.BooleanVar()
        frame15_checkbox17_var = tk.BooleanVar()
        frame15_checkbox18_var = tk.BooleanVar()
        frame15_checkbox19_var = tk.BooleanVar()
        frame15_checkbox20_var = tk.BooleanVar()
        frame15_checkbox21_var = tk.BooleanVar()
        frame15_checkbox22_var = tk.BooleanVar()
        frame15_checkbox23_var = tk.BooleanVar()
        frame15_checkbox24_var = tk.BooleanVar()
        frame15_checkbox25_var = tk.BooleanVar()
        frame15_checkbox26_var = tk.BooleanVar()
        frame15_checkbox27_var = tk.BooleanVar()
        frame15_checkbox28_var = tk.BooleanVar()
        frame15_checkbox29_var = tk.BooleanVar()

        frame15_checkbox_16 = customtkinter.CTkCheckBox(frame15_content, text="Dobroczynność, filantropia", width=420, font=customtkinter.CTkFont(size=20), variable=frame15_checkbox16_var)
        frame15_checkbox_16.pack(pady=10, padx=20)
        frame15_checkbox_17 = customtkinter.CTkCheckBox(frame15_content, text="Współpraca z biznesem, CSR", width=420, font=customtkinter.CTkFont(size=20), variable=frame15_checkbox17_var)
        frame15_checkbox_17.pack(pady=10, padx=20)
        frame15_checkbox_18 = customtkinter.CTkCheckBox(frame15_content, text="Ekonomia, rynek pracy", width=420, font=customtkinter.CTkFont(size=20), variable=frame15_checkbox18_var)
        frame15_checkbox_18.pack(pady=10, padx=20)
        frame15_checkbox_19 = customtkinter.CTkCheckBox(frame15_content, text="Działalność międzynarodowa", width=420, font=customtkinter.CTkFont(size=20), variable=frame15_checkbox19_var)
        frame15_checkbox_19.pack(pady=10, padx=20)
        frame15_checkbox_20 = customtkinter.CTkCheckBox(frame15_content, text="Unia Europejska", width=420, font=customtkinter.CTkFont(size=20), variable=frame15_checkbox20_var)
        frame15_checkbox_20.pack(pady=10, padx=20)
        frame15_checkbox_21 = customtkinter.CTkCheckBox(frame15_content, text="Edukacja i wychowanie", width=420, font=customtkinter.CTkFont(size=20), variable=frame15_checkbox21_var)
        frame15_checkbox_21.pack(pady=10, padx=20)
        frame15_checkbox_22 = customtkinter.CTkCheckBox(frame15_content, text="Ekologia, zwierzęta", width=420, font=customtkinter.CTkFont(size=20), variable=frame15_checkbox22_var)
        frame15_checkbox_22.pack(pady=10, padx=20)
        frame15_checkbox_23 = customtkinter.CTkCheckBox(frame15_content, text="Kultura i tradycja", width=420, font=customtkinter.CTkFont(size=20), variable=frame15_checkbox23_var)
        frame15_checkbox_23.pack(pady=10, padx=20)
        frame15_checkbox_24 = customtkinter.CTkCheckBox(frame15_content, text="Religia", width=420, font=customtkinter.CTkFont(size=20), variable=frame15_checkbox24_var)
        frame15_checkbox_24.pack(pady=10, padx=20)
        frame15_checkbox_25 = customtkinter.CTkCheckBox(frame15_content, text="Nauka i technika", width=420, font=customtkinter.CTkFont(size=20), variable=frame15_checkbox25_var)
        frame15_checkbox_25.pack(pady=10, padx=20)
        frame15_checkbox_26 = customtkinter.CTkCheckBox(frame15_content, text="Polityka społeczna", width=420, font=customtkinter.CTkFont(size=20), variable=frame15_checkbox26_var)
        frame15_checkbox_26.pack(pady=10, padx=20)
        frame15_checkbox_27 = customtkinter.CTkCheckBox(frame15_content, text="Ochrona zdrowia", width=420, font=customtkinter.CTkFont(size=20), variable=frame15_checkbox27_var)
        frame15_checkbox_27.pack(pady=10, padx=20)
        frame15_checkbox_28 = customtkinter.CTkCheckBox(frame15_content, text="Bezpieczeństwo", width=420, font=customtkinter.CTkFont(size=20), variable=frame15_checkbox28_var)
        frame15_checkbox_28.pack(pady=10, padx=20)
        frame15_checkbox_29 = customtkinter.CTkCheckBox(frame15_content, text="Sport, czas wolny", width=420, font=customtkinter.CTkFont(size=20), variable=frame15_checkbox29_var)
        frame15_checkbox_29.pack(pady=10, padx=20)
             

        frame15_nav = customtkinter.CTkFrame(frame15,corner_radius=0)
        frame15_nav.pack(side='bottom',fill="both", expand=False)


        frame15_nav_button_prev = customtkinter.CTkButton(frame15_nav,height= 60,width=180,text="< Poprzedni krok", command=lambda: self.show_frame("frame14"),font=customtkinter.CTkFont(size=20))
        frame15_nav_button_prev.pack(side='left',padx=70,pady=10)

        frame15_nav_button_next = customtkinter.CTkButton(frame15_nav,height= 60,width=180,text="Następny krok >", command=combine_funcs(lambda: self.show_frame("frame19"),show_checked10),font=customtkinter.CTkFont(size=20))
        frame15_nav_button_next.pack(side='right',padx=70,pady=10)
        frame15.pack(fill="both", expand=True)

# Okno wyboru Filtrów Archiwum Fundusze
        frame16 = customtkinter.CTkFrame(content_frame)
        frame16.pack(fill="both", expand=True)

        frame16_header = customtkinter.CTkFrame(frame16,corner_radius=0)
        frame16_header.pack(side='top',fill="both", expand=False)
        frame16_title = customtkinter.CTkLabel(frame16_header, text="Archiwum, Fundusze",font=customtkinter.CTkFont(size=45))
        frame16_title.pack(padx=20,pady=(40,30))

        frame16_content = customtkinter.CTkFrame(frame16,corner_radius=0)
        frame16_content.pack(fill="both", expand=True)
        frame16_con = customtkinter.CTkLabel(frame16_content, text="""Wybierz który z funduszy cię interesuje, możesz zaznaczyć dowolną ilość:""",font=customtkinter.CTkFont(size=25))
        frame16_con.pack(padx=20,pady=(0,30))

        def show_checked11():
            checked_boxes11 = []
            if frame16_checkbox1_var.get():
                checked_boxes11.append("&cats%5B630%5D=631")
            if frame16_checkbox2_var.get():
                checked_boxes11.append("&cats%5B630%5D=632")
            if frame16_checkbox3_var.get():
                checked_boxes11.append("&cats%5B630%5D=633")
            if frame16_checkbox4_var.get():
                checked_boxes11.append("&cats%5B630%5D=634")
            if frame16_checkbox5_var.get():
                checked_boxes11.append("&cats%5B630%5D=635")
            if frame16_checkbox6_var.get():
                checked_boxes11.append("&cats%5B630%5D=636")
            if frame16_checkbox7_var.get():
                checked_boxes11.append("&cats%5B630%5D=637")
            if frame16_checkbox8_var.get():
                checked_boxes11.append("&cats%5B630%5D=638")
            if frame16_checkbox9_var.get():
                checked_boxes11.append("&cats%5B630%5D=639")
            if frame16_checkbox11_var.get():
                checked_boxes11.append("&cats%5B630%5D=640")
            if frame16_checkbox12_var.get():
                checked_boxes11.append("&cats%5B630%5D=3590")
            if frame16_checkbox13_var.get():
                checked_boxes11.append("&cats%5B630%5D=642")

            if checked_boxes11:
                with open('User_Link_Files.py/A_Fundusze.txt', 'w') as file:
                    file.writelines(checked_boxes11)
            else:
                with open('User_Link_Files.py/A_Fundusze.txt', 'w') as file:
                    file.writelines("")

        frame16_checkbox1_var = tk.BooleanVar()
        frame16_checkbox2_var = tk.BooleanVar()
        frame16_checkbox3_var = tk.BooleanVar()
        frame16_checkbox4_var = tk.BooleanVar()
        frame16_checkbox5_var = tk.BooleanVar()
        frame16_checkbox6_var = tk.BooleanVar()
        frame16_checkbox7_var = tk.BooleanVar()
        frame16_checkbox8_var = tk.BooleanVar()
        frame16_checkbox9_var = tk.BooleanVar()
        frame16_checkbox11_var = tk.BooleanVar()
        frame16_checkbox12_var = tk.BooleanVar()
        frame16_checkbox13_var = tk.BooleanVar()



        frame16_checkbox_1 = customtkinter.CTkCheckBox(frame16_content, text="Centralny", width=420, font=customtkinter.CTkFont(size=20), variable=frame16_checkbox1_var)
        frame16_checkbox_1.pack(pady=10, padx=20)
        frame16_checkbox_2 = customtkinter.CTkCheckBox(frame16_content, text="Dzielnicowy", width=420, font=customtkinter.CTkFont(size=20), variable=frame16_checkbox2_var)
        frame16_checkbox_2.pack(pady=10, padx=20)
        frame16_checkbox_3 = customtkinter.CTkCheckBox(frame16_content, text="EOG, CH", width=420, font=customtkinter.CTkFont(size=20), variable=frame16_checkbox3_var)
        frame16_checkbox_3.pack(pady=10, padx=20)
        frame16_checkbox_4 = customtkinter.CTkCheckBox(frame16_content, text="Marszałkowski", width=420, font=customtkinter.CTkFont(size=20), variable=frame16_checkbox4_var)
        frame16_checkbox_4.pack(pady=10, padx=20)
        frame16_checkbox_5 = customtkinter.CTkCheckBox(frame16_content, text="Miejsko-gminny", width=420, font=customtkinter.CTkFont(size=20), variable=frame16_checkbox5_var)
        frame16_checkbox_5.pack(pady=10, padx=20)
        frame16_checkbox_6 = customtkinter.CTkCheckBox(frame16_content, text="Powiatowy", width=420, font=customtkinter.CTkFont(size=20), variable=frame16_checkbox6_var)
        frame16_checkbox_6.pack(pady=10, padx=20)
        frame16_checkbox_7 = customtkinter.CTkCheckBox(frame16_content, text="Prywatny", width=420, font=customtkinter.CTkFont(size=20), variable=frame16_checkbox7_var)
        frame16_checkbox_7.pack(pady=10, padx=20)
        frame16_checkbox_8 = customtkinter.CTkCheckBox(frame16_content, text="Strukturalny", width=420, font=customtkinter.CTkFont(size=20), variable=frame16_checkbox8_var)
        frame16_checkbox_8.pack(pady=10, padx=20)
        frame16_checkbox_9 = customtkinter.CTkCheckBox(frame16_content, text="Stypendialny", width=420, font=customtkinter.CTkFont(size=20), variable=frame16_checkbox9_var)
        frame16_checkbox_9.pack(pady=10, padx=20)
        frame16_checkbox_11 = customtkinter.CTkCheckBox(frame16_content, text="Unijny", width=420, font=customtkinter.CTkFont(size=20), variable=frame16_checkbox11_var)
        frame16_checkbox_11.pack(pady=10, padx=20)
        frame16_checkbox_12 = customtkinter.CTkCheckBox(frame16_content, text="Wojewódzki", width=420, font=customtkinter.CTkFont(size=20), variable=frame16_checkbox12_var)
        frame16_checkbox_12.pack(pady=10, padx=20)
        frame16_checkbox_13 = customtkinter.CTkCheckBox(frame16_content, text="Zagraniczny", width=420, font=customtkinter.CTkFont(size=20), variable=frame16_checkbox13_var)
        frame16_checkbox_13.pack(pady=10, padx=20)
  
             

        frame16_nav = customtkinter.CTkFrame(frame16,corner_radius=0)
        frame16_nav.pack(side='bottom',fill="both", expand=False)


        frame16_nav_button_prev = customtkinter.CTkButton(frame16_nav,height= 60,width=180,text="< Poprzedni krok", command=lambda: self.show_frame("frame15"),font=customtkinter.CTkFont(size=20))
        frame16_nav_button_prev.pack(side='left',padx=70,pady=10)

        frame16_nav_button_next = customtkinter.CTkButton(frame16_nav,height= 60,width=180,text="Następny krok >", command=combine_funcs(lambda: self.show_frame("frame17"),show_checked11),font=customtkinter.CTkFont(size=20))
        frame16_nav_button_next.pack(side='right',padx=70,pady=10)
        frame16.pack(fill="both", expand=True)

# Okno wyboru Filtrów Archiwum Temat 1
        frame17 = customtkinter.CTkFrame(content_frame)
        frame17.pack(fill="both", expand=True)

        frame17_header = customtkinter.CTkFrame(frame17,corner_radius=0)
        frame17_header.pack(side='top',fill="both", expand=False)
        frame17_title = customtkinter.CTkLabel(frame17_header, text="Archiwum, Temat I",font=customtkinter.CTkFont(size=45))
        frame17_title.pack(padx=20,pady=(40,30))

        frame17_content = customtkinter.CTkFrame(frame17,corner_radius=0)
        frame17_content.pack(fill="both", expand=True)
        frame17_con = customtkinter.CTkLabel(frame17_content, text="""Wybierz który z tematów cię interesuje, możesz zaznaczyć dowolną ilość:""",font=customtkinter.CTkFont(size=25))
        frame17_con.pack(padx=20,pady=(0,30))

        def show_checked12():
            checked_boxes12 = []
            if frame17_checkbox1_var.get():
                checked_boxes12.append("&cats%5B464%5D=4286")
            if frame17_checkbox2_var.get():
                checked_boxes12.append("&cats%5B464%5D=514")
            if frame17_checkbox3_var.get():
                checked_boxes12.append("&cats%5B464%5D=513")
            if frame17_checkbox4_var.get():
                checked_boxes12.append("&cats%5B464%5D=515")
            if frame17_checkbox5_var.get():
                checked_boxes12.append("&cats%5B464%5D=512")
            if frame17_checkbox6_var.get():
                checked_boxes12.append("&cats%5B464%5D=504")
            if frame17_checkbox7_var.get():
                checked_boxes12.append("&cats%5B464%5D=501")
            if frame17_checkbox8_var.get():
                checked_boxes12.append("&cats%5B464%5D=511")
            if frame17_checkbox9_var.get():
                checked_boxes12.append("&cats%5B464%5D=2895")
            if frame17_checkbox11_var.get():
                checked_boxes12.append("&cats%5B464%5D=490")
            if frame17_checkbox12_var.get():
                checked_boxes12.append("&cats%5B464%5D=491")
            if frame17_checkbox13_var.get():
                checked_boxes12.append("&cats%5B464%5D=507")
            if frame17_checkbox14_var.get():
                checked_boxes12.append("&cats%5B464%5D=492")
            if frame17_checkbox15_var.get():
                checked_boxes12.append("&cats%5B464%5D=509")
            if checked_boxes12:
                with open('User_Link_Files.py/A_Temat1.txt', 'w') as file:
                    file.writelines(checked_boxes12)
            else:
                with open('User_Link_Files.py/A_Temat1.txt', 'w') as file:
                    file.writelines("")

        frame17_checkbox1_var = tk.BooleanVar()
        frame17_checkbox2_var = tk.BooleanVar()
        frame17_checkbox3_var = tk.BooleanVar()
        frame17_checkbox4_var = tk.BooleanVar()
        frame17_checkbox5_var = tk.BooleanVar()
        frame17_checkbox6_var = tk.BooleanVar()
        frame17_checkbox7_var = tk.BooleanVar()
        frame17_checkbox8_var = tk.BooleanVar()
        frame17_checkbox9_var = tk.BooleanVar()
        frame17_checkbox11_var = tk.BooleanVar()
        frame17_checkbox12_var = tk.BooleanVar()
        frame17_checkbox13_var = tk.BooleanVar()
        frame17_checkbox14_var = tk.BooleanVar()
        frame17_checkbox15_var = tk.BooleanVar()


        frame17_checkbox_1 = customtkinter.CTkCheckBox(frame17_content, text="Ukraina", width=420, font=customtkinter.CTkFont(size=20), variable=frame17_checkbox1_var)
        frame17_checkbox_1.pack(pady=10, padx=20)
        frame17_checkbox_2 = customtkinter.CTkCheckBox(frame17_content, text="Zarządzanie, księgowość", width=420, font=customtkinter.CTkFont(size=20), variable=frame17_checkbox2_var)
        frame17_checkbox_2.pack(pady=10, padx=20)
        frame17_checkbox_3 = customtkinter.CTkCheckBox(frame17_content, text="Finansowanie", width=420, font=customtkinter.CTkFont(size=20), variable=frame17_checkbox3_var)
        frame17_checkbox_3.pack(pady=10, padx=20)
        frame17_checkbox_4 = customtkinter.CTkCheckBox(frame17_content, text="Prawo i obowiązki", width=420, font=customtkinter.CTkFont(size=20), variable=frame17_checkbox4_var)
        frame17_checkbox_4.pack(pady=10, padx=20)
        frame17_checkbox_5 = customtkinter.CTkCheckBox(frame17_content, text="Pożytek publiczny i (1%) 1,5%", width=420, font=customtkinter.CTkFont(size=20), variable=frame17_checkbox5_var)
        frame17_checkbox_5.pack(pady=10, padx=20)
        frame17_checkbox_6 = customtkinter.CTkCheckBox(frame17_content, text="Promocja, media społecznościowe", width=420, font=customtkinter.CTkFont(size=20), variable=frame17_checkbox6_var)
        frame17_checkbox_6.pack(pady=10, padx=20)
        frame17_checkbox_7 = customtkinter.CTkCheckBox(frame17_content, text="Technologie", width=420, font=customtkinter.CTkFont(size=20), variable=frame17_checkbox7_var)
        frame17_checkbox_7.pack(pady=10, padx=20)
        frame17_checkbox_8 = customtkinter.CTkCheckBox(frame17_content, text="Wzmacnianie III sektora", width=420, font=customtkinter.CTkFont(size=20), variable=frame17_checkbox8_var)
        frame17_checkbox_8.pack(pady=10, padx=20)
        frame17_checkbox_9 = customtkinter.CTkCheckBox(frame17_content, text="Rozwój zawodowy i osobisty", width=420, font=customtkinter.CTkFont(size=20), variable=frame17_checkbox9_var)
        frame17_checkbox_9.pack(pady=10, padx=20)
        frame17_checkbox_11 = customtkinter.CTkCheckBox(frame17_content, text="Aktywność obywatelska", width=420, font=customtkinter.CTkFont(size=20), variable=frame17_checkbox11_var)
        frame17_checkbox_11.pack(pady=10, padx=20)
        frame17_checkbox_12 = customtkinter.CTkCheckBox(frame17_content, text="Prawa człowieka", width=420, font=customtkinter.CTkFont(size=20), variable=frame17_checkbox12_var)
        frame17_checkbox_12.pack(pady=10, padx=20)
        frame17_checkbox_13 = customtkinter.CTkCheckBox(frame17_content, text="Działalność lokalna", width=420, font=customtkinter.CTkFont(size=20), variable=frame17_checkbox13_var)
        frame17_checkbox_13.pack(pady=10, padx=20)
        frame17_checkbox_14 = customtkinter.CTkCheckBox(frame17_content, text="Współpraca z administracją", width=420, font=customtkinter.CTkFont(size=20), variable=frame17_checkbox14_var)
        frame17_checkbox_14.pack(pady=10, padx=20)
        frame17_checkbox_15 = customtkinter.CTkCheckBox(frame17_content, text="Wolontariat", width=420, font=customtkinter.CTkFont(size=20), variable=frame17_checkbox15_var)
        frame17_checkbox_15.pack(pady=10, padx=20)
             

        frame17_nav = customtkinter.CTkFrame(frame17,corner_radius=0)
        frame17_nav.pack(side='bottom',fill="both", expand=False)


        frame17_nav_button_prev = customtkinter.CTkButton(frame17_nav,height= 60,width=180,text="< Poprzedni krok", command=lambda: self.show_frame("frame16"),font=customtkinter.CTkFont(size=20))
        frame17_nav_button_prev.pack(side='left',padx=70,pady=10)

        frame17_nav_button_next = customtkinter.CTkButton(frame17_nav,height= 60,width=180,text="Następny krok >", command=combine_funcs(lambda: self.show_frame("frame18"),show_checked12),font=customtkinter.CTkFont(size=20))
        frame17_nav_button_next.pack(side='right',padx=70,pady=10)
        frame17.pack(fill="both", expand=True)

        # Okno wyboru Filtrów Archiwum Temat 2
        frame18 = customtkinter.CTkFrame(content_frame)
        frame18.pack(fill="both", expand=True)

        frame18_header = customtkinter.CTkFrame(frame18,corner_radius=0)
        frame18_header.pack(side='top',fill="both", expand=False)
        frame18_title = customtkinter.CTkLabel(frame18_header, text="Archiwum, Temat II",font=customtkinter.CTkFont(size=45))
        frame18_title.pack(padx=20,pady=(40,30))

        frame18_content = customtkinter.CTkFrame(frame18,corner_radius=0)
        frame18_content.pack(fill="both", expand=True)
        frame18_con = customtkinter.CTkLabel(frame18_content, text="""Wybierz który z tematów cię interesuje, możesz zaznaczyć dowolną ilość:""",font=customtkinter.CTkFont(size=25))
        frame18_con.pack(padx=20,pady=(0,30))

        def checked_boxes13():
            checked_boxes13 = []
            if frame18_checkbox16_var.get():
                checked_boxes13.append("&cats%5B464%5D=493")
            if frame18_checkbox17_var.get():
                checked_boxes13.append("&cats%5B464%5D=510")
            if frame18_checkbox18_var.get():
                checked_boxes13.append("&cats%5B464%5D=498")
            if frame18_checkbox19_var.get():
                checked_boxes13.append("&cats%5B464%5D=494")
            if frame18_checkbox20_var.get():
                checked_boxes13.append("&cats%5B464%5D=495")
            if frame18_checkbox21_var.get():
                checked_boxes13.append("&cats%5B464%5D=496")
            if frame18_checkbox22_var.get():
                checked_boxes13.append("&cats%5B464%5D=497")
            if frame18_checkbox23_var.get():
                checked_boxes13.append("&cats%5B464%5D=499")
            if frame18_checkbox24_var.get():
                checked_boxes13.append("&cats%5B464%5D=506")
            if frame18_checkbox25_var.get():
                checked_boxes13.append("&cats%5B464%5D=500")
            if frame18_checkbox26_var.get():
                checked_boxes13.append("&cats%5B464%5D=505")
            if frame18_checkbox27_var.get():
                checked_boxes13.append("&cats%5B464%5D=502")
            if frame18_checkbox28_var.get():
                checked_boxes13.append("&cats%5B464%5D=503")
            if frame18_checkbox29_var.get():
                checked_boxes13.append("&cats%5B464%5D=508")
            if checked_boxes13:
                with open('User_Link_Files.py/A_Temat2.txt', 'w') as file:
                    file.writelines(checked_boxes13)
            else:
                with open('User_Link_Files.py/A_Temat2.txt', 'w') as file:
                    file.writelines("")


        frame18_checkbox16_var = tk.BooleanVar()
        frame18_checkbox17_var = tk.BooleanVar()
        frame18_checkbox18_var = tk.BooleanVar()
        frame18_checkbox19_var = tk.BooleanVar()
        frame18_checkbox20_var = tk.BooleanVar()
        frame18_checkbox21_var = tk.BooleanVar()
        frame18_checkbox22_var = tk.BooleanVar()
        frame18_checkbox23_var = tk.BooleanVar()
        frame18_checkbox24_var = tk.BooleanVar()
        frame18_checkbox25_var = tk.BooleanVar()
        frame18_checkbox26_var = tk.BooleanVar()
        frame18_checkbox27_var = tk.BooleanVar()
        frame18_checkbox28_var = tk.BooleanVar()
        frame18_checkbox29_var = tk.BooleanVar()

        frame18_checkbox_16 = customtkinter.CTkCheckBox(frame18_content, text="Dobroczynność, filantropia", width=420, font=customtkinter.CTkFont(size=20), variable=frame18_checkbox16_var)
        frame18_checkbox_16.pack(pady=10, padx=20)
        frame18_checkbox_17 = customtkinter.CTkCheckBox(frame18_content, text="Współpraca z biznesem, CSR", width=420, font=customtkinter.CTkFont(size=20), variable=frame18_checkbox17_var)
        frame18_checkbox_17.pack(pady=10, padx=20)
        frame18_checkbox_18 = customtkinter.CTkCheckBox(frame18_content, text="Ekonomia, rynek pracy", width=420, font=customtkinter.CTkFont(size=20), variable=frame18_checkbox18_var)
        frame18_checkbox_18.pack(pady=10, padx=20)
        frame18_checkbox_19 = customtkinter.CTkCheckBox(frame18_content, text="Działalność międzynarodowa", width=420, font=customtkinter.CTkFont(size=20), variable=frame18_checkbox19_var)
        frame18_checkbox_19.pack(pady=10, padx=20)
        frame18_checkbox_20 = customtkinter.CTkCheckBox(frame18_content, text="Unia Europejska", width=420, font=customtkinter.CTkFont(size=20), variable=frame18_checkbox20_var)
        frame18_checkbox_20.pack(pady=10, padx=20)
        frame18_checkbox_21 = customtkinter.CTkCheckBox(frame18_content, text="Edukacja i wychowanie", width=420, font=customtkinter.CTkFont(size=20), variable=frame18_checkbox21_var)
        frame18_checkbox_21.pack(pady=10, padx=20)
        frame18_checkbox_22 = customtkinter.CTkCheckBox(frame18_content, text="Ekologia, zwierzęta", width=420, font=customtkinter.CTkFont(size=20), variable=frame18_checkbox22_var)
        frame18_checkbox_22.pack(pady=10, padx=20)
        frame18_checkbox_23 = customtkinter.CTkCheckBox(frame18_content, text="Kultura i tradycja", width=420, font=customtkinter.CTkFont(size=20), variable=frame18_checkbox23_var)
        frame18_checkbox_23.pack(pady=10, padx=20)
        frame18_checkbox_24 = customtkinter.CTkCheckBox(frame18_content, text="Religia", width=420, font=customtkinter.CTkFont(size=20), variable=frame18_checkbox24_var)
        frame18_checkbox_24.pack(pady=10, padx=20)
        frame18_checkbox_25 = customtkinter.CTkCheckBox(frame18_content, text="Nauka i technika", width=420, font=customtkinter.CTkFont(size=20), variable=frame18_checkbox25_var)
        frame18_checkbox_25.pack(pady=10, padx=20)
        frame18_checkbox_26 = customtkinter.CTkCheckBox(frame18_content, text="Polityka społeczna", width=420, font=customtkinter.CTkFont(size=20), variable=frame18_checkbox26_var)
        frame18_checkbox_26.pack(pady=10, padx=20)
        frame18_checkbox_27 = customtkinter.CTkCheckBox(frame18_content, text="Ochrona zdrowia", width=420, font=customtkinter.CTkFont(size=20), variable=frame18_checkbox27_var)
        frame18_checkbox_27.pack(pady=10, padx=20)
        frame18_checkbox_28 = customtkinter.CTkCheckBox(frame18_content, text="Bezpieczeństwo", width=420, font=customtkinter.CTkFont(size=20), variable=frame18_checkbox28_var)
        frame18_checkbox_28.pack(pady=10, padx=20)
        frame18_checkbox_29 = customtkinter.CTkCheckBox(frame18_content, text="Sport, czas wolny", width=420, font=customtkinter.CTkFont(size=20), variable=frame18_checkbox29_var)
        frame18_checkbox_29.pack(pady=10, padx=20)
             

        frame18_nav = customtkinter.CTkFrame(frame18,corner_radius=0)
        frame18_nav.pack(side='bottom',fill="both", expand=False)


        frame18_nav_button_prev = customtkinter.CTkButton(frame18_nav,height= 60,width=180,text="< Poprzedni krok", command=lambda: self.show_frame("frame17"),font=customtkinter.CTkFont(size=20))
        frame18_nav_button_prev.pack(side='left',padx=70,pady=10)

        frame18_nav_button_next = customtkinter.CTkButton(frame18_nav,height= 60,width=180,text="Następny krok >", command=combine_funcs(lambda: self.show_frame("frame19"),checked_boxes13),font=customtkinter.CTkFont(size=20))
        frame18_nav_button_next.pack(side='right',padx=70,pady=10)
        frame18.pack(fill="both", expand=True)

        # Okno wyboru Dofinansowania
        frame19 = customtkinter.CTkFrame(content_frame)
        frame19.pack(fill="both", expand=True)

        frame19_header = customtkinter.CTkFrame(frame19,corner_radius=0)
        frame19_header.pack(side='top',fill="both", expand=False)
        frame19_title = customtkinter.CTkLabel(frame19_header, text="Dofinansowanie",font=customtkinter.CTkFont(size=45))
        frame19_title.pack(padx=20,pady=(40,30))

        frame19_content = customtkinter.CTkFrame(frame19,corner_radius=0)
        frame19_content.pack(fill="both", expand=True)
        frame19_con = customtkinter.CTkLabel(frame19_content, text="""Za pomocą suwaków wybierz zakres dofinansowania oferty:""",font=customtkinter.CTkFont(size=25))
        frame19_con.pack(padx=20,pady=(0,30))


        def update_label_from(value_from):
            label1.configure(text=f"Dofinansowanie OD : {value_from} %")
        def update_label_to(value_to):
            label2.configure(text=f"Dofinansowanie DO : {value_to} %")

        def update_label():
            min_val = slider1.get()
            max_val = slider2.get()
            
        def concate_link_parts():
            # print(os.getcwd())
            if (switch_var.get()=="on"):
                with open('User_Link_Files.py/Dofinansowanie.txt', 'w') as file:
                    file.writelines("")
            if (switch_var.get()=="off"):
                with open('User_Link_Files.py/Dofinansowanie.txt', 'w') as file: 
                    if (int(slider1.get())<=int(slider2.get())):
                        file.writelines(f"percent%5Bfrom%5D={int(slider1.get())}&percent%5Bto%5D={int(slider2.get())}")
                    else:
                        file.writelines(f"&percent%5Bfrom%5D={int(slider2.get())}&percent%5Bto%5D={int(slider1.get())}")
            file_list = []
            if ((str(frame3_radio_var.get())+str(frame2_radio_var.get()) == '01') or (str(frame3_radio_var.get())+str(frame2_radio_var.get()) == '00')):
                file_list = ['User_Link_Files.py/Typ_Konkursu.txt','User_Link_Files.py/Typ_Lokalizacja.txt','User_Link_Files.py/AK_Fundusze.txt','User_Link_Files.py/AK_Koniec_Naboru.txt','User_Link_Files.py/AK_Temat1.txt','User_Link_Files.py/AK_Temat2.txt','User_Link_Files.py/AK_Odbiorcy1.txt','User_Link_Files.py/AK_Odbiorcy2.txt','User_Link_Files.py/Dofinansowanie.txt']
            if (str(frame3_radio_var.get())+str(frame2_radio_var.get()) == '02'):
                file_list = ['User_Link_Files.py/Typ_Konkursu.txt','User_Link_Files.py/Lokalizacja_Dokladna.txt','User_Link_Files.py/AK_Fundusze.txt','User_Link_Files.py/AK_Koniec_Naboru.txt','User_Link_Files.py/AK_Temat1.txt','User_Link_Files.py/AK_Temat2.txt','User_Link_Files.py/AK_Odbiorcy1.txt','User_Link_Files.py/AK_Odbiorcy2.txt','User_Link_Files.py/Dofinansowanie.txt']
            if ((str(frame3_radio_var.get())+str(frame2_radio_var.get()) == '11'or (str(frame3_radio_var.get())+str(frame2_radio_var.get()) == '10'))):
                file_list = ['User_Link_Files.py/Typ_Konkursu.txt','User_Link_Files.py/Typ_Lokalizacja.txt','User_Link_Files.py/WK_Fundusze.txt','User_Link_Files.py/WK_Koniec_Naboru.txt','User_Link_Files.py/WK_Temat1.txt','User_Link_Files.py/WK_Temat2.txt','User_Link_Files.py/Dofinansowanie.txt']
            if (str(frame3_radio_var.get())+str(frame2_radio_var.get()) == '12'):
                file_list = ['User_Link_Files.py/Typ_Konkursu.txt','User_Link_Files.py/Lokalizacja_Dokladna.txt','User_Link_Files.py/WK_Fundusze.txt','User_Link_Files.py/WK_Koniec_Naboru.txt','User_Link_Files.py/WK_Temat1.txt','User_Link_Files.py/WK_Temat2.txt','User_Link_Files.py/Dofinansowanie.txt']
            if ((str(frame3_radio_var.get())+str(frame2_radio_var.get()) == '21'or (str(frame3_radio_var.get())+str(frame2_radio_var.get()) == '20'))):
                file_list = ['User_Link_Files.py/Typ_Konkursu.txt','User_Link_Files.py/Typ_Lokalizacja.txt','User_Link_Files.py/A_Fundusze.txt','User_Link_Files.py/A_Temat1.txt','User_Link_Files.py/A_Temat2.txt','User_Link_Files.py/Dofinansowanie.txt']
            if (str(frame3_radio_var.get())+str(frame2_radio_var.get()) == '22'):
                file_list = ['User_Link_Files.py/Typ_Konkursu.txt','User_Link_Files.py/Lokalizacja_Dokladna.txt','User_Link_Files.py/A_Fundusze.txt','User_Link_Files.py/A_Temat1.txt','User_Link_Files.py/A_Temat2.txt','User_Link_Files.py/Dofinansowanie.txt']
            with open('Users_current_link.txt', 'w') as output_file:
                    for file_name in file_list:
                        with open(file_name, 'r') as input_file:
                            file_contents = input_file.read()
                            output_file.write(file_contents)
            # Define the command to run the scrapy script
            os.chdir('NGO_Pages/NGO_Pages')
            command = ['scrapy', 'crawl', 'Pages']
            current_path = os.getcwd() 
            # Run the command in a subprocess and capture the output and error messages
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            print(error.decode())
            with open('Pages.csv', 'r', newline='') as file:
                reader = csv.reader(file)
                rows = list(reader)
                if len(rows) >= 2:
                    second_row = rows[1]
                    pierwsza = second_row[0]
                    druga = second_row[1]
                    wyniki = druga[0:-1]
                    user_link = second_row[2]
                    if (pierwsza != ""):
                        numbers_list = pierwsza.split(",")
                        numbers_int = [int(num) for num in numbers_list]
                        max_value = max(numbers_int)
                        if wyniki =='':
                            wyniki = 'Nieznana ilość'
                        csv_content.set(f'{wyniki} na {max_value} stronach z ofrtami konkursów!')
                    else:
                        max_value = 0
                        csv_content.set(f'{wyniki} na 1 stronie z ofrtami konkursów!')
                    
                    if (max_value > 0):
                        for pages_links in range(1, max_value+1):
                            page =user_link.replace("page=1", f'page={pages_links}')
                            # print(page)
                            # Push URLs to Redis Queue
                            redisClient.lpush('pages_queue:start_urls', page)
                    if (max_value == 0):

                        # Push URLs to Redis Queue
                        redisClient.lpush('pages_queue:start_urls', user_link)          
        label1 = customtkinter.CTkLabel(frame19_content, font=customtkinter.CTkFont(size=22),width=600, text="Dofinansowanie OD : 0 %")
        label1.pack(pady=(60,20))

        slider1 = customtkinter.CTkSlider(frame19_content, from_=0, to=100,width=600, command=update_label_from)
        slider1.set(0)
        slider1.configure(number_of_steps=100)
        slider1.pack(pady=(10,40))

        label2 = customtkinter.CTkLabel(frame19_content, font=customtkinter.CTkFont(size=22),width=600, text="Dofinansowanie DO : 100 %")
        label2.pack(pady=20)



        slider2 = customtkinter.CTkSlider(frame19_content, from_=0, to=100,width=600, command=update_label_to)
        slider2.configure(number_of_steps=100)
        slider2.set(100)
        slider2.pack(pady=(10,40))

            
        def switch_event():
            if (switch_var.get()=="off"):
                slider1.configure(state="normal")
                slider2.configure(state="normal")

            elif (switch_var.get()=="on"):
                slider1.configure(state="disabled")
                slider2.configure(state="disabled")
                slider1.set(0)
                slider2.set(100)
                label1.configure(text="Dofinansowanie OD : 0 %")
                label2.configure(text="Dofinansowanie DO : 100 %")

        switch_var = customtkinter.StringVar(value="off")
        switch = customtkinter.CTkSwitch(frame19_content,width=30,text="", command=switch_event,
                                 variable=switch_var, onvalue="on", offvalue="off")
        switch.pack(pady=(100,0))

        label4 = customtkinter.CTkLabel(frame19_content, font=customtkinter.CTkFont(size=22),width=600, text="*Nie chcesz podawać informacji o dofinansowaniu ")
        label4.pack(pady=(10,20))
        label3 = customtkinter.CTkLabel(frame19_content, font=customtkinter.CTkFont(size=14),width=600, text=" !!! Jeżeli wybierzesz niepoprawny zakres program atomatycznie zmieni wartości !!!")
        label3.pack(pady=(40,20))

        frame19_nav = customtkinter.CTkFrame(frame19,corner_radius=0)
        frame19_nav.pack(side='bottom',fill="both", expand=False)


        frame19_nav_button_prev = customtkinter.CTkButton(frame19_nav,height= 60,width=180,text="< Poprzedni krok", command=lambda: self.show_frame(check_variable_frame3()),font=customtkinter.CTkFont(size=20))
        frame19_nav_button_prev.pack(side='left',padx=70,pady=10)

        frame19_nav_button_next = customtkinter.CTkButton(frame19_nav,height= 60,width=180,text="Następny krok >", command=combine_funcs(lambda: self.show_frame("frame20"),concate_link_parts),font=customtkinter.CTkFont(size=20))
        frame19_nav_button_next.pack(side='right',padx=70,pady=10)
        frame19.pack(fill="both", expand=True)

        # Link i ilość stron
        frame20 = customtkinter.CTkFrame(content_frame)
        frame20.pack(fill="both", expand=True)

        frame20_header = customtkinter.CTkFrame(frame20,corner_radius=0)
        frame20_header.pack(side='top',fill="both", expand=False)
        frame20_title = customtkinter.CTkLabel(frame20_header, text="Twoje artykuły",font=customtkinter.CTkFont(size=45))
        frame20_title.pack(padx=20,pady=(40,30))

        frame20_content = customtkinter.CTkFrame(frame20,corner_radius=0)
        frame20_content.pack(fill="both", expand=True)
        csv_content = tk.StringVar()
        frame20_con = customtkinter.CTkLabel(frame20_content, textvariable=csv_content, text="""Znaleziono ??? stron z ??? ofrtami konkursów.
        Jeżeli chcesz poznać znalezione konkursy, po wciśnięciu pszycisku szukaj uruchomi się program szukający wyników
        Może to zająć nawet kilka minut!""",font=customtkinter.CTkFont(size=25))
        frame20_con.pack(padx=20,pady=(0,30))

        def delete_pages_que():
            redisClient.delete('pages_queue:start_urls')
            os.chdir('../../')
        def open_terminal_command():
            current_os = platform.system()
            if current_os == "Linux":
                return ["gnome-terminal", "--"]
            elif current_os == "Darwin":  # macOS
                return ["open", "-a", "Terminal", "--"]
            elif current_os == "Windows":
                return ["cmd.exe", "/c", "start"]
        def drop_rows_with_invalid_html(csv_file_path):
            with open(csv_file_path, 'r', newline='') as file:
                reader = csv.reader(file)
                rows = list(reader)
            rows_to_keep = [rows[0]]  
            for row in rows[1:]:
                first_record = row[0]
                if first_record.endswith('html'):
                    rows_to_keep.append(row)
            with open(csv_file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows_to_keep)

        def article_evaluation_data():
            data = []
            with open('Article_data.csv', 'r', newline='') as file_final:
                reader = csv.reader(file_final)
                for row in reader:
                    if len(row) >= 3:
                        value_2 = row[1]
                        value_3 = row[2]
                        result = f'({value_2};{value_3})'
                        data.append(result)
                article_information = data[1:]
                tokenizer = tiktoken.get_encoding("cl100k_base")
                color_codes = ['0;47', '0;42', '0;43', '0;44', '0;46', '0;45']

                user_input2 = str(article_information)

                encoded3 = tokenizer.encode(user_input2)
                decoded2 = tokenizer.decode_tokens_bytes(encoded3)
                token_list2 = [token.decode() for token in decoded2]

                character_count = sum(len(i) for i in token_list2)

                # for idx, token in enumerate(token_list2):
                    # print(f'\x1b[{color_codes[idx % len(color_codes)]};1m{token}\x1b[0m', end='')

                Token_Count1 =(int(len(encoded3)))
                Character_Count = ("Characters: " + str(character_count))
                if (Token_Count1 < 1840):
                    tokeny_konkórsów = 1
                    tokeny_konkórsów_liczba = Token_Count1
                    return Token_Count1,article_information
                if (Token_Count1 > 1840):
                    tokeny_konkórsów = 0
                    tokeny_konkórsów_liczba = Token_Count1
                    return Token_Count1,article_information

                
                    


        def run_scrapy():
            os.chdir('../../')
            os.chdir('NGO_ArticlesLinks/RedisDB_Filters/scaling-python-scrapy-redis/redis-python-scrapy-examples')
            command2 = ['scrapy', 'crawl', 'ArticlesLinks']
            current_path = os.getcwd() 
            # Run the command in a subprocess and capture the output and error messages
            process2 = subprocess.Popen(command2, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process2.communicate()
            print(error.decode())
            # print(os.getcwd())
            os.chdir('../../../../')
            num_runs = 1
            for i in range(num_runs):
                run_scrapy_finale()
            
            os.chdir('NGO_ArticlesLinks/RedisDB_Filters/scaling-python-scrapy-redis/redis-python-scrapy-examples')
            # print(os.getcwd())
            csv_file_path = 'Article_data.csv'  
            drop_rows_with_invalid_html(csv_file_path)
            tokeny_cz1 = article_evaluation_data()
            tokeny_cz1 = str(tokeny_cz1)
            # print(tokeny_cz1)
            with open('Tokeny_Konkursy.txt', 'w') as file:
                file.write(tokeny_cz1)

        frame20button_next = customtkinter.CTkButton(frame20_content,height= 120,width=360,text="Wyszukaj Oferty", command=combine_funcs(lambda: self.show_frame("frame21"),run_scrapy),font=customtkinter.CTkFont(size=30))
        frame20button_next.pack(padx=(0,0),pady=(200,10))
        frame20.pack(fill="both", expand=True)
                                                                                                                    # command=combine_funcs(lambda: self.show_frame("frame21"),run_scrapy)
 
        frame20_nav = customtkinter.CTkFrame(frame20,corner_radius=0)
        frame20_nav.pack(side='bottom',fill="both", expand=False)


        frame20_nav_button_prev = customtkinter.CTkButton(frame20_nav,height= 60,width=180,text="< Poprzedni krok", command=combine_funcs(lambda: self.show_frame("frame19"),delete_pages_que),font=customtkinter.CTkFont(size=20))
        frame20_nav_button_prev.pack(side='left',padx=70,pady=10)



        # GPT AI
        frame21 = customtkinter.CTkFrame(content_frame)
        frame21.pack(fill="both", expand=True)

        frame21_header = customtkinter.CTkFrame(frame21,corner_radius=0)
        frame21_header.pack(side='top',fill="both", expand=False)
        frame21_title = customtkinter.CTkLabel(frame21_header, text="Konkursy specjalnie dla ciebie",font=customtkinter.CTkFont(size=45))
        frame21_title.pack(padx=20,pady=(40,30))

        frame21_content = customtkinter.CTkFrame(frame21,corner_radius=0)
        frame21_content.pack(fill="both", expand=True)
        frame21_con = customtkinter.CTkLabel(frame21_content, text="""Masz możliwośc jeszcze wiekszego spersonalizowania swoich wyników.
        Wystarczy żę w polu poniżej streścisz swoją osobę (Imie,zainteresowania,praca itd.).""",font=customtkinter.CTkFont(size=25))
        frame21_con.pack(padx=20,pady=(0,30))

        def switch_event2():
            if (switch_var2.get()=="off"):
                textbox.configure(state="normal")
            elif (switch_var2.get()=="on"):
                textbox.configure(state="disabled")


        def user_des ():
            if (switch_var2.get()=="off"):
                GPT_Descryption = textbox.get("0.0", "end")
                # print(GPT_Descryption)

                tokenizer = tiktoken.get_encoding("cl100k_base")
                color_codes = ['0;47', '0;42', '0;43', '0;44', '0;46', '0;45']

                user_input2 = str(GPT_Descryption)

                encoded3 = tokenizer.encode(user_input2)
                decoded2 = tokenizer.decode_tokens_bytes(encoded3)
                token_list2 = [token.decode() for token in decoded2]

                character_count = sum(len(i) for i in token_list2)

                # for idx, token in enumerate(token_list2):
                    # print(f'\x1b[{color_codes[idx % len(color_codes)]};1m{token}\x1b[0m', end='')

                Token_Count1 =(int(len(encoded3)))
                return Token_Count1 
            if (switch_var2.get()=="on"):
                Token_Count1 = 50000
                return Token_Count1

        def user_des2 ():
            if (switch_var2.get()=="on"):
                GPT_Descryption = textbox.get("0.0", "end")
                # print(GPT_Descryption)

                tokenizer = tiktoken.get_encoding("cl100k_base")
                color_codes = ['0;47', '0;42', '0;43', '0;44', '0;46', '0;45']

                user_input2 = str(GPT_Descryption)

                encoded3 = tokenizer.encode(user_input2)
                decoded2 = tokenizer.decode_tokens_bytes(encoded3)
                token_list2 = [token.decode() for token in decoded2]

                character_count = sum(len(i) for i in token_list2)

                # for idx, token in enumerate(token_list2):
                    # print(f'\x1b[{color_codes[idx % len(color_codes)]};1m{token}\x1b[0m', end='')

                Token_Count1 =(int(len(encoded3)))
                return GPT_Descryption 
            if (switch_var2.get()=="off"):
                Token_Count1 = 50000
                GPT_Descryption = ''
                return GPT_Descryption

        def what_to_show():
            tokeny_cz2 = user_des() 
            GPT_Opis_Użytkownika = user_des2()
            ile_tokenów_opis= tokeny_cz2
            with open('Tokeny_Opis.txt', 'w') as file4:
                tokeny_cz2 = str(tokeny_cz2)
                file4.write(GPT_Opis_Użytkownika)
            with open('Tokeny_Konkursy.txt', 'r') as file3:
                file_contents5 = file3.read()
                ile_tokenów_konkursy = ast.literal_eval(file_contents5)
                ile_tokenów_konkursy = ile_tokenów_konkursy[0]
                konkursy = file_contents5[1]
                if (int(ile_tokenów_konkursy)+int(ile_tokenów_opis < 2000)):
                    treść_dla_ciebie = Chat_GPT_API(GPT_Opis_Użytkownika,konkursy)
                    with open('treść_dla_ciebie.txt', 'w') as file7:
                        file7.write(treść_dla_ciebie)

                else:
                    treść_dla_ciebie = f"Niestety przekroczyłeś limit tokenów :( [{ile_tokenów_konkursy+ile_tokenów_opis}]"
                    with open('treść_dla_ciebie.txt', 'w') as file7:
                        file7.write(treść_dla_ciebie)
                




        textbox = customtkinter.CTkTextbox(frame21_content,width =1400,height = 400, border_width = 4, corner_radius=10,font=customtkinter.CTkFont(size=18))
        textbox.pack(padx=20,pady=(20,0))

        switch_var2 = customtkinter.StringVar(value="off")
        switch2 = customtkinter.CTkSwitch(frame21_content,width=60,text="", command=switch_event2,
                                 variable=switch_var2, onvalue="on", offvalue="off") 
            
        frame21_warning = customtkinter.CTkLabel(frame21_content, text="*Nie chce spersonalizowanych wyników",font=customtkinter.CTkFont(size=18))
        frame21_warning.pack(padx=20,pady=(40,20))
        switch2.pack(pady=(0,0))

        frame21_nav = customtkinter.CTkFrame(frame21,corner_radius=0)
        frame21_nav.pack(side='bottom',fill="both", expand=False)
    

        frame21_nav_button_next = customtkinter.CTkButton(frame21_nav,height= 60,width=250,text="Pokaż wyniki", command=combine_funcs(lambda: self.show_frame("frame22"),what_to_show),font=customtkinter.CTkFont(size=20))
        frame21_nav_button_next.pack(side='right',padx=70,pady=10)
        frame21.pack(fill="both", expand=True)
        # Finalne Okno
        frame22 = customtkinter.CTkFrame(content_frame)
        frame22.pack(fill="both", expand=True)

        frame22_header = customtkinter.CTkFrame(frame22,corner_radius=0)
        frame22_header.pack(side='top',fill="both", expand=False)
        frame22_title = customtkinter.CTkLabel(frame22_header, text="Twoje NGO",font=customtkinter.CTkFont(size=45))
        frame22_title.pack(padx=20,pady=(40,30))

        frame22_content = customtkinter.CTkFrame(frame22,corner_radius=0)
        frame22_content.pack(fill="both", expand=True)
        frame22_con = customtkinter.CTkLabel(frame22_content, text="""Przeglądaj wybrane oferty, za pomocą przycisków możesz wyeksportować 
        konkursy na swojego maila oraz zacząć wyszukiwanie od początku.""",font=customtkinter.CTkFont(size=25))
        frame22_con.pack(padx=20,pady=(0,30))



        def segmented_button_callback(value):
            if (segemented_button_var.get() == 'Wszystkie Konkursy'):
                scrollable_frame_data.delete("0.0", "end")
                filename = 'Article_data.csv' 
                with open(filename, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        for field, value in row.items():
                            scrollable_frame_data.insert("0.0",(field + ": " + value))
                            scrollable_frame_data.insert("0.0","""\n""")
                        scrollable_frame_data.insert("0.0","""\n---------------------------------\n""")

            if (segemented_button_var.get() == 'Specjalnie dla Ciebie'):
                scrollable_frame_data.delete("0.0", "end")
                filename = 'treść_dla_ciebie.txt'  
                with open(filename, 'r') as file:
                    content = file.read() 

                scrollable_frame_data.insert("0.0", content)
            if (segemented_button_var.get() == 'Used Tokens Visual'):
                scrollable_frame_data.insert("0.0", "")



        segemented_button_var = customtkinter.StringVar(value="Value 1")
        segemented_button = customtkinter.CTkSegmentedButton(frame22_content, values=["Wszystkie Konkursy", "Specjalnie dla Ciebie", "Used Tokens Visual"],
                                                            command=segmented_button_callback,
                                                            variable=segemented_button_var, font=customtkinter.CTkFont(size=20))

        segemented_button.pack(pady= (0,0))
        scrollable_frame_data = customtkinter.CTkTextbox(frame22_content, width=1450, height=500,border_width= 4, corner_radius = 10)
        scrollable_frame_data.pack(pady=(0,15),padx = (15))

             

        frame22_nav = customtkinter.CTkFrame(frame22,corner_radius=0)
        frame22_nav.pack(side='bottom',fill="both", expand=False)


        frame22_nav_button_prev = customtkinter.CTkButton(frame22_nav,height= 60,width=250,text="Zacznij od początku", command=lambda: self.show_frame("frame1"),font=customtkinter.CTkFont(size=20))
        frame22_nav_button_prev.pack(side='left',padx=70,pady=10)

        frame22_nav_button_next = customtkinter.CTkButton(frame22_nav,height= 60,width=250,text="Wyeksportuj plik",font=customtkinter.CTkFont(size=20))
        frame22_nav_button_next.pack(side='right',padx=70,pady=10)
        frame22.pack(fill="both", expand=True)


        #Finalne zapakowanie poszczególnych ekranów
        self.frames["frame1"] = frame1
        self.frames["frame3"] = frame3
        self.frames["frame2"] = frame2
        self.frames["frame4"] = frame4
        self.frames["frame5"] = frame5
        self.frames["frame6"] = frame6
        self.frames["frame7"] = frame7
        self.frames["frame8"] = frame8
        self.frames["frame9"] = frame9
        self.frames["frame10"] = frame10
        self.frames["frame11"] = frame11
        self.frames["frame12"] = frame12
        self.frames["frame14"] = frame14
        self.frames["frame15"] = frame15
        self.frames["frame16"] = frame16
        self.frames["frame17"] = frame17
        self.frames["frame18"] = frame18
        self.frames["frame19"] = frame19
        self.frames["frame20"] = frame20
        self.frames["frame21"] = frame21
        self.frames["frame22"] = frame22








#Funkcjonalności aplikacji
            
    def show_frame(self, frame_name):
        if self.current_frame is not None:
            self.frames[self.current_frame].pack_forget()
        self.current_frame = frame_name
        self.frames[frame_name].pack(fill="both", expand=True)

    # def show_frame(self, frame_name):
    #     if self.current_frame is not None:
    #         self.frames[self.current_frame].pack_forget()

    #     self.current_frame = frame_name

    #     def show_next_frame():
    #         self.frames[frame_name].pack(fill="both", expand=True)

    #     self.after(200, show_next_frame)

    def show_frame4(self, frame_name):
        if self.current_frame is not None:
            self.frames[self.current_frame].pack_forget()
        self.current_frame = frame_name
        self.frames[frame_name].pack(fill="both", expand=True)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
    
app = App()
app.mainloop()
