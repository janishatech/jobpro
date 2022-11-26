import frappe
import json
from frappe.utils.csvutils import read_csv_content
from six.moves import range
from six import string_types
import frappe
import json
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime,datetime,get_first_day,get_last_day,today)
from datetime import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate
from datetime import date


def bulk_update_from_csv(filename):
    #below is the method to get file from Frappe File manager
    from frappe.utils.file_manager import get_file
    #Method to fetch file using get_doc and stored as _file
    _file = frappe.get_doc("File", {"file_name": filename})
    #Path in the system
    filepath = get_file(filename)
    #CSV Content stored as pps

    pps = read_csv_content(filepath[1])
    count = 0
    for pp in pps:
        ld = frappe.db.exists("Lead",{'name':pp[0]})
        if ld:
            # items = frappe.get_all("Lead",{'name':pp[0]})
            # for item in items:
            i = frappe.get_doc('Lead',pp[0])
            if not i.contac%t_by:
                i.contact_date = pp[1]
                print(pp[1])
                # i.append("supplier_items",{
                #     'supplier' : pp[1]
                # })
                # i.save(ignore_permissions=True)
                # frappe.db.commit()


def update_timesheet():
    t_list = frappe.get_all("Timesheet",{"status":"Submitted"})
    for t in t_list:
        print(t)
        doc = frappe.get_doc("Timesheet",t.name)
        for d in doc.time_logs:
            if d.task:
                status = frappe.db.get_value("Task",d.task,"status")
                ewh = frappe.db.get_value("Task",d.task,"expected_time")
                print(status)
                print(ewh)
                doc.update({
                    "task_status":status,
                    "task_ewh":ewh
                })
                doc.save(ignore_permissions=True)
                frappe.db.commit()
                


@frappe.whitelist()
def update_candidate_list(candidate,project,customer,task):
    frappe.errprint(candidate)
    can = json.loads(candidate)
    for c in can:
        frappe.errprint(c)
        cand = frappe.get_doc("Candidate",(c["candidate_id"]))
        frappe.errprint(cand)
        cand.update({
            "pending_for": c["candidate_status"],
            "degree" : c.get("degree"),
            "specialization" : c.get("specialization"),
            "current_ctc" :c.get("current_ctc"),
            "current_ctc" :c.get("current_ctc"),
            "indian_experience" : c.get("indian_experience"),
            "gulf_experience" : c.get("gulf_experience"),
            "currency_type" : c.get("currency_type"),
            "expected_ctc" : c.get("expected_ctc"),
            "passport_no" : c.get("passport_no"),
            "expiry_date" : c.get("expiry_date"),
            "ecr_status" : c.get("ecr_status"),
            "current_location" : c.get("current_location"),
            "mobile" : c.get("mobile"),
            "associate_name" : c.get("associate"),
            "user" : c.get("user"),
        })
        # child = frappe.get_all('Candidate Task',{'parent':c["candidate_id"]},['customer','project','task','pending_for','territory'])
        # for ch in child:
        #     if ch.customer == customer and ch.project == project:
        #         ch.update({
        #             "pending_for":c["candidate_status"],
        #             })
        #         ch.db_update()
        cand.db_update()
        frappe.db.commit()

@frappe.whitelist()
def update_candidates(candidate):
    frappe.errprint(candidate)
    can = json.loads(candidate)
    for c in can:
        frappe.errprint(c)
        cand = frappe.get_doc("Candidate",(c["candidate_id"]))
        frappe.errprint(cand)
        cand.update({
            "pending_for": c["candidate_status"],
            "current_location" : c.get("current_location"),
            "address_line_1" : c.get("address_line_1"),
            "mobile" : c.get("mobile"),
            "sa_agent_name" : c.get("sa_name"),
            "user" : c.get("user"),
        })
        cand.db_update()
        frappe.db.commit()

@frappe.whitelist()
def load_candidates(task):
    candidates = frappe.get_all("Candidate", "*", {"task": task}, order_by="given_name asc")
    # candidates = frappe.db.sql("""select `tabCandidate`.name as candidate_id,`tabCandidate`.pending_for as candidate_status,`tabCandidate`.given_name as given_name,
    # `tabCandidate`.mobile as mobile,`tabCandidate`.sa_name as sa_name,`tabCandidate`.candidate_created_by as candidate_created_by,`tabCandidate Task`.task
    # FROM `tabCandidate`
    # LEFT JOIN `tabCandidate Task` ON `tabCandidate`.name = `tabCandidate Task`.parent
    # WHERE `tabCandidate Task`.task = '%s' """%(task),as_dict=True)
    return candidates

def update_task():
    candidate=frappe.get_all("Candidate")
    for cand in candidate:
        doc = frappe.get_doc("Candidate",cand.name)
        if doc.candidate_task:
            for d in doc.candidate_task:
                print(doc.name)
                if d.customer:
                    frappe.db.set_value('Candidate',doc.name,'customer',d.customer)
                if d.project:
                    frappe.db.set_value('Candidate',doc.name,'project',d.project)
                if d.task:
                    frappe.db.set_value('Candidate',doc.name,'task',d.task)
                if d.pending_for:
                    frappe.db.set_value('Candidate',doc.name,'pending_for',d.pending_for)
                if d.interview_date:
                    frappe.db.set_value('Candidate',doc.name,'interview_date',d.interview_date)
                if d.offer_letter:
                    frappe.db.set_value('Candidate',doc.name,'offer_letter',d.offer_letter)
                if d.territory:
                    frappe.db.set_value('Candidate',doc.name,'territory',d.territory)
                if d.basic:
                    frappe.db.set_value('Candidate',doc.name,'basic',d.basic)
                if d.food:
                    frappe.db.set_value('Candidate',doc.name,'food',d.food)
                if d.other_allowance:
                    frappe.db.set_value('Candidate',doc.name,'other_allowances',d.other_allowance)
                if d.interview_location:
                    frappe.db.set_value('Candidate',doc.name,'interview_location',d.interview_location)
                if d.expected_doj:
                    frappe.db.set_value('Candidate',doc.name,'expected_doj',d.expected_doj)
                if d.subject:
                    frappe.db.set_value('Candidate',doc.name,'position',d.subject)

@frappe.whitelist()
def sa_candidate(task,project):
    allocated = frappe.db.sql("""
        SELECT sa_agent,sa_agent_name,sa_mobile_number,count(sa_agent) as achieved_count,
        (SELECT COUNT(pending_for) as count1 FROM `tabCandidate` cc WHERE cc.task= '%s' and cc.pending_for = 'IDB' AND 
        cc.sa_agent = sa.name) as selected,
        (SELECT COUNT(pending_for) as count2 FROM `tabCandidate` cfp WHERE cfp.task= '%s' AND cfp.pending_for IN ('Submitted','Interviewed') AND
        cfp.sa_agent = sa.name) as fp,
        (SELECT COUNT(pending_for) as count3 FROM `tabCandidate` csl WHERE csl.task= '%s' AND csl.pending_for IN ('Linedup','Shortlisted') AND
        csl.sa_agent = sa.name) as sl,
        (SELECT COUNT(pending_for) as count4 FROM `tabCandidate` cpsl WHERE cpsl.task= '%s' AND  cpsl.pending_for ='Proposed PSL' AND 
        cpsl.sa_agent = sa.name) as psl,
        (SELECT COUNT(pending_for) as count5 FROM `tabCandidate` csp WHERE csp.task= '%s' AND csp.pending_for ='Sourced' AND 
        csp.sa_agent = sa.name) as sp,
        (SELECT COUNT(pending_for) as count6 FROM `tabCandidate` tsa WHERE tsa.task= '%s' AND tsa.pending_for IN ('Submitted','Interviewed','Linedup','Shortlisted','IDB','Proposed PSL','Sourced') AND 
        tsa.sa_agent = sa.name) as tsa
        FROM `tabCandidate` c 
        JOIN `tabSAMS` sa ON  sa.name = c.sa_agent 
        WHERE c.task='%s' AND c.sa_agent IS NOT NULL AND c.task IS NOT NULL GROUP BY sa.name
        """ %(task,task,task,task,task,task,task),as_dict=1)
    # frappe.errprint(allocated)
    return(allocated)    


@frappe.whitelist()
def project_sa_candidate(project):
    allocated = frappe.db.sql("""
        SELECT sa_agent,sa_agent_name,sa_mobile_number,count(sa_agent) as achieved_count,
        (SELECT COUNT(pending_for) as count1 FROM `tabCandidate` cc WHERE cc.project= '%s' AND cc.pending_for = 'IDB' AND 
        cc.sa_agent = sa.name) as selected,
        (SELECT COUNT(pending_for) as count2 FROM `tabCandidate` cfp WHERE cfp.project= '%s' AND cfp.pending_for IN ('Submitted','Interviewed') AND
        cfp.sa_agent = sa.name) as fp,
        (SELECT COUNT(pending_for) as count3 FROM `tabCandidate` csl WHERE csl.project= '%s' AND csl.pending_for IN ('Linedup','Shortlisted') AND
        csl.sa_agent = sa.name) as sl,
        (SELECT COUNT(pending_for) as count4 FROM `tabCandidate` cpsl WHERE cpsl.project= '%s' AND  cpsl.pending_for ='Proposed PSL' AND 
        cpsl.sa_agent = sa.name) as psl,
        (SELECT COUNT(pending_for) as count5 FROM `tabCandidate` csp WHERE csp.project= '%s' AND csp.pending_for ='Sourced' AND 
        csp.sa_agent = sa.name) as sp,
        (SELECT COUNT(pending_for) as count6 FROM `tabCandidate` tsa WHERE tsa.project= '%s' AND tsa.pending_for IN ('Submitted','Interviewed','Linedup','Shortlisted','IDB','Proposed PSL','Sourced') AND 
        tsa.sa_agent = sa.name) as tsa
        FROM `tabCandidate` c 
        JOIN `tabSAMS` sa ON  sa.name = c.sa_agent 
        WHERE c.project='%s'AND c.sa_agent IS NOT NULL AND c.project IS NOT NULL GROUP BY sa.name
        """ %(project,project,project,project,project,project,project),as_dict=1)
    return(allocated)

@frappe.whitelist()
def count_task(project):
    task = frappe.db.count('Task',{'project':project})
    count = frappe.db.sql("select sum(vac),sum(sp),sum(fp),sum(sl),sum(psl) from `tabTask` where `project` = %s and status in('Open','Working','Pending Review','Overdue')" ,project)
    return task, count

# def bulk_update_from_csv(filename):
#     #below is the method to get file from Frappe File manager
#     from frappe.utils.file_manager import get_file
#     #Method to fetch file using get_doc and stored as _file
#     _file = frappe.get_doc("File", {"file_name": filename})
#     #Path in the system
#     filepath = get_file(filename)
#     #CSV Content stored as pps

#     pps = read_csv_content(filepath[1])
#     count = 0
#     for pp in pps:
#         ld = frappe.db.exists("Lead",{'name':pp[0]})
#         if ld:
            # items = frappe.get_all("Lead",{'name':pp[0]})
            # for item in items:
            # i = frappe.get_doc('Lead',pp[0])
            # if not i.temp_mobile_no:
            #     frappe.db.set_value("Lead",pp[0],"temp_mobile_no",pp[1])
            #     print(pp[0])
                # frappe.db.commit()

@frappe.whitelist()
def leave_allocation():
    employee = frappe.get_all("Employee" ,{"status":"Active","employment_type":"Full-time"}, ['name','date_of_joining'])
    for emp in employee:
        now_date = frappe.utils.datetime.datetime.now().date()
        age = now_date.year - emp.date_of_joining.year - ((now_date.month, now_date.day) < (emp.date_of_joining.month, emp.date_of_joining.day))
        if age:
            start_date = date(now_date.year, 1, 1)
            end_date = date(now_date.year, 12, 31)
            months = now_date.month
            leave_allocation = frappe.get_all("Leave Allocation",{"employee":emp.name,"from_date":start_date,"to_date":end_date},["name"])
            if not leave_allocation:
                leave_balance = 13 - int(months)
                allocation = frappe.new_doc("Leave Allocation")
                allocation.update({
                    "employee":emp.name,
                    "leave_type":"Casual Leave",
                    "from_date":now_date,
                    "to_date":end_date,
                    "new_leaves_allocated":leave_balance
                }).save(ignore_permissions=True)
                allocation.submit()
                frappe.db.commit()

@frappe.whitelist()
def auto_mail_to_sams(project,territory):
    task =frappe.get_all("Task",filters = {"project":project}, fields = ["*"])
    for t in task:
        sams =frappe.db.sql("""select email_address,person_name from`tabSAMS` where NOT sa_status= "Do Not Contact" """,as_dict=True)
        for s in sams:
            frappe.errprint(s.person_name)
            vacancy =t.vac * t.prop
            frappe.sendmail(
                recipients=["sarumathy.d@groupteampro.com"],
                subject='Regarding Vacancy' ,
                message="""<p>Dear %s,</p>
                <p>Greetings From TEAMPRO !!! <br>
                    We are always happy to be associated with you, and appreciate your sincere efforts to be support us in recruitment.
                    We have a manpower requirement������������������������������������������������������for once of our reputed client in %s������������������������������������������������������; The details for project is as below:
                    <table class='table table-bordered'>
                    <tr>
                    <th>Position</th>  <th>Vacancy</th>  <th> Valid till</th>
                    </tr>
                    <tr>
                     <td> %s </td> <td> %s </td> <td> %s </td>
                    </tr>
                     </table>
                     <br>
                     <table class='table table-bordered'>
                     <tr>
                    <th> Job Requirement</th> 
                    </tr>
                    <tr>
                    <th> Qualification Type </th>   <th> Temp Qualification </th> <th>Minimum Experience</th>  <th>Total Experience</th>
                    </tr>
                    <tr>
                    <td> %s </td>   <td> %s </td> <td> %s </td> <td> %s </td>
                    </tr>
                    <tr>
                    <th> Salary Type </th>  <th>Specialization</th> <th> Maximum Experience </th> <th>Currency</th>
                    </tr>
                    <tr>
                    <td> %s </td>  <td>%s</td> <td> %s </td> <td> %s </td>
                    </tr>
                    <tr>
                    <th> Category </th>  <th>Gulf Experience</th> <th> Amount </th> <th>Driving Licence (If any)</th>
                    </tr>
                    <tr>
                    <td> %s </td>  <td>%s</td> <td> %s </td> <td> %s </td>
                    </tr>
                     </table>
                     <br>
                     <table class='table table-bordered'>
                     <tr>
                    <th>Job Description </th> 
                    </tr>
                    <tr>
                    <td> %s </td>
                    </tr>
                     </table>
                     <br>
                     <table class='table table-bordered'>
                    <tr>
                    <th>Allowance and Benefits  </th> 
                    </tr>
                    <tr>
                    <th> Working Days/HRS </th>  <th> Food </th> <th>Visa Type </th> <th>Transportation </th> 
                    </tr>
                    <tr>
                    <td> %s </td>  <td>%s</td> <td> %s </td> <td> %s </td>
                    </tr>
                     <tr>
                    <th> Accommodation </th>  <th> Nationality </th> <th>  Contract Period Year</th> <th> Contract Period  Month</th>
                    </tr>
                    <tr>
                    <td> %s </td>  <td>%s</td> <td> %s </td> <td> %s </td>
                    </tr>
                    <tr>
                    <th>  Over Time </th>  <th> Joining Ticket </th> <th> Leave </th> <th> Any Other Allowance</th>
                    </tr>
                    <tr>
                    <td> %s </td>  <td>%s</td> <td> %s </td> <td> %s </td>
                    </tr>
                    </table>
                    <br>
                    Please contact us at������������������������������������������������������+91 73050 56202������������������������������������������������������/������������������������������������������������������+91 73050 56203������������������������������������������������������/������������������������������������������������������+91 73050 56201������������������������������������������������������/������������������������������������������������������+91 7550224400
                    or write to us at������������������������������������������������������cv@groupteampro.com������������������������������������������������������/������������������������������������������������������hr@groupteampro.com
                    </p> 
                    <style>
                    th {
                        background-color:989898
                    }
                    </style>
                    """ % (s.person_name,territory,t.subject,vacancy,t.exp_end_date ,t.qualification_type,t.temp_qualification,
                    t.minimum_experience,t.total_experience, t.salary_type,t.specialization,t.maximum_experience,t.currency,t.category,t.gulf_experience,
                    t.amount ,t.driving_licence ,t.description,t.working_days,t.food,t.visa_type,t.transportation,t.accommodation,t.nationality,
                    t.contract_period_year,t.contract_period__month,t.over_time,t.joining_ticket,t.leave,t.any_other_allowance,))

@frappe.whitelist()
def update_sams():
    sams = frappe.get_all("SAMS",{"sa_is_an_organization":1},["name","private_limited_company","proprietary_company"])
    for sm in sams:
        print(sm.name)
        if sm.private_limited_company:
            sam = frappe.get_doc("SAMS",sm.name)
            print(sam.name)
            print(sam.organization_name)
            sam.update({
                "company":"Pvt.Ltd.Company",
                "type":"Agent"
            }).save(ignore_permissions=True)
            frappe.db.commit()
        if sm.proprietary_company:
            sam = frappe.get_doc("SAMS",sm.name)
            print(sam.name)
            print(sam.organization_name)
            sam.update({
                "company":"Proprietary Company",
                "type":"Agent"
            }).save(ignore_permissions=True)
            frappe.db.commit()

# @frappe.whitelist()
# def late_entry():
#     employee = frappe.get_all("Employee",{"status":"Active"},["name"])
#     import calendar
#     now_date = frappe.utils.datetime.datetime.now().date()
#     month = calendar.monthrange(now_date.year, now_date.month)
#     start_date = date(now_date.year, now_date.month, 1)
#     end_date = date(now_date.year, now_date.month, month[1])
#     for emp in employee:
#         attendance = frappe.db.sql("""select name,employee,employee_name,shift,late_entry from `tabAttendance` where late_entry = 1 and employee = %s and attendance_date between %s and %s""",(emp.name,start_date,end_date),as_dict = 1)
#         count = len(attendance)

@frappe.whitelist()
def update_task(project,status):
    # for p in project:
    frappe.errprint(project)
    task = frappe.get_all("Task",{"project":project})
    for t in task:
        if(status == "Completed"):
            frappe.errprint(t.status)
            t.status = frappe.db.set_value("Task",t.name,"status","Completed")
        elif(status=="Cancelled"):
            t.status = frappe.db.set_value("Task",t.name,"status","Cancelled")


@frappe.whitelist()
def create_scheduled_job():
    job = frappe.db.exists('Scheduled Job Type', 'send_miss_punch')
    if not job:
        sjt = frappe.new_doc("Scheduled Job Type")
        sjt.update({
            "method": 'teampro.email_alerts.send_miss_punch',
            "frequency": 'Cron',
            "cron_format": '0 18 * * *'
        })
        sjt.save(ignore_permissions=True)   