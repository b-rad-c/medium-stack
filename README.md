# Medium stack

## setup dev environment

    python3 -m venv .venv --upgrade-deps
    source .venv/bin/activate
    pip install -e mstack

# Roadmap
🔴 = not started

🟡 = started

🟢 = finished

---

+ 🔴 UI
    + 🔴 do the following for users, file uploads, artists and still images
        + 🔴 list
        + 🔴 read
        + 🔴 delete

+ 🔴 🔴 add mock user auth
    + 🔴 🔴 backend session model

+ 🔴 🔴 make a lorem ipsom generator for each ui models 
+ 🔴 🔴 code templating
    + 🔴 api routes
    + 🔴 db wrappers
    + 🔴 model_conig example(s) -> use lorem ipsom gen and hardcode correct cid
    + 🔴 generator function
    + 🔴 unittests

+ 🔴 refactor
    + 🔴 make mart imports more granular

            mart.still_image.types

            mart.still_image.model                  ** handwritten
            mart.still_image.model.__doc__          ** handwritten
            mart.still_image.model()
            mart.still_image.example
            mart.still_image.generate()             ** handwritten

            mart.still_image.creator.model          ** handwritten
            mart.still_image.creator.model()
            mart.still_image.creator.example
            mart.still_image.creator.generate()     ** handwritten

            mart.still_image.db.list()
            mart.still_image.db.create()
            mart.still_image.db.get()

            mart.still_image.api.list()
            mart.still_image.api.create()
            mart.still_image.api.get()

            mart.still_image.router
            
            
            


+ 🔴 text editing
    + 🔴 find text editing libray
    + 🔴 update backend TextFile model for text editor serialilization format
    + 🔴 implement front end editor for text file editing
    + 🔴 incorporate TextFile with mart models

+ 🔴 msocial - new module for social media ops
    + 🔴 create a profile and profile group class, the base profile classes will be social profiles
        + 🔴 make Atrist ArtistGroup subclassess of profile?
    + 🔴 models such as post, page, primatives for img/aud/vid with typical social media metadata, and widgets referencing other items/queries
        + 🔴 widget syntax for refrencencing other items
            + 🔴 art.artists.list()
            + 🔴 art.artists.id = '...'
            + 🔴 update code templating to create a dict lookup mapping commands to functions
    + 🔴 models that organize content
        + 🔴 feeds - chronological ordering of the above models (potentially limited to certain types)
        + 🔴 forum
            + 🔴 branch - wrapper around feed model 
            + 🔴 formum - container for branch, has metadata plus hierarchical tagging
    conversation threads (integrate with heirarcy/tag model for forkable conversations)

+ 🔴 minfo
    + 🔴 hierarchical sorting of 'fact' models
    + 🔴 'context' models can be added by anyone

+ 🔴 mopinon
    ...

+ 🔴 mtheory
    ...

+ 🔴 mjournalism
    ...

###

+ 🔴 auth
    + 🔴 add actual auth
    + 🔴 add ACLs for CRUD operations

+ 🔴 backlog
    + 🔴 write tests for upload cleanup process

+ 🔴 R&D
    + 🔴 versionable CIDs
    + 🔴 add update functions to models, create & modified timestamps, and integrate changes with versionable CID


### links

https://choosealicense.com
