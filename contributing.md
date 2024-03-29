# Steps for creating good issues or pull requests

# Links to external documentation, mailing lists, or a code of conduct

# Community and behavioral expectations

# General comments on coding style

|style |for |comment |
|------|----|--------|
|`CamelCase` | class names and exception names | Class is the brueprint for an *instance*: instance is the *constructed object of the class* (aka object). |
|`all_lower_case` | methods and functions | method is a "callable attribute" defined in the class. |
|`all_lower_case` | variables; global and locals | they are another (aside from method) form of *attribute*, i.e. the object *value* (<object.attribute>). |
|`ALL_CAPS`       | constants | - |
|`all_lower_case` | module | name of the module is in most cases name of the `.py` file |

Some additional comments on naming attributes.

|style |for |comment |
|------|----|--------|
|`all_lower_case` | **Public** attributes/variables | - |
|`_single_leading_underscore` | **Private** attributes/variables | for internal use |
|`__double_leading_underscore` | **Private** attributes/variables | meant to be subclassed |
|`__double__underscores__` | **Magic** attributes/variables | *use* DON'T CREATE |

The guiding principle is **The Zen of Python**
```
>>> import this
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```
