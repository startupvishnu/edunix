a,b,x = map(int,input().split())
length = a + b
a,b=a-1,b-1
res = '10'
x-=1

while x >=2 and a and b:
    res+='10'
    a-=1
    b-=1
    x-=2
if x==0:
    res = '1'*a + res + '0'*b
else:
    if a >= b:
        res =('1'*(a-1)) + res + ('0'*b)+'1'
    else:
        res = '0'+('1'*a)+res+('0'*b)

print(res)
