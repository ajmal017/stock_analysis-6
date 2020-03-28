import os
import pandas as pd
from zipfile import ZipFile

with ZipFile('data_collected/A2M_options_2020_03_27.zip', 'r') as zipObj:
   # Extract all the contents of zip file in different directory
   zipObj.extractall()
   #zipObj.extractall('temp')

#compression_opts = dict(method='zip', archive_name=file_out_prefix+'.csv')
#df.to_csv("data_collected/A2M_options_2020_03_27.zip", index=False, compression=compression_opts)
