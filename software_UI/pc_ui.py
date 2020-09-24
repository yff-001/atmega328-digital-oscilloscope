# works with adc_reading.ino

import serial, pygame, os, sys, pygame.gfxdraw
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("ATmega328 DSO")

# frame for pygame
wave_frame =tk.Frame(master=root, width=1000, height=500)
wave_frame.grid(row=0, column=0, rowspan=4, padx=0, pady=0)
# embed pygame display 
os.environ['SDL_WINDOWID'] = str(wave_frame.winfo_id())

# set up serial
ser = serial.Serial('com3', 115200)

# set up pygame
main_clock = pygame.time.Clock()
pygame.init()
width, height = 1000, 500
s = pygame.display.set_mode((width, height))
r,g,b = 0,0,0
s.fill((240,240,240))

# event handlers
def set_prescaler():
    prescaler_value = prescaler.get()
    # put int value in a list first, pass it to bytes(), then pass it to ser.write()
    v = int(prescaler_value)
    ser.write(bytes([v]))
        
def set_run_stop():
    ser.write(bytes([170]))

# trigger setting:
side_frame0 = tk.LabelFrame(master=root, text=" Trigger Setting")
side_frame0.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
label = tk.Label(master=side_frame0, text="")
label.pack()

# horizontal control:
side_frame1 = tk.LabelFrame(master=root, text="Horizontal Control")
side_frame1.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
# prescaler--
prescaler = ttk.Combobox(master=side_frame1, values=[2,4,8,16,32,64,128])
prescaler.current(6)    # current() method controls defualt item shown in list
prescaler.pack()

# vertical control:
side_frame2 = tk.LabelFrame(master=root, text="Vertical Control")
side_frame2.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
label = tk.Label(master=side_frame2, text="")
label.pack()

# run/stop button
run_stop_button = tk.Button(master=root, text='Run/Stop', command=set_run_stop)
run_stop_button.grid(row=3, column=1, padx=5, pady=5, sticky='nsew')

button1 = tk.Button(master=side_frame1, text='Set', command=set_prescaler)
#sticky in e&w directions extends button to occupy entire grid cell
button1.pack(fill=tk.X)

#button2 = tk.Button(master=root, text='Stop', command=stop_wave)
#button2.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

def main():
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            s.fill((240,240,240))

            if ser.in_waiting > 0:
                # x is a series of bytes, turns out to be iterable
                x = ser.read(1000)
                # maybe I need threading to seperate data handling and rendering
                for i,j in enumerate(x):
                    # waveform display occupies 256 pixels
                    pygame.gfxdraw.pixel(s, i, 376-j, (128,0,255))

            pygame.display.update()
            root.update()
    except:
        ser.close()
        pygame.quit()

if __name__ == "__main__":
    main()


# In[ ]:


import serial
import tkinter as tk

root = tk.Tk()
s = serial.Serial('com6', 115200)

def set_value():
    s.write(bytes([2]))
    s.close()
    
b1 = tk.Button(text="Set", width=100, height=25, command=set_value)
b1.grid(padx=20, pady=20)

root.mainloop()


# In[ ]:


# optionmenu sample

import tkinter as tk

root = tk.Tk()

p_v = [2,4,8,16,32,64,128]
v = tk.StringVar(root)
v.set(p_v[0])
prescaler = tk.OptionMenu(root, v, *p_v)
prescaler.pack()

def set_value():
    print(v.get(), type(v.get()))
    
b1 = tk.Button(text="Set", width = 10, height = 5, command=set_value)
b1.pack()

root.mainloop()


# In[ ]:


# combobox sample

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
p = ttk.Combobox(root, values = [2,4,8,16,32,64,128])
p.current(0)
p.pack()

def set_value():
    print(p.get(), type(p.get()))
    
b1 = tk.Button(text="Set", width = 10, height = 5, command=set_value)
b1.pack()

root.mainloop()

