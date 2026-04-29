{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 """\
Reads the HC-SR501 PIR sensor on GPIO pin 17.\
Calls on_drop() with a cooldown to avoid double-triggering.\
"""\
import threading\
import time\
\
GPIO_PIN = 17        # BCM pin connected to PIR OUT\
COOLDOWN_SEC = 3     # ignore further triggers for this many seconds after one fires\
\
def start(on_drop):\
    import RPi.GPIO as GPIO\
    GPIO.setmode(GPIO.BCM)\
    GPIO.setup(GPIO_PIN, GPIO.IN)\
\
    last_trigger = 0\
\
    def loop():\
        nonlocal last_trigger\
        while True:\
            if GPIO.input(GPIO_PIN):\
                now = time.time()\
                if now - last_trigger > COOLDOWN_SEC:\
                    last_trigger = now\
                    print("Sensor triggered \'97 recording deposit")\
                    on_drop()\
            time.sleep(0.1)\
\
    t = threading.Thread(target=loop, daemon=True)\
    t.start()\
    print(f"Sensor listening on GPIO \{GPIO_PIN\}")}