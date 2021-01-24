import os
import sys
import ctypes
import weakref
import logging
import inspect
from functools import partial

import qi


def set_dll_directory():
    this_dir = os.path.abspath(os.path.dirname(__file__))
    bin_dir = os.path.join(this_dir, "..", "bin")
    if os.path.exists(bin_dir):
        ctypes.windll.kernel32.SetDllDirectoryA(bin_dir)

def load_inaoqi_deps():
    """ Helper to laod _inaoqi.so deps on linux """
    deps = [
            "libboost_python.so",
            "libboost_system.so",
            "libboost_chrono.so",
            "libboost_program_options.so",
            "libboost_thread.so",
            "libboost_filesystem.so",
            "libboost_regex.so",
            "libboost_locale.so",
            "libboost_signals.so",
            "libqi.so",
            "libalerror.so",
            "libalthread.so",
            "libalvalue.so",
            "libalcommon.so",
            "libalproxies.so",
            "libalpythontools.so",
            "libqipython.so",
            "libinaoqi.so"
    ]
    relpaths = [
            # in pynaoqi, this file is /naoqi.py and we search for /libqi.so
            [],
            # in deploys/packages/etc,
            # this file is $PREFIX/lib/python2.7/site-packages/naoqi.py
            # and we need $PREFIX/lib/libqi.so
            ["..", ".."],
            ]
    this_dir = os.path.abspath(os.path.dirname(__file__))
    for dep in deps:
        for relpath in relpaths:
            list_path = [this_dir] + relpath + [dep]
            full_path = os.path.join(*list_path)
            try:
                ctypes.cdll.LoadLibrary(full_path)
            except Exception:
                pass

if sys.platform.startswith("linux"):
    load_inaoqi_deps()

if sys.platform.startswith("win"):
    set_dll_directory()

import inaoqi

import motion
import allog

def _getMethodParamCount(func):
    r = inspect.getargspec(func)
    #normal args
    np = len(r[0])
    #*args (none if non existent)
    if r[1] is not None:
        np = np + 1
    #**kargs  (none if non existent)
    if r[2] is not None:
        np = np + 1
    return np

def autoBind(myClass, bindIfnoDocumented):
  """Show documentation for each
  method of the class"""

  # dir(myClass) is a list of the names of
  # everything in class
  myClass.setModuleDescription(myClass.__doc__)

  for thing in dir(myClass):
    # getattr(x, "y") is exactly: x.y
    function = getattr(myClass, thing)
    if callable(function):
        if (type(function) == type(myClass.__init__)):
            if (bindIfnoDocumented or function.__doc__ != ""):
                if (thing[0] != "_"):  # private method
                    if (function.__doc__):
                        myClass.functionName(thing, myClass.getName(), function.__doc__)
                    else:
                        myClass.functionName(thing, myClass.getName(), "")

                    for param in function.func_code.co_varnames:
                        if (param != "self"):
                            myClass.addParam(param)
                        myClass._bindWithParam(myClass.getName(),thing, _getMethodParamCount(function)-1)



class ALDocable():
  def __init__(self, bindIfnoDocumented):
    autoBind(self,bindIfnoDocumented)


# define the log handler to be used by the logging module
class ALLogHandler(logging.Handler):
  def __init__(self):
    logging.Handler.__init__(self)

  def emit(self, record):
    level_to_function = {
      logging.DEBUG: allog.debug,
      logging.INFO: allog.info,
      logging.WARNING: allog.warning,
      logging.ERROR: allog.error,
      logging.CRITICAL: allog.fatal,
    }
    function = level_to_function.get(record.levelno, allog.debug)
    function(record.getMessage(),
             record.name,
             record.filename,
             record.funcName,
             record.lineno)


# define a class that will be inherited by both ALModule and ALBehavior, to store instances of modules, so a bound method can be called on them.
class NaoQiModule():
  _modules = dict()

  @classmethod
  def getModule(cls, name):
    # returns a reference a module, giving its string, if it exists !
    if(name not in cls._modules):
      raise RuntimeError("Module " + str(name) + " does not exist")
    return cls._modules[name]()

  def __init__(self, name, logger=True):
    # keep a weak reference to ourself, so a proxy can be called on this module easily
    self._modules[name] = weakref.ref(self)
    self.loghandler = None
    if logger:
        self.logger = logging.getLogger(name)
        self.loghandler = ALLogHandler()
        self.logger.addHandler(self.loghandler)
        self.logger.setLevel(logging.DEBUG)

  def __del__(self):
    # when object is deleted, clean up dictionnary so we do not keep a weak reference to it
    del self._modules[self.getName()]
    if(self.loghandler != None):
        self.logger.removeHandler(self.loghandler)


class ALBroker(inaoqi.broker):
    def init(self):
        pass

class ALModule(inaoqi.module, ALDocable, NaoQiModule):

  def __init__(self,param):
    inaoqi.module.__init__(self, param)
    ALDocable.__init__(self, False)
    NaoQiModule.__init__(self, param)
    self.registerToBroker()

  def __del__(self):
    NaoQiModule.__del__(self)

  def methodtest(self):
    pass

  def pythonChanged(self, param1, param2, param3):
    pass

class MethodMissingMixin(object):
    """ A Mixin' to implement the 'method_missing' Ruby-like protocol. """
    def __getattribute__(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except:
            class MethodMissing(object):
                def __init__(self, wrapped, method):
                    self.__wrapped__ = wrapped
                    self.__method__ = method
                def __call__(self, *args, **kwargs):
                    return self.__wrapped__.method_missing(self.__method__, *args, **kwargs)

            return MethodMissing(self, attr)

    def method_missing(self, *args, **kwargs):
        """ This method should be overridden in the derived class. """
        raise NotImplementedError(str(self.__wrapped__) + " 'method_missing' method has not been implemented.")


class postType(MethodMissingMixin):
    def __init__(self):
        ""

    def setProxy(self, proxy):
        self.proxy = weakref.ref(proxy)
     #   print name

    def method_missing(self, method, *args, **kwargs):
          list = []
          list.append(method)
          for arg in args:
            list.append(arg)
          result = 0
          try:
                  p =  self.proxy()
                  result = p.pythonPCall(list)
          except RuntimeError,e:
                raise e

          return result



class ALProxy(inaoqi.proxy,MethodMissingMixin):

    def __init__(self, *args):
        self.post = postType()
        self.post.setProxy(self)
        if (len (args) == 1):
            inaoqi.proxy.__init__(self, args[0])
        elif (len (args) == 2):
            inaoqi.proxy.__init__(self, args[0],  args[1])
        else:
            inaoqi.proxy.__init__(self, args[0], args[1], args[2])

    def call(self, *args):
        list = []
        for arg in args:
            list.append(arg)

        return self.pythonCall(list)


    def pCall(self, *args):
        list = []
        for arg in args:
            list.append(arg)

        return self.pythonPCall(list)


    def method_missing(self, method, *args, **kwargs):
          list = []
          list.append(method)
          for arg in args:
            list.append(arg)
          result = 0
          try:
                result = self.pythonCall(list)
          except RuntimeError,e:
                raise e
                #print e.args[0]

          return result

    @staticmethod
    def initProxy(name, fut):
        try:
            proxy = ALProxy(name)
        except:
            print "Error: cannot get proxy to %s even though we waited for it" % name
            return

        globals()[name] = proxy
        print "Got proxy to " + name

        global _initCb
        if _initCb is not None:
            _initCb(name)

    @staticmethod
    def lazyLoad(session, name):
        session.waitForService(name, _async = True).addCallback(partial(ALProxy.initProxy, name))

    @staticmethod
    def initProxies(initCb = None):
        global _initCb
        _initCb = initCb

        #Warning: The use of these default proxies is deprecated.
        global ALLeds
        ALLeds = None

        session = inaoqi._getDefaultSession()

        ALProxy.lazyLoad(session, "ALFrameManager")
        ALProxy.lazyLoad(session, "ALMemory")
        ALProxy.lazyLoad(session, "ALMotion")
        ALProxy.lazyLoad(session, "ALLeds")
        ALProxy.lazyLoad(session, "ALLogger")
        ALProxy.lazyLoad(session, "ALSensors")


def createModule(name):
    global moduleList
    str = "moduleList.append("+ "module(\"" + name + "\"))"
    exec(str)
