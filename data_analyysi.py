import csv
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import pytz

def parse_tempdata(file):
    #input fmi csv
    #output [ [dt1,T1] , [dt2,T2] , ... ]
    temp_list=[]
    with open(file, mode='r') as data:
        csvData=csv.reader(data)
        first=True
        for line in csvData:
            if first:
                first=False
                continue
            #end if
            h,m=line[3].split(':')
            utc_time=dt.datetime(int(line[0]),int(line[1]),int(line[2]),int(h),int(m),tzinfo=dt.timezone.utc)
            try:
                temp_list.append([utc_time,float(line[5])])
            except:
                temp_list.append([utc_time,np.nan])
            #end try except
        return temp_list
        #end for
    #end with
#end def

def tz_conv(data,tz):
    for x in data:
        x[0]=x[0].astimezone(tz)
    #end for
    return data
#end def

def avg_temp(temp_list):
    """
    Examples
    --------
    >>> avg_temp([  [ 1,[[1,2],[3,2]] ], [ 2,[[3,4],[5,6]] ]  ])
    [[1, 2.0], [2, 5.0]]
    """
    avg_temps=[[x[0],np.nanmean([p[1] for p in x[1]])] for x in temp_list]
    return avg_temps
#end def

def temp_list_to_lists(temp_list):
    #separates temps and datetimes to two lists
    times_list=[x[0] for x in temp_list]
    temps_list=[x[1] for x in temp_list]
    #end for
    return times_list, temps_list
#end def

def divide_tempdata(temp_list,f,ts_f):
    divided_list=[]
    a=[]
    time0=temp_list[0][0]
    for data in temp_list:
        time=data[0]
        if f(time)!=f(time0):
            ts=ts_f(time0)
            b=[ts]
            b.extend(a)
            divided_list.append(b)
            time0=time
            a=[]
            continue
        #end if
        a.append(data)
    #end for
    return divided_list
#end def

fy=lambda x: x.year
fm=lambda x: x.month
fd=lambda x: x.day
fh=lambda x: x.hour

def ts_y(t):
    ts=dt.datetime(t.year,1,1)
    return ts
#end def
def ts_m(t):
    ts=dt.datetime(t.year,t.month,1)
    return ts
#end def
def ts_d(t):
    ts=dt.datetime(t.year,t.month,t.day)
    return ts
#end def
def ts_h(t):
    ts=dt.datetime(t.year,t.month,t.day,t.hour)
    return ts
#end def

parsed_data=parse_tempdata('temp2019.csv')
parsed_data_eet=tz_conv(parsed_data,pytz.timezone('EET'))

divided_data=divide_tempdata(parsed_data,fm,ts_m)

tempdata_jan=divided_data[0][1:]
tempdata_july=divided_data[6][1:]

print('jan',tempdata_jan)
print('july',tempdata_july)


