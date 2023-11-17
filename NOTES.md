# TO DO
+ integrate uploads with mart
+ unittests for each mart model
+ add mock user auth
+ add user_id to models as required attr
+ add actual auth

+ UI
+ test upload cleanup process
+ text editing
    + find text editing libray
    + update backend TextFile model for text editor serialilization format
    + implement front end editor for text file editing
    + incorporate TextFile with mart models

+ add update functions to models, create & modified timestamps, and integrate changes with versionable CID
+ add ACLs for CRUD operations

+ create a profile and profile group class and make artists a subclass of this, the base profile classes will be social profiles (non-artists)
    + these classes should go in a new module called 'msocial'

### links

https://choosealicense.com

https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#custom-discovery