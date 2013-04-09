from behave import *
import time
from helpers import *

@given('Homer registers and reaches the smartgrid page')
def impl(c):
    smartgrid_page = c.web2py.URL('default', 'alltables')
    fast_register(c)
    c.b.visit(smartgrid_page)

@when('he clicks on the Add button')
def impl(c):
    btn = grid_button(c, 'Add')
    btn.click()

@then('the form for inserting a person is shown')
def impl(c):
    assert c.b.is_text_present('New Person')

@when(u'he fills it with its "{name}" and submits')
def impl(c, name):
    c.b.fill('person_name', name)
    submit_form(c)

@then("he'll be back at the persons grid")
def impl(c):
    assert 'default/alltables/person?' in c.b.url #the ? to assure it's the main page


@when('he fills it with all the others')
def impl(c):
    for row in c.table:
        btn = grid_button(c, 'Add')
        btn.click()
        c.b.fill('person_name', row['person_name'])
        submit_form(c)


@then('the table will have "{number:d}" rows')
def impl(c, number):
    rows = c.b.find_by_css('.web2py_table table tbody tr')
    assert len(rows) == number


@given('Homer reaching the smartgrid page')
def impl(c):
    smartgrid_page = c.web2py.URL('default', 'alltables')
    c.b.visit(smartgrid_page)

@when('he chooses "{link_name}" in the line corresponding to "{person_name}"')
def impl(c, link_name, person_name):
    trs = c.b.find_by_css('.web2py_table table tbody tr')
    person_row = None
    for tr in trs:
        for td in tr.find_by_css('td'):
            if normstr(td.text) == normstr(person_name):
                person_row = tr
                break
    assert person_row is not None
    buttons = person_row.find_by_css('td a')
    for btn in buttons:
        if normstr(btn.text) == normstr(link_name):
            btn.click()
            return

@then('no dogs are there for "{person_name}" yet')
def impl(c, person_name):
    breadcrumb = 'Persons>%s>Dogs' % person_name
    foundtext = c.b.find_by_css('.web2py_breadcrumbs').text

    assert normstr(breadcrumb) == normstr(foundtext)

    rows = c.b.find_by_css('.web2py_table table tbody tr')
    assert len(rows) == 0

@when('fills it with "{dog_name}"')
def impl(c, dog_name):
    c.b.fill('dog_name', dog_name)

@then('he checks that "{person_name}" is in fact preselected as master')
def impl(c, person_name):
    jid = c.b.find_by_css('select[name=master_id]').first['id']
    selected_text = c.b.evaluate_script("$('#%s option:selected').text();" % jid)
    assert normstr(selected_text) == normstr(person_name)

@when('submits it')
def impl(c):
    submit_form(c)

@then('the table of dogs owned by "{person_name}" will have "{number:d}" row')
def impl(c, person_name, number):
    breadcrumb = 'Persons>%s>Dogs' % person_name
    foundtext = c.b.find_by_css('.web2py_breadcrumbs').text

    assert normstr(breadcrumb) == normstr(foundtext)

    rows = c.b.find_by_css('.web2py_table table tbody tr')
    db = c.web2py.db
    total = db(
        (db.person.person_name ==  person_name) &
        (db.dog.master_id == db.person.id)
        ).count()
    
    assert total == number
    assert len(rows) == number
