import paho.mqtt.client as mqtt
import time
from tkinter import *
from tkinter import ttk

class PianoTest:
    def __init__(self, root, client):
        root.title("Piano Test")
        frame = ttk.Frame(root, width=500, height=300)
        frame.pack()

        label1 = ttk.Label(text="Piano Test")
        label1.place(x=215, y=25)

        button = ttk.Button(text="Start new test", command=self.test)
        button.place(x=360,y=260)

    def test(self):
        client.publish("finalproject/laptop", "run test")
    
    def on_connect(client, userdata, flags, rc):
        print("Connected to server (i.e., broker) with result code "+str(rc))
        client.subscribe("finalproject/rpi")
        client.message_callback_add("finalproject/rpi",PianoTest.rpi_callback)

    def rpi_callback(client, userdata, message):
        displaymessage = str(message.payload, "utf-8")
        label2 = ttk.Label(text=displaymessage)
        label2.place(x=175, y=125)

client = mqtt.Client()
client.on_connect = PianoTest.on_connect
client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
client.loop_start()

root = Tk()
PianoTest(root,client)
root.mainloop()
