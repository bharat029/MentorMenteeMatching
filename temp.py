# def extract(data):  
#      data = data.split()
#      
#      temp = []
#  
#      try:
#          temp.append(' '.join(data[data.index('passion:') + 1 : data.index('Goal:')]))
#          temp.append(' '.join(data[data.index('Goal:') + 1 : data.index('Challenge')]))
#          temp.append(' '.join(data[data.index('Personality:') + 1 : data.index('Referral:')]))
# 
#          result = ' '.join(temp)
#          return result + '\n'
#      except  Exception as e:
#          return -1, e
#  
# fhand = open('dataset1_edited.txt')
#  
# data = fhand.read().split('\n\n\n\n')
#  
# for i in data:
#     if len(i) < 1:
#         data.remove(i)
#  
# for i in range(len(data)):
#     temp = extract(data[i])
#     if temp[0] == -1:
#         print(i, temp[1])
#     data[i] = temp
#      
# file2 = open('finalDataSet_2.txt', 'w')
#  
# for i in data:
#     file2.write(i)
#      
# file2.close()
# fhand.close()
# print('Done')
# print(len(data))

with open('finalDataSet_2.txt', 'r') as f:
    count = 0
    tot = 0
    t = open('try.txt', 'w')
    for line in f:
        tot +=1
        line = line.lower()
        if 'mentor ' in line:
            count += 1
            temp = line.split()
            try:
                idx = temp.index('mentor')
                print(temp[idx - 5 : idx + 5])
                t.write(' '.join(temp[idx - 5 : idx + 5]) + '\n')
            except:
                print(line)
            
    print(tot)
    t.close()