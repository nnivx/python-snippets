s=input()
for n in range(0,9,3):print(' '.join([b[n:n+3]for b in[''.join([' _ |_||_|'[x]if str(x)not in('4','13467','38','36','167','56','5','3467','','6')[int(c)]else' 'for x in range(0, 9)])for c in s]]))
