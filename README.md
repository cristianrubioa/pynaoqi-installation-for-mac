# Pyhon Naoqi Installation Guide For Mac

<div align="left">

<a href="https://www.python.org/downloads/"><img alt="Python 2.7+" src="https://img.shields.io/badge/python-2.7+-yellow.svg" /></a>


## Naoqi for Python

1. You can download the SDK from SoftBank Robotics Community website. [here](https://community.aldebaran.com/en/resources/software/language/en-gb/field_software_type/sdk/robot/nao-2).


2. Extract pynaoqi: 

```
$ tar -xzvf pynaoqi-python-2.7-naoqi-x.x-mac64.tar.gz.tar.gz
```

3. Add environment variables:

```
$ export PYTHONPATH=${PYTHONPATH}:/path/to/python-sdk
$ export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:/path/to/python-sdk
```

4. Run the following command on your terminal:

``` 
$ open ~/.bash_profile 
```

5. To make it use globally, copy the commands from Step-2 and paste it in .bash_profile, for example: 

```
$ export PYTHONPATH=${PHTHONPATH}:/Users/admin/Documents/pynaoqi/lib/python2.7/site-packages
$ export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:/Users/admin/Documents/pynaoqi/lib
```


6. Save the file and close the editor .bash_profile.

7. Force the execution of the .bash_profile file to see the changes immediately without having to restart.

``` 
$ source ~/.bash_profile 
```
