from difflib import Differ


def ComputeDiff(testPackage, prodPackage):
    result = Differ().compare(prodPackage, testPackage)

    diffString = ''
    lastInd = -1
    for idx, line in enumerate(result):
        if idx <= 2:
            continue
        if(line[0] in ('-', '+')):
            if idx != lastInd + 1:
                diffString += '\n----------------------\n\n'
            diffString += f'Line {str(idx+1)}: {line} \n'
            lastInd = idx
    return diffString
