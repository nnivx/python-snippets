#s=input()
#for x in range(0,3):print(''.join([''.join([' _ |_||_|'[i]if str(i) not in('4','13467','38','36','167','56','5','3467','','6')[int(c)]else' 'for i in range(x*3, x*3+3)])for c in s]))

s = input('Enter Number: ')
STAMP = ' _ |_|'
NUM   = ['4', '13467', '38', '36', '167', '56', '5', '3467', '', '6']
# data
buf = []
for nc in s:
    buf.append(''.join([STAMP[x] if (str(x) not in NUM[int(nc)]) else ' ' for x in range(0, 9)]))
    
# print per line
for x in range(0, 9, 3):
    print(' '.join([c[x:x+3] for c in buf]))
