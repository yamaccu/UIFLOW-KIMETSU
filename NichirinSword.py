from m5stack import *
from m5ui import *
from uiflow import *
import machine
import imu
import time

setScreenColor(0x111111)


angle = None
hinokami = None
xa = None
ya = None
za = None

imu0 = imu.IMU()


import math
from numbers import Number




axp.setLcdBrightness(0)
pin0 = machine.Pin(0, mode=machine.Pin.OUT, pull=machine.Pin.PULL_DOWN)
pin1 = machine.Pin(33, mode=machine.Pin.OUT, pull=machine.Pin.PULL_DOWN)
pin2 = machine.Pin(32, mode=machine.Pin.OUT, pull=machine.Pin.PULL_DOWN)
pin0.on()
pin1.on()
from machine import I2S
from wav import wave

def playwav(filePath,volume):
    wav = wave.open(filePath)
    i2s = I2S(mode=I2S.MODE_MASTER | I2S.MODE_TX | I2S.MODE_DAC_BUILT_IN)
    i2s.set_dac_mode(i2s.DAC_RIGHT_EN)
    i2s.sample_rate(wav.getframerate())
    i2s.bits(wav.getsampwidth() * 8)
    i2s.nchannels(wav.getnchannels())
    i2s.volume(volume)
    while True:
        data = wav.readframes(256)
        if len(data) > 0:
            i2s.write(data)
        else:
            wav.close()
            i2s.deinit()
            break
playwav('res/PowerOn.wav',100)
pin0.off()
pin1.off()
angle = 0
hinokami = 0
while True:
  if (axp.getVinVoltage()) < 3:
    axp.powerOff()
  xa = imu0.acceleration[0]
  ya = imu0.acceleration[1]
  za = imu0.acceleration[2]
  if math.fabs(imu0.gyro[2]) < 15:
    if math.fabs(za) > 0.75:
      angle = 1
    elif math.fabs(xa) + math.fabs(ya) > 0.8:
      angle = 2
  if math.fabs(imu0.gyro[2]) > 450:
    wait_ms(50)
    if math.fabs(imu0.gyro[2]) > 450:
      if hinokami == 3:
        pin1.on()
        pin0.on()
        playwav('res/hekira.wav',100)
        pin0.off()
        pin1.off()
        hinokami = 0
      else:
        if angle == 1:
          pin2.on()
          pin0.on()
          playwav('res/minamo.wav',100)
          pin0.off()
          pin2.off()
          hinokami = (hinokami if isinstance(hinokami, Number) else 0) + 1
        elif angle == 2:
          pin2.on()
          pin0.on()
          playwav('res/takitsubo.wav',100)
          pin0.off()
          pin2.off()
          hinokami = (hinokami if isinstance(hinokami, Number) else 0) + 1
  wait_ms(2)
