import tkinter as tk
from tkinter import ttk
from functools import partial
import libserver

open_close_dict = {"o": True}
frames = {"fr_devi": None}
windows = {"Car": None, "Car2": None, "Traffic": None, "Garage": None}


def Close(self):
    windows[self].destroy()
    windows[self] = None


def __CancelCommand(event=None):
    pass

def window_device_info(device_name):
    windows[device_name] = tk.Tk()
    windows[device_name].protocol('WM_DELETE_WINDOW', __CancelCommand)
    windows[device_name].rowconfigure([0, 1], minsize=800, weight=1)
    windows[device_name].columnconfigure([1], minsize=800, weight=1)
    windows[device_name].title(f'{device_name}_info.')
    fra_Data = tk.Frame(windows[device_name], relief=tk.RAISED, borderwidth=5)                       # create frame for the device new window
    if device_name == "Traffic":
        fra_StatusT = tk.Frame(windows[device_name], relief=tk.RAISED, borderwidth=5)
        fra_Data.grid(row=0, column=0, sticky="nsw")
        fra_StatusT.grid(row=0, column=1, sticky="ne")
        lab_fraT= tk.Label(master=fra_Data,text="Data",font=40)
        lab_fraTS = tk.Label(master=fra_StatusT, text="Status", font=40,pady=10)
        lab_id = tk.Label(master=fra_Data, text="ID", font=30)
        lab_longitude = tk.Label(master=fra_Data, text="Longitude", font=30)
        lab_lattiude = tk.Label(master=fra_Data, text="Lattiude", font=30)
        ent_id = tk.Entry(master=fra_Data, width=20)
        ent_longtiude = tk.Entry(master=fra_Data, width=20)
        ent_lattiude = tk.Entry(master=fra_Data, width=20)

        lab_fraT.grid(row=0 ,column=0,sticky="n")
        lab_fraTS.grid(row=0 ,column=0,sticky="n")

        lab_id.grid(row=2, column=0, sticky="w", pady=5)
        lab_longitude.grid(row=3, column=0, sticky="w", pady=5)
        lab_lattiude.grid(row=4, column=0, sticky="w", pady=5)

        ent_id.grid(row=2, column=1, sticky="e", pady=5, padx=10)
        ent_longtiude.grid(row=3, column=1, sticky="e", pady=5, padx=10)
        ent_lattiude.grid(row=4, column=1, sticky="e", pady=5, padx=10)
        V= tk.StringVar(fra_StatusT,"1")
        lab_red = tk.Radiobutton(master=fra_StatusT, text="Red", variable=V,value='1',font=40,bg="red",width=15)
        lab_green = tk.Radiobutton(master=fra_StatusT, text="Green", variable=V,value='2',font=30,bg="green",width=15)
        ent_time = tk.Entry(master=fra_StatusT, width=20)
        lab_red.grid(row=2,column=0,sticky="sw",pady=10)
        lab_green.grid(row=3,column=0,pady=10,sticky="sw")
        ent_time.grid(row=4,column=0,pady=20,sticky="sw",padx=5)

        but_close = tk.Button(windows[device_name], text="Close", borderwidth=5, width=20,
                              command=partial(Close, device_name), fg="red", font=30)
        but_close.grid(row=0, column=1, sticky="s",pady=350)

        ent_id.insert(1, "122")
        ent_longtiude.insert(1, "1111")
        ent_lattiude.insert(1, "5555555")
        ent_time.insert(0, "1")
        ent_time.configure(state='disabled')
        ent_id.configure(state='disabled')
        ent_longtiude.configure(state='disabled')
        ent_lattiude.configure(state='disabled')


    elif device_name == "Garage":
        fra_StatusG = tk.Frame(windows[device_name], relief=tk.RAISED, borderwidth=5)
        fra_Data.grid(row=0, column=0, sticky="nsw")
        fra_StatusG.grid(row=0, column=1, sticky="ne")
        lab_fraT = tk.Label(master=fra_Data, text="Data", font=40)
        lab_fraTS = tk.Label(master=fra_StatusG, text="Status", font=40, pady=10)
        lab_id = tk.Label(master=fra_Data, text="ID", font=30)
        lab_longitude = tk.Label(master=fra_Data, text="Longitude", font=30)
        lab_lattiude = tk.Label(master=fra_Data, text="Lattiude", font=30)
        ent_id = tk.Entry(master=fra_Data, width=20)
        ent_longtiude = tk.Entry(master=fra_Data, width=20)
        ent_lattiude = tk.Entry(master=fra_Data, width=20)

        lab_fraT.grid(row=0, column=0, sticky="n")
        lab_fraTS.grid(row=0, column=0, sticky="n")

        lab_id.grid(row=2, column=0, sticky="w", pady=5)
        lab_longitude.grid(row=3, column=0, sticky="w", pady=5)
        lab_lattiude.grid(row=4, column=0, sticky="w", pady=5)

        ent_id.grid(row=2, column=1, sticky="e", pady=5, padx=10)
        ent_longtiude.grid(row=3, column=1, sticky="e", pady=5, padx=10)
        ent_lattiude.grid(row=4, column=1, sticky="e", pady=5, padx=10)

        lab_slots = tk.Label(master=fra_StatusG, text="Available Slots", font=30, width=20)
        ent_slots = tk.Entry(master=fra_StatusG, width=25,font=40)
        lab_slots.grid(row=2, column=0, sticky="sw", pady=5, padx=5)
        ent_slots.grid(row=3, column=0, pady=10, sticky="sw", padx=5)

        ent_id.insert(1,"122")
        ent_longtiude.insert(1,"1111")
        ent_lattiude.insert(1,"5555555")
        ent_slots.insert(0,"1")
        ent_slots.configure(state='disabled')
        ent_id.configure(state='disabled')
        ent_longtiude.configure(state='disabled')
        ent_lattiude.configure(state='disabled')

        but_close = tk.Button(windows[device_name], text="Close", borderwidth=5, width=15,
                              command=partial(Close, device_name), fg="red", font=30)
        but_close.grid(row=0, column=1, sticky="s", pady=350)
    else:
        fra_Data.grid(row=0, column=0, sticky="nsew")
        lab_data = tk.Label(fra_Data, text="Data", font=40)                                        #create "Data" label
        lab_data.grid(row=0, column=0, sticky="n")

        lab_id = tk.Label(master=fra_Data, text="ID", font=30)                                     #create "ID" label
        lab_longitude = tk.Label(master=fra_Data, text="Longitude", font=30)                       #create "Longitude" label
        lab_lattiude = tk.Label(master=fra_Data, text="Lattiude", font=30)                         #create "Latitude" label
        lab_type = tk.Label(master=fra_Data, text="Type", font=30)                                 #create "Type" label
        lab_speed = tk.Label(master=fra_Data, text="Speed", font=30)                               #create "Speed" label

        ent_id = tk.Entry(master=fra_Data, width=20)                                                #create "ID" entry
        ent_longtiude = tk.Entry(master=fra_Data, width=20)                                         #create "Longitude" entry
        ent_lattiude = tk.Entry(master=fra_Data, width=20)                                          #create "Latitude" entry
        ent_type = tk.Entry(master=fra_Data, width=20)                                              #create "Type" entry
        ent_speed = tk.Entry(master=fra_Data, width=20)                                             #create "Speed" entry

    # Gridding labels:
        lab_id.grid(row=2, column=0, sticky="w", pady=5)
        lab_longitude.grid(row=3, column=0, sticky="w", pady=5)
        lab_lattiude.grid(row=4, column=0, sticky="w", pady=5)
        lab_type.grid(row=5, column=0, sticky="w", pady=5)
        lab_speed.grid(row=6, column=0, sticky="w", pady=5)

    #Gridding entries:
        ent_id.grid(row=2, column=1, sticky="e", pady=5, padx=10)
        ent_longtiude.grid(row=3, column=1, sticky="e", pady=5, padx=10)
        ent_lattiude.grid(row=4, column=1, sticky="e", pady=5, padx=10)
        ent_type.grid(row=5, column=1, sticky="e", pady=5, padx=10)
        ent_speed.grid(row=6, column=1, sticky="e", pady=5, padx=10)

    #create "CLose" button:
        but_close = tk.Button(fra_Data, text="Close", borderwidth=5, width=10,
                          command=partial(Close, device_name), fg="red", font=30)
        but_close.grid(row=7, column=1, sticky="nsw", pady=250)

    #create "Textbox":
        txt_info = tk.Text(windows[device_name], borderwidth=5)
        txt_info.grid(row=0, column=1, sticky="nsew")


    #********** Configuration **********#
        ent_id.insert(1, "122")
        ent_longtiude.insert(1, "1111")
        ent_lattiude.insert(1, "5555555")
        ent_type.insert(0, "1")
        ent_speed.insert(0, "1")
        ent_id.configure(state='disabled')
        ent_longtiude.configure(state='disabled')
        ent_lattiude.configure(state='disabled')
        ent_type.configure(state='disabled')
        ent_speed.configure(state='disabled')

def Devices_info(event):
    for window_name, status in windows.items():
        if device_name == window_name:
            if not windows[device_name]:
                window_device_info(device_name)

            else:
                windows[device_name].destroy()
                window_device_info(device_name)

def devices_List():
    if open_close_dict["o"]:
        frames["fr_devi"] = tk.Frame(master=window, relief=tk.RAISED, borderwidth=5)
        lab_frD = tk.Label(master=frames["fr_devi"], text="Devices List", width=50, font=44)
        lab_car1 = tk.Label(master=frames["fr_devi"], text="Car1", font=44)
        lab_car2 = tk.Label(master=frames["fr_devi"], text="Car2", font=44)
        lab_traffic2 = tk.Label(master=frames["fr_devi"], text="Traffic Lights", font=44)
        lab_garage2 = tk.Label(master=frames["fr_devi"], text="Garages", font=44)

        frames["fr_devi"].grid(row=0, column=2, sticky="new", padx=10, pady=5)

        lab_frD.grid(row=0, column=0, sticky="nsew")
        lab_car1.grid(row=2, column=0, sticky="w", pady=5)
        lab_car2.grid(row=3, column=0, sticky="w", pady=5)
        lab_traffic2.grid(row=4, column=0, sticky="w", pady=5)
        lab_garage2.grid(row=5, column=0, sticky="w", pady=5)

        open_close_dict["o"] = False
    else:
        frames["fr_devi"].grid_forget()
        open_close_dict["o"] = True


# window
window = tk.Tk()
window.title("V2X SERVER")
window.rowconfigure([0], minsize=800, weight=1)
window.columnconfigure([2], minsize=800, weight=1)

# status
fr_Status = tk.Frame(master=window, relief=tk.RAISED, borderwidth=5, width=50, height=50)

lab_frS = tk.Label(master=fr_Status, text="Status", width=50, font=44)
lab_devices = tk.Label(master=fr_Status, text="Online Devices", font=30)
lab_cars = tk.Label(master=fr_Status, text="Cars", font=30)
lab_traffic = tk.Label(master=fr_Status, text="Traffic Lights", font=30)
lab_garage = tk.Label(master=fr_Status, text="Garages", font=30)

ent_devices = tk.Entry(master=fr_Status, width=10,font=40)
ent_cars = tk.Entry(master=fr_Status, width=10,font=40)
ent_traffic = tk.Entry(master=fr_Status, width=10,font=40)
ent_garage = tk.Entry(master=fr_Status, width=10,font=40)

fr_Status.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

lab_frS.grid(row=0, column=0, sticky="nsew")
lab_devices.grid(row=2, column=0, sticky="w", pady=5)
lab_cars.grid(row=3, column=0, sticky="w", pady=5)
lab_traffic.grid(row=4, column=0, sticky="w", pady=5)
lab_garage.grid(row=5, column=0, sticky="w", pady=5)

ent_devices.grid(row=2, column=1, sticky="e", pady=5, padx=10)
ent_cars.grid(row=3, column=1, sticky="e", pady=5, padx=10)
ent_traffic.grid(row=4, column=1, sticky="e", pady=5, padx=10)
ent_garage.grid(row=5, column=1, sticky="e", pady=5, padx=10)

###### Configuration ##################
ent_devices.insert(1, "7")
ent_cars.insert(1, "2")
ent_traffic.insert(1, "1")
ent_garage.insert(0, "1")
ent_devices.configure(state='disabled')
ent_cars.configure(state='disabled')
ent_traffic.configure(state='disabled')
ent_garage.configure(state='disabled')


# buttons & combo
fr_buttons = tk.Frame(master=window, relief=tk.RAISED)
fr_buttons.grid(row=0, column=1, sticky="nsew")

var_box = tk.StringVar()
combo_Devices = ttk.Combobox(fr_buttons, textvariable=var_box, state="readonly", width=30)
combo_Devices["values"] = ("Car", "Traffic", "Garage")
device_name = combo_Devices.get()                                                                   #Global combo name

lab_combo = tk.Label(fr_buttons, text="Devices_Info", font=44)
lab_combo.grid(row=0, column=0, sticky="nw", padx=10, pady=25)

combo_Devices.grid(row=0, column=0, sticky="n", padx=10, pady=50)
combo_Devices.bind('<<ComboboxSelected>>', Devices_info)

btn_show = tk.Button(fr_buttons, text="Show", borderwidth=5, width=10, command=devices_List, font=15)
btn_show.grid(row=0, column=2, sticky="e", pady=650, ipadx=10)

window.mainloop()
