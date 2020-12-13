import pandas as pd
import re

from utilities import getChoice
#---------------------------CONSTANTS---------------------------
SL_THRESHOLD = 80 #image detection objects on the same line
V_THRESHOLD = 80 #image detection objects adjacent vertically
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
    total_cost_list = [] #stores sum of each person and shared sum at end of list
    money_owed = [0.0 for i in range(numPerson)] #amount that each person owes the one who paid

    for person in person_list:
        temp_sum = 0.0 #sum for current person
        for index, row in person.iterrows():
            cost = float(row["cost"].replace('$', ''))
            temp_sum += cost
        temp_sum = round(temp_sum, 2)
        total_cost_list.append(temp_sum)

    total_cost = sum(total_cost_list)
    print("total_cost: {}".format(total_cost))
    print("total_cost_list: {}".format(total_cost_list))

    print("Which Person paid?\nEnter 1-{}:".format(numPerson))
    person_paid = getChoice(numPerson)-1
    # person_paid = 0 #DEBUG REMOVE LATER ################################################################################################
    for index, person_cost in enumerate(total_cost_list):
        if index == person_paid or index == numPerson:
            continue
        else:
            # print("person_cost: {}".format(person_cost))
            person_owes = person_cost + (total_cost_list[-1] / numPerson)
            person_owes = round(person_owes, 2)
            money_owed[index] = person_owes
    # print("money_owed: {}".format(money_owed))
    return (money_owed, person_paid)



#------------------------------------------------------
def printResults(money_owed, person_paid):
    for i, person_owed in enumerate(money_owed):
        if i == person_paid:
            continue
        else:
            print("Person {} owes ${}".format(i+1, person_owed))



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
df_result = convertExcelToDataframe('temp.csv')
# print(df_result)
person_list = sortItems(numPerson, df_result)

# test_list = []
# test_list.append(pd.DataFrame(data = {'item_name': ['ALMOND', 'ALFREDO', 'VEG', 'BANANA'], 'cost': ['$5.38', '$6.49', '$1.99', '$1.14']}))
# test_list.append(pd.DataFrame(data = {'item_name': ['GREEK HONEY', 'COOKIES'], 'cost': ['$9.98', '$13.93']}))
# test_list.append(pd.DataFrame(data = {'item_name': ['CHICKEN', 'SPINACH', 'BACON'], 'cost': ['$9.22', '$1.99', '$5.49']}))

(money_owed, person_paid) = calculations(numPerson, person_list)
printResults(money_owed, person_paid)
