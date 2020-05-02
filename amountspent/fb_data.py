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


from facebook_business.api import FacebookAdsApi, FacebookAdsApiBatch
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adpromotedobject import AdPromotedObject
from facebook_business.adobjects.adreportrun import AdReportRun
from facebook_business.adobjects.page import Page

from facebook_business.adobjects.customaudience import CustomAudience
from facebook_business.adobjects.business import Business
# from batch_utils import generate_batches
import datetime
import time
import logging
import requests as rq
from facebook_business.exceptions import FacebookRequestError


def compare_values(list_of_tuples):
    page_list = []
    sum_of_amount_list = []
    for i, val in enumerate(list_of_tuples):
        amount = float(val[2])
        # print(amount)
        for j in range(i+1,len(list_of_tuples)):
            # print(j)
            # print(list_of_tuples[j][1])
            if val[1] == list_of_tuples[j][1]:
                if val[1] not in page_list:
                    page_list.append(val[1])
                amount += float(list_of_tuples[j][2])
        sum_of_amount_list.append(amount)    
    sum_of_pages = list(zip(page_list,sum_of_amount_list))
    return sum_of_pages  


# Function to find the string between two strings or characters
#Function to find the string between two strings or characters
# def find_between( s, first, last ):
#     try:
#         start = s.index( first ) + len( first )
#         end = s.index( last, start )
#         return s[start:end]
#     except ValueError:
#         return ""

# #Function to check how close you are to the FB Rate Limit
# def check_limit(account_number,my_access_token):
#     check=rq.get('https://graph.facebook.com/v6.0/'+account_number+'/insights?access_token='+my_access_token)
#     print(check)
#     call=float(find_between(check.headers['x-business-use-case-usage'],'call_count":','}'))
#     cpu=float(find_between(check.headers['x-business-use-case-usage'],'total_cputime":','}'))
#     total=float(find_between(check.headers['x-business-use-case-usage'],'total_time":',','))
#     usage=max(call,cpu,total)
#     return usage


def get_data_from_api(start_date,end_date):

    Campaign_ID = []
    Page_ID = []
    Amount_Spent = []
    # Page_Name = []
    
    campaigns_all = {"Campaign_id":[],
                    "Page_id":[],
                    "Amount_spent":[],
                    }
    page_id = None
    pixel_id = None


    access_token = 'EAAUbBhxccoEBALbQCDsVMLzwdZBZAZBXApZA0t1Qy3GtjZALfs89EMFhH62f5Kp7FWvshYRTrur41B14vICAgTf1TOba8qx7SBPejdqR4gZBqZCGDo0l0WvsmzubUKKqHncpyqhSpUqcO7O0WJsB1PnSZAMY7t7awukDuIYwrisTYwZDZD'
    bussiness_account_id = '1517651558352959'
    app_secret = '7a3ad485c97dbf45ee83562bc0dcb570'
    app_id = '1437087943127681'
    start_time = datetime.datetime.now()

    FacebookAdsApi.init(app_id, app_secret, access_token)

    business =  Business(bussiness_account_id)

    # Get all ad accounts on the business account
    my_ad_account =business.get_owned_ad_accounts(fields=[AdAccount.Field.id])

    # fields = [
    #     'name',
    #     'objective',
    #     # 'spend',

    # ]
    # params = {
    #     'time_range':{'since':start_date,'until':end_date},
    #     # 'date_preset':'yesterday',
    #     'effective_status': ['ACTIVE','PAUSED'],    

    # }

    # Iterate through the adaccounts
    for account in my_ad_account:
        print(len(my_ad_account))
        # i = 0
        # Create an addaccount object from the adaccount id to make it possible to get insights
        tempaccount = AdAccount(account[AdAccount.Field.id])
        # campaigns_iter = tempaccount.get_campaigns(fields = fields, params = params)
        # CAMPAIGN_UPDATE_BATCH_LIMIT = 5

        # for campaigns in generate_batches(campaigns_iter,CAMPAIGN_UPDATE_BATCH_LIMIT):
        #     api_batch = api.new_batch()
                
        #     for i, campaign in enumerate(campaigns_iter):
        #         adset = AdAccount(campaign[Campaign.Field.id]).get_ad_sets(
        #                                     fields=['id', 'name', 'promoted_object'], 
        #                                     params = {})
        #         print(adset)
        #     api_batch.execute()    
            
            
            # spend_val.append(campaign[Campaign.Field.id])
            # print(campaign, i)
        
        
        # print(spend_val)

        # print(set(spend_val))
        


        # Grab insight info for all ads in the adaccount
        account_data = tempaccount.get_insights(params={
                                                        # 'time_increment':'1',
                                                        'time_range':{'since':start_date, 'until':end_date},
                                                        'level':'campaign',
                                                        },
                                    
                                        fields=[
                                            AdsInsights.Field.campaign_id,
                                            AdsInsights.Field.campaign_name,
                                            AdsInsights.Field.spend,

                                            ]
        )
       
        for campaign in account_data:

            try:
                #Check if you reached 75% of the limit, if yes then back-off for 5 minutes (put this chunk in your 'for ad is ads' loop, every 100-200 iterations)
                # if (check_limit(bussiness_account_id,access_token)>75):
                #     print('75% Rate Limit Reached. Cooling Time 5 Minutes.')
                #     logging.debug('75% Rate Limit Reached. Cooling Time 5 Minutes.')
                #     time.sleep(300)

                #ID OF Campaign
                # if campaign!=[]:
                # print(campaign)
                # print(len(account_data))
                campaign_id = campaign[AdsInsights.Field.campaign_id]
                campaign_spent_val = campaign[AdsInsights.Field.spend]
                # print(campaign_spent_val)
                my_camp = Campaign(campaign_id)
                print(my_camp)
                #Campaign Insights Object
                # campaign_spent_obj = my_camp.get_insights(params={}, fields=[AdsInsights.Field.spend])
                # campaign_spent = campaign_spent_obj[Campaign.Field.spend] 
                # print(campaign_spent_obj)
                #Campaign Spend value
                
                # campaigns_all["Amount_spent"].append(campaign_spent_val)

                #AdSet Object
                adset = AdAccount(my_camp[Campaign.Field.id]).get_ad_sets(
                                                fields=['id', 'name', 'promoted_object'], 
                                                params = {})
                #page and Pixel ID from Adset
                if 'page_id' in adset[0][AdSet.Field.promoted_object]:
                    page_id = adset[0][AdSet.Field.promoted_object][AdPromotedObject.Field.page_id]  
                    campaigns_all["Page_id"].append(page_id)
                    Page_ID.append(page_id)
                    # page_req = rq.head('https://facebook.com/'+page_id)
                    # print(page_req.headers)
                    # # for page in Page_ID:
                    # print(Page(page_id).api_get(fields=['name'],params={}))
                elif 'pixel_id' in adset[0][AdSet.Field.promoted_object]:
                    pixel_id = adset[0][AdSet.Field.promoted_object][AdPromotedObject.Field.pixel_id]
                    campaigns_all["Page_id"].append(pixel_id)
                    Page_ID.append(pixel_id)
                    
                else:
                    continue
 
 
                # Add Values to Dictionary
                campaigns_all["Campaign_id"].append(campaign_id)
                campaigns_all["Amount_spent"].append(campaign_spent_val)
                Campaign_ID.append(campaign_id)
                Amount_Spent.append(campaign_spent_val)                   
                # print(campaigns_all)
                time.sleep(2)  

            except KeyError as e:
                print(e)
                continue

            except Exception as e:
                print(e)
                if FacebookRequestError.api_error_code(e) == 17:
                    print(campaigns_all)
                    print("Limit Reached")
                    print("Wait 5 minutes for cooldown")
                    time.sleep(300)
                    continue
            
                

            finally:
                end_time = datetime.datetime.now()
                diff = end_time - start_time
                print(diff)
        
        tuples_of_data = list(zip(Campaign_ID,Page_ID,Amount_Spent))
        sum_amount = compare_values(tuples_of_data)
        
        print(sum_amount)
        # print(diff.total_seconds())

    return campaigns_all,sum_amount
    

        # # Iterate through all accounts in the business account
        # for campaign in ads:
        #     # # Set default values in case the insight info is empty
        #     # date = yesterdayslash
        #     # accountid = ad[AdsInsights.Field.account_id]
        #     # accountname = ""
        #     # adid = ""
        #     # adname = ""
        #     # adsetid = ""
        #     # adsetname = ""
        #     # campaignid = ""
        #     # campaignname = ""
        #     # costperoutboundclick = ""
        #     # outboundclicks = ""
        #     # spend = ""
        #     # currency = ""
        #     # return_val = ""
        #     page = ""

        #     # # Set values from insight data
        #     # if ('account_id' in ad) :
        #     #     accountid = ad[AdsInsights.Field.account_id]
        #     # if ('account_name' in ad) :
        #     #     accountname = ad[AdsInsights.Field.account_name]
        #     # if ('ad_id' in ad) :
        #     #     adid = ad[AdsInsights.Field.ad_id]
        #     # if ('ad_name' in ad) :
        #     #     adname = ad[AdsInsights.Field.ad_name]
        #     # if ('adset_id' in ad) :
        #     #     adsetid = ad[AdsInsights.Field.adset_id]
        #     # if ('adset_name' in ad) :
        #     #     adsetname = ad[AdsInsights.Field.adset_name]
        #     if ('campaign_id' in campaign) :
        #         campaignid = campaign[AdsInsights.Field.campaign_id]
        #     if ('campaign_name' in campaign) :
        #         campaignname = campaign[AdsInsights.Field.campaign_name]
        #     # campaign_spent = campaign.get_insights(
        #     #                                         params={'time_range':{'since':start_date, 'until':end_date},},
        #     #                                         fields=[AdsInsights.Field.spend]
        #     #                                         )
        #     # if ('cost_per_outbound_click' in ad) : # This is stored strangely, takes a few steps to break through the layers
        #     #     costperoutboundclicklist = ad[AdsInsights.Field.cost_per_outbound_click]
        #     #     costperoutboundclickdict = costperoutboundclicklist[0]
        #     #     costperoutboundclick = costperoutboundclickdict.get('value')
        #     # if ('outbound_clicks' in ad) : # This is stored strangely, takes a few steps to break through the layers
        #     #     outboundclickslist = ad[AdsInsights.Field.outbound_clicks]
        #     #     outboundclicksdict = outboundclickslist[0]
        #     #     outboundclicks = outboundclicksdict.get('value')
        #     if ('spend' in campaign) :
        #         spend = campaign[AdsInsights.Field.spend]
            
        #     # if ('account_currency' in ad):
        #     #     currency = ad[AdsInsights.Field.account_currency]

        #     # if ('website_purchase_roas' in ad):
        #     #     return_val = ad[AdsInsights.Field.website_purchase_roas]
        #     #     print(return_val)
        #     # spend_val.append(spend)
        #     if('place_page_name' in campaign):
        #         page = campaign[AdsInsights.Field.place_page_name]

        #     spend_val.append([campaignid,campaignname,spend,page])
        #     # Write all ad info to the file, and increment the number of rows that will display
        # #     filewriter.writerow([date, accountid, accountname, adid, adname, adsetid, adsetname, campaignid, campaignname, costperoutboundclick, outboundclicks, spend, currency])
        # #     rows += 1


        # # csvfile.close()

        # # Print report
        # # print (str(rows) + " rows added to the file " + filename)

        



if __name__ == "__main__":
    x = get_data_from_api(start_date='2020-03-01', end_date = '2020-03-15')
    print(x)