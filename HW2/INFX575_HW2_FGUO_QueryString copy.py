
# coding: utf-8

# In[5]:

from boto.s3.connection import S3Connection
# conn = S3Connection('accesskey', 'secretkey')

import boto

conn = boto.connect_s3()
b = conn.get_bucket('fei-guo') 

secret_key = b.get_key('HW2/A.txt')
print secret_key

secret_key.add_email_grant('READ', 'jevinw@uw.edu')
secret_url = secret_key.generate_url(604800, query_auth=True, force_http=True)
print secret_url

