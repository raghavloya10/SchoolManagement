from django import template

register = template.Library()

def myConcat(value,arg):
    val = str(value)
    a = str(arg)
    return val+" "+a

def func(value,args):
    # you would need to do any localization of the result here
    if args is None:
        return False
    arg_list = args.split(' ')
    a1 = int(arg_list[0])
    a2 = int(arg_list[1])
    return value+a1*a2

def index(indexable, i):
    return indexable[i]

register.filter('index', index)
register.filter('myConcat', myConcat)
register.filter('func', func)
