import subprocess,os
import time
from getpw import *

fan0min = 2317
fan0safemax = 5500
fan0max = 6898

fan1min = 2502
fan1safemax = 5500
fan1max = 7450

activationtemp = 75
maxtemp = 90

def gettargetrpmpercent(activationtemp, maxtemp, currenttemp):
    return((currenttemp-activationtemp)/(maxtemp-activationtemp))
    #example: a = 30, m = 50, c = 40
    # will return 0.5 or 50% fan speed

def gettargetrpm(targetrpmpercent,minrpm,maxrpm):
    rawtarget = ((maxrpm-minrpm)*targetrpmpercent)+minrpm
    
    if rawtarget>maxrpm:
        return maxrpm
    elif rawtarget>0 and targetrpmpercent>0:
        return rawtarget
    else:
        return 0

def removewhitespaces(string):
    try:
        #print("removing whitespace from: "+string)
        integer = ""
        for i in string:
            if not i == " ": 
                integer = integer+i
        return float(integer)
    except:
        return -1

#regular output format: [Tf0A]     39.521873474121094

#process = subprocess.Popen(["cd","/Applications/Stats.app/Contents/Resources","&&", "./smc","list"], stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE)

def gethighestcputemp():
    process = os.popen('./smc list | egrep "(Te05|Te0L|Te0P|Te0S|Tf04|Tf09|Tf0A|Tf0B|Tf0D|Tf0ETf44|Tf49|Tf4A|Tf4B|Tf4D|Tf4E)"')


    alltempsstr = process.read().split("\n")
    alltempsfloat = []
    for i in alltempsstr:
        #print("temp: "+i)
        alltempsfloat.append(removewhitespaces(i[6:]))

    highesttemp = 0

    for i in alltempsfloat:
        if i>highesttemp:
            highesttemp=i
        if(i == -1):
            alltempsfloat.remove(i)
            #print("i removed")
        #print(i)
    print("highest temp cpu: "+str(highesttemp))
    return highesttemp


def getsudopassword(process):
    getsudopassword_getpw(process)
    #print("password fetched")

def setfanspeed(fan,rpm):

    #./smc fan 1 -v 4000
    #need to put in stdin to subprocess

    rpmchanger = subprocess.Popen(["sudo","./smc", "fan", str(fan),"-v", str(rpm)], stdin= subprocess.PIPE)
    getsudopassword(rpmchanger)
    
    print("fan "+str(fan)+" successfully set to rpm "+str(rpm))

def changefanmode(fan,mode):
    #mode 0 = automatic, 1 = manual
    modechanger = subprocess.Popen(["sudo", "./smc", "fan", str(fan), "-m", str(mode)])
    getsudopassword(modechanger)

def isfaninauto(fan):
    process = os.popen("./smc fans | grep Mode")
    return ("automatic" in process.readlines()[fan])

def isfaninforced(fan):
    return not isfaninauto(fan)

def getfanspeed(fan):
    process = os.popen("./smc fans | grep Target")
    #print("reading proc lines...")
    #print(process.readlines()[fan][14:])

    return float(process.readlines()[fan][14:])


def getadjustedfanspeed(fan):
    fanspeed = getfanspeed(fan)
    #print("recorded fan speed on fan "+str(fan)+": "+str(int(getfanspeed(fan))))
    if fanspeed == -1:
        return 0
    else:
        return fanspeed


def isfaninorder(fan,targetrpm):
    return isfaninforced(fan) and int(getadjustedfanspeed(fan))==int(targetrpm)

#setfanspeed(0,3500)
#setfanspeed(1,3500)
#isfaninauto(0)
#print(isfaninorder(0,0))