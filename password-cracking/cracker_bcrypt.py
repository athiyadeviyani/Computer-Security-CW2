import bcrypt

read_file = "rockyou-samples.bcrypt.txt"
write_file = "bcrypt-lines.txt"
password = b"123456"

def writeToFile(s):
    f = open(write_file, "w")
    for c in s:
        line = str(c) + "\n"
        f.write(line)
    f.close()


def crack():

    data = open(read_file).readlines()

    # Create an occurence list 
    lineNumbers = []

    # Loop through dictionary and determine how many occurences or each key are in data
    print("Getting password occurences...")
    lineCounter = 1
    found = 0
    for line in data:
        hashedPassword = line[:-1]
        if bcrypt.checkpw(password, hashedPassword.encode('utf-8')):
            print("Found occurence in line " + str(lineCounter))
            lineNumbers.append(lineCounter)
            found += 1
        if found == 5:
            break
        lineCounter += 1

    writeToFile(lineNumbers)
    return 

crack()
