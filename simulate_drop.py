{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 """\
Simulates a sensor trigger. Run this to test the full pipeline\
without any physical hardware connected.\
\
Usage:  python simulate_drop.py\
        python simulate_drop.py --count 5   (simulate 5 drops)\
        python simulate_drop.py --host 192.168.1.42  (target a Pi on your network)\
"""\
import argparse\
import time\
import urllib.request\
import json\
\
parser = argparse.ArgumentParser()\
parser.add_argument("--host", default="localhost")\
parser.add_argument("--port", default=5000, type=int)\
parser.add_argument("--count", default=1, type=int)\
parser.add_argument("--delay", default=2.0, type=float,\
                    help="Seconds between drops when --count > 1")\
args = parser.parse_args()\
\
url = f"http://\{args.host\}:\{args.port\}/api/trigger"\
\
for i in range(args.count):\
    req = urllib.request.Request(url, data=b"\{\}", method="POST",\
                                 headers=\{"Content-Type": "application/json"\})\
    with urllib.request.urlopen(req) as resp:\
        data = json.loads(resp.read())\
        print(f"Drop \{i+1\}/\{args.count\} \uc0\u8594  total: \{data['total']\}")\
    if i < args.count - 1:\
        time.sleep(args.delay)}