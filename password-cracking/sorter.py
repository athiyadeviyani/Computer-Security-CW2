def sort_md5():
    f = open("md5-cracked.txt")
    arr = []
    for line in f.readlines():
        line = line.rstrip()
        count, password = line.split(',')
        arr.append((int(count), password))
    # print(arr)

    arr = sorted(arr, key=lambda x: x[1])
    arr = sorted(arr, key=lambda x: x[0])[::-1]

    wf = open("md5-cracked-sorted.txt", "w")
    wf.writelines(["{},{}\n".format(count, password) for count, password in arr])
    wf.close()
    f.close()

    print(arr)
    return

def sort_sha():
    f = open("salt-cracked.txt")
    arr = []
    for line in f.readlines():
        line = line.rstrip()
        count, password = line.split(',')
        arr.append((int(count), password))
    # print(arr)

    arr = sorted(arr, key=lambda x: x[0])[::-1]

    wf = open("salt-cracked-sorted.txt", "w")
    wf.writelines(["{},{}\n".format(count, password) for count, password in arr])
    wf.close()
    f.close()

    print(arr)
    return

sort_md5()
sort_sha()