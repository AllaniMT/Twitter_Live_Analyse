#!/usr/bin/env python
# coding: utf-8

# In[14]:


from pyspark.sql import SparkSession


# In[15]:


from pyspark.sql.functions import explode, split


# In[16]:


spark = SparkSession.builder.appName("TwitterBeispiel").getOrCreate()


# In[17]:


lines = spark.readStream.format("socket").option("host","localhost").option("port",5553).load()


# In[18]:


words = lines.select(explode(split(lines.value, " ")).alias("tag"))


# In[19]:


hashtags = words.filter(words.tag.startswith('#'))


# In[20]:


tagCounts = hashtags.groupBy("tag").count().sort('count', ascending=False)


# In[21]:


query = tagCounts.writeStream.queryName("tweetss").outputMode("complete").format("memory").start()


# In[22]:


print(query.lastProgress)


# In[23]:


spark.sql("select * from tweetss").show()


# In[24]:


query.stop()


# In[25]:


import time
from IPython import display
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')


# In[27]:


count = 0
while count < 100:
    time.sleep(3)
    
    top_10_tweets = spark.sql("select tag, count from tweetss limit 10")
    top_10_df = top_10_tweets.toPandas()
    display.clear_output(wait=True)
    plt.figure(figsize = (10, 8))
    sns.barplot(x='count', y='tag', data= top_10_df)
    plt.show()
    count = count + 1


# In[ ]:




