##################################################################
# Earl Dominic Nivero Cipre, BSCS 3-1N
#
# Subject: Advanced Programming
# Professor: Alexis Libunao
# 
# smart_counter.py
# 
# Partial smart counter, the algorithm for determining the next
# smart counter value.
#
##################################################################

class NoNumberPart(Exception):
    """
        Thrown when there is no number part in a string value
    """
    
    def __init__(self):
        message = 'No number part in value'
        Exception.__init__(self, message)
    
def next_scvalue(value):
    """
        Given a string value, return the next smart counter value
        
        Additional operations, fetches the complete number part
        before incrementing.
    """
    parse = []
    val = []
    
    fetchDigits = None
    
    # assembles the parse and value string as list in reverse
    for i in range(len(value) - 1, -1, -1):
        c = value[i]
        if c.isdigit():
            if fetchDigits is None:
                fetchDigits = True
                parse.append('s')
                parse.append('%')
            
            if fetchDigits:
                val.append(c)
            else:
                parse.append(c)
        else:
            # do not remove "is not None"
            if fetchDigits is not None and fetchDigits:
                fetchDigits = False
            parse.append(c)
            
    if fetchDigits is None:
        raise NoNumberPart
    
    # reverse it
    parse.reverse()
    val.reverse()
    
    # transform into string
    parse = "".join(parse)
    val = "".join(val)
    
    return parse%(int(val) + 1)
    

def main():
    """
        Input a string, print the next value
    """    
    word = raw_input('Enter a string: ')
    try:
        print('The next smart counter value is: %s'%next_scvalue(word))
    except NoNumberPart, e:
        print(e.message)
        
if __name__ == '__main__': main()











    
