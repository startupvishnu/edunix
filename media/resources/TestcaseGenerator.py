import random
import os
import string
import sys
def getPathSep():
    operator=sys.platform
    if operator=="darwin" or operator=="linux":
        return '/'
    return '\\'

def getTime(timeFormat):
    hrs=int(random.random()*timeFormat)
    mn=int(random.random()*60)
    time=str(hrs)+':'+str(mn)
    yield time
    

def gen_rand_integer(start,end):
    x=int((random.random()*end) +start-1)
    yield x

def gen_rand_str(start,end):
    length=int((random.random()*end) +start-1)
    res=""
    for i in range(length):
         ind=int(random.random()*26)
         res+=string.ascii_lowercase[ind]
    yield res


    
while True:
    typ=input("Enter the data type (str/int/time) :")
    while(typ != 'int' and typ !='str' and typ!='time'):
        typ=input("type ca only be a str or int, enter again :")
    if typ=='time':
        timeFormat=int(input('enter valid time format (12/24) : '))
    else:
        start=int(input('enter the minimum digits/stringLenght value : '))
        end=int(input('enter the maximum digits/stringLenght value : '))
    size= int(input('enter how many values you want : '))
    sep=input("enter the seperator you want to use(' ','\\n'...) : ")
    fileName=input('enter thr file name you want to put them in : ')
    ans=input('do you want to specify the location [y/n] : ')
    if ans.lower()=='y':
        path=input('enter the path where you want to put this file : ')
    else:
        path=os.getcwd()
    location =path+getPathSep()+fileName+'.txt'

    while os.path.isfile(location):
            tmp=fileName
            fileName=input('file name already exists , enter another name : ')
            if tmp==fileName:
                print('rewriting the file !!!')
                break
            location =path+getPathSep()+fileName+'.txt'
    try:
        
        fp=open(location,'w')
    except Exception as e:
        print("\n\n\tError opening the file")
        print(e)

    else:
        try:
            fp.write(str(size)+'\n')
            if typ=='int':
                for i in range(size):
                    fp.write(str(next(gen_rand_integer(start,end)))+sep)
            elif typ=='str':
                for i in range(size):
                    fp.write(next(gen_rand_str(start,end))+sep)
            elif typ=='time':
                for i in range(size):
                    fp.write(next(getTime(timeFormat))+sep)
            fp.close()
            print('the file\'s location is '+location)
        except Exception as e:
            print("error while writing to the file",e)
    print('\n\npress any key ....')
    input()
