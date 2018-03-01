
def run():
    outDict = open("outDic.txt", "w")
    with open("tempDict.txt") as myDic:
        for line in myDic:
            if "'" in line:
                print("Adding %s" %line)
                outDict.write(line)

    myDic.close()
    outDict.close()

run()