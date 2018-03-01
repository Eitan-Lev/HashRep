



#returns file as lines list
def readfile(file):
    with open(file,'r') as fh:
        lines = fh.readlines()
        lines = [x.rstrip('\n') for x in lines]
        return lines


