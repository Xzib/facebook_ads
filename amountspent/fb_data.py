# Copyright 2014 Facebook, Inc.

# You are hereby granted a non-exclusive, worldwide, royalty-free license to
# use, copy, modify, and distribute this software in source code or binary
# form for use in connection with the web services and APIs provided by
# Facebook.

# As with any software that integrates with the Facebook platform, your use
# of this software is subject to the Facebook Developer Principles and
# Policies [http://developers.facebook.com/policy/]. This copyright notice
# shall be included in all copies or substantial portions of the software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import sys
sys.path.append('C:\\Users\\syedz\\Anaconda3\\envs\\facebook_api\\lib\\site-packages') # Replace this with the place you installed facebookads using pip
sys.path.append('C:\\Users\\syedz\\Anaconda3\\envs\\facebook_api\\lib\\site-packages\\facebook_business-6.0.2-py3.8.egg') # same as above


from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adsinsights import AdsInsights 
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.business import Business
import datetime
import csv
from functools import partial
# FacebookAdsApi.init(access_token=access_token)

def get_data_from_api(start_date,end_date):

    spend_val = []

    access_token = 'EAAUbBhxccoEBACYABVi5uXdZCfQ94oZAM1B8s0ZB32qsCShZAW3ShDZAstZClenWH0s4bD55aVZCpTgokZA9kfwCJvsKBPD6dmSu2lHGZAf0U2OY2kjphsw8MpZAtgZCUs5KRyV2PXWJoum9vFA4bnUa8Gy6ubTlo7xxROB55qXAKEU5AZDZD'
    bussiness_account_id = '1517651558352959'
    app_secret = '7a3ad485c97dbf45ee83562bc0dcb570'
    app_id = '1437087943127681'

    FacebookAdsApi.init(app_id, app_secret, access_token)

    business =  Business(bussiness_account_id)
    # Get yesterday's date for the filename, and the csv data
    # yesterdaybad = datetime.datetime.now() - datetime.timedelta(days=1)
    # yesterdayslash = yesterdaybad.strftime('%m/%d/%Y')
    # yesterdayhyphen = yesterdaybad.strftime('%m-%d-%Y')

    # Define the destination filename
    # filename = yesterdayhyphen + '_fb.csv'
    # filelocation = "./"+ filename

    # Get all ad accounts on the business account
    my_ad_account =business.get_owned_ad_accounts(fields=[AdAccount.Field.id])

    # Open or create new file 
    # try:
    #     csvfile = open(filelocation , 'w+')
    # except:
    #     print ("Cannot open file.")


    # To keep track of rows added to file
    # rows = 0

    # try:
    # # Create file writer
    #     filewriter = csv.writer(csvfile, delimiter=',')
    # except Exception as err:
    #     print(err)

    # Iterate through the adaccounts
    for account in my_ad_account:
        # Create an addaccount object from the adaccount id to make it possible to get insights
        tempaccount = AdAccount(account[AdAccount.Field.id])

        # Grab insight info for all ads in the adaccount
        ads = tempaccount.get_insights(params={#'date_preset':'last_30d',
                                            #'time_increment':'monthly',
                                            'time_range':{'since':start_date, 'until':end_date},
                                            'level':'ad'
                                            },
                                    fields=[AdsInsights.Field.account_id,
                                            #AdsInsights.Field.account_name,
                                            #AdsInsights.Field.ad_id,
                                            #AdsInsights.Field.ad_name,
                                            #AdsInsights.Field.adset_id,
                                            #AdsInsights.Field.adset_name,
                                            #AdsInsights.Field.campaign_id,
                                            #AdsInsights.Field.campaign_name,
                                            #AdsInsights.Field.cost_per_outbound_click,
                                            #AdsInsights.Field.outbound_clicks,
                                            AdsInsights.Field.spend,
                                            # AdsInsights.Field.account_currency,
                                            #AdsInsights.Field.website_purchase_roas,
                                            ]
        )

        # Iterate through all accounts in the business account
        for ad in ads:
            # # Set default values in case the insight info is empty
            # date = yesterdayslash
            # accountid = ad[AdsInsights.Field.account_id]
            # accountname = ""
            # adid = ""
            # adname = ""
            # adsetid = ""
            # adsetname = ""
            # campaignid = ""
            # campaignname = ""
            # costperoutboundclick = ""
            # outboundclicks = ""
            # spend = ""
            # currency = ""
            # return_val = ""

            # # Set values from insight data
            # if ('account_id' in ad) :
            #     accountid = ad[AdsInsights.Field.account_id]
            # if ('account_name' in ad) :
            #     accountname = ad[AdsInsights.Field.account_name]
            # if ('ad_id' in ad) :
            #     adid = ad[AdsInsights.Field.ad_id]
            # if ('ad_name' in ad) :
            #     adname = ad[AdsInsights.Field.ad_name]
            # if ('adset_id' in ad) :
            #     adsetid = ad[AdsInsights.Field.adset_id]
            # if ('adset_name' in ad) :
            #     adsetname = ad[AdsInsights.Field.adset_name]
            # if ('campaign_id' in ad) :
            #     campaignid = ad[AdsInsights.Field.campaign_id]
            # if ('campaign_name' in ad) :
            #     campaignname = ad[AdsInsights.Field.campaign_name]
            # if ('cost_per_outbound_click' in ad) : # This is stored strangely, takes a few steps to break through the layers
            #     costperoutboundclicklist = ad[AdsInsights.Field.cost_per_outbound_click]
            #     costperoutboundclickdict = costperoutboundclicklist[0]
            #     costperoutboundclick = costperoutboundclickdict.get('value')
            # if ('outbound_clicks' in ad) : # This is stored strangely, takes a few steps to break through the layers
            #     outboundclickslist = ad[AdsInsights.Field.outbound_clicks]
            #     outboundclicksdict = outboundclickslist[0]
            #     outboundclicks = outboundclicksdict.get('value')
            if ('spend' in ad) :
                spend = ad[AdsInsights.Field.spend]
            
            # if ('account_currency' in ad):
            #     currency = ad[AdsInsights.Field.account_currency]

            # if ('website_purchase_roas' in ad):
            #     return_val = ad[AdsInsights.Field.website_purchase_roas]
            #     print(return_val)
            spend_val.append(spend)

            # Write all ad info to the file, and increment the number of rows that will display
        #     filewriter.writerow([date, accountid, accountname, adid, adname, adsetid, adsetname, campaignid, campaignname, costperoutboundclick, outboundclicks, spend, currency])
        #     rows += 1


        # csvfile.close()

        # Print report
        # print (str(rows) + " rows added to the file " + filename)
        return spend_val 



if __name__ == "__main__":
    get_data_from_api(start_date='2020-04-01', end_date = '2020-04-14')