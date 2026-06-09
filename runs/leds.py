#!/usr/bin/env python
# coding: utf8
import sys
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# 27 = bl; 17 = gn; 4 = rt
GPIO.setup(27, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
GPIO.output(27, GPIO.LOW)
GPIO.output(17, GPIO.LOW)
GPIO.output(4, GPIO.LOW)

if (sys.argv[1] == "aus"):
    GPIO.output(27, GPIO.LOW)
    GPIO.output(17, GPIO.LOW)
    GPIO.output(4, GPIO.LOW)
if (sys.argv[1] == "1aus"):
    GPIO.output(27, GPIO.LOW)
if (sys.argv[1] == "2aus"):
    GPIO.output(17, GPIO.LOW)
if (sys.argv[1] == "3aus"):
    GPIO.output(4, GPIO.LOW)
if (sys.argv[1] == "an"):
    GPIO.output(27, GPIO.HIGH)
    GPIO.output(17, GPIO.HIGH)
    GPIO.output(4, GPIO.HIGH)
if (sys.argv[1] == "1an"):
    GPIO.output(27, GPIO.HIGH)
if (sys.argv[1] == "2an"):
    GPIO.output(17, GPIO.HIGH)
if (sys.argv[1] == "3an"):
    GPIO.output(4, GPIO.HIGH)


if (sys.argv[1] == "startup"):
    n = 0
    while n < 5:
        GPIO.output(27, GPIO.HIGH)
        GPIO.output(17, GPIO.HIGH)
        GPIO.output(4, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(27, GPIO.LOW)
        GPIO.output(17, GPIO.LOW)
        GPIO.output(4, GPIO.LOW)
        time.sleep(2)
        n += 1
    time.sleep(1)
    GPIO.output(27, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(17, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(4, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(27, GPIO.LOW)
    time.sleep(3)
    GPIO.output(17, GPIO.LOW)
    time.sleep(3)
    GPIO.output(4, GPIO.LOW)

if (sys.argv[1] == "blink1"):
    while True:
        GPIO.output(27, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(27, GPIO.LOW)
        time.sleep(2)
if (sys.argv[1] == "blink12"):
    while True:
        GPIO.output(27, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(27, GPIO.LOW)
        GPIO.output(17, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(17, GPIO.LOW)
if (sys.argv[1] == "blink13"):
    while True:
        GPIO.output(27, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(27, GPIO.LOW)
        GPIO.output(4, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(4, GPIO.LOW)
if (sys.argv[1] == "blink17"):
    while True:
        GPIO.output(17, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(17, GPIO.LOW)
        GPIO.output(4, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(4, GPIO.LOW)
if (sys.argv[1] == "blink2"):
    while True:
        GPIO.output(17, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(17, GPIO.LOW)
        time.sleep(2)
if (sys.argv[1] == "blink3"):
    while True:
        GPIO.output(4, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(4, GPIO.LOW)
        time.sleep(2)
if (sys.argv[1] == "an1"):
    GPIO.output(27, GPIO.HIGH)
if (sys.argv[1] == "an2"):
    GPIO.output(17, GPIO.HIGH)
if (sys.argv[1] == "an3"):
    GPIO.output(4, GPIO.HIGH)
if (sys.argv[1] == "an12"):
    GPIO.output(27, GPIO.HIGH)
    GPIO.output(17, GPIO.HIGH)
if (sys.argv[1] == "an13"):
    GPIO.output(27, GPIO.HIGH)
    GPIO.output(4, GPIO.HIGH)
if (sys.argv[1] == "an17"):
    GPIO.output(4, GPIO.HIGH)
    GPIO.output(17, GPIO.HIGH)
