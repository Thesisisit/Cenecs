from tkinter import *
from decimal import Decimal
import mysql.connector as conn
root= Tk()

connectss = conn.connect(host='localhost', user='root', password='root1234', db='ceneco_old')

ba = connectss.cursor()
ba.execute("select bill_amount from bills where bill_id= 2019101396013 ")
resultba = ba.fetchall()
lis = list(resultba)
res = str(lis)[2:-3]
flot = float(str(res))
re1s = flot*2
print(re1s)
print(type(resultba))

#res = sorted(lis, key = lambda x: float(x[0]), reverse = True)
#sol = res
#resultbal = float(str(res) for res in resultba)

#res= str(resultba[0])


#    tempResult = []
 #   tempResult = resultba  

 #   tempResult1 = []
#    count = 0
#    tempresultcount = 0
#    tempresult1count = 0
#    print(resultba[0])

 #   tempString = str(resultba)
 #   tempString1 = str(tempResult1)
 #   print(tempString)

 #     while count == 0:

 #       if tempString[tempresultcount] == "(":
 # #          tempresultcount += 1
  #          print(tempString[tempresultcount])
 #       else:
 ##       tempresultcount += 1

  #      if tempString[tempresultcount] == ",":
 #           count = 1











#res = float('.'.join(str(ele) for ele in resultba))


#output = []
#for row in b:
#    output.append(float(row(11)))
        
#line1var = []
#line1var.set("[(1234.56, )]")
#result = []
#lenresult[20]
#strlength = len(line1var.get())
#i_find = 0
#while i_find < strlength:
 #   i_find += 1 
#    if(line1var[i_find] == "("):
     #   i_find += 1
    #    i_result=0
   #     while line1var[i_find] == ",":
  #              result[i_result] = result[i_find]
 #               i_result += 1
#                i_find += 1



root.mainloop()