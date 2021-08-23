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
