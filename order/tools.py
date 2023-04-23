# tools and utilities, NyksNivero

# back-up data
# k = code
# v = (desc, price, qty, discount%)
_product_bkup = {
    '0000-A':('Bagh Nakh',99000,7,5),
    '0001-A':('Silver Arm',157500,3,0),
    '0002-A':('Demonic Fist',210000,15,2),
    '0003-A':('Mirage',630000,4,1),
    '0004-A':('Vajra',165000,8,7),
    '0005-A':('Mistral Sword',230000,21,0),
    '0006-A':('Kusanagi',3450000,12,23),
    '0007-A':('Jupiter Spear',110000,2,12),
    '0008-A':('Special Lance',132000,5,15),
    '0009-A':('Vile Brilliance',172500,12,6),
    '0010-A':('Golden Lance',220000,32,25),
    '0011-A':('Benkei',517500,5,0),
    '0012-A':('Gungnir',5750000,1,2),
    '0013-A':('Mistral Bow',165000,16,3),
    '0014-A':('GH401WZ',172500,14,5),
    '0015-A':('PS-714',283500,100,75),
    '0016-A':('Siegfried',8800000,2,0),
    '0017-A':('Platinum Axe',2300000,3,0),
    '0018-A':('Virtue Staff',220000,98,2),
    '0019-A':('Dark Matter',6900000,5,5),
    '0020-A':('Fiendish Claw',367500,10,10),
    '0021-A':('Pink Melon Seed',620,999,20),
    '0022-A':('Formula A',540,999,15),
    '0023-A':('Rice',90,9999,0),
    '0024-A':('Gold Pumpkin',16500,99,10),
    '0025-A':('Youth Grass',750,999,20),
    '0026-A':('Magnifying Glass',2000,9,0),
    '0027-A':('Super Fail',100,999,75),
    '0028-A':('Large Milk',1200,70,25),
    '0029-A':('Invisisword',6600000,3,0),
    '0030-A':('Platinum Shield',4464000,7,7),
    '0031-A':('Pancakes',8020,23,6,14)
}
# Should be accessed after prepare_db() is called.
BASEDIR      = None
PRODUCT_PATH = None
STOCK_PATH   = None
PROMO_PATH   = None

def sortedlist(m):
    """
        Returns a list from a mp such that:
        for k, v in sortedlist(m)
            can be substituted for
        for k, v in m.items()
    """
    l = [(k, v) for k, v in m.items()]
    l.sort()
    return l
    
def mkprod(filename):
    with open(filename, 'w') as product:
        for k, v in sortedlist(_product_bkup):
            # write strProdCode, strProdDesc, floatPrice
            product.write('{0},{1},{2}\n'.format(k, v[0], v[1]))
        
def mkstock(filename):
    with open(filename, 'w') as stock:
        for k, v in sortedlist(_product_bkup):
            # write strProdCode, intQuantity
            stock.write('{0},{1}\n'.format(k, v[2]))

def mkpromo(filename):
    with open(filename, 'w') as promo:
        for k, v in sortedlist(_product_bkup):
            # write strProdCode, intDiscount if discount > 0
            if v[3] > 0: promo.write('{0},{1}\n'.format(k, v[3]))
            
import os

def prepare_db(basedir):
    """
        Ensures that the 'databases' are present from preferred directory.
        
        Order of preference:
        1) In same directory as basedir
        2) In current working directory
        
        If the files are not found, it will be created in the CWD.
    """
    global BASEDIR, PRODUCT_PATH, STOCK_PATH, PROMO_PATH
    BASEDIR      = os.path.abspath(basedir)
    PRODUCT_PATH = os.path.join(BASEDIR, 'Product.csv')
    STOCK_PATH   = os.path.join(BASEDIR, 'Stock.csv')
    PROMO_PATH   = os.path.join(BASEDIR, 'Promo.csv')
    
    # if the file does not exist in default path(same dir as base):
    #   set the path in the current directory
    #   if the file does not exist, create it
    
    if not os.path.exists(PRODUCT_PATH):
        PRODUCT_PATH = os.path.abspath('Product.csv')
        if not os.path.exists('Product.csv'): mkprod(PRODUCT_PATH)
        
    if not os.path.exists(STOCK_PATH):
        STOCK_PATH = os.path.abspath('Stock.csv')
        if not os.path.exists('Stock.csv'): mkstock(STOCK_PATH)
        
    if not os.path.exists(PROMO_PATH):
        PROMO_PATH = os.path.abspath('Promo.csv')
        if not os.path.exists('Promo.csv'): mkpromo(PROMO_PATH)
        
    # be nice and let the user know which files are used
    print("product: '{0}'".format(PRODUCT_PATH))
    print("stock: '{0}'".format(STOCK_PATH))
    print("promo: '{0}'".format(PROMO_PATH))
        
        
        
        
        
        
