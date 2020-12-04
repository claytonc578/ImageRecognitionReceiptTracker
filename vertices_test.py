import pandas as pd
import re

from utilities import getChoice
#---------------------------CONSTANTS---------------------------
SL_THRESHOLD = 15 #image detection objects on the same line
V_THRESHOLD = 10 #image detection objects adjacent vertically
EXIT = 0
SORT = 1

#---------------------------FUNCTIONS---------------------------
#------------------------------------------------------
def convertExcelToDataframe(file_name):
    results = pd.DataFrame(columns= ["item_name", "cost", "vertex"])
    df1 = pd.read_csv(file_name)
    cost = df1[df1['description'].str.contains(pat = '\.[0-9][0-9]', regex=True)]
    cost.drop(cost.index[0], inplace=True)

    for index1, row_all in df1.iterrows(): #iterate all rows in df1
        if re.search('[0-9]', row_all['description']): #continue if pattern true
            continue
        else:
            for index2, row_cost in cost.iterrows(): #iterate prices DataFrame
                if (row_all['y0'] < row_cost['y0'] + SL_THRESHOLD) and (row_all['y0'] > row_cost['y0'] - SL_THRESHOLD): #item_name and cost within vertex threshold
                    check = results[(row_all['y0'] - V_THRESHOLD < results['vertex']) & (row_all['y0'] + V_THRESHOLD > results['vertex'])]
                    if check.empty: #check if item_name already exist, needs to be joined
                        new_row = {'item_name': row_all['description'], 'cost': row_cost['description'], 'vertex': row_all['y0']}
                        results = results.append(new_row, ignore_index=True)
                    else:
                        new_item = row_all['description']
                        existing_item = check['item_name'].values
                        combined_item = existing_item + " " + new_item
                        results.loc[check.index, 'item_name'] = combined_item
    return results


#------------------------------------------------------
def sortItems(numPerson, df1):
    person_list = [] #contains list of DataFrames, each person has 1, last index is shared items
    SHARED = numPerson+1
    SKIP = numPerson+2
    NUM_CHOICES = numPerson+2

    for i in range(numPerson+1):
        person_list.append(pd.DataFrame(columns=['item_name', 'cost']))

    for index, row in df1.iterrows():
        curr_item = row['item_name']
        curr_cost = row['cost']

        #print out menu choices
        print("\n\nItem name: {}Cost: {}".format(curr_item.ljust(40), curr_cost))
        for i in range(numPerson):
            print("1) Person {}'s Item".format(i+1, i+1))
        print("{}) Shared".format(SHARED))
        print("{}) Not an item. Skip".format(SKIP))

        choice = getChoice(NUM_CHOICES) #get user input choice

        if choice == SKIP: #skip item
            continue

        person_df = person_list[choice-1] #get current person from person_list
        new_df = pd.DataFrame(data={'item_name': [curr_item], 'cost': [curr_cost]}) #add item and cost to person
        person_list[choice-1] = person_df.append(new_df, ignore_index=True)

    for index, person in enumerate(person_list): #print results of person_list
        if index == SHARED-1:
            print("\n\nShared List of Items\n-----------------------------".format(index))
        else:
            print("\n\nPerson {} List of Items\n-----------------------------".format(index))
        print(person)
        print("-----------------------------\n\n")

    return person_list
#------------------------------------------------------
def calculations(numPerson, person_list):
    print("Which Person paid?\nEnter 1-{}:".format(numPerson))
    # choice = getChoice(numPerson)
    choice = 1 #DEBUG REMOVE LATER ################################################

#------------------------------------------------------
def menu():
    while(True):
        print("\nReceipt OCR Parsing\nChoices:\n0: Exit\n1: Sort Items\n")
        choice = int(input("Enter choice: "))
        if choice == EXIT:
            return
        elif choice == SORT:
            pass
        else:
            print("Invalid Choice")

#---------------------------MAIN---------------------------
numPerson = 2
# df_result = convertExcelToDataframe('TraderJoes1.csv')
# print(df_result)
# person_list = sortItems(numPerson, df_result)

test_list = []
test_list.append(pd.DataFrame(data = {'item_name': ['ALMOND', 'ALFREDO', 'VEG', 'BANANA'], 'cost': ['$5.38', '$6.49', '$1.99', '$1.14']}))
test_list.append(pd.DataFrame(data = {'item_name': ['GREEK HONEY', 'COOKIES'], 'cost': ['$9.98', '$13.93']}))
test_list.append(pd.DataFrame(data = {'item_name': ['CHICKEN', 'SPINACH', 'BACON'], 'cost': ['$9.22', '$1.99', '$5.49']}))
# print(test_list)

calculations(numPerson, test_list)
