import random

def divide(fname):
    fhand = open(fname, errors = 'ignore')
    
    data = fhand.read()
    data = data.split('\n\n')
        
    data2 = []
    size_data = len(data)

    for i in range(int(size_data * 0.25)):
        pos = random.choice(data)
        data2.append(pos)
        data.remove(pos)

    fhand.close()
    
    fhand = open('test_data.txt', 'w')
    
    for idx, line in enumerate(data2):
        if idx == (len(data2) - 1):
            fhand.write(line)
            break
        fhand.write(line + '\n\n')
        
    fhand.close()
    
    fhand = open('training_data.txt', 'w')
    
    for idx, line in enumerate(data):
        if idx == (len(data) - 1):
            fhand.write(line)
            break
        fhand.write(line + '\n\n')
        
    fhand.close()
    
    print("----------DATA SET DIVIDED----------")