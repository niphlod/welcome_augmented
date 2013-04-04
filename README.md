welcome_augmented
=================

What needs to happen in an app (augmented reality)
This is a stub that starts to explore real live testing of a web2py app.
Tests are written with [behave](http://pythonhosted.org/behave/) and leverage [splinter](http://splinter.cobrateam.info/)
to explore the app.
Main goal of this is being able to support BDD and test all the "moving parts" of a webapp, Javascript included.

Instructions:
- install latest web2py
- pip install behave and splinter
- have firefox (for starters) installed
- copy this app to the applications/* folder
- cd into the applications/welcome_augmented/tests directory
- start the test with ```behave features/smartgrid.feature``` or ```behave features/register.feature```

NB1: if you launch ```behave``` with no parameters, it'll try to run one after another, and the latter would fail cause "Homer" is registered yet 
(both features are ATM meant to be run separately, cause I meant register.feature to be a closed reproducible test of the current gluon/tests/test_web.py)

Notes: I made some helpers available in helpers.py and some initialization in environment.py, namely:
in any step you can access:
- c.host --> 127.0.0.1:8000
- c.URL --> you can use c.URL instead of the "usual" URL to build urls against the app
- c.appname --> welcome_augmented
- c.l --> logger
- c.b --> splinter's Browser() instance

all helpers (imported in every steps/*.py file) take the context as the first parameter
- fill_form_typing --> emulates keypresses
- close_flash --> clicks on the default flash message
- submit_form --> submits the main form on the current page
- fast_register --> speedier register routine for the user
- grid_button --> selects the proper grid button
- normstr --> useful for comparison
- BHrow2dict --> turns a behave.Table.row into a dict

environment.py takes care of starting the default webserver and, if it finds a fixture.csv file it loads it into the database before
launching the actual tests (see before_all() in environment.py)

NB2: every test run WIPES OUT the databases folder (so, for sqlite uris, the data too)
NB2: python files inside steps can be named independantly from the *.feature files
NB3: as long as you have the same line in a *.feature file, only one corresponding decorated step (def impl(c)) needs to be defined, 
e.g. line 4 and 20 from the smartgrid.feature file call both line 12 of step1.py
NB4: additional helpers and shortcuts can be added, this is only a first mockup

TODO:
- [ ] smooth integration with web2py
- [ ] smooth integration with travis-ci
