# TODO

🔴 = not started

🟡 = started

🟢 = finished

1. 🟢 build out client/server unittest test template
1. 🟢 create new environment for generated app, verify it passes unittests
1. 🟡 rewrite templates to be extracted from actual code
    * 🟢 GENERATE new minimal test project called 'sample_app'
    * 🟢 integrate into mstack module, app+docker+tests should work w/o generating code
    * 🟢 restructure folders, verify tests works
        * 🟢 restructure folders
        * 🟢 rework `./medium-stack/` docker files and scripts to be for the builder
            * is used to test app which is used for template extraction
            * is different than the dockerfile in mapplication/mtemplate/app
        * 🟢 create `sample_app` specific unittests
    * 🟡 template extraction
        * 🟢 add extractor to mtemplate package
        * 🟡 update generator to use extracted templates
        * 🔴 generated app + unittests are passing
    * 🔴 refactor unittests?


# RESTRUCTURE

```
medium-stack
    mbuilder
        examples
            sample_app_1
                mtemplate.conf
                dist
                src
                    __init__.py
                    models.py
        py
            mapplication
                pyproject.toml
                tests
                    ...
                src
                    mcore
                    mserve
                    mtemplate
                        __init__.py
                        __main__.py
                        app
                            README.md
                            .env
                            .dockerignore
                            .gitignore
                            docker-compose.yml
                            Dockerfile
                            py
                                web.sh
                                pyproject.toml
                                entry.py
                                tests/
                                    ...
                                src/
                                    ...
                            js
                                ...

        js
            ...

    mstack
        mstack      * template projects
            mart
            msocial
            minfo
            ...

```