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

+ 🟡 UI models :: users, file uploads, artists and still images
    + 🟡 make a lorem ipsom generator for each ui model
    + 🔴 for each ui model build components: 
        + 🔴 list
        + 🔴 create
        + 🔴 read
        + 🔴 delete

+ 🔴 add mock user auth
    + 🔴 backend session model

 
+ 🔴 code templating
    + 🔴 api routes
    + 🔴 db wrappers
    + 🔴 model_conig example(s) -> use lorem ipsom gen and hardcode correct cid
    + 🔴 generator function
    + 🔴 unittests

    + 🔴 new module structure:

        ** handwritten **

            mart/still_image/types.py
            mart/still_image/models.py
                StillImage
                StillImage.__doc__
                StillImageCreator
                generator()
                creator_generator()

        ** generated **
            
            mart/sdk/
                still_image_types.py            ** copied from original
                still_image_model.py            ** copied from original
                still_image_template.py         ** generated template code

                    example()

                    db_list()
                    db_create()
                    db_get()
                    db_delete()

                    api_list()
                    api_create()
                    api_get()
                    api_delete()

                    router

                still_image.py                  ** a generated module that creates aliases enabling the following imports to work

                    from mart.sdk import *

                    still_image
                    still_image.model
                    still_image.example
                    still_image.generate()

                    still_image.creator_model
                    still_image.creator_model()
                    still_image.creator_example
                    still_image.creator_generate()

                    still_image.db_list()
                    still_image.db_create()
                    still_image.db_get()

                    still_image.api_list()
                    still_image.api_create()
                    still_image.api_get()

                    still_image.router
            
            tests/mart/still_image/

                test_model.py
                test_creator.py
                test_example.py
                test_generator.py
                test_db.py
                test_api.py

                creator/
                    test_model.py
                    test_creator.py
                    test_example.py
                    test_generator.py

+ 🔴 refactor mart.TitleData model


        from:
            TitleData.title
            TitleData.short_title
            TitleData.abreviated_title
            ...
        to:
            TitleData.full
            TitleData.short
            TitleData.abreviated
            ...
    
        this way you wont have duplicate attributes when accessing via parent model

        StillImage.title.title
        StillImage.title.full
        StillImage.title.abreviated

        instead of

        StillImage.title.title
        StillImage.title.short_title
        StillImage.title.abreviated_title

        this should be done after code templating and generation so that new models, examples and unittests will be auto generated instead of manually updating CIDs


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
