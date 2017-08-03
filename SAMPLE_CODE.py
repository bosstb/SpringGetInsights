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

from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.campaign import Campaign
from facebookads.adobjects.adset import AdSet
from facebookads.adobjects.adcreative import AdCreative
from facebookads.adobjects.ad import Ad
from facebookads.adobjects.adpreview import AdPreview
from facebookads.api import FacebookAdsApi

access_token = 'EAAFmddf9xhUBAOxXD2nZCdVJZCMZBiwS25jDi2ZAaZCPBZCOppTWdQd9TZCqq8J1SK0ZA62xNOf5ZAhzapZCXjjay3LBFZAlZAtJrvmIx3VyfxF4ThKeZCuYar49tCeprxhjDi5nfPZCurwSCZAOPyXr0XmrmFgArBNbxGgV9SojFq5D45C7IAeYZAuzUgOv5ZBRdAWmtZB2Y8kalnl2TyyARmN4j5thJkVplVYl9MKRgZD'
ad_account_id = '102768263761596'
app_secret = '507bab92fb9fde79b9ad20823bea87a0'
page_id = '1994110527537082'
FacebookAdsApi.init(access_token=access_token)

fields = [
]
params = {
    'name': 'My Campaign',
    'buying_type': 'AUCTION',
    'objective': 'PAGE_LIKES',
    'status': 'PAUSED',
}
campaign = AdAccount(ad_account_id).create_campaign(
    fields=fields,
    params=params,
)
print 'campaign', campaign

campaign_id = campaign.get_id()
print 'campaign_id:', campaign_id, '\n'

fields = [
]
params = {
    'name': 'My AdSet',
    'optimization_goal': 'PAGE_LIKES',
    'billing_event': 'IMPRESSIONS',
    'bid_amount': '20',
    'promoted_object': {'page_id': page_id},
    'daily_budget': '1000',
    'campaign_id': campaign_id,
    'targeting': {'geo_locations':{'countries':['US']}},
    'status': 'PAUSED',
}
ad_set = AdAccount(ad_account_id).create_ad_set(
    fields=fields,
    params=params,
)
print 'ad_set', ad_set

ad_set_id = ad_set.get_id()
print 'ad_set_id:', ad_set_id, '\n'

fields = [
]
params = {
    'name': 'My Creative',
    'object_id': page_id,
    'title': 'My Page Like Ad',
    'body': 'Like My Page',
    'image_url': 'http://www.facebookmarketingdevelopers.com/static/images/resource_1.jpg',
}
creative = AdAccount(ad_account_id).create_ad_creative(
    fields=fields,
    params=params,
)
print 'creative', creative

creative_id = creative.get_id()
print 'creative_id:', creative_id, '\n'

fields = [
]
params = {
    'name': 'My Ad',
    'adset_id': ad_set_id,
    'creative': {'creative_id':creative_id},
    'status': 'PAUSED',
}
ad = AdAccount(ad_account_id).create_ad(
    fields=fields,
    params=params,
)
print 'ad', ad

ad_id = ad.get_id()
print 'ad_id:', ad_id, '\n'

fields = [
]
params = {
    'ad_format': 'DESKTOP_FEED_STANDARD',
}
print Ad(ad_id).get_previews(
    fields=fields,
    params=params,
)


