#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert
import pytest

from pages.desktop.feedback import FeedbackPage


class TestPagination:
    SEARCH_TERM = u'firefox'

    @pytest.mark.nondestructive
    def test_search_pagination(self, mozwebqa):
        """Litmus 13636 - Input: Verify Search results have pagination."""
        feedback_pg = FeedbackPage(mozwebqa)
        feedback_pg.go_to_feedback_page()
        # Set the date range to 2013-01-01 -> today so that we're more
        # likely to have so many messages in the results that it
        # paginates. Otherwise it might not paginate on stage or local
        # environments.
        feedback_pg.set_date_range('2013-01-01')
        feedback_pg.search_for(self.SEARCH_TERM)

        # Check the total message count. If it's less than 50 (two
        # pages worth), then we will fail with a helpful message.
        Assert.greater(feedback_pg.total_message_count, 50, "Search term didn't kick up enough messages. Please prime the server with more data!")

        Assert.true(feedback_pg.is_older_messages_link_visible)
        Assert.true(feedback_pg.is_newer_messages_link_not_visible)
        Assert.equal(feedback_pg.older_messages_link, 'Older Messages')

        feedback_pg.click_older_messages()
        Assert.equal(feedback_pg.search_term_from_url, self.SEARCH_TERM)

        Assert.true(feedback_pg.is_older_messages_link_visible)
        Assert.true(feedback_pg.is_newer_messages_link_visible)
        Assert.equal(feedback_pg.older_messages_link, 'Older Messages')
        Assert.equal(feedback_pg.newer_messages_link, 'Newer Messages')
        Assert.equal(feedback_pg.page_from_url, 2)

        feedback_pg.click_newer_messages()
        Assert.equal(feedback_pg.search_term_from_url, self.SEARCH_TERM)

        Assert.true(feedback_pg.is_older_messages_link_visible)
        Assert.true(feedback_pg.is_newer_messages_link_not_visible)
        Assert.equal(feedback_pg.older_messages_link, 'Older Messages')
        Assert.equal(feedback_pg.page_from_url, 1)
