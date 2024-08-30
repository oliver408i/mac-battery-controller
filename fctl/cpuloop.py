

from cputemp import setfanspeed, gettargetrpmpercent, gethighestcputemp, gettargetrpm, changefanmode, isfaninauto, isfaninorder
import time

targetrpm0 = 0
targetrpm1 = 0
# need definition for loop

timeinterval = 2
#1 second between loop parse

state = 0
# different states correspond to levels of the activation curve. 0 is gentle curve and so on

fan0min = 2317
fan0safemax = 5500
fan0max = 6898

fan1min = 2502
fan1safemax = 5500
fan1max = 7450


gentleactivationtemp = 70
gentlemaxtemp = 100

curveswitchtemp = 85

steepactivationtemp = 60
steepmaxtemp = 90

changefanmode(0,0)
changefanmode(0,1)
changefanmode(1,0)
changefanmode(1,1)


if input("loop or reset? 0-1? ") == "0":
    while(True):

        time.sleep(timeinterval)


        highestcputemp = gethighestcputemp()
        #assign variables to save compute

        if not isfaninorder(0,targetrpm0):
            changefanmode(0,0)
            changefanmode(0,1)
            print("fan 0 not in order; fixing...")
        else:
            print("fan 0 config checks out!")
        if not isfaninorder(1,targetrpm1):
            changefanmode(1,0)
            changefanmode(1,1)
            print("fan 1 not in order; fixing...")
        else:
            print("fan 1 config checks out!")

        #fix fan config



        if highestcputemp < steepactivationtemp:
            if state != 0:
                print("\nfans now in gentle mode\n")
            state = 0

        #if temp is below threshold switch back into gentle mode

        if highestcputemp > curveswitchtemp:
            if state != 1:
                print("\nfans now in aggressive mode\n")
            state = 1

        #if temp crosses boundary switch into agressive mode



        if state == 0:
            targetrpmpercent = gettargetrpmpercent(gentleactivationtemp,gentlemaxtemp,highestcputemp)
        #gentle fan mode (78-100)

        if state == 1:
            targetrpmpercent = gettargetrpmpercent(steepactivationtemp,steepmaxtemp,highestcputemp)
        #steep fan mode (60-90)

        #assign terget rpm percent        


        print(targetrpmpercent)
    

        targetrpm0 = int(gettargetrpm(targetrpmpercent,fan0min,fan0max))
        targetrpm1 = int(gettargetrpm(targetrpmpercent,fan1min,fan1max))

        #calculate target rpm for each fan

        print(targetrpm0,targetrpm1)


        setfanspeed(0,targetrpm0)
        setfanspeed(1,targetrpm1)

        #set fan speed

        print("\n")

        
else:
    print("resetting fan config...")
    changefanmode(0,0)
    changefanmode(1,0)
    #put into auto mode

#setfanspeed(0,3500)