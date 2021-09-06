# import mysql
import serial
# import RPi.GPIO as GPIO
import time, sys
import datetime
import mysql.connector
from mysql.connector import Error

from pip._vendor.distlib.compat import raw_input

# P_BUTTON =24 #BUTTON, adapt to your writing
# def setup():
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(P_BUTTON, GPIO.IN,GPIO_UP)


#SERIAL_PORT = "/dev/cu.usbserial"
#com_port in windows
SERIAL_PORT = "/dev/tty.usbserial-1420"
ser = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=3)
# setup()

# print("its working")
temp1 = "AT+CMGF=1\r"
ser.write(temp1.encode())
time.sleep(0.5)


def total_m():
    ser.read(ser.inWaiting())
    temp2 = "AT+CPMS?\r"
    #time.sleep(0.25)
    ser.write(temp2.encode())
    time.sleep(0.5)
    reply = ser.read(ser.inWaiting())
    time.sleep(0.25)
    print(reply)
    if (reply[24] >= 48) and (reply[24] <= 57):
        temp3 = chr(reply[23:25])

    else:
        temp3 = chr(reply[23])

    return temp3
def data_insert(q, w, e, r, t):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",
                database="test")
            mycursor = mydb.cursor()

            sql = "INSERT INTO panel_health (panel_id,zone,type,date,time) VALUES (%s,%s,%s,%s,%s)"




            val = (q, w, e, r, t)
            mycursor.execute(sql, val)
            mydb.commit()
            print("into sql")



        except mysql.connector.Error as err:
            print("Failed to create table in MySQL: {}".format(err))
        finally:
            if (mydb.is_connected()):
                mycursor.close()
                mydb.close()
                print("MySQL connection is closed")
def string_manipulation(d):
    if ("ZONE=" in str_reply):

        print("in IF block")

        x = int(str_reply.find(',"+'))
        y = int(str_reply.find('ZONE='))
        z = int(str_reply.find('OK'))

        ph_no_ = str_reply[x + 2:x + 15]
        zone_ = str_reply[y + 5:y + 7]
        type_ = str_reply[y + 8:y + 13]
        date_ = str_reply[x+21:x+29]
        time_ = str_reply[x+30:x+38]
        print(ph_no_)
        print(zone_)
        print(type_)
        print(date_)
        print(time_)
        data_insert(ph_no_,zone_,type_,date_,time_)


# temp5='AT+CMGS="+916206345803"\r\n'
# ser.write(temp5.encode())
# time.sleep(1)
# temp = "kaisey ho"
# ser.write(temp.encode()+chr(26).encode())                              if reply!=" ":(to ask )

ser.read(ser.inWaiting())
total = int(total_m())

while 1:

    print("Listening for incoming SMS...")
    # total=total_m()
    # index = 1

    print(total)
    if 1 > total:
        print("no msg")
        total = int(total_m())

    else:

        #temp2 = "AT+CMGR=" + str(total) + "\r"
        temp2 = 'AT+CMGL="ALL"\r'
        ser.write(temp2.encode())
        time.sleep(0.6)
        reply = ser.read(ser.inWaiting())
        str_reply = str(reply)
        print(str_reply)
        # print(str_reply[86])
        # print(str_reply.index("ALARM"))
        # print(str_reply.index("11.03.19"))
        # print(str_reply.index("16:05"))
        # print(str_reply.index("+91"))

        print("SMS Received.  Content:- ")
        string_manipulation(str_reply)


        #print(reply)
        time.sleep(0.5)
        temp3 = "AT+CMGD=" + str(total) + "\r"
        recheck = int(total_m())
        time.sleep(0.25)
        if recheck > total:
            total = recheck + 2
            print("rechecking has ben done")

        ser.write(temp3.encode())
        time.sleep(0.5)
        ser.read(ser.inWaiting())
        time.sleep(0.5)
        total = total - 1



