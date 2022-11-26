from email.mime import message
from shutil import ignore_patterns
import frappe
import pandas as pd

@frappe.whitelist(allow_guest=True)
def test_api(**args):
    frappe.log_error(message=args)
    can = frappe.new_doc("Candidate")
    can.given_name = args['given_name']
    can.position =args ['position']
    can.passport_number = args['passport_number']
    can.mobile_number = args['mobile_number']
    can.mail_id = args['mail_id']
    can.age = args['age']
    can.dob = pd.to_datetime(args['dob']).date()
    can.india_experience = args['india_experience']
    can.total_experience = args['total_experience']
    can.overseas_experience = args['overseas_experience']
    can.ecr_status = args ['ecr_status']
    # can.qualification= args ['qualification']
    # can.specialization = args['specialization']
  
    can.save(ignore_permissions=True)
    frappe.db.commit()
    
    return args
# def update_api(**args):
#     can = frappe.get_doc("Candidate")
#     can.name = args['name']
#     can.given_name = args['given_name']
#     can.position =args ['position']
#     can.passport_number = args['passport_number']
#     can.mobile_number = args['mobile_number']
#     can.mail_id = args['mail_id']
#     can.age = args['age']
#     can.dob = pd.to_datetime(args['dob']).date()
#     can.india_experience = args['india_experience']
#     can.total_experience = args['total_experience']
#     can.overseas_experience = args['overseas_experience']
#     can.ecr_status = args ['ecr_status']
#      can.qualification= args ['qualification']
#     can.specialization = args['specialization']
#     can.save(ignore_permissions=True)
#     frappe.db.commit()
    
#     return args