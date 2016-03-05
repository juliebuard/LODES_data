# load the data 
import pandas as pd

lodes_data = pd.read_csv('ca_od_main_JT00_2013.csv')
data = pd.DataFrame(lodes_data, columns = ['w_geocode','h_geocode','S000','SA01','SA02','SA03','SE01','SE02','SE03','SI01','SI02','SI03','createdate'])


# convert the geocodes into strings 
for i in range(len(data)):
    data.loc[i,'str w_geoc'] = 'g0' + str(data['w_geocode'][i])
    data.loc[i,'str h_geoc'] = 'g0' + str(data['h_geocode'][i])
    
data.to_pickle('entire_lodes_data_with_string_w_h_geocode.pkl')
data.to_csv('entire_lodes_data_with_string_w_h_geocode.csv')


### merge with the shapefile 

##merge for the work geocodes
df1 = pd.read_csv("entire_lodes_data_with_string_w_h_geocode.csv")
df2 = pd.read_csv("shapefile_with_string_16_geocode.csv")
merged = df1.merge(df2,left_on='str w_geoc', right_on='str_16_geoc', how="inner")
#rename the columns 
merged.rename(columns={'shape area': 'shape_area_w', 'shape length': 'shape_length_w'}, inplace=True)
merged.rename(columns={'lat': 'lat_w', 'lon': 'lon_w'}, inplace=True)

## merged for the home geocodes
merged = merged.merge(df2,left_on='str h_geoc', right_on='str_16_geoc', how="inner")
merged.rename(columns={'shape area': 'shape_area_h', 'shape length': 'shape_length_h'}, inplace=True)
merged.rename(columns={'lat': 'lat_h', 'lon': 'lon_h'}, inplace=True)

#save the results 
merged.to_csv("merged_entire_w_h_with_shapefiles.csv", index=False)


### compute the great circle distance 

import geopy
from geopy.distance import great_circle

for i in range (0,len(merged)):
    w_loc = (merged['lat_w'][i],merged['lon_w'][i])
    h_loc = (merged['lat_h'][i],merged['lon_h'][i])
    merged.loc[i,'GC_distance_w_h_miles'] = great_circle(w_loc, h_loc).miles
    merged.loc[i,'GC_distance_w_h_kilometers'] = (great_circle(w_loc, h_loc).meters)/1000

merged.to_csv("entire_lodes_readyToWork_shapefile_distance_h_w.csv", index=False)

