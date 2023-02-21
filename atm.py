import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Bagesree@27",
  database='ATM'
)
mycursor=mydb.cursor()
sql=('CREATE DATABASE IF NOT EXISTS ATM')
mycursor.execute(sql)
mycursor.execute('use ATM')
mycursor.execute('CREATE TABLE IF NOT EXISTS BRANCH(IFSC VARCHAR(250) PRIMARY KEY NOT NULL,BRANCH_NAME VARCHAR(250))')
mycursor.execute('CREATE TABLE IF NOT EXISTS CUSTOMER(IFSC VARCHAR(250) PRIMARY KEY NOT NULL, NAME VARCHAR(250) NOT NULL,ADDRESS VARCHAR(250) NOT NULL,PHONE VARCHAR(250) NOT NULL )')
mycursor.execute('CREATE TABLE IF NOT EXISTS ACCOUNT(IFSC VARCHAR(250) PRIMARY KEY NOT NULL, AC_No INT NOT NULL,AC_Type VARCHAR(250) NOT NULL,PASSWORD INT NOT NULL,BALANCE INT)')

# Create new customer
def newcustomer():
  print('Enter the details')
  IFSC=input('Enter customer IFSC:')
  Name=input('Enter customer name:')
  Address=input('Enter customer address:')
  Phone=input('Enter customer Contact number:')
  sql='INSERT INTO CUSTOMER(IFSC,Name,Address,Phone) values(%s,%s,%s,%s)'
  values=(IFSC,Name,Address,Phone)
  mycursor=mydb.cursor()
  mycursor.execute(sql,values)
  mydb.commit()
  print('*** Data enterd succesfully ***')
  newaccount()
def newaccount():
  print('Create new acoount')
  IFSC=input('Enter customer IFSC:')
  AC_No=int(input('Enter account number:'))
  AC_type=input('Enter the account type savings or current:')
  Password=int(input('Enter the password [Use Number]:'))
  Balance = 0
  sql='INSERT INTO ACCOUNT(IFSC,AC_No,AC_type,Password,Balance) values(%s,%s,%s,%s,%s)'
  values=(IFSC,AC_No,AC_type,Password,Balance)
  mycursor=mydb.cursor()
  mycursor.execute(sql,values)
  mydb.commit()
  print('*** Account Created succesfully ***')
  main()
def searchAccount():
  AC_No=int(input('Enter your account number:'))
  password=int(input('Enter the password:'))
  mycursor=mydb.cursor()
  mycursor.execute('SELECT *FROM account WHERE AC_No=%s and password=%s;',(AC_No,password))
  data=mycursor.fetchone()
  if data:
    print("Your Account Details")
    print(data)
  else:
    print("*** Sorry ! Something went wrong, Please Try Again ***")

  main()

def withdrawAmount():
  count=3
  AC_No = int(input('Enter your account number:'))
  data = mycursor.execute('SELECT *FROM account WHERE AC_No=%s;',(AC_No,))
  data=mycursor.fetchall()
  if data:
    while True:
      password = int(input('Enter the password:'))
      mycursor.execute('SELECT *FROM account WHERE password=%s;',(password,))
      data = mycursor.fetchall()
      if data:
        amount=int(input('Please enter the amout to withdraw:'))
        mycursor.execute('SELECT BALANCE FROM ACCOUNT WHERE AC_No=%s', (AC_No,))
        myresult = mycursor.fetchone()
        for y in myresult:
          if y>amount:
            mycursor.execute('UPDATE ACCOUNT SET BALANCE = BALANCE-%s;',(amount,))
            mydb.commit()
            mycursor.execute('SELECT BALANCE FROM ACCOUNT WHERE AC_No=%s',(AC_No,))
            myresult=mycursor.fetchone()
            for y in myresult:
              print("BALANCE=",y)
          else:
            print('INSUFFICIENT BALANCE')
        print('*** TRANSACTION COMPLEATED SUCCESSFULLY ***')
        break
      else:
        print('*** Wrong Password! Please Enter a Valid Pin ***')
        count=count-1
        print('*** You are left with only',count,'attempts ***')
      if count==0:
        print("*** Your Card has been Blocked, Please Visit the Branch to activate it ***")
        break
  else:
    print('*** Sorry! Account Information Not Found, Please Try Again ***')
  main()

def depositAmount():
  count=3
  IFSC = input('Enter your IFSC CODE:')
  AC_No = int(input('Enter your account number:'))
  data = mycursor.execute('SELECT *FROM account WHERE AC_No=%s and IFSC=%s;',(AC_No,IFSC))
  data=mycursor.fetchall()
  if data:
    while True:
      password = int(input('Enter the password:'))
      mycursor.execute('SELECT *FROM account WHERE password=%s;',(password,))
      data = mycursor.fetchall()
      if data:
        amount=int(input('Please enter the amout to Deposit:'))
        mycursor.execute('UPDATE ACCOUNT SET BALANCE = BALANCE+%s;',(amount,))
        mydb.commit()
        mycursor.execute('SELECT BALANCE FROM ACCOUNT WHERE AC_No=%s', (AC_No,))
        myresult = mycursor.fetchone()
        for y in myresult:
          print("BALANCE=", y)
        print('*** TRANSACTION COMPLEATED SUCCESSFULLY ***')
        break
      else:
        print('*** Wrong Pin! Please Enter a Valid Pin ***')
        count=count-1
        print('*** You are left with only',count,'attempts ***')
      if count==0:
        print("*** Your Card has been Blocked, Please Visit the Branch to activate it ***")
        break
  else:
    print('*** Sorry! Account Information Not FOund, Please Try Again ***')
  main()
def closeaccount():
  AC_No=int(input('Enter your account number:'))
  password=int(input('Enter the password:'))
  mycursor=mydb.cursor()
  mycursor.execute('SELECT *FROM account WHERE AC_No=%s and password=%s;', (AC_No, password))
  data = mycursor.fetchone()
  if data:
    mycursor.execute('DELETE FROM account WHERE AC_No=%s and password=%s;', (AC_No, password))
    mydb.commit()
    print("Your Account Closed Succesfully")
  else:
    print("*** Sorry ! Something went wrong, Please Try Again ***")

  main()
def Changepassword():
  AC_No = int(input('Enter your account number:'))
  password = int(input('Enter the password:'))
  mycursor = mydb.cursor()
  mycursor.execute('SELECT *FROM account WHERE AC_No=%s and password=%s;', (AC_No, password))
  data = mycursor.fetchone()
  if data:
    newpassword = int(input('Enter the new password:'))
    mycursor.execute('UPDATE ACCOUNT SET PASSWORD =%s;', (newpassword,))
    mydb.commit()
    print('*** YOUR PASSWORD CHANGED SUCCESFULLY ***')
  else:
    print('*** Sorry! Account Information Not FOund, Please Try Again ***')

  main()
def main():
  print("--------------------------------------")
  print('        ATM MANAGEMENT SYSTEM         ')
  print("--------------------------------------")
  print('1.NEW CUSTOMER')
  print('2.SEARCH ACCOUNT')
  print('3.WITHDRAW AMOUNT')
  print('4.DEPOSIT AMOUNT')
  print('5.CLOSE ACCOUNT')
  print('6.CHANGE PASSWORD')
  choice=int(input("Enter the task no:"))
  if choice == 1:
    newcustomer()
  elif choice==2:
    searchAccount()
  elif choice==3:
    withdrawAmount()
  elif choice==4:
    depositAmount()
  elif choice==5:
    closeaccount()
  elif choice==6:
    Changepassword()
  else:print("*** Wrong choice ***")
main()