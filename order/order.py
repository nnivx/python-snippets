#!/usr/bin/env python2
################################################################################
# Earl Dominic, Eujene BSCS3-1N
# AdProg
# CSV
#
####################################
# PROGRAM OUTPUT
####################################
# Product Code: <input>
# Description:  <output>
# Price:        <output>
# Discount:     <output>
# Quantity:     <input>
# Amount:       <output>
#
# [a]dd, [c]ancel, [t]otal
#
#
# add - saves the item and begins another transaction
# cancel - cancel transaction and begins another transaction
# total - calculates total and display receipt
#
####################################
# RECEIPT
####################################
# <Grocery Name>
# <Description> <Discounted Price> <Quantity>  <Amount>
# ...
# Total                                        <total>
################################################################################
import tools
from tools import sortedlist
import os, sys

#python3
if sys.version_info[0] != 2:
    def raw_input(*args):
        return input(args)
        
def basedir():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def input_choice(choices, message=None):
    choice = None
    if message == None:
        message = ' '.join(['[{0}]'.format(c) for c in choices]) + ' >> '
    while choice not in choices:
        choice = raw_input(message)
    return choice

def reload_products(mapProducts):
    """
        This opens the files and (re)initializes a map of products.

        Separated so that the mapping can be reloaded anytime.
    """
    # we assume the csv count is always right
    split_line = lambda line: [word.strip() for word in line.split(',')]
    with open(tools.PRODUCT_PATH) as objProduct, open(tools.STOCK_PATH) as objStock, open(tools.PROMO_PATH) as objPromo:
	    # parse from products
	    objProduct.seek(0)
	    for strLine in objProduct:
		    strCode, strDesc, strPrice = split_line(strLine)
		    mapProducts[strCode] = [strDesc, float(strPrice), 0, 0]
	    # parse from stock
	    for strLine in objStock:
	        strCode, strQty = split_line(strLine)
	        mapProducts[strCode][2] = int(strQty)
	    # parse from promo
	    for strLine in objPromo:
	        strCode, strDiscount = split_line(strLine)
	        mapProducts[strCode][3] = int(strDiscount)

def update_stock(mapProducts):
    """
        This is the only 'editing'. Although the files are read by lines,
        there is no such magic to skip over lines, as we will still be
        reading the files sequentially per character. Furthermore, the
        file is plain-text rather than binary, EVERYTHING after the edited
        part will be updated (most of the time).

        To reduce program complexity, we decided to use a QAD solution:
            rewrite the stocks at once every after reload.
    """
    with open(tools.STOCK_PATH, 'w') as objStock:
        for k, v in sortedlist(mapProducts):
            strCode, intQty = k, v[2]
            objStock.write('{0},{1}\n'.format(strCode, intQty))

################################################################################

GROCERY_HEADER = [
    'YER GROCERIES',
    'Owned By:',
    'Nyks N Co.',
    'E411/S510 PUP',
    '\n'
]

def print_prod(what): # for debugging
    print('========================================')
    for k, v in what.items():
        print('{0}:{1}'.format(k, v))
    print('========================================')
    
    
def interactive():
    """
        Runs the interactive program.
    """
    # 0) initialization
    tools.prepare_db(basedir())

    mapProducts = {}
    mapCart = {}

    # 1) load the products
    reload_products(mapProducts)
    
    # 2) fill the cart
    while True:
        print('---')
        strProdCode, intQuantity = cart_add(mapProducts)
        strChoice = input_choice(['a', 'c', 't'], '[a]dd, [c]ancel, [t]otal >> ')

        if strChoice != 'c':
            # get old qty, safe even if first item of type
            intOldQty = mapCart.get(strProdCode) or 0
            # reduce quantity
            mapProducts[strProdCode][2] -= intQuantity
            # add to cart
            mapCart[strProdCode] = intOldQty + intQuantity

        if strChoice == 't':
            break

    # 3) update the stock and display total
    update_stock(mapProducts)
    cart_view(mapProducts, mapCart)


def cart_add(mapProducts):
    """
        Returns the product code and quantity of ordered item.

        mapProducts - mapping of products
    """
    LJUST = 14
    pinput = lambda strMessage: raw_input(strMessage.ljust(LJUST))
    
    strCode = None
    strDesc = None
    intQty = 0
    intDiscount = 0
    floatPrice = 0
    
    # fetch the product
    while True:
        strCode = pinput('Product Code:')
        if strCode not in mapProducts:
            print('Error: product code not found')
        else:
            strDesc, floatPrice, intQty, intDiscount = mapProducts[strCode]
            # check: out of stock
            if intQty < 1:
                print('Product out of stock!')
            else:
                break
            
    print('Description:'.ljust(LJUST) + strDesc)
    print('Price:'.ljust(LJUST) + str(floatPrice))
    print('Discount:'.ljust(LJUST) + str(intDiscount) + '%')
   
    # quantity
    while True:
        intOrderQty = int(pinput('Quantity:'))
        if intOrderQty < 1:
            print('Invalid quantity!')
        else:
            break
            
    # check: stock
    if intOrderQty > intQty:
        print('Warning: Insufficient stock, {0}/{1} of item ordered taken from stock.'.format(intQty, intOrderQty))
        intOrderQty = intQty
        
    return strCode, intOrderQty


def cart_view(mapProducts, mapCart):
    """
        Displays the receipt and returns the total

        mapProducts - the mapping of products
        mapCart - the mapping of cart
    """
    floatTotal = 0.
    
    objBuffer = [['Description', 'Price', 'Quantity', 'Amount']]
    arrWidth = [len(word) for word in objBuffer[0]]
    
    for strCode, intQty in sortedlist(mapCart):
        strDesc = mapProducts[strCode][0]
        floatPrice, intDiscount = mapProducts[strCode][1], mapProducts[strCode][3]
        
        # compute for the price
        floatdPrice = floatPrice*(1 - intDiscount/100.)
        floatAmount = floatdPrice*intQty
        floatTotal += floatAmount
        
        # just formatting :p
        tmplen = len(strDesc), len(str(floatdPrice)), len(str(intQty)), len(str(floatAmount))
        for i in range(0, 4):
            if tmplen[i] > arrWidth[i]:
                arrWidth[i] = tmplen[i]
        objBuffer.append([strDesc, floatdPrice, intQty, floatAmount])
    
    # DISPLAY
    totalWidth = arrWidth[0]+arrWidth[1]+arrWidth[2]+arrWidth[3]+3*3
    border = ''.ljust(totalWidth, '-')
    
    print(border)
    for detail in GROCERY_HEADER:
        print(detail.center(totalWidth))
    for e in objBuffer:
        for i in range(0, 4):
            e[i] = str(e[i]).rjust(arrWidth[i])
        print('   '.join(e))
        
    print(''.ljust(arrWidth[3], '-').rjust(totalWidth))
    print('Total:'.ljust(arrWidth[0]+arrWidth[1]+arrWidth[2]+9) + str(floatTotal))
    print(border)
    
    return floatTotal


if __name__ == '__main__':
    interactive()











