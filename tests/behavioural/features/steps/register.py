from behave import *
import time
from helpers import *


@given(u'Homer accesses the app')
def impl(c):
    pass

@when('Homer reaches the registration page')
def impl(c):
    #dismiss the flash
    close_flash(c)
    c.b.click_link_by_partial_text('Login')
    time.sleep(1)
    c.b.click_link_by_partial_href('/register?_next=/welcome_augmented/default/index')
    assert 'default/user/register' in c.b.url

@then('he fills the form with an incorrect email')
def impl(c):
    data = BHrow2dict(c.table[0])
    fill_form_typing(c, data)
    submit_form(c)

@then('an error will be returned')
def impl(c):
    assert c.b.is_element_present_by_css('#email__error')

@when('he re-fills the form with the correct email')
def impl(c):
    data = BHrow2dict(c.table[0])
    fill_form_typing(c, data)

@then('he will check that the password is reported as strong enough')
def impl(c):
    green = "background-color: rgb(0, 255, 0);"
    assert green == c.b.find_by_css('#auth_user_password').first['style']

@then('he will submit it')
def impl(c):
    submit_form(c)

@then('he will be registered and taken to the index page')
def impl(c):
    assert '/welcome_augmented/default/index' in c.b.url
    assert c.b.is_text_present('Welcome Homer')
