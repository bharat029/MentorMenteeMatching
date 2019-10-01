def extract(data):  
    """
        Extract Passion, Goal and Personality from a single entry of the raw input
    Args:
        data: A single entry of the raw input
    Return: 
        A single line of string containing the values for Passion, Goal and Personality plus a '\n'
    """
    data = data.split()
     
    temp = []
 
    try:
        temp.append(' '.join(data[data.index('passion:') + 1 : data.index('Goal:')]))
        temp.append(' '.join(data[data.index('Goal:') + 1 : data.index('Challenge')]))
        temp.append(' '.join(data[data.index('Personality:') + 1 : data.index('Referral:')]))

        result = ' '.join(temp)
        return result + '\n'
    except  Exception as e:
        return -1, e
 
def main(inpFname, outFname):
    """
        Extract Passion, Goal and Personality from all entry of the raw input
    Args: 
        inpFname: input file anem
        outFname: output file name
    """
    fhand = open(inpFname)
    
    data = fhand.read().split('\n\n\n\n')
    
    for i in data:
        if len(i) < 1:
            data.remove(i)
    
    for i in range(len(data)):
        temp = extract(data[i])
        if temp[0] == -1:
            print(i, temp[1])
        data[i] = temp
        
    file2 = open(outFname, 'w')
    
    for i in data:
        file2.write(i)
        
    file2.close()
    fhand.close()
    print('Done')

if __name__ == "__main__":
    main('rawData.txt', 'requiredData.txt')