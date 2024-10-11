import inspect

from typing import Callable
from types import UnionType

     
     
def validate_arguments(func: Callable):
     def wrapper(*args, **kwargs):
          annotation = func.__annotations__
          
          # Если return останется, то выкинет ошибку
          if 'return' in annotation:
               del annotation['return']
          
          # Если нет аннотаций, то валидировать нечего
          if not annotation:
               return func(*args, **kwargs)
          
          # Собираю все аргументы из главной функции. В данном случаее у функции f
          dict_func = {}
          func_data = inspect.signature(func)
          for key in func_data.parameters:
               dict_func[key] = {
                    'an': func_data.parameters[key].annotation,
                    'value': func_data.parameters[key].default
               }
          
          # Проверяю все args и переношу их в словарь kwargs чтобы провалидировать в конце
          if args:
               count = 0
               for df in dict_func:
                    if count <= len(args):
                         try:
                              kwargs[df] = args[count]
                              count += 1
                         
                         except IndexError:
                              if dict_func[df]['value'] != inspect._empty:
                                   kwargs[df] = dict_func[df]['value']
                                   continue
                                        
                              if isinstance(dict_func[df]['an'], UnionType):
                                   if type(None) not in dict_func[df]['an'].__args__:
                                        raise TypeError(f"Missed argument {df}")
                                   
                                   else: kwargs[df] = None
                              else: raise TypeError(f"Missed argument {df}")
                              
                              
          # Если не было передано ни args, ни kwargs, значит все аргументы имеют None либи дефолтные значения
          if (not kwargs) and not (args):
               for df in dict_func:
                    if dict_func[df]['value'] == inspect._empty:
                         if isinstance(dict_func[df]['an'], UnionType):
                              if type(None) not in annotation[df].__args__:
                                   raise TypeError(f"Missed argument {df}")
                              kwargs[df] = None
                              
                         else: raise TypeError(f"Missed argument {df}")
                         
                    else:
                         kwargs[df] = dict_func[df]['value']  # Дефолтное значение
                         
                    
          # Валидирию полученные kwargs
          for key in dict_func.keys():
               if key in kwargs.keys():
                    if dict_func[key]['an'] == inspect._empty:
                         continue
                    
                    if not isinstance(kwargs[key], dict_func[key]['an']):
                         raise TypeError(f"Expected {dict_func[key]['an']} but got {type(kwargs[key])} for argument {key}")
                    
               else:
                    if dict_func[key]['value'] != inspect._empty:
                         if not isinstance(dict_func[key]['value'], dict_func[key]['an']):
                              raise TypeError(f"Expected {dict_func[key]['an']} but got {type(dict_func[key]['value'])} for argument {key}")
                         
                    else: raise TypeError(f"Missed argument {key}")
                    
                    
                    if isinstance(dict_func[key]['an'], UnionType):
                         if type(None) not in dict_func[key]['an'].__args__:
                              raise TypeError(f"Missed argument {df}")
                                   
                         else: kwargs[key] = None  # В аннтации есть None
          return func(**kwargs)
     return wrapper
          
          
'''
     Небольшие объяснения:
     
     Передача args(строка 29):
          Начинаю идти по словарю dict_func и параллельно 
          добавляю к переменной count 1. 
          
          строка 32 - проверка чтобы не уйти за границы кортежа args
          Дальше присваиваю значения ключам kwargs по правилу 0 - 0, 1 - 1 (Первому ключу - элемент 0 и тд.)
          Если ловится ошибка IndexError, то значит, что переданных args меньше, чем аргументов в основной функции
          
          строка 39 - если аргументу было присвоено дефолтное значение, то ключ kwargs это значение тоже получает
          continue для того чтобы не нарваться на ошибку Missed argument.
          
          строка 42 - проверяет на UnionType(Это например int | str) и если в этом юнионе присутствует None(Например: int | None),
          то ключ kwargs получает знаение None(строка 46). Если аннотация не UnionType или None не присутсвует в этом юнионе, то ошибка.
          
     Если нет ни кваргов, ни аргов(строка 51):
          Происходит проверка имеет ли аргумент дефолтное значение или аннотацию с None
          
     Передача kwargs:
          По сути у меня всё работает так, что kwargs формируются сразу же, даже если были переданы args
          и это всё идёт уже в валидацию.
          
     Валидация(строка 63):
          Итерацию начинается по словарю  dict_func и дальше идёт проверка есть ли переданные аргументы в функции в kwargs.
          Если они все же есть, то начинается валидация.
          
          строка 65 - если в аргументе не аннтации, то валидация на него не действуется и поэтому continue
          строка 68 - если аннотация значения ключа из kwargs, не соответствует аннотации в функции, то ошибка.
          
          А если всё же ключа из dict_func нет в kwargs, то идёт проверка если ли в аннтации None или дефлтный аргумент,
          который также валидируется.
'''
     


          
               
          

     
     

