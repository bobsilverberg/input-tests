#!/usr/bin/env python
# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Firefox Input.
#
# The Initial Developer of the Original Code is
# Mozilla Corp.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Dave Hunt <dhunt@mozilla.com>
#                 Matt Brandt <mbrandt@mozilla.com>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****
'''
Created on Jan 28, 2011
'''
import input_base_page
import vars

page_load_timeout = vars.ConnectionParameters.page_load_timeout


class SubmitFeedbackPage(input_base_page.InputBasePage):

    _page_title = u'Submit Feedback \u2014 Firefox Input'
    _duplicate_feedback_error_message = u'We already got your feedback! Thanks.'
    
    _errorlist_locator = "css=ul.errorlist>li"

    _feedback_locator = 'id=id_description'
    _remaining_character_count_locator = 'id=count'
    _submit_feedback_locator = 'css=button[type=submit]'

    def __init__(self, selenium):
        self.selenium = selenium

    def set_feedback(self, feedback):
        self.selenium.type_keys(self._feedback_locator, feedback)
        self.selenium.key_up(self._feedback_locator, feedback[-1:])

    @property
    def is_duplicate_feedback_error_messgae_present(self):
        try:
            return self.selenium.get_text(self._errorlist_locator) == self._duplicate_feedback_error_message
        except:
            return False

    @property
    def remaining_character_count(self):
        return self.selenium.get_text(self._remaining_character_count_locator)

    @property
    def is_remaining_character_count_low(self):
        try:
            return self.selenium.get_attribute(self._remaining_character_count_locator + "@class") == "low"
        except:
            return False

    @property
    def is_remaining_character_count_very_low(self):
        try:
            return self.selenium.get_attribute(self._remaining_character_count_locator + "@class") == "verylow"
        except:
            return False

    @property
    def is_submit_feedback_enabled(self):
        return self.selenium.is_editable(self._submit_feedback_locator)

    def submit_feedback(self):
        self.selenium.click(self._submit_feedback_locator)
        self.selenium.wait_for_page_to_load(page_load_timeout)
