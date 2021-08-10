import streamlit as st
import pandas as pd
import pyrebase
import smtplib
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials


def dbstore():
  '''config = {
      "apiKey": "AIzaSyCdNjl2S-Jfhs7KddP8Zkr6I_fQA3a3qJk",
      "authDomain": "globalchambers.firebaseapp.com",
      "databaseURL": "https://globalchambers-default-rtdb.firebaseio.com",
      "projectId": "globalchambers",
      "storageBucket": "globalchambers.appspot.com",
      "messagingSenderId": "669589600381",
      "appId": "1:669589600381:web:246770209d3b3ef2379914"
  }'''
  config = {
    "apiKey": "AIzaSyAEi4bInCtTYL6a3pWUu3fvHrFhxhHTppY",
    "authDomain": "gcintroapp.firebaseapp.com",
    "databaseURL": "https://gcintroapp-default-rtdb.firebaseio.com/",
    "projectId": "gcintroapp",
    "storageBucket": "gcintroapp.appspot.com",
    "messagingSenderId": "523429056431",
    "appId": "1:523429056431:web:5315ba05f2fee71d70a95a"
  }
  firebase = pyrebase.initialize_app(config)
  db = firebase.database()
  data = {"date": date, "intro_to_1": intro_to_1, "intro_to_2": intro_to_2, "to_person1": to_person_1, \
          "to_person_2": to_person_2, "to_email_1": to_email_1, "to_email_2": to_email_2, "Intro_by": name, \
         "BCC_1":bcc_1, "BCC_2":bcc_2}
  db.child("Data").push(data)

def dbretrieve():
  config = {
      "apiKey": "AIzaSyAEi4bInCtTYL6a3pWUu3fvHrFhxhHTppY",
      "authDomain": "gcintroapp.firebaseapp.com",
      "databaseURL": "https://gcintroapp-default-rtdb.firebaseio.com/",
      "projectId": "gcintroapp",
      "storageBucket": "gcintroapp.appspot.com",
      "messagingSenderId": "523429056431",
      "appId": "1:523429056431:web:5315ba05f2fee71d70a95a"
    }
  firebase = pyrebase.initialize_app(config)
  db = firebase.database()
  complete_data = db.child("Data").get()
  format_data = complete_data.val()
  global df ,k
  df = pd.DataFrame(format_data, columns=format_data.keys())
  df = df.transpose()
  df.reset_index(drop=True, inplace=True)
  from oauth2client.service_account import ServiceAccountCredentials
  scope = ['https://spreadsheets.google.com/feeds',
          'https://www.googleapis.com/auth/drive']
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      'credentials.json', scope)
  gc = gspread.authorize(credentials)
  spreadsheet_key = '1YOmTVk4co35JFDU3msTknO3aZccdi1ccL2H8sZtjXLY'
  wks_name = 'Master'
  d2g.upload(df, spreadsheet_key, wks_name, credentials=credentials, row_names=True)
  #url = 'https://docs.google.com/spreadsheets/d/1YOmTVk4co35JFDU3msTknO3aZccdi1ccL2H8sZtjXLY/edit#gid=279434135'
  st.header("[Go To Google Sheets](https://docs.google.com/spreadsheets/d/1YOmTVk4co35JFDU3msTknO3aZccdi1ccL2H8sZtjXLY/edit#gid=279434135)")


def send_mail():
  me = 'me'
  global cc
  cc = []
  cc.append(to_email_1)
  cc.append(to_email_2)
  if(opt_mail!='none'):
    cc.append(opt_mail)

  s = smtplib.SMTP('smtp.gmail.com', 587)
  s.starttls()
  s.login(username, passwd)
  message1 = "From: %s\r\n"% username\
    + "To: %s\r\n" % to_email_1\
    + "CC: %s\r\n" % to_email_2\
    + "Subject: %s\r\n" % subject\
    + "\r\n" \
    + body
  s.sendmail(username, to_email_1, message1)

  message2 = "From: %s\r\n"% username\
    + "To: %s\r\n" % to_email_2\
    + "CC: %s\r\n" % to_email_1\
    + "Subject: %s\r\n" % subject\
    + "\r\n" \
    + body
  s.sendmail(username, to_email_2, message2)

  if(opt_mail!='none'):
    message3 = "From: %s\r\n"% username\
    + "To: %s\r\n" % opt_mail\
    + "CC: %s\r\n" % ",".join(cc)\
    + "Subject: %s\r\n" % subject\
    + "\r\n" \
    + body
    s.sendmail(username, opt_mail, message3)
  
  if(bcc_1!='none'):
    message4 = "From: %s\r\n"% username\
    + "To: %s\r\n" % bcc_1\
    + "CC: %s\r\n" % ",".join(cc)\
    + "BCC: %s\r\n" % me\
    + "Subject: %s\r\n" % subject\
    + "\r\n" \
    + body
    s.sendmail(username, bcc_1, message4)

  if(bcc_2!='none'):
    message5 = "From: %s\r\n"% username\
    + "To: %s\r\n" % opt_mail\
    + "CC: %s\r\n" % ",".join(cc)\
    + "BCC: %s\r\n" % me\
    + "Subject: %s\r\n" % subject\
    + "\r\n" \
    + body
    s.sendmail(username, bcc_2, message5)

  s.quit()

def main():
  global intro_to_1, intro_to_2, to_person_1, to_person_2,\
   to_email_1, to_email_2, intro_by, message, subject, body, date, \
   opt_mail, username, name, passwd, bcc_1, bcc_2
  st.image("logo.jpg")
  st.title("Global Chamber Intro Management System")
  st.sidebar.title("User Info:")
  name = st.sidebar.text_input("Enter Name :")
  username = st.sidebar.text_input("Enter email: ")
  passwd = st.sidebar.text_input("Enter the Password: ", type = 'password')
  st.sidebar.text_input("Designation:")
  st.sidebar.title("")  
  st.sidebar.header("Issues? Contact Developer: ")
  st.sidebar.text("Kartik Tripathi")
  st.sidebar.text("kartik@globalchamber.org")

  st.header("Intro Details")
  date = str(st.date_input("Date of Intro"))
  c1, c2 = st.beta_columns(2)
  
  intro_to_1 = c1.text_input("Intro To (Organization 1): ")
  intro_to_2 = c2.text_input("Intro To (Organization 2): ")

  to_person_1 = c1.text_input("Intro To (Person 1): ")
  to_person_2 = c2.text_input("Intro To (Person 2): ")
  to_email_1 = c1.text_input("To_email (Person 1): ")
  to_email_2 = c2.text_input("To_email (Person 2): ")

  bcc_1 = c1.text_input("BCC Person 1: (if not enter 'none') :")
  bcc_2 = c2.text_input("BCC Person 2: (if not enter 'none') :")
  opt_mail = c1.text_input("Optional email (if not enter 'none'): ")

  subject = st.text_input("Subject of the Mail: ")
  body = st.text_area("Body of the Mail: ")
  message = "Subject: "+subject+"\n\n"+body
  
  C1,C2,C3 = st.beta_columns(3)
  if C1.button("Register Data"):
    dbstore()
  if C2.button("Retrieve All Existing Data"):
    dbretrieve()
  if C3.button("Send Mail"):
    send_mail()
  footer="""<style>
  a:link , a:visited{
  color: #F63366;
  background-color: transparent;
  text-decoration: underline;
  }
  a:hover,  a:active {
  color: red;
  background-color: transparent;
  text-decoration: underline;
  }
  .footer {
  position: absolute;
  top: 100%;
  padding-top: 20%;
  left: 0;
  bottom: 0;
  width: 100%;
  background-color: transparent;
  color: grey;
  text-align: center;
  }
  </style>
  <div class="footer">
  <p>Developed by: <a style='display: block; text-align: center;' href="https://www.linkedin.com/in/kartik-tripathi-964806121/" target="_blank">Kartik Tripathi</a></p>
  </div>
  """
  st.markdown(footer,unsafe_allow_html=True)

if __name__ == '__main__':
  main()
