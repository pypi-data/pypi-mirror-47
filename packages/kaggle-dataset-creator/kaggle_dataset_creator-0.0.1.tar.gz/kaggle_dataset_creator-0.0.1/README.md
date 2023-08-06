# kaggle_dataset_creator - A  Python package to generate csv/json

A Python package that allows you to create CSV/JSON files by manually entering each
of the entries of cells row by row in Terminal (Windows CMD / Bash).


## Installation

Open terminal and enter the below command (Python 3).

> pip install kaggle_dataset_creator

## Features

+ It allows you to create your own CSV file if you are looking for creating a CSV with manually entered data. You can also get the JSON version of the entered data.

+ You can also view your data at any point of time in your Terminal and again continue 
to enter data if you wish to add more rows/records for your final CSV/JSON file.

> Note: Currently the package is in development, it will be released soon.

## Example

```python
from kaggle_dataset_creator import KaggleDataSet

kd = KaggleDataSet()
kd.start()

print(kd.columns)
print(kd.container)

kd.view();   # To view the final DataFrame on Terminal
kd.to_csv(); # To save in csv, default file name is take if filename is not provided 

print("DATA:- ")
print(kd.dataset) # Accessing dataset attribute to get the final DataFrame

print('Total rows: ', kd.rows)
print('Types: ', kd.data_types)
```

If you want to try above in the terminal, try as below after installation.

> In next version, it will be released with more features. Here our intension is to get the final CSV/JSON.

```bash
>>> from kaggle_dataset_creator import KaggleDataSet
>>>
>>> kd = KaggleDataSet()
>>> kd.start()
Enter number of columns that you want in your dataset: 3

SUCCESS: You are successfully done with no. of columns
Enter the name of 1st column: fullname
Enter the name of 2nd column: age
Enter the name of 3rd column: salary

SUCCESS: You are successfully done with the column names
[DATA ENTRY] <row: 1>  fullname    : Raj Shekhar
[DATA ENTRY] <row: 1>  age         : 45
[DATA ENTRY] <row: 1>  salary      : 600000

==================================================
Do you want to add 1 more row / view data (y/n/v): y
==================================================
[DATA ENTRY] <row: 2>  fullname    : Venc Bell
[DATA ENTRY] <row: 2>  age         : 67
[DATA ENTRY] <row: 2>  salary      : 900000

==================================================
Do you want to add 1 more row / view data (y/n/v): y
==================================================
[DATA ENTRY] <row: 3>  fullname    : Robert Grime
[DATA ENTRY] <row: 3>  age         : 89
[DATA ENTRY] <row: 3>  salary      : 9000000

==================================================
Do you want to add 1 more row / view data (y/n/v): v

--------------------------------------------------
       fullname age   salary
0   Raj Shekhar  45   600000
1     Venc Bell  67   900000
2  Robert Grime  89  9000000
--------------------------------------------------

==================================================
Do you want to add 1 more row / view data (y/n/v): y
==================================================
[DATA ENTRY] <row: 4>  fullname    : Elen Goom
[DATA ENTRY] <row: 4>  age         : 55
[DATA ENTRY] <row: 4>  salary      : 800000

==================================================
Do you want to add 1 more row / view data (y/n/v): y
==================================================
[DATA ENTRY] <row: 5>  fullname    : Rita Ora
[DATA ENTRY] <row: 5>  age         : 36
[DATA ENTRY] <row: 5>  salary      : 9900000

==================================================
Do you want to add 1 more row / view data (y/n/v): v

--------------------------------------------------
       fullname age   salary
0   Raj Shekhar  45   600000
1     Venc Bell  67   900000
2  Robert Grime  89  9000000
3     Elen Goom  55   800000
4      Rita Ora  36  9900000
--------------------------------------------------

==================================================
Do you want to add 1 more row / view data (y/n/v): y
==================================================
[DATA ENTRY] <row: 6>  fullname    : Senso Tomy
[DATA ENTRY] <row: 6>  age         : 54
[DATA ENTRY] <row: 6>  salary      : 7700000

==================================================
Do you want to add 1 more row / view data (y/n/v): n
Is this mistakenly typed (y/n): n
==================================================

SUCCESS: You are successfully done with entering data for your dataset
>>>
>>> # View the data
...
>>> kd.view()

--------------------------------------------------
       fullname age   salary
0   Raj Shekhar  45   600000
1     Venc Bell  67   900000
2  Robert Grime  89  9000000
3     Elen Goom  55   800000
4      Rita Ora  36  9900000
5    Senso Tomy  54  7700000
--------------------------------------------------
True
>>>
>>> success = kd.view()

--------------------------------------------------
       fullname age   salary
0   Raj Shekhar  45   600000
1     Venc Bell  67   900000
2  Robert Grime  89  9000000
3     Elen Goom  55   800000
4      Rita Ora  36  9900000
5    Senso Tomy  54  7700000
--------------------------------------------------
>>>
>>> success
True
>>>
>>> # Store the dataset as DataFrame
...
>>> df = kd.dataset
>>> df
       fullname age   salary
0   Raj Shekhar  45   600000
1     Venc Bell  67   900000
2  Robert Grime  89  9000000
3     Elen Goom  55   800000
4      Rita Ora  36  9900000
5    Senso Tomy  54  7700000
>>>
>>> type(df)
<class 'pandas.core.frame.DataFrame'>
>>>
>>> kd.rows
6
>>>
>>> kd.data_types
{'fullname': 'string', 'age': 'numeric', 'salary': 'numeric'}
>>>
```


## Generating random strings

```bash
Python 3.6.7 (v3.6.7:6ec5cf24b7, Oct 20 2018, 03:02:14) 
[GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 
>>> from kaggle_dataset_creator.random_string import random_string
>>> 
>>> random_string()
'VFdwQmVFOV'
>>> 
>>> random_string()
'TWpBeE9TMH'
>>> 
>>> random_string()
'=UDN0gDN54'
>>> 
>>> random_string()
'TWpBeE9TMH'
>>> 
>>> random_string()
'=ATM1UDMz4'
>>> 
>>> random_string(11)
'VFdwQmVFOVR'
>>> 
>>> random_string(15)
'5M2RW5kTUVVRxAT'
>>> 
>>> random_string(15)
'VFdwQmVFOVRNSGR'
>>> 
>>> random_string(15)
'5M2RS9kQUFVR5sW'
>>> 
>>> random_string(15)
'=AzN2MDMy4iNzoz'
>>> 
>>> random_string(15)
'MjAxOS0wNS0yMSA'
>>> 
```
