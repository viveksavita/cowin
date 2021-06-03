#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 16:54:29 2021

@author: viveksavita
"""

import pandas as pd
import requests
import json
import time
from pandas.io.json import json_normalize
from twilio.rest import Client
import json
import schedule
import urllib

#df=pd.DataFrame()







from datetime import date, timedelta , datetime


age =18
sdate = date.today() # start date
      # as timedelta

date_list = []
for i in range(7 + 1):
    day = sdate + timedelta(days=i)
    #print(day.strftime('%d-%m-%Y'))
    date_list.append(day.strftime('%d-%m-%Y'))



pin_list = [411013] #[284401,400011]#[411014,411038,411006,411028,411029,411001,412207]
final_df = pd.DataFrame([])
counter = 0

for d in date_list:
    for pin in pin_list:
        url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode='+str(pin)+'&'+'date='+d
        print(url)
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

        
        headers={'User-Agent':user_agent,} 

        request=urllib.request.Request(url,None,headers) #The assembled request
        response = urllib.request.urlopen(request)
       
        data = json.loads(response.read())
      
        
        df = pd.DataFrame( list(data['sessions']) ) #
        print(df)
        #df = pd.read_json(url)
        if not df.empty:
            final_df = final_df.append(df)
            print(final_df)
            


final_df = final_df[(final_df['min_age_limit'] == age) & (final_df['available_capacity_dose2'] > 0)]  
final_df.to_csv('/Users/viveksavita/vac/'+'testing.csv')
if not final_df.empty:
    final_df = final_df[final_df['min_age_limit'] == age]     
    final_df= final_df.astype(str) 
    
    select_df = pd.DataFrame(final_df[['date','pincode','name']], columns=['date','pincode','name'])
    print(select_df)
    select_df['pin_hospital'] = select_df['pincode']+ '-'+select_df['name']
    #select_df['new'] = select_df.groupby(['date'])['pincode'].transform(lambda x: ','.join((x))).reset_index(drop=True)
    select_df['hospital'] = select_df.groupby(['date'])['pin_hospital'].transform(lambda x: ','.join((x))).reset_index(drop=True)
    select_df.drop(columns=['pincode','name'], inplace=True)
    select_df = select_df.drop_duplicates( ) 
    print(select_df)
    sms_df = select_df[['date','hospital']].to_dict()
    print(sms_df)
    select_df['Slot'] = select_df.values.tolist()  
    sms=json.dumps(select_df[['Slot']].to_dict())
    print(sms)
    file = 'Vacc_centre_pin_'+datetime.today().strftime('%d_%m_%Y_%H_%M_%S')+'.csv'
    final_df.to_csv('/Users/viveksavita/vac/'+file)
    
    
    
    account_sid = 'AC91586966368a1f853255e6989d387591'
    auth_token = '7dbe6dd3311af7b36fbac19ac7fb9170'
    
    client = Client(account_sid, auth_token)
    
    print(sms)
    message = client.messages.create(
                          body='Available on date and at pincode :'+sms,
                          from_='whatsapp:+14155238886',
                          to='whatsapp:+917769872169'
                      )
        
        
else:
    print('Not available slot')

final_df.to_csv('/Users/viveksavita/vac/test_vac_list.csv')

print('Script is completed') 

   