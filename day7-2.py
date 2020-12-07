file = open("./day7.txt", mode="r")
bags = file.readlines()

# eligibleBags = [] # all bags that could hold a shiny gold bag
# counter = 0
# 
# # part 1
# for bag in bags:
#     if bag.startswith("shiny gold") == False and 'shiny gold' in bag: # get all bags that can directly hold a shiny gold bag
#         bag = bag.split(" ")
#         bag = bag[0] + " " + bag[1]
#         eligibleBags.append(bag)
#         
# for bag in bags:
#     for eBag in eligibleBags:
#         if eBag in bag and bag.startswith(eBag) == False: # get all bags that can indirectly hold a shiny gold bag
#             bag = bag.split(" ")
#             bag = bag[0] + " " + bag[1]
#             eligibleBags.append(bag)
#             
# for bag in bags:
#     for eBag in eligibleBags:
#         if eBag in bag and bag.startswith(eBag) == False: # loop through one more time to get bagceptions (will write a while loop in the future)
#             bag = bag.split(" ")
#             bag = bag[0] + " " + bag[1]
#             eligibleBags.append(bag)
#             
# for bag in bags:
#     for eBag in eligibleBags:
#         if eBag in bag and bag.startswith(eBag) == False: # loop through one more time to get bagceptions
#             bag = bag.split(" ")
#             bag = bag[0] + " " + bag[1]
#             eligibleBags.append(bag)
# 
# for bag in bags:
#     for eBag in eligibleBags:
#         if eBag in bag and bag.startswith(eBag) == False: # loop through one more time to get bagceptions
#             bag = bag.split(" ")
#             bag = bag[0] + " " + bag[1]
#             eligibleBags.append(bag)
# 
# for bag in bags:
#     for eBag in eligibleBags:
#         if eBag in bag and bag.startswith(eBag) == False: # loop through one more time to get bagceptions (you may have to do this more times, hence why it should be a while loop controlled by a counter)
#             bag = bag.split(" ")
#             bag = bag[0] + " " + bag[1]
#             eligibleBags.append(bag)
#             
# eligibleBags = set(eligibleBags) #eliminate duplicate entries; this is redundant due to the startswith() in each loop
# 
# print(len(eligibleBags))

# part 2 - DOESN'T WORK

goldBagList = [] # list of all bags and subbags in the shiny gold bag
allBags = []

for bag in bags: # making a list of all the bag names
    bag = bag.split(" ")
    bag = bag[0] + " " + bag[1]
    allBags.append(bag)

goldBagDict = dict((elem, 0) for elem in allBags) # dictionary has bag colors as keys and increments their value as they are appear

#BASE CASE
for bag in bags:
    if bag.startswith("shiny gold") == True: # get bags within the shiny gold bag
        bag = bag.split(" ")
        containee = [' '.join(bag[i: i + 3]) for i in range(4, len(bag), 4)] # get the tokens with the subbags
        print(containee)
        thisnum = 0
        for s in containee: # iterate over each color of subbag i.e. s = "3 dark fuchsia"
            for x in s:
                if x.isdigit() == True:
                    thisnum = int(x) # get the number of subbags of a given color
            s = s.split()
            thisbag = s[1] + ' ' + s[2] # make the name of this subbag
            if thisbag != "other bags.":
                goldBagDict[thisbag] += thisnum
                goldBagList.append(thisbag)

#ITERATE THROUGH
while sum(goldBagDict.values()) < 1000000: # just gonna keep looping til a "stable" value appears, then this will be changed to len(bags)
    for bag in bags:
        thatbag = bag.split()
        thatbag = thatbag[0] + ' ' + thatbag[1]
        if thatbag in goldBagList: # check to see if the line is a subbag of the shiny gold bag or its subbags
            newbag = bag.split(" ")
            containee = [' '.join(newbag[i: i + 3]) for i in range(4, len(newbag), 4)] # get the tokens with the subbags
            print(containee)
            thisnum = 0
            for s in containee: # iterate over each color of subbag i.e. s = "3 dark fuchsia"
                for x in s:
                    if x.isdigit() == True:
                        thisnum = int(x) # get the number of subbags of a given color
                s = s.split()
                thatbag = s[1] + ' ' + s[2] # make the name of this subbag
                if thatbag != "other bags.":
                    goldBagDict[thatbag] += thisnum
                    goldBagList.append(thatbag) # append name of subbags back to goldBagList
            print(bag)
            bags.remove(bag) # remove that line from the input since bags don't appear twice
            print(sum(goldBagDict.values()))
