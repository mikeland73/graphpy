# graphpy

### Python graph DB ORM

graphpy is a migration free plug and play ORM for any Python project. It was inspired by the graph db module from [graphp](https://github.com/mikeland86/graphp). It allows you to build quick and dirty db based models using a graph abstraction on top of MySQL.

A simple example:

### Define nodes (your model) with minimum boilerplate

```python
class User(GPNode):
    node_data = {
        'name': '',
        'last_name': '',
    }

# Use the model:
me = User()
me.set_name('Mike')
me.get_name()     # Mike
try:
    me.get_foo()  # throws exception
except: 
    me.get('foo') # this is fine, returns None
me.save()
```

### Edge 
*todo*

### Indexed data
*todo*

*graphpy is a work in progress*

