##################################################################
# Earl Dominic Nivero Cipre, BSCS 3-1N
#
# Subject: Advanced Programming
# Professor: Alexis Libunao
# 
# palindrome.py
# 
# Given a string, determines if it is a palindrome
#
##################################################################

def is_palindrome(what):
    """
       Returns True if palindrome, False otherwise
    """
    n = len(what)
    for i in range(0, n/2):
        # better if (n - 1) is hoisted outside the loop
        if what[i] != what[n - 1 - i]:
            return False
    return True
    
def main():
    """
        Input a string, and determine if palindrome
    """    
    word = raw_input('Enter a string: ')
    if is_palindrome(word):
        print('%s is a palindrome'%word)
    else:
        print('%s is not a palindrome'%word)
    
if __name__ == '__main__': main()
            
