#!/usr/bin/env python
# -*- coding: utf-8 -*-

def fill_form_typing(c, data):
    for k,v in data.iteritems():
        c.b.fill(k, '')
        c.b.type(k, v, slowly=False)

def close_flash(c):
    c.b.find_by_css('div.flash').first.click()

def BHrow2dict(row):
    newdict = {}
    for a in row.headings:
        newdict[a] = row[a]
    return newdict

def submit_form(c, selector='form input[type=submit]'):
    c.b.find_by_css(selector).click()

def fast_register(c):
    data = dict(
        first_name='Homer',
        last_name='Simpson',
        password='astrongpassword',
        password_two='astrongpassword',
        email='homer@localhost'
        )

    register_page = c.URL('default', 'user', args='register')
    c.l.info('reached %s', register_page)
    c.b.visit(register_page)
    fill_form_typing(c, data)
    submit_form(c)

def grid_button(c, text='Add'):
    el = c.b.find_by_css('.w2p_trap.button.btn').find_by_css('span.buttontext').first
    assert el.text == text
    return el

def normstr(c):
    return c.strip().lower()
