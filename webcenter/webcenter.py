import requests
import urllib
import lxml.html as lxhl
import time

class WebcenterSession:
    LOGIN_URL = 'https://webcenter.studentservices.tufts.edu/login.aspx'
    GROUP_REPORT_URL = 'https://webcenter.studentservices.tufts.edu/HousingPortal/GroupsReport.aspx'
    EXAM_URL = 'https://webcenter.studentservices.tufts.edu/examlibrary/' # Prepended to pdf files. Automatically redirects to Default.aspx otherwise.


    def __init__(self, username=None, password=None):
        self.session = requests.Session()
        if username and password:
            self.login(username, password)

    def login(self, username, password):
        login_viewstate = self._get_viewstate(self.session.get(self.LOGIN_URL).content)
        # Is the viewstate always: dDwtMTQzNjc3ODQ2ODs7Pulw5t0rsoQM7aqTVouY5dhcF3RB ?
        credentials = {'username': username, 'password': password, 'Button1': 'Login', '__VIEWSTATE': login_viewstate}
        login_resp = self.session.post(self.LOGIN_URL, data=credentials)
        return login_resp.status_code == 200

    #---
    # Housing
    #---
    
    # Returns a list of the possible parameters for get_housing_groups_report.
    def get_housing_locations(self):
        html = self.session.get(self.GROUP_REPORT_URL).content
        doc = lxhl.fromstring(html)
        options_list = doc.cssselect('select[name="LotteryDropDownList"]')[0]
        return [option_tag.text_content() for option_tag in options_list.cssselect('option')]


    # Returns a map of {group_size => [list of HousingGroups]}
    def get_housing_groups_report(self, location_name):
        if location_name not in self.get_housing_locations():
            raise ValueError("Invalid housing location {}".format(location_name))

        groups_viewstate = self._get_viewstate(self.session.get(self.GROUP_REPORT_URL).content)
        groups_params = {'LotteryDropDownList': location_name, 'ShowGroupsButton': 'Show Groups', '__VIEWSTATE': groups_viewstate}
        groups_resp = self.session.post(self.GROUP_REPORT_URL, data=groups_params)
        return self._parse_groups(groups_resp.content)

    #---
    # Exams
    #---

    def get_exam_departments(self, html=None):
        if not html: html = self.session.get(self.EXAM_URL).content
        doc = lxhl.fromstring(html)
        options_list = doc.cssselect('select[name="DropDownList1"]')[0]
        return [option_tag.attrib['value'] for option_tag in options_list.cssselect('option')[1:]] # Skip the "Select department..." option

    def get_exams(self, department_name):
        base_html = self.session.get(self.EXAM_URL).content

        if department_name not in self.get_exam_departments(base_html):
            raise ValueError("Invalid exam department {}".format(department_name))

        exams_viewstate = self._get_viewstate(base_html)
        exams_params = {'DropDownList1': department_name, '__EVENTTARGET':'DropDownList1', '__EVENTARGUMENT': "", '__VIEWSTATE': exams_viewstate}
        exams_resp = self.session.post(self.EXAM_URL, data=exams_params)
        return self._parse_exams(exams_resp.content)


    #---
    # Helpers
    #---

    # VIEWSTATE is stored in a hidden input on the returned page.
    #<input type="hidden" name="__VIEWSTATE" value="we want this" />
    @staticmethod
    def _get_viewstate(html):
        value = ""
        doc = lxhl.fromstring(html)
        state_tag = doc.cssselect('input[name="__VIEWSTATE"]')
        if state_tag: value = state_tag[0].get('value')
        return value

    # Parse a housing group page and return a map of {group_size => [list of HousingGroups]}
    @staticmethod
    def _parse_groups(html):
        group_report = {}
        doc = lxhl.fromstring(html)
        group_tables = doc.cssselect('table[id="GroupGrid"]')
        for group_table in group_tables:
            for row in group_table.cssselect('tr')[1:]: # skip the table header
                new_group = HousingGroup()
                cols = row.cssselect('td')
                new_group.size = int(cols[0].text_content())
                new_group.rank = int(cols[1].text_content())
                new_group.name = cols[2].text_content().strip()
                selection_string = cols[3].text_content().strip()
                if selection_string:
                    new_group.selection_time = time.strptime(selection_string, "%m/%d/%Y %H:%M")

                # Get the list, making it if necessary. 
                group_report.setdefault(new_group.size, []).append(new_group)
        return group_report

    @staticmethod
    def _parse_exams(html):
        exams = []
        doc = lxhl.fromstring(html)
        exam_tables = doc.cssselect('table[id="dgExamList"]')
        for exam_table in exam_tables:
            for row in exam_table.cssselect('tr')[1:]: # skip the table header
                exam = Exam()
                cols = row.cssselect('td')
                exam.url = WebcenterSession.EXAM_URL + cols[0].cssselect('a')[0].attrib['href'].strip()
                exam.class_name = cols[1].text_content().strip()
                exam.instructor = cols[2].text_content().strip()
                exam.year = cols[3].text_content().strip()
                exam.term = cols[4].text_content().strip()
                exam.comments = cols[5].text_content().strip()
                date_string = cols[6].text_content().strip()
                if date_string:
                    exam.date_posted = time.strptime(date_string, "%m/%d/%y")

                exams.append(exam)
        return exams

class HousingGroup:
    def __init__(self):
        self.size = -1
        self.rank = -1
        self.name = ""
        self.selection_time = None

    def __repr__(self):
        return "<HousingGroup #%d %s>" % (self.rank, self.name)

class Exam:
    def __init(self):
        self.class_name = ""
        self.instructor = ""
        self.year = ""
        self.term = ""
        self.comments = ""
        self.date_posted = None
        self.url = ""

    # Exams don't require authentication to access.
    def download(self, path):
        req = requests.get(self.url)
        with open(path, 'wb') as f:
            f.write(req.content)

    def __repr__(self):
        return "<Exam %s %s %s>" % (self.class_name, self.term, self.year)
