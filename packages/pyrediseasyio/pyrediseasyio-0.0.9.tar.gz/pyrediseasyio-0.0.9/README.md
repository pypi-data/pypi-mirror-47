# PyRedisEasyIO
A project to simplify reading/writing single objects from/to redis


## Description
Redis is a great way to share data between applications - or processes in an application. 
However, in its raw form, the application has to deal with data type conversion to/from
string, check for existence, and other pesky stuff. It would be nice if that were 
abstracted in such a way to where it didn't appear in code that redis was being used
at all. 

This project seeks to allow the exchange of single data points in a readable way, eg. 
my_data.my_value = 30 (automatically writes '30' to redis) 

## Installation
pip install pyrediseasyio


## Usage
The basis of functionality is the IOGroup class. It acts as a container for individual values
and performs the behind-the-scenes reads and writes. 

~~~~
from io_group import IOGroup
from single_io import BooleanIO, IntIO, FloatIO


class TestGroup1(IOGroup):
    Bool1 = BooleanIO("Boolean 1", "Bool1", False)
    Bool2 = BooleanIO("Boolean 2", "Bool2", True)
    Int1 = IntIO("Integer 1", "Int1")
    Int2 = IntIO("Integer 2", "Int2", default=34)
    Float1 = FloatIO("Float 1", "Float1", default=1.2)

class TestGroup2(IOGroup):
    Bool1 = BooleanIO("Boolean 1", "Bool1", False)
    Bool2 = BooleanIO("Boolean 2", "Bool2", True)
    Int1 = IntIO("Integer 1", "Int1")
    Int2 = IntIO("Integer 2", "Int2", default=34)
    Float1 = FloatIO("Float 1", "Float1", default=1.2)
   

group1a = TestGroup1()
group1b = TestGroup1()
group2 = TestGroup2()

group1a.Float1 = 1234.5
print(group1b.Float1.value)
print(group2.Float1.value)
~~~~

That is really all there is to it. For more specific cases, see the unit tests.