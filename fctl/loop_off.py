from cputemp import setfanspeed, gettargetrpmpercent, gethighestcputemp, gettargetrpm, changefanmode, isfaninauto, isfaninorder


changefanmode(0,0)
changefanmode(0,1)
changefanmode(1,0)
changefanmode(1,1)



print("resetting fan config...")
changefanmode(0,0)
changefanmode(1,0)
#put into auto mode

#setfanspeed(0,3500)