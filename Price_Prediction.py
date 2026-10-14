#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


# In[2]:


df=pd.read_excel(r"C:\Users\anami\Downloads\Data_Train.xlsx")


# In[3]:


df.head()


# In[4]:


df.shape


# In[5]:


df.info()


# In[6]:


# converting to datetime datatype
df['Date_of_Journey']=pd.to_datetime(df['Date_of_Journey'])


# In[7]:


df['journey_day']=df['Date_of_Journey'].dt.day


# In[8]:


#df["Journey_day"]=pd.to_datetime(df.Date_of_Journey,format="%d/%m/%Y").dt.day


# In[9]:


#Day of week
df['journey_Dow']=df['Date_of_Journey'].dt.dayofweek


# In[10]:


# month
df['journey_month']=df['Date_of_Journey'].dt.month


# In[11]:


# month name
df['journey_month name']=df['Date_of_Journey'].dt.month_name()


# In[12]:


# Day of week name
df['journey_week name']=df['Date_of_Journey'].dt.day_name()


# In[13]:


# is weekend?
df['date is weekend']=np.where(df['Date_of_Journey'].isin(['Sunday','Saturday']),1,0)


# In[14]:


#extract week of the year
df['week of the year']=df['Date_of_Journey'].dt.week


# In[15]:


# extract quarter
df['quarter of the year']=df['Date_of_Journey'].dt.quarter


# In[16]:


# extract semester
df['semester']=np.where(df['quarter of the year'].isin([1,2]),1,2)


# In[17]:


df.head()


# In[18]:


df["Journey_month"]=pd.to_datetime(df.Date_of_Journey,format="%d/%m/%Y").dt.month


# In[19]:


df.head()


# In[20]:


df.drop(["Date_of_Journey"],axis=1,inplace=True)


# In[21]:


df.head()


# In[22]:


df["dep_hour"]=pd.to_datetime(df.Dep_Time).dt.hour


# In[23]:


df.head()


# In[24]:


df["dep_min"]=pd.to_datetime(df.Dep_Time).dt.minute


# In[25]:


df.drop(["Dep_Time"],axis=1,inplace=True)


# In[26]:


df.head()


# In[27]:


df["Arrival_hour"]=pd.to_datetime(df.Arrival_Time).dt.hour


# In[28]:


df["Arrival_min"]=pd.to_datetime(df.Arrival_Time).dt.minute


# In[29]:


df.drop(["Arrival_Time"],axis=1,inplace=True)


# In[30]:


df.head()


# In[31]:


# Time taken by plane to reach destination is called Duration
# It is the differnce betwwen Departure Time and Arrival time


# Assigning and converting Duration column into list
duration = list(df["Duration"])

for i in range(len(duration)):
    if len(duration[i].split()) != 2:    # Check if duration contains only hour or mins
        if "h" in duration[i]:
            duration[i] = duration[i].strip() + " 0m"   # Adds 0 minute
        else:
            duration[i] = "0h " + duration[i]           # Adds 0 hour

duration_hours = []
duration_mins = []
for i in range(len(duration)):
    duration_hours.append(int(duration[i].split(sep = "h")[0]))    # Extract hours from duration
    duration_mins.append(int(duration[i].split(sep = "m")[0].split()[-1]))   # Extracts only minutes from duration


# In[32]:


# Adding duration_hours and duration_mins list to train_data dataframe

df["Duration_hours"] = duration_hours
df["Duration_mins"] = duration_mins
df.drop(["Duration"], axis = 1, inplace=True)


# In[33]:


df.head()


# In[34]:


df["Airline"].value_counts()


# In[35]:


# From graph we can see that Jet Airways Business have the highest Price.
# Apart from the first Airline almost all are having similar median

# Airline vs Price
sns.catplot(y = "Price", x = "Airline", data = df.sort_values("Price", ascending = False), kind="boxen", height = 6, aspect = 3)
plt.show()


# In[37]:


# As Airline is Nominal Categorical data we will perform OneHotEncoding

Airline = df[["Airline"]]

Airline = pd.get_dummies(Airline, drop_first= True)

Airline.head()


# In[38]:


df["Source"].value_counts()


# In[39]:


# Source vs Price

sns.catplot(y = "Price", x = "Source", data = df.sort_values("Price", ascending = False), kind="boxen", height = 4, aspect = 3)
plt.show()


# In[40]:


# As Source is Nominal Categorical data we will perform OneHotEncoding

Source = df[["Source"]]

Source = pd.get_dummies(Source, drop_first= True)

Source.head()


# In[41]:


df["Destination"].value_counts()


# In[42]:


df["Price"].value_counts()


# In[43]:


# As Destination is Nominal Categorical data we will perform OneHotEncoding

Destination = df[["Destination"]]

Destination = pd.get_dummies(Destination, drop_first = True)

Destination.head()


# In[44]:


# Additional_Info contains almost 80% no_info
# Route and Total_Stops are related to each other

df.drop(["Route", "Additional_Info"], axis = 1, inplace = True)


# In[45]:


df["Total_Stops"].value_counts()


# In[46]:


# As this is case of Ordinal Categorical type we perform LabelEncoder
# Here Values are assigned with corresponding keys

df.replace({"non-stop": 0, "1 stop": 1, "2 stops": 2, "3 stops": 3, "4 stops": 4}, inplace = True)


# In[47]:


df.head()


# In[48]:


df.info()


# In[49]:


df.astype({'Total_Stops':'int'}).dtypes


# In[ ]:


# Concatenate dataframe --> train_data + Airline + Source + Destination

df = pd.concat([df, Airline, Source, Destination], axis = 1)


# In[42]:


df.head()


# In[43]:


df.drop(["Airline", "Source", "Destination"], axis = 1, inplace = True)


# In[44]:


df.shape


# In[45]:


test_data = pd.read_excel(r"C:\Users\anami\Downloads\Test_set.xlsx")


# In[46]:


test_data.head()


# In[47]:



print("-"*75)


# In[48]:


print("Test data Info")
print("-"*75)
print(test_data.info())

print()
print()

print("Null values :")
print("-"*75)
test_data.dropna(inplace = True)
print(test_data.isnull().sum())

# EDA

# Date_of_Journey
test_data["Journey_day"] = pd.to_datetime(test_data.Date_of_Journey, format="%d/%m/%Y").dt.day
test_data["Journey_month"] = pd.to_datetime(test_data["Date_of_Journey"], format = "%d/%m/%Y").dt.month
test_data.drop(["Date_of_Journey"], axis = 1, inplace = True)

# Dep_Time
test_data["Dep_hour"] = pd.to_datetime(test_data["Dep_Time"]).dt.hour
test_data["Dep_min"] = pd.to_datetime(test_data["Dep_Time"]).dt.minute
test_data.drop(["Dep_Time"], axis = 1, inplace = True)

# Arrival_Time
test_data["Arrival_hour"] = pd.to_datetime(test_data.Arrival_Time).dt.hour
test_data["Arrival_min"] = pd.to_datetime(test_data.Arrival_Time).dt.minute
test_data.drop(["Arrival_Time"], axis = 1, inplace = True)

# Duration
duration = list(test_data["Duration"])

for i in range(len(duration)):
    if len(duration[i].split()) != 2:    # Check if duration contains only hour or mins
        if "h" in duration[i]:
            duration[i] = duration[i].strip() + " 0m"   # Adds 0 minute
        else:
            duration[i] = "0h " + duration[i]           # Adds 0 hour

duration_hours = []
duration_mins = []
for i in range(len(duration)):
    duration_hours.append(int(duration[i].split(sep = "h")[0]))    # Extract hours from duration
    duration_mins.append(int(duration[i].split(sep = "m")[0].split()[-1]))   # Extracts only minutes from duration

# Adding Duration column to test set
test_data["Duration_hours"] = duration_hours
test_data["Duration_mins"] = duration_mins
test_data.drop(["Duration"], axis = 1, inplace = True)


# Categorical data

print("Airline")
print("-"*75)
print(test_data["Airline"].value_counts())
Airline = pd.get_dummies(test_data["Airline"], drop_first= True)

print()
print("Source")
print("-"*75)
print(test_data["Source"].value_counts())
Source = pd.get_dummies(test_data["Source"], drop_first= True)

print()

print("Destination")
print("-"*75)
print(test_data["Destination"].value_counts())
Destination = pd.get_dummies(test_data["Destination"], drop_first = True)

# Additional_Info contains almost 80% no_info
# Route and Total_Stops are related to each other
test_data.drop(["Route", "Additional_Info"], axis = 1, inplace = True)

# Replacing Total_Stops
test_data.replace({"non-stop": 0, "1 stop": 1, "2 stops": 2, "3 stops": 3, "4 stops": 4}, inplace = True)

# Concatenate dataframe --> test_data + Airline + Source + Destination
data_test = pd.concat([test_data, Airline, Source, Destination], axis = 1)

data_test.drop(["Airline", "Source", "Destination"], axis = 1, inplace = True)

print()
print()

print("Shape of test data : ", data_test.shape)


# In[49]:


data_test.head()


# In[50]:


pd.set_option('display.max_columns', None)


# In[51]:


x=df.drop(["Price"],axis=1)


# In[52]:


x


# In[53]:


y=df['Price']


# In[54]:


y


# In[55]:


x.shape


# In[56]:


y.shape


# In[57]:


# Finds correlation between Independent and dependent attributes

plt.figure(figsize = (28,28))
sns.heatmap(df.corr(), annot = True, cmap = "RdYlGn")

plt.show()


# In[58]:


# Important feature using ExtraTreesRegressor

from sklearn.ensemble import ExtraTreesRegressor
selection = ExtraTreesRegressor()
selection.fit(x, y)


# In[59]:


print(selection.feature_importances_)


# In[60]:


#plot graph of feature importances for better visualization

plt.figure(figsize=(12,8))
feat_importances=pd.Series(selection.feature_importances_,index=x.columns)
feat_importances.nlargest(30).plot(kind='barh')
plt.show()


# In[61]:


from sklearn.model_selection import train_test_split


# In[62]:


x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=2)


# In[63]:


from sklearn.ensemble import RandomForestRegressor
reg_rf=RandomForestRegressor()
reg_rf.fit(x_train,y_train)


# In[64]:


y_pred=reg_rf.predict(x_test)


# In[65]:


reg_rf.score(x_test,y_test)


# In[66]:


sns.distplot(y_test-y_pred)
plt.show()


# In[69]:


plt.scatter(y_test,y_pred,alpha=0.5)
plt.xlabel("x_test")
plt.ylabel("y_pred")
plt.show()


# In[ ]:




