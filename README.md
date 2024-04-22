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

+ 🟡 implement profiles
    + 🟢 router
    + 🟢 ops
    + 🟢 client
    + 🟡 unittests

+ 🟡 build out ops
    + 🟢 file uploader - move logic from router to ops
    + 🟢 profiles
    + 🟢 each type of file
    + 🟢 update router to use ops
    + 🔴 ops unittests

+ 🟡 update client to have matching ops api
    + 🟡 update client unittests

+ 🟢 update unittests for users
    + 🟢 unique emails for users
    + 🟢 login procedure

+ 🟢 update file ingest
    + 🟢 create new file ingest methods for files that don't need to be uploaded (already on server)
    + 🟢 uploads should have a temp folder and be moved into long term storage folder after recieving CID
+ 🟢 add API endpoints for image files / releases
+ 🟡 UI models :: users, file uploads, artists, image files, image releases, still images
    + 🟢 make a lorem ipsom generator for each ui model
    + 🟢 index page linking to other pages
    + 🟡 for each ui model build components/pages for list, create (plus file upload), read, delete
        + 🟡 users
        + 🟡 file uploads
        + 🟡 artists
        + 🟡 image files
        + 🟡 image releases
        + 🟡 still images

+ 🟡 update backend
    + 🟢 serve static files
    + 🔴 add backend widget and list item models for each content model that will be used to generate the front end models
    + 🔴 unittests

+ 🟢 UI auth
    + 🟢 login page
    + 🟢 account page
    + 🟢 create account

+ 🟢 add user auth
    + 🟢 web api
    + 🟢 client
    + 🟢 update unittests

+ 🟡 file updates
    + 🟢 delete files
    + 🔴 file delete unittests
    + 🔴 file/upload background process unittests
    + 🔴 download file methods in ops/client
    + 🔴 s3 support

+ 🔴 migrate to yaml config

+ 🔴 update apis (urls, client/ops method calls, etc) to use `cid` by default, but allow database `id` optionally
    + 🔴 for URLs
        + `/url/base/model/<cid>`
        + `/url/base/model/<id>?db_id=true`
    + 🔴 for methods
        + `id:str = None, cid:str = None` --> `id:str, db_id=False`
 
+ 🟡 code templating
    + 🔴 db wrappers
    + 🟡 ops -> wrap calls like delete because they need to be different for users/files/models with just data
    + 🟡 client
    + 🔴 api routes -> uses above ops
    + 🔴 cli -> uses above ops
    + 🔴 model_config example(s) -> use lorem ipsom gen and hardcode correct cid
    + 🔴 generator function
    + 🔴 unittests              -> retain hard coded CIDs for data+files for testing CID type
    + 🔴 move mcore.util.example* funcs to model attributes

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
            
            mart/ops/
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

                    from mart.ops import *

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

+ 🔴 remane StillImageCreator.id to StillImageCreator.cid -> and check for other similar naming problems
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

+ 🔴 profile groups

+ 🔴 add tests for seeder - these will also test that user login and item/creator ownership is working

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

### backlog

+ 🔴 authentication improvments
    + 🔴 ensure only 1 user can be created per email and phonenumber
        + 🔴 create unit test for this and ensure email is case insensitive
    + 🔴 create admin+user auth scopes to lock down endpoints like users and file uploads
        https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/
    + 🔴 add user sessions so that tokens can be expired prematurly by admins or users
    + 🔴 only owner can delete items
    + 🔴 process to delete user, artist, files
    + 🔴 ACLs - allow users to create custom ACLs for items they own
    + 🔴 disable deleting users, artists, file uploads, (image files?)

+ 🔴 create password requirements

+ 🔴 add unique index on user email field and user_id field for password hash

+ 🔴 write tests for upload cleanup process

+ 🔴 versionable CIDs
    + 🔴 add update functions to models, create & modified timestamps, and integrate changes with versionable CID


### links

https://choosealicense.com
