import customtkinter as ctk
import os
import time
import requests
import threading 
import tkinter
import colorama
from colorama import Fore
from PIL import Image
import webbrowser


def send_friend_requests(delay_friends):
    global running_friends
    var1 = entry1.get()
    var2 = entry2.get()
    var_api = api_entry.get()

    def loadTokens():
        with open(var1, 'r') as f:
            content = f.read()
        return content

    tokens = loadTokens()

    os.system("cls")
    invalid = valid = 0
    for token in tokens.splitlines():
        if not running_friends:
            break
        url = 'https://api.ssab.tools/discord/sendFriendRequest'   
        headers = {'ssab-api-key': var_api}
        data = {'token': token, 'userId': var2}
        r = requests.post(url, json=data, headers=headers)
        jsonResponse = r.json()
        if jsonResponse["response"]["status"] != 'error':
            valid += 1
            print(jsonResponse)
        else:
            invalid += 1
            print(jsonResponse)
        time.sleep(delay_friends)
        # update valid and invalid tokens count
        valid_text.set(f"Sent: {valid}")
        invalid_text.set(f"Fail: {invalid}")

    # reset button to start state after function finishes
    button.configure(text="START", command=start_send_friend_requests)
    running_friends = False

def start_send_friend_requests():
    global running_friends
    if running_friends:
        return
    running_friends = True
    button.configure(text="STOP", command=stop_send_friend_requests)
    delay_friends = int(delay_friends_var.get())
    t = threading.Thread(target=send_friend_requests, args=(delay_friends,))
    t.start()

def stop_send_friend_requests():
    global running_friends
    running_friends = False
    button.configure(text="START", command=start_send_friend_requests)

running_friends = False

def checker(delay_checker):
    global running_checker
    var_checker_path = entry1_c.get()
    var_api = api_entry.get()

    def loadTokens():
        with open(var_checker_path, 'r') as f:
            content = f.read()
        return content

    tokens = loadTokens()
    os.system("cls")
    tvalid = tinvalid = tnitro = tphone = 0
    for token in tokens.splitlines():
        if not running_checker:
            break
        url = 'https://api.ssab.tools/discord/checkToken'   
        headers = {'ssab-api-key': var_api}
        data = {'token': token}
        r = requests.post(url, json=data, headers=headers)
        jsonResponse = r.json()
        if jsonResponse["response"]["code"] == 200:
            print(f"{Fore.LIGHTGREEN_EX}{token}{Fore.RESET}")
            tvalid += 1
            with open("valid.txt", "a") as f:
                f.write(f"{token}\n")
            if jsonResponse["response"]["data"]["premium_type"] != 0:
                with open("premium.txt", "a") as f:
                    f.write(f"{token}\n")
                tnitro += 1
            if jsonResponse["response"]["data"]["phone"] is not None:
                with open("phone.txt", "a") as f:
                    f.write(f"{token}\n")
                tphone += 1
        else:
            print(f"{token}")
            tinvalid += 1
        time.sleep(delay_checker)
        # update valid and invalid tokens count
        valid_text_c.set(f"Valid Tokens: {tvalid}")
        invalid_text_c.set(f"Invalid Tokens: {tinvalid}")
        phone_text_c.set(f"Phone Tokens: {tphone}")
        nitro_text_c.set(f"Nitro Tokens: {tnitro}")

    # reset button to start state after function finishes
    button_checker.configure(text="START", command=start_checker)
    running_checker = False

def start_checker():
    global running_checker
    if running_checker:
        return
    running_checker = True
    button_checker.configure(text="STOP", command=stop_checker)
    delay_checker = int(delay_checker_var.get())
    t = threading.Thread(target=checker, args=(delay_checker,))
    t.start()

def stop_checker():
    global running_checker
    running_checker = False
    button_checker.configure(text="START", command=start_checker)

running_checker = False

def checker_pay(delay_checker_pay):
    global running_checker_pay
    var_checker_pay_path = entry1_p.get()
    var_api = api_entry.get()

    def loadTokens():
        with open(var_checker_pay_path, 'r') as f:
            content = f.read()
        return content

    tokens = loadTokens()
    os.system("cls")
    invalid = valid = tpay = tnopay = 0
    for token in tokens.splitlines():
        if not running_checker_pay:
            break
        url = 'https://api.ssab.tools/discord/getPaymentMethods'   
        headers = {'ssab-api-key': var_api}
        data = {'token': token}
        r = requests.post(url, json=data, headers=headers)
        jsonResponse = r.json()
        if jsonResponse["response"]["code"] == 40002:
            invalid += 1
        else:
            valid += 1
            if len(jsonResponse["response"]["data"]) > 0:
                print(f"{Fore.LIGHTGREEN_EX}{token}{Fore.RESET}")
                tpay += 1
                with open("payment.txt", "a") as f:
                    f.write(f"{token}\n")
            else:
                print(f"{token}")
                tnopay += 1
        time.sleep(delay_checker_pay)
        # update valid and invalid tokens count
        valid_text_p.set(f"Payment: {tpay}")
        invalid_text_p.set(f"No Payment: {tnopay}")
    # reset button to start state after function finishes
    button_checker_pay.configure(text="START", command=start_checker_pay)
    running_checker_pay = False

def start_checker_pay():
    global running_checker_pay
    if running_checker_pay:
        return
    running_checker_pay = True
    button_checker_pay.configure(text="STOP", command=stop_checker_pay)
    delay_checker_pay = int(delay_checker_pay_var.get())
    t = threading.Thread(target=checker_pay, args=(delay_checker_pay,))
    t.start()

def stop_checker_pay():
    global running_checker_pay
    running_checker_pay = False
    button_checker_pay.configure(text="START", command=start_checker_pay)

running_checker_pay = False

def open_url():
    url = "https://ssab.sellpass.io/"
    webbrowser.open_new(url)

def on_closing():
    root.destroy()
    os._exit(0)

root = ctk.CTk()
root.title("discordAIO")

# set close event handler
root.protocol("WM_DELETE_WINDOW", on_closing)


# Create CTkImage object    
image_d = ctk.CTkImage(light_image=Image.open("buy.png"), dark_image=Image.open("buy.png"), size=(24, 24))
button_image = ctk.CTkButton(root, text="Get Access", image=image_d, width=40, height=24, command=open_url)
button_image.pack(side="top", pady=10, padx=120)

api_tab = ctk.CTkFrame(master=root)
api_tab.pack(side="top", pady=10, padx=120, fill="both", expand=True)

api_label = ctk.CTkLabel(master=api_tab, width=120, height=32, text="To use this application you need an api key provided by SSAB Technology.")
api_label.pack(pady=12, padx=10, expand=True)
api_entry = ctk.CTkEntry(master=api_tab, width=240, height=32, placeholder_text="ssab-api-key", show='*')
api_entry.pack(pady=12, padx=10, expand=True)

# create tab view
tabview = ctk.CTkTabview(root)

# create tabs
tab1 = tabview.add("Friend Request")
tab2 = tabview.add("Tokens Checker")
tab3 = tabview.add("Check Payments")


# add widgets to tab 1
label = ctk.CTkLabel(master=tab1, text="Send friend requests to anyone using tokens.")
label.pack(expand=True)
entry1 = ctk.CTkEntry(master=tab1, width=200, placeholder_text="Tokens Path")
entry1.pack(expand=True)
entry2 = ctk.CTkEntry(master=tab1, width=200, placeholder_text="User ID")
entry2.pack(expand=True)

# add delay_friends slider to tab 1
delay_friends_var = tkinter.DoubleVar(value=2)  
delay_friends_label = ctk.CTkLabel(master=tab1, text="Delay: 2")
delay_friends_label.pack(expand=True)

def set_delay_friends(value):
    delay_friends = int(round(value))
    delay_friends_var.set(delay_friends)

def update_delay_friends_label(val):
    delay_friends_label.configure(text="Delay: " + str(val))
delay_friends_var.trace_add("write", lambda *args: update_delay_friends_label(delay_friends_var.get()))

delay_friends_slider = ctk.CTkSlider(master=tab1, from_=2, to=10, variable=delay_friends_var, command=set_delay_friends)
delay_friends_slider.pack(expand=True)

# add valid and invalid tokens frame to tab 1
tokens_frame = ctk.CTkFrame(master=tab1)
tokens_frame.pack(expand=True)
valid_text = tkinter.StringVar(value="Sent: 0")
invalid_text = tkinter.StringVar(value="Fail: 0")
valid_label = ctk.CTkLabel(master=tokens_frame, textvariable=valid_text)
valid_label.pack(side="left", padx=10)
invalid_label = ctk.CTkLabel(master=tokens_frame, textvariable=invalid_text)
invalid_label.pack(side="left", padx=10)

button = ctk.CTkButton(master=tab1, width=20, text="START", command=start_send_friend_requests)
button.pack(expand=True)

# add widgets to tab 2
label_c = ctk.CTkLabel(master=tab2, text="Check tokens and sort them to valid/phone/nitro.")
label_c.pack(expand=True)
entry1_c = ctk.CTkEntry(master=tab2, width=200, placeholder_text="Tokens Path")
entry1_c.pack(expand=True)

# add delay_friends slider to tab 2
delay_checker_var = tkinter.DoubleVar(value=1)  
delay_checker_label = ctk.CTkLabel(master=tab2, text="Delay: 1")
delay_checker_label.pack(expand=True)

def set_delay_checker(value):
    delay_checker = int(round(value))
    delay_checker_var.set(delay_checker)

def update_delay_checker_label(val):
    delay_checker_label.configure(text="Delay: " + str(val))
delay_checker_var.trace_add("write", lambda *args: update_delay_checker_label(delay_checker_var.get()))

delay_checker_slider = ctk.CTkSlider(master=tab2, from_=1, to=10, variable=delay_checker_var, command=set_delay_checker)
delay_checker_slider.pack(expand=True)

# add valid and invalid tokens frame to tab 2
tokens_c_frame = ctk.CTkFrame(master=tab2)
tokens_c_frame.pack(expand=True)
valid_text_c = tkinter.StringVar(value="Valid Tokens: 0")
invalid_text_c = tkinter.StringVar(value="Invalid Tokens: 0")
valid_label_c = ctk.CTkLabel(master=tokens_c_frame, textvariable=valid_text_c)
valid_label_c.pack(side="left", padx=10)
invalid_label_c = ctk.CTkLabel(master=tokens_c_frame, textvariable=invalid_text_c)
invalid_label_c.pack(side="left", padx=10)
tokens2_c_frame = ctk.CTkFrame(master=tab2)
tokens2_c_frame.pack(expand=True)
phone_text_c = tkinter.StringVar(value="Phone Tokens: 0")
nitro_text_c = tkinter.StringVar(value="Nitro Tokens: 0")
phone_label_c = ctk.CTkLabel(master=tokens2_c_frame, textvariable=phone_text_c)
phone_label_c.pack(side="left", padx=10)
nitro_label_c = ctk.CTkLabel(master=tokens2_c_frame, textvariable=nitro_text_c)
nitro_label_c.pack(side="left", padx=10)

button_checker = ctk.CTkButton(master=tab2, width=20, text="START", command=start_checker)
button_checker.pack(expand=True)

# add widgets to tab 3
label_p = ctk.CTkLabel(master=tab3, text="Check tokens if they have payment methods.")
label_p.pack(expand=True)
entry1_p = ctk.CTkEntry(master=tab3, width=200, placeholder_text="Tokens Path")
entry1_p.pack(expand=True)

# add delay_friends slider to tab 3
delay_checker_pay_var = tkinter.DoubleVar(value=1)  
delay_checker_pay_label = ctk.CTkLabel(master=tab3, text="Delay: 1")
delay_checker_pay_label.pack(expand=True)

def set_delay_checker_pay(value):
    delay_checker_pay = int(round(value))
    delay_checker_pay_var.set(delay_checker_pay)

def update_delay_checker_pay_label(val):
    delay_checker_pay_label.configure(text="Delay: " + str(val))
delay_checker_pay_var.trace_add("write", lambda *args: update_delay_checker_pay_label(delay_checker_pay_var.get()))

delay_checker_pay_slider = ctk.CTkSlider(master=tab3, from_=1, to=10, variable=delay_checker_pay_var, command=set_delay_checker_pay)
delay_checker_pay_slider.pack(expand=True)

# add valid and invalid tokens frame to tab 3
tokens_p_frame = ctk.CTkFrame(master=tab3)
tokens_p_frame.pack(expand=True)
valid_text_p = tkinter.StringVar(value="Payment: 0")
invalid_text_p = tkinter.StringVar(value="No Payment: 0")
valid_label_p = ctk.CTkLabel(master=tokens_p_frame, textvariable=valid_text_p)
valid_label_p.pack(side="left", padx=10)
invalid_label_p = ctk.CTkLabel(master=tokens_p_frame, textvariable=invalid_text_p)
invalid_label_p.pack(side="left", padx=10)

button_checker_pay = ctk.CTkButton(master=tab3, width=20, text="START", command=start_checker_pay)
button_checker_pay.pack(expand=True)

# Set window minimum size
root.update_idletasks()
root.minsize(root.winfo_width(), root.winfo_height())

# pack tab view
tabview.pack(expand=True, fill="both")

root.mainloop()