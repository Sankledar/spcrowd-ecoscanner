import io
import api_client.methods as api

def processGood():
    inputPath = "resources/good/!good.txt"
    outPath = "good_output.json"
    processFiles(inputPath, outPath)

def processBad():
    inputPath = "resources/bad/!bad.txt"
    outPath = "bad_output.json"
    processFiles(inputPath, outPath)

def processFiles(inputFilePath, outputFilePath):
    files = readFile(inputFilePath)
    result = api.annotate_image_batch_json(files)
    outputfile = open(outputFilePath, mode="w")
    outputfile.write(result)
    outputfile.close()

def readFile(filePath):
    file = open(filePath, mode='r')
    fileList = []
    for line in file:
        fileList.append(line.replace('\n',''))
    return fileList
