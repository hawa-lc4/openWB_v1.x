#!/usr/bin/env python
# coding: utf8
import sys
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# 23 = bl; 24 = gn; 25 = rt
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.output(5, GPIO.LOW)
GPIO.output(6, GPIO.LOW)
GPIO.output(26, GPIO.LOW)

if (sys.argv[1] == "aus"):
    GPIO.output(5, GPIO.LOW)
    GPIO.output(6, GPIO.LOW)
    GPIO.output(26, GPIO.LOW)
if (sys.argv[1] == "1aus"):
    GPIO.output(5, GPIO.LOW)
if (sys.argv[1] == "2aus"):
    GPIO.output(6, GPIO.LOW)
if (sys.argv[1] == "3aus"):
    GPIO.output(26, GPIO.LOW)
if (sys.argv[1] == "an"):
    GPIO.output(5, GPIO.HIGH)
    GPIO.output(6, GPIO.HIGH)
    GPIO.output(26, GPIO.HIGH)
if (sys.argv[1] == "1an"):
    GPIO.output(5, GPIO.HIGH)
if (sys.argv[1] == "2an"):
    GPIO.output(6, GPIO.HIGH)
if (sys.argv[1] == "3an"):
    GPIO.output(26, GPIO.HIGH)


if (sys.argv[1] == "startup"):
    n = 0
    while n < 5:
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(6, GPIO.HIGH)
        GPIO.output(26, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)
        GPIO.output(26, GPIO.LOW)
        time.sleep(2)
        n += 1
    time.sleep(1)
    GPIO.output(5, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(6, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(26, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(5, GPIO.LOW)
    time.sleep(3)
    GPIO.output(6, GPIO.LOW)
    time.sleep(3)
    GPIO.output(26, GPIO.LOW)

if (sys.argv[1] == "blink1"):
    while True:
        GPIO.output(5, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(5, GPIO.LOW)
        time.sleep(2)
if (sys.argv[1] == "blink12"):
    while True:
        GPIO.output(5, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(6, GPIO.LOW)
if (sys.argv[1] == "blink13"):
    while True:
        GPIO.output(5, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(5, GPIO.LOW)
        GPIO.output(26, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(26, GPIO.LOW)
if (sys.argv[1] == "blink24"):
    while True:
        GPIO.output(6, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(6, GPIO.LOW)
        GPIO.output(26, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(26, GPIO.LOW)
if (sys.argv[1] == "blink2"):
    while True:
        GPIO.output(6, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(6, GPIO.LOW)
        time.sleep(2)
if (sys.argv[1] == "blink3"):
    while True:
        GPIO.output(26, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(26, GPIO.LOW)
        time.sleep(2)
if (sys.argv[1] == "an1"):
    GPIO.output(5, GPIO.HIGH)
if (sys.argv[1] == "an2"):
    GPIO.output(6, GPIO.HIGH)
if (sys.argv[1] == "an3"):
    GPIO.output(26, GPIO.HIGH)
if (sys.argv[1] == "an12"):
    GPIO.output(5, GPIO.HIGH)
    GPIO.output(6, GPIO.HIGH)
if (sys.argv[1] == "an13"):
    GPIO.output(5, GPIO.HIGH)
    GPIO.output(26, GPIO.HIGH)
if (sys.argv[1] == "an24"):
    GPIO.output(26, GPIO.HIGH)
    GPIO.output(6, GPIO.HIGH)
