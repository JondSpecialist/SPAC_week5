import numpy as np
import random
from faker import Faker
#import matplotlib.colors as mcolors

# Main class for storing other objects, with singelton functionality 
class DataFrame: 
    #################    
    ### SINGLETON ###
    #################
    # initialisation checks for instance and only initialises the actual object if there are no other instances
    __instance  = None
    def  __init__(self):
        if DataFrame.__instance is None:
            DataFrame.__instance = DataFrame.__impl()  
        #self.__dict__['_DataFrame_instance'] = DataFrame.__instance
        
    #redirects any function calls to the inner class __impl
    def __getattr__(self, attr):
        return getattr(self.__instance, attr)
    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)
    
    #Actual code goes in this inner class
    class __impl:
        def __init__(self):
            self.inventory = []
            self.inventoryDicts = []
            self.totalInventory = 0
            self.inventoryOverview = {}
            self.inventoryValue = 0
            self.activeOrderWares = []
            self.soldWaresLog = []
            self.orderLog = []
        # Test function to check ID
        def spam(self):
            return id(self)
    

#Test class to check if I can bypass the singleton (I can't, at least not this way)
class idk(DataFrame):
    pass

# Base class for items to be stored in the database, classes for all wares inherit from this one
class Ware:
    def __init__(self, price):
        self.ID = id(self)
        self.price = price
        self.status = 'Available'

# 8 classes for articles of clothing, all subclasses of Ware
class Shirt(Ware):
    def __init__(self,color,price):
        super().__init__(price)
        self.category = 'Shirt'
        self.color = color
    
class Shorts(Ware):
    def __init__(self,color,price):
        super().__init__(price)
        self.category = 'Shorts'
        self.color = color
        
class Shoes(Ware):
    def __init__(self,color,price):
        super().__init__(price)
        self.category = 'Shoes'
        self.color = color
        
class Socks(Ware):
    def __init__(self,color,price):
        super().__init__(price)
        self.category = 'Socks'
        self.color = color

class Jeans(Ware):
    def __init__(self,color,price):
        super().__init__(price)
        self.category = 'Jeans'
        self.color = color

class Hat(Ware):
    def __init__(self,color,price):
        super().__init__(price)
        self.category = 'Hat'
        self.color = color

class Dress(Ware):
    def __init__(self,color,price):
        super().__init__(price)
        self.category = 'Dress'
        self.color = color
        
class Underwear(Ware):
    def __init__(self,color,price):
        super().__init__(price)
        self.category = 'Underwear'
        self.color = color

# 2 functions for choosing random clothes and colors
def random_clothes():
    return random.choice(['Shirt','Shorts','Socks','Shoes','Jeans','Hat','Dress', 'Underwear'])

def random_color():
    #random_color =list(mcolors.TABLEAU_COLORS.keys())
    #for i in range(len(random_color)):
    #    random_color[i] = random_color[i][4:]
    #random_color.append('black')
    #random_color.append('white')
    #random_color.append('yellow')
    #print(random_color)
    #return random.choice(random_color)
    
    # Sometimes simpler is better:
    return random.choice(['Blue', 'Orange', 'Green', 'Red', 'Purple', 'Brown', 'Pink', 'Gray', 'Olive', 'Cyan', 'Black', 'White', 'Yellow'])


# Class for storing customer orders, storing the items ordered as well as an adress and the shipping cost.
# The initialisation takes a DataFrame object and store the order there, also adjusting relevant attributes
class Order:
    def __init__(self, DataFrame, items, adress, shipping): #maybe just 1 item?
        self.ID = id(self)
        self.items = items
        self.itemsDescr = items.__dict__
        self.total = shipping
        self.total += items.price
        self.adress = adress
        self.status = 'Order placed'
        
        index = matchOrderIDindex(self, DataFrame.inventory)
        DataFrame.inventory[index].status = 'Order placed'
        DataFrame.inventoryValue -= items.price
        DataFrame.totalInventory -= 1
        changeInventoryStatus(DataFrame.activeOrderWares,DataFrame.inventory, index)
        #DataFrame.activeOrderWares.append(DataFrame.inventory[index])
        #DataFrame.inventory.pop(index)
        DataFrame.inventoryDicts.pop(index)
        DataFrame.inventoryOverview[items.category] -= 1
        
        DataFrame.orderLog.append(self)

# Many of the functions below could probably be part of the Order class.        
# function for moving items to another list, ie from the purchasable inventory to being associated with an order
def changeInventoryStatus(_to, _from, index):
    _to.append(_from[index])
    _from.pop(index)

# function for updating the status attribute of a Ware object in both an order object and the dataframe
# The ID of the object is used to locate its location in the dataframe
def UpdateOrderStatus(DataFrame, Order, status):
    Order.status = status
    index = matchOrderIDindex(Order, DataFrame)
    DataFrame[index].status = status

# simple function to update the status attribute of an object
def UpdateItemStatus(Item, Status):
    Item.status = Status

# Change the status of an Order object and the associated Ware object to shipped
def shipOrder(DataFrame, Order):
    UpdateOrderStatus(DataFrame.activeOrderWares, Order, 'Shipped')

# Change the status of an Order object and the associated Ware object to delivered 
# and move the Ware object to the DataFrame attribute for sold wares
def deliverOrder(DataFrame, Order):
    UpdateOrderStatus(DataFrame.activeOrderWares, Order, 'Delivered')
    index = matchOrderIDindex(Order, DataFrame.activeOrderWares)
    changeInventoryStatus(DataFrame.soldWaresLog, DataFrame.activeOrderWares, index)


# Change the status of an Order object and the associated Ware object to returned
# and move the Ware object to the DataFrame attribute for inventory as it is now available again.
# Also edits other relevant attributes in the Dataframe to reflect the Ware object being added back.
def returnOrder(DataFrame, Order):
    UpdateOrderStatus(DataFrame.soldWaresLog, Order, 'Returned')
    DataFrame.inventoryValue += Order.items.price
    DataFrame.totalInventory += 1
    index = matchOrderIDindex(Order, DataFrame.soldWaresLog)
    DataFrame.inventoryDicts.append(DataFrame.soldWaresLog[index].__dict__)
    changeInventoryStatus(DataFrame.inventory,DataFrame.soldWaresLog, index)
    DataFrame.inventoryOverview[Order.items.category] += 1

# for the Ware of an Order object looks for its location in a dataframe attribute using the ID attribute. 
def matchOrderIDindex(Order, Inventory):
    index = next((i for i, item in enumerate(Inventory) if item.ID == Order.items.ID), None)
    if index == None:
        print('No ID match found!')
    return index

# Class for creating wares
class Factory: 
    def __init__(self, _type,*args): 
        temp =_type(*args)
        self.__dict__ = temp.__dict__

# use the Factory class to add a number of copies of a ware to the DataFrame instance and
# update the relevant attributes using the UpdateDataFrame function
class Restock:
    def __init__(self, DataFrame, _type, args, volume=1, randomColor =False): #DataFrame,
        self.inventory = []
        if randomColor == True:
            args.pop(0)
            for i in range(volume):
                self.inventory.append(Factory(_type, random_color() ,*args))
        else:
            for i in range(volume):
                self.inventory.append(Factory(_type,*args))
        for item in self.inventory:
            UpdateDataFrame(DataFrame, item)

# changes the relevant attributes of the dataframe instance using the attributes of a given Ware object
def UpdateDataFrame(DataFrame, item):
    DataFrame.inventory.append(item)
    DataFrame.inventoryDicts.append(item.__dict__)
    DataFrame.totalInventory += 1
    DataFrame.inventoryValue += item.price
    if item.category not in DataFrame.inventoryOverview.keys(): #might need an () after keys or conversion to list
        DataFrame.inventoryOverview[item.category] = 1
    else:
        DataFrame.inventoryOverview[item.category] += 1

# Tries to create an Order object given desired attributes of the associated Ware object.
def OrderRequest(DataFrame, _type, color, maxPrice, adress, shipping, anyColor = False):
    # check if desired item is available & make order
    _available = CheckAvailability(DataFrame, _type, color, maxPrice, _anyColor=anyColor)
    if _available[0] == True:
        Order(DataFrame,DataFrame.inventory[_available[2]],adress,shipping)
        #print(test_OR.__dict__)
    elif _available[0] == False and anyColor == True:
        _available = CheckAvailabilityAnyColor(DataFrame, _type, maxPrice)
        if _available[0] == True:
            Order(DataFrame,DataFrame.inventory[_available[2]],adress,shipping)
    pass

# Checks if the desired attributes matches a ware object present in the dataframe instance
# The function returns the first object that matches the search parameters
# has an option to ignore color preferences if unavailable
# If the check comes back negative a print statement is made to that effect.
def CheckAvailability(DataFrame, _type, color, maxPrice, _anyColor=False):
    for i in range(len(DataFrame.inventory)):
        if MatchProductDetails(DataFrame.inventory[i], _type, color, maxPrice) is True:
            #print((DataFrame.inventoryDicts[i])) #Just for checking code
            return True, DataFrame.inventory[i], i
            break
    if _anyColor == False:
        print('Desired product not in stock! '+color+' '+_type+' for less than '+str(maxPrice)+'$')
    return [False]

# Returns True only if all 3 attributes of a Ware object match search parameters, used in CheckAvailability
def MatchProductDetails(item, _type, color, maxPrice):
    # _type and color should be written in string to match the attributes of the Ware classes
    return item.category == _type and item.color == color and item.price <= maxPrice

# Variation of CheckAvailability that ignores color
def CheckAvailabilityAnyColor(DataFrame, _type,  maxPrice):
    for i in range(len(DataFrame.inventory)):
        if MatchProductDetailsAnyColor(DataFrame.inventory[i], _type, maxPrice) is True:
            #print((DataFrame.inventoryDicts[i])) #Just for checking code
            return True, DataFrame.inventory[i], i
            break 
    print('Desired product not in stock! '+_type+' for less than '+str(maxPrice)+'$')

# Variation of MatchProductDetails that ignores color
def MatchProductDetailsAnyColor(item, _type, maxPrice):
    # _type and color should be written in string to match the attributes of the Ware classes
    return item.category == _type  and item.price <= maxPrice

# Quality of life function that calls the Restock class 9 times to add items you would expect to sell most of
def RestockBasics(DataFrame):
    Restock(DataFrame, Underwear, ['Black', 8.00], volume=5) # 5 underwear black
    Restock(DataFrame, Underwear, ['Gray', 8.00], volume=5) # 5 underwear gray
    Restock(DataFrame, Underwear, ['White', 8.00], volume=5) # 5 underwear white
    Restock(DataFrame, Socks, ['Black', 5.00], volume=5) # 5 socks black
    Restock(DataFrame, Socks, ['White', 5.00], volume=5) # 5 socks white
    Restock(DataFrame, Shirt, ['White', 35.00], volume=5) # 5 shirts white
    Restock(DataFrame, Jeans, ['Blue', 45.00], volume=5) # 5 jeans blue
    Restock(DataFrame, Jeans, ['Black', 45.00], volume=5) # 5 jeans black
    Restock(DataFrame, Shoes, ['Black', 50.00], volume=5) # 5 shoes black   


# Integration test for the implemented classes and functions; 
#       - Initiates the singleton class DataFrame
#       - stocks the virtual warehouse
#       - places a bunch of orders, some of which may fail
#       - advances some of the orders by shipping, delivering and returning some
#       - prints out info about the final state of the Dataframe instance:
#           * Overview of number of wares of each type
#           * Total number of items and total value
#           * dicts of 5 random items from the DataFrame.inventory attribute
#           * dicts of 5 random orders
class Warehouse:
    def __init__(self):
        # DataFrame initiated
        Warehouse_df = DataFrame()
        
        
        # Getting some items for the warehouse
        RestockBasics(Warehouse_df)
        #Restock(DataFrame, _type, args, volume=1, randomColor =False) #just to help me remember the inputs
        Restock(Warehouse_df, Dress,[random_color(),55.00],volume=10,randomColor=True)
        Restock(Warehouse_df, Hat,[random_color(),25.00],volume=10,randomColor=True)
        Restock(Warehouse_df, Shorts,[random_color(),35.00],volume=10,randomColor=True)
        Restock(Warehouse_df, Shirt,[random_color(),35.00],volume=10,randomColor=True)
        Restock(Warehouse_df, Socks,[random_color(),5.00],volume=10,randomColor=True)
        Restock(Warehouse_df, Jeans,[random_color(),45.00],volume=10,randomColor=True)
        Restock(Warehouse_df, Shoes,[random_color(),50.00],volume=10,randomColor=True)
        
        
        # Making up some customer orders, using the Faker module to generate adresses
        Warehouse_fake = Faker()
        #OrderRequest(DataFrame, _type, color, maxPrice, adress, shipping, anyColor = False) #just to help me remember the inputs
        OrderRequest(Warehouse_df, 'Dress', 'Red', 60, Warehouse_fake.address(), 10, anyColor=False)
        OrderRequest(Warehouse_df, 'Dress', 'Blue', 75, Warehouse_fake.address(), 10, anyColor=False)
        OrderRequest(Warehouse_df, 'Dress', ' ', 75, Warehouse_fake.address(), 10, anyColor=True)
        OrderRequest(Warehouse_df, 'Dress', ' ', 75, Warehouse_fake.address(), 10, anyColor=True)
        OrderRequest(Warehouse_df, 'Dress', ' ', 75, Warehouse_fake.address(), 10, anyColor=True)
        OrderRequest(Warehouse_df, 'Hat', ' ', 30, Warehouse_fake.address(), 10, anyColor=True)
        OrderRequest(Warehouse_df, 'Shorts', ' ', 40, Warehouse_fake.address(), 10, anyColor=True)
        OrderRequest(Warehouse_df, 'Jeans', 'Blue', 50, Warehouse_fake.address(), 10, anyColor=False)
        OrderRequest(Warehouse_df, 'Jeans', 'Black', 50, Warehouse_fake.address(), 10, anyColor=False)
        OrderRequest(Warehouse_df, 'Shirt', 'White', 55, Warehouse_fake.address(), 10, anyColor=False)
        OrderRequest(Warehouse_df, 'Shirt', ' ', 55, Warehouse_fake.address(), 10, anyColor=True)
        OrderRequest(Warehouse_df, 'Shirt', ' ', 55, Warehouse_fake.address(), 10, anyColor=True)
        OrderRequest(Warehouse_df, 'Socks', 'Black', 10, Warehouse_fake.address(), 10, anyColor=False)
        OrderRequest(Warehouse_df, 'Socks', 'Black', 10, Warehouse_fake.address(), 10, anyColor=False)
        OrderRequest(Warehouse_df, 'Underwear', ' ', 10, Warehouse_fake.address(), 10, anyColor=True)
        OrderRequest(Warehouse_df, 'Underwear', ' ', 10, Warehouse_fake.address(), 10, anyColor=True)
        OrderRequest(Warehouse_df, 'Underwear', ' ', 10, Warehouse_fake.address(), 10, anyColor=True)
        OrderRequest(Warehouse_df, 'Underwear', ' ', 10, Warehouse_fake.address(), 10, anyColor=True)
        OrderRequest(Warehouse_df, 'Shoes', 'Black', 60, Warehouse_fake.address(), 10, anyColor=False)
        OrderRequest(Warehouse_df, 'Shoes', ' ', 60, Warehouse_fake.address(), 10, anyColor=True)
        OrderRequest(Warehouse_df, 'Dress', 'Cyan', 10, Warehouse_fake.address(), 10, anyColor=False)
        
        # Arbitrarily progressing some orders, 
        # using 2^n as modulo ensures the shipping order order place -> shipped -> delivered (-> returned) is followed
        for o in range(len(Warehouse_df.orderLog)):
            if (o % 2) == 0 or (o % 3) == 0:
                shipOrder(Warehouse_df, Warehouse_df.orderLog[o])
            if (o % 4) == 0:
                deliverOrder(Warehouse_df, Warehouse_df.orderLog[o])
            if (o % 8) == 0:
                returnOrder(Warehouse_df, Warehouse_df.orderLog[o])
        
        
        #Printing out an overview and some samples of the logs of the warehouse
        print('\n########## WAREHOUSE ##########\n')
        print()
        print('Inventory overview:\n'+str(Warehouse_df.inventoryOverview)+'\n')
        print('Total wares in warehouse: '+str(Warehouse_df.totalInventory))
        print('Value of goods in warehouse: '+str(Warehouse_df.inventoryValue)+'$\n')
        print('Wares in inventory (5 random):')
        random_wares = random.choices(Warehouse_df.inventoryDicts,k=5)
        for r in range(5):
            print('- - - - - - -')
            print(random_wares[r])
            
        print('\nLog of orders (5 random):')
        random_orders = random.choices(Warehouse_df.orderLog,k=5)
        for l in range(5):
            print('- - - - - - -')
            print(random_orders[l].__dict__)
        
###########################################################################
######################### Executing functions #############################
###########################################################################

Warehouse()

print('\n - - - - - - - - - \n')

df = DataFrame()
print(df.spam())
df2 = DataFrame()
print(df2.spam())
df3 = idk()
print(df3.spam())
print(df.inventoryOverview)
print(df3.inventoryOverview)
print('\nTrying to create new instances of DataFrame just points back to the old, singleton pattern seems to be working.')

#['Blue', 'Orange', 'Green', 'Red', 'Purple', 'Brown', Pink', 'Gray', 'Olive', 'Cyan', 'Black', 'White', 'Yellow']
#['Shirt','Shorts','Socks','Shoes','Jeans','Hat','Dress', 'Underwear']






