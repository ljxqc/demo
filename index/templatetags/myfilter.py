from django import template

# 声明模板对象，也称注册过滤器
register = template.Library()
# 声明并定义过滤器
@register.filter
def myrepalce(value, args):
    oldvalue = args.split(':')[0]
    newvalue = args.split(':')[1]
    return value.replace(oldvalue, newvalue)
