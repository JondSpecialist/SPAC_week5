The file Uge5_OOP is the submission for the week5 niveau 2 assignment

It creates a artificial database for a clothing warehouse, using a singleton pattern
to ensure everything is stored in the same instance of the database.
It also attempts to adhere to the factory method pattern to keep the classes and functions
robust and reusable.

The class DataFrame is the singleton class used to store the variables of the virtual warehouse.
The Singleton instance is implemented by setting a parameter to None and having the __init__
function check if this parameter is None and only then running the main body of this class (and
updating the parameter so calling this class again won't initialise a new instance.
This implementation of a singleton pattern is adapted from a code recipe from activestate.com.
The DataFrame object acts as storage of variables and most other classes and functions will
append or add to one of its attributs or act on an object stored within.

The Ware class is the parent class for the clothing objects to be stored in the DataBase object,
it has a few attributes, most importantly ID, which is used to crossreference between different
lists and objects.
Following are the 8 subclasses of Ware, each for an article of clothing, each adding the category
attribute.

The functions random_color and random_clothing (not in use, but possibly useful) are defined
to make arbitrary choices of arguments for other objects and functions.

The Order class creates an object with attributes describing a shipping order, containing 
information about the item being shipped, shipping status, destination adress and shipping cost.
It modifies the DataFrame instance corresponding to an item being removed from the inventory
and being prepared for shipping.

The 3 functions shipOrder, deliverOrder and returnOrder are used to update the status attribute
of an Order object and a Ware object as well as move the Ware object to the appropriate list
stored in the DataFrame instance and adjusts other DataFrame attributes as needed.
4 small functions help with these, and a few other places:
	- matchOrderIndex takes the ID attribute of an Order object and finds the index of a 
	  Ware object with matching ID in a requested DataFrame list.
	- changeInventoryStatus simply moves an object from one list to another.
	- UpdateOrderStatus uses matchOrderIndex to change the status attribute of both an 
	  Order object and a Ware object in a DataFrame list.
	- UpdateItemStatus simply changes the status parameter of a Ware or Order Object.

The Factory class is used to produce new Ware objects, taking the name of one of the Ware
subclasses and the arguments needed to initiate it.

The Restock Class adds items to the Dataframe instance using the Factory class.
It then uses the UpdateDataFrame function to change any other relevant attributes in the
DataFrame instance.

The function OrderRequest attempts to create an Order object containing a Ware object with
attributes matching the arguments passed to the function.
To do this it utilises 4 other functions:
	- MatchProductDetails checks if the attributes of a Ware object matches the 3 passed
	  arguments and only returns True if all 3 do.
	- CheckAvailability uses this to loop through the inventory attribute of the DataFrame
	  instance and returns True, the object and the index if it finds the match.
	- MatchProductDetailsAnyColor and CheckAvailabilityAnyColor are variations on the
	  2 above functions that allows to look for Ware objects while ignoring the color
	  attribute, thus potentially finding additional matches.

The RestockBasis function is a simple quality of life function, utilising the Restock class
to create a bunch of Ware objects that any selfrespecting clothing store should have.  

The Warehouse class is the integration test of everything above, it:
       - Initiates the singleton class DataFrame
       - stocks the virtual warehouse
       - places a bunch of orders, some of which may fail
       - advances some of the orders by shipping, delivering and returning some
       - prints out info about the final state of the Dataframe instance:
          * Overview of number of wares of each type
          * Total number of items and total value
          * dicts of 5 random items from the DataFrame.inventory attribute
          * dicts of 5 random orders

Potential improvements:
- A small inconsistency means the Ware subclass is passed directly to the Restock class, 
  while the OrderRequest function needs to be passed the subclass name as string. Slightly
  annoying but manageable.
- the Order class can currently only contain one Ware object, adding the ability to have
  several items per order could be nice.
- Having an option to pass an argument to give discounts on orders could be nice.



Dependencies:
-faker





