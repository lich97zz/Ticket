import unittest
import sys
sys.path.append('../')
import ticketViewer
import contextlib
from io import StringIO 
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout
        
def time_to_arr(time_str):
        date = time_str.split('T')[0]
        time = time_str.split('T')[1][:-1]
        year,month,day = date.split('-')
        hour,minute,second = time.split(':')
        year = int(year)
        month = int(month)
        day = int(day)
        hour = int(hour)
        minute = int(minute)
        second = int(second)
        return [year,month,day,hour,minute,second]

class TestViewer(unittest.TestCase):

    def test_invalid_configure(self):
        #should detect invalid configuration file
        file_name = "test_configure1"
        with contextlib.redirect_stdout(None):
            subdomain = ticketViewer.read_configure(file_name)[0]
        self.assertEqual(subdomain,"")

    def test_invalid_json(self):
        #should detect empty, and invalid json
        throw_err = False
        content = "{}"
        try:
            q = ticketViewer.Query(content)
        except ValueError:
            throw_err = True
        self.assertEqual(throw_err, True)

        throw_err = False
        content = "{invalid json"
        try:
            q = ticketViewer.Query(content)
        except ValueError:
            throw_err = True
        self.assertEqual(throw_err, True)

    def test_catch_error_in_query(self):
        #should detect error when parsing json
        throw_err = False
        content = "{'error':an error}"
        try:
            q = ticketViewer.Query(content)
        except Exception:
            throw_err = True
        self.assertEqual(throw_err, True)

    def test_parse_json(self):
        #test with given json in test_content.txt, should read 100 tickets
        content = ""
        with open("test_content.txt") as f:
            content = f.readlines()[0]
        q = ticketViewer.Query(content)
        ticket_num = len(q.ticket_arr)
        self.assertEqual(ticket_num, 100)

        #is sorted according to correct time order
        for i in range(len(q.ticket_arr)-2):
            time1 = q.ticket_arr[i].contents['updated_at']
            time2 = q.ticket_arr[i+1].contents['updated_at']
            time1 = time_to_arr(time1)
            time2 = time_to_arr(time2)
            boolean = time1>=time2
            self.assertTrue(ticket_num, boolean)
        
        #should have read correct dict keys
        attrs = ['url', 'id', 'status', 'priority', 'type', 'subject', 'description', 'organization_id', 'via', 'custom_fields', 'requester_id', 'collaborator_ids', 'email_cc_ids', 'is_public', 'due_at', 'can_be_solved_by_me', 'created_at', 'updated_at', 'recipient', 'followup_source_id', 'assignee_id', 'ticket_form_id', 'fields']
        ticket = q.ticket_arr[0]
        self.assertEqual(list(ticket.contents.keys()), attrs)

        #should have correct display info
        out = ['View  1 to 2  out of 100 tickets', '+-----+---------------------+-----------------------------------+---------------+', '|  id |      Updated at     |              subject              |   requester   |', '+-----+---------------------+-----------------------------------+---------------+', '| 101 | 2021-11-24 02:30:55 | in nostrud occaecat consectetu... | 1524137416421 |', '|  99 | 2021-11-24 02:30:54 | elit sit laborum commodo labor... | 1524137416421 |', '+-----+---------------------+-----------------------------------+---------------+']
        with Capturing() as output:
            q.display_ticket_simple(0,2)
        self.assertEqual(out, output)    


if __name__ == '__main__':
    unittest.main()
