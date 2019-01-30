#!/usr/bin/python

# makes input arguments for a script:
# usage:
#  make_arg(<flag>,<value?>,<required?>)
#  <flag> = the input flag ie '--i' or '--help'
#  <value?> = does the input require a value?  if so use True or  else use False
#  <required?> = is the flag required? if so use True


import sys
#-----------------------------------------------------------------------------------#
errormsg = ""
class Arg(object):
    _registry = []
    def __init__(self, flag, value, req):
        self._registry.append(self)
        self.flag = flag
        self.value = value
        self.req = req

def make_arg(flag, value, req):
    Argument = Arg(flag, value, req)
    if Argument.req == True:
        if Argument.flag not in sys.argv:
            print(errormsg)
            sys.exit("ERROR: required argument '{0}' is missing".format(Argument.flag))
    if Argument.value == True:
        try:
            test = sys.argv[sys.argv.index(Argument.flag)+1]
        except ValueError:
            if Argument.req == True:
                print(errormsg)
                sys.exit("ERROR: required argument '{0}' is missing".format(Argument.flag))
            elif Argument.req == False:
                return False
        except IndexError:
                print(errormsg)
                sys.exit("ERROR: argument '{0}' requires a value".format(Argument.flag))
        else:
            if Argument.value == True:
                Argument.value = sys.argv[sys.argv.index(Argument.flag)+1]
        
    if Argument.value == False:
        if Argument.flag in sys.argv:
            Argument.value = True
        else:
            Argument.value = False
    return Argument.value
#-----------------------------------------------------------------------------------#

# arg1 = make_arg('--i',True,True)
# arg2 = make_arg('--f',True,False)
# arg3 = make_arg('-n', False,False)
# arg4 = make_arg('--testing',True,False)
# arg5 = make_arg('--blah',False,False)
# print(arg1)
# print(arg2)
# print(arg3)
# print(arg4)
# print(arg5)