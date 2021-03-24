# -*- coding: utf-8 -*-
# Copyright (c) 2020, teamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import today, add_years
import json
from datetime import date

class Candidate(Document):
    pass
    # def validate(self):
    #     frappe.errprint(type(self.dob))
    #     frappe.errprint(type(self.issued_date))
    #     if self.dob and self.dob > date.today():
    #         frappe.throw("Date Of Birth can't be Future Date")
    #     if self.issued_date and self.issued_date > date.today():
    #         frappe.throw("Issued Date can't be Future Date")
    #     if self.expected_doj and self.expected_doj < date.today():
    #         frappe.throw("Expected Date of Joining can't be Past Date")

    # def validate_date(self):        
    #     if self.issued_date and self.issued_date > date.today():
    #         return "Issued Date can't be Future Date"
            
    # def validate_dob(self):
    #     if self.dob and self.dob > date.today():
    #         return "DOB can't be Future Date"

@frappe.whitelist()
def Specialization(q_data):
    category = frappe.get_value("Qualification", {"name": q_data},['category'])
    # specialization = frappe.get_all("Specialization", {"category": category},['name'])
    return category
@frappe.whitelist()
def check_territory(territory):
    site = frappe.db.get_value("Territory",{"territory_name":territory},["parent_territory"])
    return site
       

@frappe.whitelist()
def create_closure(doc,method):
    if doc.pending_for == 'Proposed PSL':
        
        closure_id = frappe.db.exists("Closure", {"candidate": doc.name})
        if closure_id:
            closure = frappe.get_doc("Closure", closure_id)
        else:    
            closure = frappe.new_doc("Closure")
        closure.update({
            "candidate": doc.name,
            "given_name": doc.given_name,
            "territory":doc.territory,
            "mobile": doc.mobile_number,
            "mail_id": doc.mail_id,
            "basic": doc.basic,
            "food_allowance": doc.food,
            "other_allowance": doc.other_allowances,
            "customer": doc.customer,
            "task": doc.task,
            "project": doc.project,
            "candidate_owner":doc.candidate_created_by,
            "sa_owner":doc.sa_agent,
            "name_sa_owner":doc.sa_agent_name,
            "passport_no": doc.passport_number,
            "date_of_birth":doc.dob,
            "ecr_status":doc.ecr_status,
            "issued_date":doc.issued_date,
            "expiry_date":doc.expiry_date,
            "expected_doj":doc.expected_doj,
            "place_of_issue":doc.place_of_issue,
            "selection_date":doc.interview_date,
            })
        if doc.irf:
            closure.update({"irf": doc.irf})
        if doc.candidate_image:
            closure.update({"photo": doc.candidate_image})
        if doc.passport:
            closure.update({"passport": doc.passport})
        if doc.offer_letter:
            closure.update({"offer_letter": doc.offer_letter})
        closure.save(ignore_permissions=True)
        frappe.db.commit()