import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from django.core.exceptions import ObjectDoesNotExist
import os

import datetime
import mysql.connector
import requests
import csv
from .models import UserRegister,EmailVerify
import math,random

email_address = os.getenv('EMAIL_ADD')
password = os.getenv('EMAIL_PASS')

auth_key = os.getenv('AUTH_KEY')
url = os.getenv('URL')
def code_generator():
    digits="0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[random.randint(0,9)]
    print(OTP)
    return OTP

def delete_late():
    connect = mysql.connector.connect(
        user=os.getenv('USER'), password=os.getenv('PASS'), database=os.getenv('DB'))
    con = connect.cursor()
    con.execute(f"select email,date_joined from hello_userregister where verified=false")
    result = con.fetchall()
    if len(result)>0:
        for i in result:
            print('scaning')
            email = i[0]
            print(email)
            date_joined = i[1] 
            max_time = datetime.timedelta(minutes=5)
            delete_on = date_joined + max_time
            check_now = datetime.datetime.now()
            if check_now > delete_on:
                email = f"\'{email}\'"
                print(email)
                try:
                    user = UserRegister.objects.get(Email=email)
                    try:
                        verify = EmailVerify.objects.get(Email=user)
                        print('deleting verify code')
                        verify.delete()
                        verify.save()
                    except ObjectDoesNotExist:
                        print('not exist verify')
                    print('deleting user')
                    user.delete()
                    user.save()
                    print(email)
                except ObjectDoesNotExist:
                    print('not exist')


                print('done')
            else:
                print('not found')
    print('done scaning')
    connect.commit()
    connect.close()


def send_mail(email,verification_code):
    msg=EmailMessage()
    msg['From'] = formataddr(('Prabal Pathak',email_address))
    msg['To'] = formataddr(('Prabal',email))
    msg['Subject'] = 'Verify Mail'
    html_content = f"""
            <html>
                <head>
                    <title>new</title>
                </head>
                <body>
                    <div style='font-family: 'Vardana',Sans-sariff;'>
                    <h1>Welcome</h1>to the world of <h2>webprogramming.</h2> Please verify You mail with <p style='font-size:50px;
                                                                                                            font-family:"Lucid Hardwriting",cursive;'>
                                                                                                            CODE {verification_code}</p>
                    <a href='http://127.0.0.1:8000'>Web World</a>
                    <h3>This code is valid for 10 minutes<h3>
                    </div>
                </body>
            </html>
            """
    msg.add_alternative(html_content,subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login(email_address,password)
        smtp.send_message(msg)
        print('done')

def send_sms(name,code,phone):
    phone = int(phone)
    message = f"Hello {name} , Your account Verification Code {code} Please Verify Yourself"
    payload = f"sender_id=FSTSMS&message={message}&language=english&route=p&numbers={phone}"
    headers = {
            'authorization': auth_key,
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
            }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

def list_name(csv_file):
    with open(csv_file) as csv_file:
        csvfile = csv.DictReader(csv_file)
        field = csvfile.fieldnames
        first_name = []
        last_name = []
        for row in csvfile:
            first_name.append(row[field[0]])
            last_name.append(row[field[1]])
    return first_name, last_name

