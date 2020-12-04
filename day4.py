# DOESN'T WORK! I ended up using a shell script. Thank you for the help anons.

import re

file = open("./day4.txt", mode="r")
rows = file.read()
rows = rows.split("\n\n")
counter = 0
print(rows)
#part 1

for row in rows:
    if 'byr' in row and 'iyr' in row and 'eyr' in row and 'hgt' in row and 'hcl' in row and 'ecl' in row and 'pid' in row:
        counter = counter + 1
print(counter)

#part 2
rowList = []
for row in rows:
    thisRow = row.split()
    rowList.append(thisRow)
print(rowList)

for row in rowList:
    if any('byr' in elem for elem in row) == False:
        del rowList[rowList.index(row)]
    elif any('iyr' in elem for elem in row) == False:
        del rowList[rowList.index(row)]
    elif any('eyr' in elem for elem in row) == False:
        del rowList[rowList.index(row)]
    elif any('hgt' in elem for elem in row) == False:
        del rowList[rowList.index(row)]
    elif any('hcl' in elem for elem in row) == False:
        del rowList[rowList.index(row)]
    elif any('ecl' in elem for elem in row) == False:
        del rowList[rowList.index(row)]
    elif any('pid' in elem for elem in row) == False:
        del rowList[rowList.index(row)]

for row in rowList:
    if(len(row) == 8 or len(row) == 7):
        continue
    else:
        del rowList[rowList.index(row)]
        
counter = len(rowList)

for row in rowList:
    thisBool = True
    for elem in row:
        print(elem)
        if 'byr' in elem:
            thisNum = int(re.search(r'\d\d\d\d', elem).group(0))
            if thisNum < 1920 and thisNum > 2002:
                thisBool = False
                print("no")
        if 'iyr' in elem:
            thisNum = int(re.search(r'\d\d\d\d', elem).group(0))
            if thisNum < 2010 and thisNum > 2020:
                print("no")
                thisBool = False
        if 'eyr' in elem:
            thisNum = int(re.search(r'\d\d\d\d', elem).group(0))
            if thisNum < 2020 and thisNum > 2030:
                print("no")
                thisBool = False
        if 'hgt' in elem:
            if 'cm' in elem:
                thisNum = int(re.search(r"\d+", elem).group(0))
                if int(thisNum) < 150 and int(thisNum) > 193:
                    print("no")
                    thisBool = False
            if 'in' in elem:
                thisNum = int(re.search(r'\d+', elem).group(0))
                if thisNum < 59 and thisNum > 76:
                    print("no")
                    thisBool = False
        if 'hcl' in elem:
            thisNum = re.search(r'^#(?:[0-9a-fA-F]{3}){1-2}$', elem)
            if not thisNum:
                print("no")
                thisBool = False
        if 'ecl' in elem:
            if 'amb' not in elem and 'blu' not in elem and 'brn' not in elem and 'gry' not in elem and 'grn' not in elem and 'hzl' not in elem and 'oth' not in elem:
                print("no")
                thisBool = False
        if 'pid' in elem:
            thisNum = re.search(r"(?<!\d)\d{9}(?!\d)", elem)
            if not thisNum:
                print("no")
                thisBool = False
    if(thisBool == False):
        counter = counter -1
        
print(len(rowList))        
print(counter)
