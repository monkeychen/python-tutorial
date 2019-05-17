import os
import time
import jieba.analyse


def processData(srcDir, outputFile=None, stopWords=None, encoding="UTF-8"):
    for item in os.scandir(srcDir):
        fileName = item.name
        filePath = item.path
        if fileName.startswith(".D"):
            continue

        if item.is_dir():
            processData(filePath, outputFile, stopWords, encoding)
        elif item.is_file():
            print("filePath =", filePath)
            flag = fileName.split("-")[0]
            articleLine = flag + " "
            try:
                with open(filePath, mode='r', encoding=encoding) as articleFile:
                    for line in articleFile.readlines():
                        line = line.strip()
                        line = line.replace(" ", "")
                        words = [word for word in jieba.cut(line) if word not in stopWords]
                        articleLine += " ".join(set(words))

                    print(articleLine + "\n")
                    outputFile.write(articleLine + "\n")
            except UnicodeDecodeError:
                print("UnicodeDecodeError: path = [%s]" % filePath)
                errLog.writelines(filePath + "\n")
            del articleLine


def extractWordFromFile(srcDir, outputPath):
    outputFile = open(outputPath, mode='w', encoding='utf-8')
    processData(srcDir, outputFile, stopWordSet, "GBK")


b_t = time.time()
errLog = open("/Users/chenzhian/Mushroom/data/err.log", mode='w', encoding='UTF-8')
stopFile = open("/Users/chenzhian/Mushroom/data/stop.txt", mode='r', encoding='utf-8')
stopWordSet = stopFile.read()
stopWordSet = set(stopWordSet.replace("\n", " ").split(" "))

trainDir = "/Users/chenzhian/Mushroom/data/train_corpus"
testDir = "/Users/chenzhian/Mushroom/data/test_corpus"
outputTrainPath = "/Users/chenzhian/Mushroom/data/train.txt"
outputTestPath = "/Users/chenzhian/Mushroom/data/test.txt"

# extractWordFromFile(trainDir, outputTrainPath)
# extractWordFromFile(testDir, outputTestPath)
extractWordFromFile("/Users/chenzhian/Mushroom/data/demo_corpus",
                    "/Users/chenzhian/Mushroom/data/demo.txt")
e_t = time.time()
print("It took [{0}]s to process data!".format(e_t - b_t))
