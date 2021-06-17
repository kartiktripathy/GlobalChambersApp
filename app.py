import streamlit as st
import pandas as pd
import pyrebase
import smtplib
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials


def dbstore():
  config = {
      "apiKey": "AIzaSyCdNjl2S-Jfhs7KddP8Zkr6I_fQA3a3qJk",
      "authDomain": "globalchambers.firebaseapp.com",
      "databaseURL": "https://globalchambers-default-rtdb.firebaseio.com",
      "projectId": "globalchambers",
      "storageBucket": "globalchambers.appspot.com",
      "messagingSenderId": "669589600381",
      "appId": "1:669589600381:web:246770209d3b3ef2379914"
  }
  firebase = pyrebase.initialize_app(config)
  db = firebase.database()
  data = {"company": company, "main_contact": main_contact, "target": target, "last_aff_date": last_aff, 
    "date": date, "intro_to": intro_to, "From": From, "to_person": to_person, 
    "intro by": intro_by, "commision": commission, "From_email": From_email, "To_email": to_email}
  db.child("Data").push(data)

def dbretrieve():
  config = {
      "apiKey": "AIzaSyCdNjl2S-Jfhs7KddP8Zkr6I_fQA3a3qJk",
      "authDomain": "globalchambers.firebaseapp.com",
      "databaseURL": "https://globalchambers-default-rtdb.firebaseio.com",
      "projectId": "globalchambers",
      "storageBucket": "globalchambers.appspot.com",
      "messagingSenderId": "669589600381",
      "appId": "1:669589600381:web:246770209d3b3ef2379914"
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
  global li
  li = [to_email,From_email]
  for dest in li:
      s = smtplib.SMTP('smtp.gmail.com', 587)
      s.starttls()
      s.login('cesartrabanco@globalchamber.org', 'Intros2025')
      s.sendmail('cesartrabanco@globalchamber.org', dest, message)
      s.quit()

def main():
  st.image("/content/drive/MyDrive/gcapp/logo.jpg")
  st.title("The Global Chambers Intro DBMS")
  
  st.header("Basic Details")
  col1, col2 = st.beta_columns(2)
  global company, main_contact, intro_by, intro_to, \
  main_contact, target, last_aff, date, From, to_person, commission, From_email, to_email, message
  company = col1.text_input("Enter the name of the company :")
  main_contact = col2.text_input("Who is the main contact ?")
  target = col1.text_input("Target of the Company")
  last_aff = col2.text_input("Last Affiliate Date")

  st.header("Intro Details")
  c1, c2 = st.beta_columns((1, 2))
  date = c1.text_input("Date of Intro")
  intro_to = c2.text_input("Intro to (Organisation)")
  From = c1.text_input("From")
  From_email = c1.text_input("From_email")
  to_person = c2.text_input("To (Person)")
  to_email = c2.text_input("To_email")
  intro_by = c2.text_input("Intro By")
  commission = c1.slider("Commission Opportunity (%)", value = 10 )
  message = st.text_area("Enter the message:")
  C1,C2,C3 = st.beta_columns(3)
  if C1.button("Register Data"):
    dbstore()
  if C2.button("Retieve All Existing Data"):
    dbretrieve()
  if C3.button("Send Mail"):
    send_mail()

if __name__ == '__main__':
  main()

  