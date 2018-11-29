
# coding: utf-8

# In[151]:

import json
from collections import defaultdict
import pandas as pd


# # Part 1

# In[152]:

#prompting dish id and user id
dishId = input('Enter dish ID: ')
userId = input('Enter user ID: ')


# In[153]:

list1 = json.load(open('user_ratings.json', 'r'))
#print(list1)


# In[154]:

dictionary = {}
for i in list1:
    dictionary.setdefault(i, list1[i])
#print(dictionary.get("0"))


# In[155]:

final_dict = {}
for key,value in dictionary.items():
    dict2 = {}
    for i in value:
        #print(i)
        dict2[i[0]] = i[1]
    final_dict[key] = dict2
#print(final_dict)


# In[156]:

#calculate cosine similarities of all documents with userID and dishID where dishID exists

#first, calculate sub_mean for userID
a = final_dict.get(str(userId))
total = 0
for key, value in a.items():
    total = total + value
sub_mean = total/len(a)
#print(sub_mean)


# In[157]:

#calculate adjusted means
i = 0
averages = {}
while (i < len(final_dict)):
    total = 0
    dict_sub = final_dict.get(str(i))
    for k in dict_sub:
        total = total + dict_sub[k]
    average = total/len(dict_sub)
    averages[i] = average
    #print(average)
    #for n in final_dict[str(i)]:
        #final_dict[str(i)][n] -= average
    i = i + 1
#print(final_dict)


# In[158]:

import math

#calculate cosine similarity with weighted means 
temp_dict = final_dict.get(str(userId))
i = 0
cosineSimilarities = {}
actualValuesdishID = {}
while i < len(final_dict):
    #only consider users with validdishID ratings
    dict_sub = final_dict.get(str(i))
    if (dict_sub.get(int(dishId))) != None:
        #find common ratings between the subset
        numerator = 0
        denominatorLeft = 0
        denominatorRight = 0
        actualValuesdishID[i] = dict_sub.get(int(dishId))
        for key in dict_sub:
            if temp_dict.get(key) != None:
                mult = temp_dict.get(key) * dict_sub.get(key)
                numerator = mult + numerator
                denominatorRight = (temp_dict.get(key) * temp_dict.get(key)) + denominatorRight
                denominatorLeft = (dict_sub.get(key) * dict_sub.get(key)) + denominatorLeft
        if (denominatorRight != 0 and denominatorLeft != 0):
            cosineSimilarities[i] = numerator/ (math.sqrt(denominatorRight) * math.sqrt(denominatorLeft))
    i = i + 1
#print(cosineSimilarities)
#print("SPACEEEE")
#print (actualValuesdishID)


# In[159]:

#making the prediction

if (final_dict.get(str(userId)).get(int(dishId)) == None):
    numerator = 0
    denominator = 0
    i = 0
    for key in cosineSimilarities:
        numerator = (cosineSimilarities.get(key) * 
                      (actualValuesdishID.get(key) - averages.get(key))) + numerator
        denominator = cosineSimilarities.get(key) + denominator
    prediction = sub_mean + (numerator/denominator)
    print("Rating: ", prediction, "(Estimated)")
else:
    print("Rating: ", final_dict.get(str(userId)).get(int(dishId)), "(Existing)")


# # Part 2

# In[160]:

#prompting dish id and user id
userID = input('Enter user ID: ')
ingredients = input('Enter number of ingredients: ')
i = 0
ingredList = []
while i < int(ingredients):
    a = input('Enter Item: ')
    ingredList.append(a)
    i = i + 1


# In[161]:

#read in csv
dishes = pd.read_csv('dishes.csv')


# In[162]:

for i in ingredList:
    dishes = dishes[(dishes[i] == 1)]
#dishes.head(n=20)


# In[163]:

#store dish_ids in list
validDishes = dishes.ix[:, 0].tolist()


# In[164]:

#find estimated ratings for each of these dishes and reccommend one

predictions_dict = {}
existing_dict = {}
for dish in validDishes:
#calculate cosine similarity with means 
    temp_dict = final_dict.get(str(userID))
    i = 0
    cosineSimilarities = {}
    actualValuesdishID = {}

    while i < len(final_dict):
        #only consider users with validdishID ratings
        dict_sub = final_dict.get(str(i))
        if (dict_sub.get(int(dish))) != None:
            #find common ratings between the subset
            numerator = 0
            denominatorLeft = 0
            denominatorRight = 0
            actualValuesdishID[i] = dict_sub.get(int(dish))
            for key in dict_sub:
                if temp_dict.get(key) != None:
                    mult = temp_dict.get(key) * dict_sub.get(key)
                    numerator = mult + numerator
                    denominatorRight = (temp_dict.get(key) * temp_dict.get(key)) + denominatorRight
                    denominatorLeft = (dict_sub.get(key) * dict_sub.get(key)) + denominatorLeft
            if (denominatorRight != 0 and denominatorLeft != 0):
                cosineSimilarities[i] = numerator/ (math.sqrt(denominatorRight) * math.sqrt(denominatorLeft))
        i = i + 1
        
    if (final_dict.get(str(userID)).get(int(dish)) == None):
        numerator = 0
        denominator = 0
        i = 0
        for key in cosineSimilarities:
            numerator = (cosineSimilarities.get(key) * 
                      (actualValuesdishID.get(key) - averages.get(key))) + numerator
            denominator = cosineSimilarities.get(key) + denominator
        prediction = sub_mean + (numerator/denominator)
        predictions_dict[dish] = prediction
        #print("Prediction")
        #print(prediction)
    else:
        #print("exists")
        existing_dict[dish] = final_dict.get(str(userID)).get(int(dish))
        #print(final_dict.get(str(userID)).get(int(dish)))


# In[165]:

#find all max items in dictionary
if predictions_dict:
    value = max(predictions_dict, key=predictions_dict.get)
    print("Suggested dish: ")
    print(dishes[dishes['dish_id']==value]['dish_name'].values[0])
elif existing_dict:
    value = max(existing_dict, key=existing_dict.get)
    print("No new dish with specified ingredients")
    print("Your best-rated dish:")
    print(dishes[dishes['dish_id']==value]['dish_name'].values[0])
else:
    print("No dish with specified ingredients")


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



