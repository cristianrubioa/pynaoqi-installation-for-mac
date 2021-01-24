# Pyhon Naoqi Installation Guide For Mac

<div align="left">

<a href="https://www.python.org/downloads/"><img alt="Python 2.7+" src="https://img.shields.io/badge/python-2.7+-yellow.svg" /></a>


## Installing the SDK

1. You can download the SDK from [SoftBank Robotics](https://developer.softbankrobotics.com/nao6/downloads/nao6-downloads-mac) for the latest version of the SDK **OR** from the following repository for robots older than NAO Power V6:

```
git clone https://github.com/cristianrubioa/pynaoqi-installation-for-mac
```


2. Extract Python SDK: 

**Note:** In case of downloading from the repository, go to the third step.

```
tar -xzvf pynaoqi-python-2.7-naoqi-x.x-mac64.tar.gz
mv pynaoqi-python-2.7-naoqi-x.x-mac64 pynaoqi	
```


3. Add environment variables:

```
export PYTHONPATH=${PYTHONPATH}:/path/to/python-sdk/lib/python2.7/site-packages
export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:/path/to/python-sdk/lib
export QI_SDK_PREFIX=/path/to/python-sdk
```

4. Run the following command on your terminal:

``` 
open ~/.bash_profile 
```

5. To make it use globally, copy the commands from Step-3 and paste it in ```.bash_profile```, for example: 

```
export PYTHONPATH=${PHTHONPATH}:/Users/admin/Documents/pynaoqi/lib/python2.7/site-packages
export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:/Users/admin/Documents/pynaoqi/lib
export QI_SDK_PREFIX=/Users/admin/Documents/pynaoqi
```


6. Save the file and close the editor ```.bash_profile```.

7. Force the execution of the .bash_profile file to see the changes immediately without having to restart:

``` 
source ~/.bash_profile 
```


## Checking the Installation

Open the terminal and try to run:

```python
python
>>> import naoqi
>>>
```
**Note:** If you do not get any error message, you are now ready to use the Python SDK.
