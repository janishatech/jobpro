import frappe
import json
from frappe.utils.csvutils import read_csv_content
from six.moves import range
from six import string_types
import frappe
import json
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
	nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
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
    count = frappe.db.sql("select sum(vac),sum(sp),sum(fp),sum(sl),sum(psl) from `tabTask` where `project` = %s",project)
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