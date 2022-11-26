# -*- coding: utf-8 -*-
# Copyright (c) 2020, teamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from inspect import classify_class_attrs
import frappe
from frappe.model.document import Document
from frappe.utils import today, flt, add_days, date_diff
from frappe.utils import cstr, formatdate, add_months, cint, fmt_money, add_days, flt
from frappe.utils.data import nowdate
from erpnext.setup.utils import get_exchange_rate

class Closure(Document):
    def on_update(self):
        if self.client_si:
            conversion = get_exchange_rate(self.billing_currency, "INR")
            self.client_payment_company_currency = conversion * self.client_si
            self.client_payment_dec_cc = conversion * self.client_dec
            self.client_payment_sc_cc = conversion * self.client_service_charge
    def validate(self):
        if self.status == 'Dropped':
            frappe.db.set_value("Candidate", self.candidate,
                                "pending_for", "IDB")
            self.status = 'Dropped'

        elif self.status == 'Waitlisted':
            self.status = 'Waitlisted'
        else:
            self.validate_psl()

    def validate_psl(self):
        # frappe.errprint(today)
        if not self.onboarded:
            parent_territory = frappe.get_value(
                'Territory', self.territory, 'parent_territory')
            if self.territory == 'India' or parent_territory == 'India':
                if self.so_created or self.so_confirmed_date:
                    self.status = 'Onboarded'
                    self.onboarded = 1
                    self.status_updated_on = today()
                else:
                    self.status = 'Sales Order'
                    self.status_updated_on = today()

            elif self.territory == 'Qatar':
                if self.irf and self.passport and self.photo:
                    if self.offer_letter:
                        if self.sol:
                            if self.pcc or self.pcc_not_applicable:                   
                                # if self.final_medical:
                                    if self.visa and self.so_created:
                                        if self.visa_stamping:
                                            if self.ecr_status != 'ECR' or self.emigration or self.emigration_not_applicable ==1:
                                                if self.ticket:
                                                    if self.status == 'Onboarded':
                                                        self.status = 'Onboarded'
                                                        self.onboarded = 1
                                                        self.boarded_date = today()
                                                    else:
                                                        self.status = 'Onboarding'
                                                        self.status_updated_on = today()
                                                else:
                                                    self.status = 'Ticket'
                                                    self.ticket_date = today()
                                            else:
                                                self.status = 'Emigration'
                                                self.emigration_date = today()
                                        else:
                                            self.status = 'Visa Stamping'
                                            self.date_of_visa = today()
                                    else:
                                        if self.is_required:
                                            if not self.certificate_attestation:
                                                frappe.db.set_value(
                                                    "Closure", self.name, "status", "Certificate Attestation")
                                                # self.save(ignore_permissions=True)
                                                frappe.reload_doctype("Closure")
                                            else:
                                                self.status = 'Visa'
                                                self.visa_date = today()
                                                # self.save()
                                        else:
                                            self.status = 'Visa'
                                            self.visa_date = today()
                                # else:
                                #     self.status = 'Final Medical'
                                #     self.premedical_date = today()
                            else:
                                self.status = "PCC"
                                self.pcc_uploaded_date = today() 

                        else:
                            self.status = 'Signed Offer Letter'
                            self.pcc_not_applicable = 1
                            self.offer_letter_date = today()
                    else:
                        self.status = 'Client Offer Letter'
                        self.status_updated_on = today()
                else:
                    self.status = 'PSL'
                    self.status_updated_on = today()

            elif self.territory == 'UAE' and self.visa_state == 'Abudhabi':
                if self.irf and self.passport and self.photo:
                    if self.offer_letter:
                        if self.sol:
                            if self.pcc or self.pcc_not_applicable:                   
                                if self.visa and self.so_created:
                                    if self.final_medical:
                                        if self.visa_stamping:
                                            if self.ecr_status != 'ECR' or self.emigration:
                                                if self.ticket:
                                                    if self.status == 'Onboarded':
                                                        self.status = 'Onboarded'
                                                        self.onboarded = 1
                                                        self.boarded_date = today()
                                                    else:
                                                        self.status = 'Onboarding'
                                                        self.status_updated_on = today()
                                                else:
                                                    self.status = 'Ticket'
                                                    self.ticket_date = today()
                                            else:
                                                self.status = 'Emigration'
                                                self.emigration_date = today()
                                        else:
                                            self.status = 'Visa Stamping'
                                            self.stamped_visa_date = today()
                                    else:
                                        self.status = 'Final Medical'
                                        self.final_medical_date = today()
                                else:
                                    if self.is_required:
                                        if not self.certificate_attestation:
                                            self.status = 'Certificate Attestation'
                                            # self.reload()
                                        else:
                                            self.status = 'Visa'
                                            self.visa_date = today()
                                    else:
                                        self.status = 'Visa'
                                        self.visa_date = today()
                            else:
                                self.status = "PCC"
                                self.pcc_uploaded_date = today()
                        else:
                            self.status = 'Signed Offer Letter'
                            self.pcc_not_applicable = 1
                            self.offer_letter_date = today()
                        # else:
                        #     self.status = 'Sales Order'
                        #     self.status_updated_on = today()
                    else:
                        self.status = "Client Offer Letter"
                        self.col_date = today()
                else:
                    self.status = 'PSL'
                    self.status_updated_on = today()

            elif self.territory == 'UAE' and self.visa_state == 'Dubai':
                if self.irf and self.passport and self.photo:
                    if self.offer_letter:
                        # if self.so_created or self.so_confirmed_date:
                        if self.sol:
                            if self.final_medical:
                                if self.pcc or self.pcc_not_applicable == 1:
                                    if self.visa:
                                        if self.ecr_status != 'ECR' or self.emigration:
                                            if self.ticket:
                                                if self.status == 'Onboarded':
                                                    self.status = 'Onboarded'
                                                    self.onboarded = 1
                                                    self.boarded_date = today()
                                                else:
                                                    self.status = 'Onboarding'
                                                    self.status_updated_on = today()
                                            else:
                                                self.status = 'Ticket'
                                                self.ticket_date = today()
                                        else:
                                            self.status = 'Emigration'
                                            self.emigration_date = today()
                                    else:
                                        if self.is_required:
                                            if not self.certificate_attestation:
                                                self.status = 'Certificate Attestation'
                                                # self.reload()
                                            else:
                                                self.status = 'Visa'
                                                self.visa_date = today()
                                        else:
                                            self.status = 'Visa'
                                            self.visa_date = today()
                                else:
                                    self.status = "PCC"
                                    self.pcc_uploaded_date
                            else:
                                self.status = 'Final Medical'
                                self.premedical_date = today()
                        else:
                            self.status = 'Signed Offer Letter'
                            self.offer_letter_date = today()
                        # else:
                        #     self.status = 'Sales Order'
                        #     self.status_updated_on = today()
                    else:
                        self.status = 'Client Offer Letter'
                        self.col_date = today()
                else:
                    self.status = 'PSL'
                    self.status_updated_on = today()

            elif self.territory == 'Oman':
                if self.irf and self.passport and self.photo:
                    if self.offer_letter:
                        if self.sol:
                            if self.pcc or self.pcc_not_applicable == 1 :
                                if self.final_medical:
                                    if self.visa and self.so_created == 1:
                                        if self.ecr_status != 'ECR' or self.emigration or self.emigration_not_applicable == 1:
                                            if self.ticket:
                                                if self.status == 'Onboarded':
                                                    self.status = 'Onboarded'
                                                    self.onboarded = 1
                                                    self.boarded_date = today()
                                                else:
                                                    self.status = 'Onboarding'
                                                    self.status_updated_on = today()
                                            else:
                                                self.status = 'Ticket'
                                                self.ticket_date = today()
                                        else:
                                            self.status = 'Emigration'
                                            self.emigration_date = today()
                                    else:
                                        if self.is_required:
                                            if not self.certificate_attestation:
                                                frappe.db.set_value(
                                                    "Closure", self.name, "status", "Certificate Attestation")
                                                # self.reload()
                                            else:
                                                self.status = 'Visa'
                                                self.visa_date = today()
                                        else:
                                            self.status = 'Visa'
                                            self.visa_date = today()
                                else:
                                    self.status = 'Final Medical'
                                    self.date_of_final_medical = today()
                            else:
                                self.status = 'PCC'
                                self.pcc_uploaded_date = today()
                        else:
                            self.status = 'Signed Offer Letter'
                            self.pcc_not_applicable = 1
                            self.sol_uploaded_date = today()
                    else:
                        self.status = 'Client Offer Letter'
                        self.col_date = today()
                else:
                    self.status = 'PSL'
                    self.status_updated_on = today()

            elif self.territory == 'Kuwait':
                if self.status != "Dropped":
                    if self.irf and self.passport and self.photo:
                        if self.offer_letter:
                            if self.sol:
                                if self.premedical or self.premedical_not_applicable == 1:
                                    if self.visa and self.so_created:
                                        if self.pcc or self.pcc_not_applicable ==1:
                                            if self.final_medical:
                                                if self.visa_stamping:
                                                    if self.ecr_status != 'ECR' or self.emigration or self.emigration_not_applicable == 1:
                                                        if self.ticket:
                                                            if self.status == 'Onboarded':
                                                                self.status = 'Onboarded'
                                                                self.onboarded = 1
                                                                self.boarded_date = today()
                                                            else:
                                                                self.status = 'Onboarding'
                                                                self.status_updated_on = today()
                                                        else:
                                                            self.status = 'Ticket'
                                                            self.ticket_date = today()
                                                    else:
                                                        self.status = 'Emigration'
                                                        self.emigration_date = today()
                                                else:
                                                    self.status = 'Visa Stamping'
                                                self.date_of_visa = today()                
                                            else:
                                                self.status = 'Final Medical'
                                                self.final_medical_date = today()
                                        else:
                                            self.status = 'PCC'
                                            self.pcc_uploaded_date = today()    
                                    else:
                                        if self.is_required:
                                            if not self.certificate_attestation:
                                                self.status = 'Certificate Attestation'
                                                # self.reload()
                                            else:
                                                self.status = 'Visa'
                                                self.visa_date = today()
                                        else:
                                            self.status = 'Visa'
                                            self.visa_date = today()
                                else:
                                    self.status = 'Premedical'
                                    self.premedical_date = today()
                                    # else:
                                    #     self.status = 'MOH Approval'
                                    #     self.moh_uploaded_date = today()                                                                  
                                
                            else:
                                self.status = 'Signed Offer Letter'
                                self.sol_uploaded_date = today()
                        else:
                            self.status= 'Client Offer Letter'
                            self.col_date = today()    
                    else:
                        self.status = 'PSL'
                        self.status_updated_on = today()

            elif self.territory in ['Dammam', 'Jeddah', 'Riyadh'] or self.territory == 'KSA':
                if self.irf and self.passport and self.photo:
                    if self.offer_letter:
                        if self.sol:
                            # if self.pcc or self.pcc_not_applicable: 
                            if self.visa:
                                if self.pcc or self.pcc_not_applicable: 
                                    if self.final_medical:
                                        if self.visa_stamping:
                                            if self.ecr_status != 'ECR' or self.emigration or self.emigration_not_applicable:
                                                if self.ticket:
                                                    if self.status == 'Onboarded':
                                                        self.status = 'Onboarded'
                                                        self.onboarded = 1
                                                        self.boarded_date = today()
                                                    else:
                                                        self.status = 'Onboarding'
                                                        self.status_updated_on = today()
                                                else:
                                                    self.status = 'Ticket'
                                                    self.ticket_date = today()
                                            else:
                                                self.status = 'Emigration'
                                                self.emigration_date = today()
                                        else:
                                            self.status = 'Visa Stamping'
                                            self.stamped_visa_date = today()
                                    else:
                                        self.status = 'Final Medical'
                                        self.final_medical_date = today()
                                else:
                                    self.status = "PCC"
                                    self.pcc_uploaded_date = today() 
                            else:
                                if self.is_required:
                                    if not self.certificate_attestation:
                                        self.status = 'Certificate Attestation'
                                        # self.reload()
                                    else:
                                        self.status = 'Visa'
                                        self.visa_date = today()
                                else:
                                    self.status = 'Visa'
                                    self.visa_date = today()
                            

                        else:
                            self.status = "Signed Offer Letter"
                            self.col_date = today()
                    else:
                        self.status = 'Client Offer Letter'
                        self.offer_letter_date = today()
                else:
                    self.status = 'PSL'
                    self.status_updated_on = today()

            elif self.territory == 'Bahrain':
                if self.irf and self.passport and self.photo:
                    if self.offer_letter:
                        # if self.so_created or self.so_confirmed_date:
                        if self.sol:
                            if self.final_medical:
                                if self.visa and self.so_created == 1:
                                    if self.ecr_status != 'ECR' or self.emigration or self.emigration_not_applicable == 1:
                                        if self.ticket:
                                            if self.status == 'Onboarded':
                                                self.status = 'Onboarded'
                                                self.onboarded = 1
                                                self.boarded_date = today()
                                            elif self.status == 'Dropped':
                                                self.status = 'Dropped'
                                            else:
                                                self.status = 'Onboarding'
                                                self.status_updated_on = today()
                                        else:
                                            self.status = 'Ticket'
                                            self.ticket_date = today()
                                    else:
                                        self.status = 'Emigration'
                                        self.emigration_date = today()
                                else:
                                    if self.is_required:
                                        if not self.certificate_attestation:
                                            self.status = 'Certificate Attestation'
                                            # self.reload()
                                        else:
                                            self.status = 'Visa'
                                            self.visa_date = today()
                                    else:
                                        self.status = 'Visa'
                                        self.visa_date = today()
                            else:
                                self.status = 'Final Medical'
                                self.premedical_date = today()
                        else:
                            self.status = 'Signed Offer Letter'
                            self.pcc_not_applicable = 1
                            self.offer_letter_date = today()
                        # else:
                        #     self.status = 'Sales Order'
                        #     self.status_updated_on = today()
                    else:
                        self.status = "Client Offer Letter"
                        self.col_date = today()
                else:
                    self.status = 'PSL'
                    self.status_updated_on = today()

@frappe.whitelist()
def create_sale_order(closure, project, customer, task, candidate_name, contact, payment,client_sc,candidate_owner,sa_id,candidate_sc,billing_currency, territory, associate,passport_no, expected_doj, delivery_manager, account_manager,service,supplier,associate_si,client_si,candidate_si,candidate_dec,dec):
    # cg = frappe.db.get_value("Customer", customer, "customer_group")
    parent_territory = frappe.get_value(
        'Territory', territory, 'parent_territory')
    if payment:
        item_candidate_id = frappe.db.get_value("Item", {"name": contact})
        item_pp_id = frappe.db.get_value("Item", {"name": passport_no})
        if item_candidate_id or item_pp_id:
            pass
        else:
            item = frappe.new_doc("Item")
            if parent_territory == 'India':
                item.item_code = candidate_name
                item.append("taxes", {
                            "item_tax_template": "T - GST @ 18% - THIS",
                            "tax_category": "Professional Service - GST",
                            "valid_from": today()
                            })
            else:
                item.item_code = passport_no
                item.is_non_gst = "0"
            item.item_name = passport_no + ":"+candidate_name
            if candidate_owner:
                item.candidate_owner = candidate_owner
            if sa_id:
                item.sa_id = sa_id
            item.item_group = "Candidates"
            item.stock_uom = "Nos"
            item.qty = "1"
            item.gst_hsn_code = '9985'
            item.is_stock_item = "0"
            item.include_item_in_manufacturing = "0"
            item.description = customer
            item.append("item_defaults", {
                "company": "TeamPRO HR & IT Services Pvt. Ltd."
            })
            item.append("customer_items", {
                "customer_name": customer,
                "ref_code": contact
            })
            item.insert()
            item.save(ignore_permissions=True)

            if territory != 'India' or parent_territory != 'India':
                if payment == "Client":
                    so = frappe.new_doc("Sales Order")
                    so.customer = customer
                    so.reference_customer_ = customer
                    so.passport_number = passport_no
                    so.account_manager = account_manager
                    so.delivery_manager = delivery_manager
                    so.closure_project = project
                    so.currency = billing_currency
                    so.supplier = supplier
                    so.service = service
                    so.total_orginal_dec = dec
                    
                    
                    # so.sa_id = sa_id
                    so.append("items", {
                        "item_code": item.item_code,
                        "item_name": item.item_name,
                        "candidate_owner": item.candidate_owner,
                        "sa_id":item.sa_id,
                        "payment_type": "Candidate",
                        "description": item.description,
                        "uom": item.stock_uom,
                        "is_stock_item": "0",
                        "passport_no": passport_no,
                        "delivery_date": expected_doj or '',
                        "qty": "1",
                        "rate": client_si,
                        "dec1": dec,
                        "sc1": client_sc,
                        
                        # "currency":currency,
                        "cost_center": "Main - THIS",
                    })
                    so.save(ignore_permissions=True)
                    frappe.db.commit()
                    # so.submit()

                # candidate
                if payment == "Candidate":
                    candidate_customer = frappe.new_doc("Customer")
                    candidate_customer.customer_name = candidate_name + '-' + passport_no
                    candidate_customer.customer_type = "Individual"
                    candidate_customer.customer_group = "Individual"
                    candidate_customer.territory = territory
                    candidate_customer.insert()
                    candidate_customer.save(ignore_permissions=True)
                    frappe.db.commit()

                    so = frappe.new_doc("Sales Order")
                    so.customer = candidate_name + '-' + passport_no
                    so.reference_customer_ = customer
                    so.customer_group = "Individual"
                    so.passport_number = passport_no
                    so.account_manager = account_manager
                    so.delivery_manager = delivery_manager
                    so.service = service
                    so.currency = "INR"
                    so.total_original_dec = candidate_dec
                    so.append("items", {
                        "item_code": item.item_code,
                        "item_name": item.item_name,
                        "candidate_owner": item.candidate_owner,
                        "sa_id":item.sa_id,
                        "payment_type": "Candidate",
                        "description": item.description,
                        "uom": item.stock_uom,
                        "is_stock_item": "0",
                        "passport_no": passport_no,
                        "delivery_date": expected_doj or '',
                        "qty": "1",
                        "rate": candidate_si,
                        "dec1":candidate_dec,
                        "sc1":candidate_sc,
                        # "currency":currency,
                        "cost_center": "Main - THIS",
                    })
                    so.save(ignore_permissions=True)
                    frappe.db.commit()
                    # so.submit()

                # associate
                if payment == "Associate":

                    so = frappe.new_doc("Sales Order")
                    so.customer = associate
                    so.reference_customer_ = customer
                    so.customer_group = "Associate"
                    # so.passport_number = passport_no
                    # so.account_manager = account_manager
                    # so.delivery_manager = delivery_manager
                    so.service = service
                    so.total_orginal_dec = dec
                    so.append("items", {
                        "item_code": item.item_code,
                        "item_name": item.item_name,
                        "candidate_owner": item.candidate_owner,
                        "sa_id":item.sa_id,
                        # "payment_type": "Candidate",
                        "description": item.description,
                        "uom": item.stock_uom,
                        "is_stock_item": "0",
                        "passport_no": passport_no,
                        "delivery_date": expected_doj or '',
                        "qty": "1",
                        "rate": associate_si,
                        "dec1":dec,
                        # "sc1":sc,
                        # "currency":currency,
                        "cost_center": "Main - THIS",
                    })
                    so.save(ignore_permissions=True)
                    frappe.db.commit()
                    # so.submit()

                
                # both
                if payment == "Both":
                    # client
                    so = frappe.new_doc("Sales Order")
                    so.customer = customer
                    so.reference_customer_ = customer
                    so.passport_number = passport_no
                    so.account_manager = account_manager
                    so.currency = billing_currency
                    so.delivery_manager = delivery_manager
                    so.service = service
                    #so.total_orginal_dec = client_dec
                    
                    so.append("items", {
                        "item_code": item.item_code,
                        "item_name": item.item_name,
                        "candidate_owner": item.candidate_owner,
                        "sa_id":item.sa_id,
                        "payment_type": "Candidate",
                        "description": item.description,
                        "uom": item.stock_uom,
                        "is_stock_item": "0",
                        "passport_no": passport_no,
                        "delivery_date": expected_doj or '',
                        "qty": "1",
                        "rate": client_si,
                        #"dec1": client_dec,
                        "sc1": client_sc,
                        # "rate": client_sc,
                        # "currency":currency,
                        "cost_center": "Main - THIS",
                    })
                    so.save(ignore_permissions=True)
                    frappe.db.commit()
                    # so.submit()

                    # candidate
                    candidate_customer = frappe.new_doc("Customer")
                    candidate_customer.customer_name = candidate_name + '-' + passport_no
                    candidate_customer.customer_type = "Individual"
                    candidate_customer.customer_group = "Individual"
                    candidate_customer.territory = territory
                    candidate_customer.insert()
                    candidate_customer.save(ignore_permissions=True)
                    frappe.db.commit()
                    so = frappe.new_doc("Sales Order")
                    so.customer = candidate_name + '-' + passport_no
                    so.reference_customer_ = customer
                    so.customer_group = "Individual"
                    so.passport_number = passport_no
                    so.account_manager = account_manager
                    so.currency ="INR"
                    so.delivery_manager = delivery_manager
                    so.service = service
                    so.append("items", {
                        "item_code": item.item_code,
                        "item_name": item.item_name,
                        "candidate_owner": item.candidate_owner,
                        "sa_id":item.sa_id,
                        "payment_type": "Candidate",
                        "description": item.description,
                        "uom": item.stock_uom,
                        "is_stock_item": "0",
                        "passport_no": passport_no,
                        "delivery_date": expected_doj or '',
                        "qty": "1",
                        "rate": candidate_si,
                        "dec1":candidate_dec,
                        "sc1":candidate_sc,
                        # "rate": candidate_sc,
                        "cost_center": "Main - THIS",
                    })
                    so.save(ignore_permissions=True)
                    frappe.db.commit()
                    # so.submit()
                    frappe.set_value('Closure', closure, 'status', 'Visa')

                # if territory == 'India' or parent_territory == 'India':
                #     # client
                #     if payment == "Client":
                #         so = frappe.new_doc("Sales Order")
                #         so.customer = customer
                #         so.account_manager = account_manager
                #         so.append("items", {
                #             "item_code": item.item_code,
                #             "item_name": item.item_name,
                #             "payment_type": "Candidate",
                #             "description": item.description,
                #             "uom": item.stock_uom,
                #             "is_stock_item": "0",
                #             "passport_no": passport_no,
                #             "delivery_date": expected_doj,
                #             "qty": "1",
                #             "rate": client_sc,
                #             "cost_center":"Main - THIS",
                #         })
                #         so.save(ignore_permissions=True)
                #         frappe.db.commit()
                #         # so.submit()

                #     # candidate
                #     if payment == "Candidate":
                #         customer = frappe.new_doc("Customer")
                #         customer.customer_name = candidate_name
                #         customer.customer_type = "Individual"
                #         customer.customer_group = "Individual"
                #         customer.territory = territory
                #         customer.insert()
                #         customer.save(ignore_permissions=True)
                #         frappe.db.commit()

                #         so = frappe.new_doc("Sales Order")
                #         so.customer = candidate_name
                #         so.account_manager = account_manager
                #         so.append("items", {
                #             "item_code": item.item_code,
                #             "item_name": item.item_name,
                #             "payment_type": "Candidate",
                #             "description": item.description,
                #             "uom": item.stock_uom,
                #             "is_stock_item": "0",
                #             "passport_no": passport_no,
                #             "delivery_date": expected_doj,
                #             "qty": "1",
                #             "rate": candidate_sc,
                #             "cost_center":"Main - THIS",
                #         })

                #         so.save(ignore_permissions=True)
                #         frappe.db.commit()
                #         # so.submit()

                #     if payment == "Both":
                #         #client
                #         so = frappe.new_doc("Sales Order")
                #         so.customer = customer
                #         so.account_manager = account_manager
                #         so.append("items", {
                #             "item_code": item.item_code,
                #             "item_name": item.item_name,
                #             "payment_type": "Candidate",
                #             "description": item.description,
                #             "uom": item.stock_uom,
                #             "is_stock_item": "0",
                #             "passport_no": passport_no,
                #             "delivery_date": expected_doj,
                #             "qty": "1",
                #             "rate": client_sc,
                #             "cost_center":"Main - THIS",
                #         })
                #         so.save(ignore_permissions=True)
                #         frappe.db.commit()
                #         # so.submit()

                #         #candidate
                #         customer = frappe.new_doc("Customer")
                #         customer.customer_name = candidate_name
                #         customer.customer_type = "Individual"
                #         customer.customer_group = "Individual"
                #         customer.territory = territory
                #         customer.insert()
                #         customer.save(ignore_permissions=True)
                #         frappe.db.commit()
                #         so = frappe.new_doc("Sales Order")
                #         so.customer = candidate_name
                #         so.account_manager = account_manager
                #         so.append("items", {
                #             "item_code": item.item_code,
                #             "item_name": item.item_name,
                #             "payment_type": "Candidate",
                #             "description": item.description,
                #             "uom": item.stock_uom,
                #             "is_stock_item": "0",
                #             "passport_no": passport_no,
                #             "delivery_date": expected_doj,
                #             "qty": "1",
                #             "rate": candidate_sc,
                #             "cost_center":"Main - THIS",
                #         })
                # frappe.set_value('Closure', closure, 'status', 'Onboarded')

            frappe.set_value('Closure', closure, 'so_created', 1)
            frappe.set_value('Closure', closure, 'so_confirmed_date', today())

            total = cint(client_sc) + cint(candidate_sc)

            return "Sales Order Created for Total value {0}".format(frappe.bold(fmt_money(total, currency=billing_currency)))

        # elif self.territory == 'Abudhabi':
        #     if self.irf and self.passport and self.photo:
        #         if self.so_created or self.so_confirmed_date:
        #             if self.offer_letter:
        #                 if self.mol:
        #                     if self.visa:
        #                         if self.final_medical:
        #                             if self.stamped_visa:
        #                                 if self.ecr_status != 'ECR' or self.emigration:
        #                                     if self.ticket:
        #                                         if self.status == 'Onboarded':
        #                                             self.status = 'Onboarded'
        #                                             self.boarded_date = today()
        #                                         else:
        #                                             self.status = 'Onboarding'
        #                                             self.status_updated_on = today()
        #                                     else:
        #                                         self.status = 'Ticket'
        #                                         self.ticket_date = today()
        #                                 else:
        #                                     self.status = 'Emigration'
        #                                     self.emigration_date = today()
        #                             else:
        #                                 self.status = 'Visa Stamping'
        #                                 self.stamped_visa_date = today()
        #                         else:
        #                             self.status = 'Final Medical'
        #                             self.final_medical_date = today()
        #                     else:
        #                         self.status = 'Visa'
        #                         self.visa_date = today()
        #                 else:
        #                     self.status = 'MOL'
        #                     self.mol_date = today()
        #             else:
        #                 self.status = 'Client Offer Letter'
        #                 self.offer_letter_date = today()
        #         else:
        #             self.status = 'Sales Order'
        #             self.status_updated_on = today()
        #     else:
        #         self.status = 'PSL'
        #         self.status_updated_on = today()

        # elif self.territory == 'UAE' or self.territory == 'Dubai':
        #     if self.irf and self.passport and self.photo:
        #         if self.status == 'Sales Order Confirmed' or self.sales_order_confirmed_date:
        #             if self.offer_letter:
        #                 if self.premedical:
        #                     if self.mol:
        #                         if self.visa:
        #                             if self.ecr_status != 'ECR' or self.poe:
        #                                 # if self.payment_reciept:
        #                                 if self.ticket:
        #                                     if self.status == 'Onboarded':
        #                                         self.status = 'Onboarded'
        #                                         self.boarded_date = today()
        #                                     else:
        #                                         self.status = 'Onboarding'
        #                                         self.status_updated_on = today()
        #                                 else:
        #                                     self.status = 'Ticket Details'
        #                                     self.ticket_date = today()
        #                                 # else:
        #                                 #     self.status = 'Payment Receipt'
        #                                 #     self.payment_receipt_date = today()
        #                             else:
        #                                 self.status = 'PoE'
        #                                 self.poe_date = today()
        #                         else:
        #                             self.status = 'Visa'
        #                             self.visa_date = today()
        #                     else:
        #                         self.status = 'MOL'
        #                         self.mol_date = today()
        #                 else:
        #                     self.status = 'Premedical'
        #                     self.premedical_date = today()
        #             else:
        #                 self.status = 'Client Offer Letter'
        #                 self.offer_letter_date = today()
        #         else:
        #             self.status = 'Sales Order'
        #             self.status_updated_on = today()
        #     else:
        #         self.status = 'PSL'
        #         self.status = 'Sales Order'
        #         self.status_updated_on = today()

        # elif self.territory == 'Dammam' or self.territory == 'Jeddah' or self.territory == 'Riyadh':
        #     if self.irf and self.passport and self.photo:
        #         if self.status == 'Sales Order Confirmed' or self.sales_order_confirmed_date:
        #             if self.offer_letter:
        #                 if self.visa:
        #                     if self.final_medical:
        #                         if self.stamped_visa:
        #                             if self.ecr_status != 'ECR' or self.poe:
        #                                 # if self.payment_reciept:
        #                                 if self.ticket:
        #                                     if self.status == 'Onboarded':
        #                                         self.status = 'Onboarded'
        #                                         self.boarded_date = today()
        #                                     else:
        #                                         self.status = 'Onboarding'
        #                                         self.status_updated_on = today()
        #                                 else:
        #                                     self.status = 'Ticket Details'
        #                                     self.ticket_date = today()
        #                                 # else:
        #                                 #     self.status = 'Payment Receipt'
        #                                 #     self.payment_receipt_date = today()
        #                             else:
        #                                 self.status = 'PoE'
        #                                 self.poe_date = today()
        #                         else:
        #                             self.status = 'Visa Stamping'
        #                             self.stamped_visa_date = today()
        #                     else:
        #                         self.status = 'Final Medical'
        #                         self.final_medical_date = today()
        #                 else:
        #                     self.status = 'Visa'
        #                     self.visa_date = today()
        #             else:
        #                 self.status = 'Client Offer Letter'
        #                 self.offer_letter_date = today()
        #         else:
        #             self.status = 'Sales Order'
        #             self.status_updated_on = today()
        #     else:
        #         self.status = 'PSL'
        #         self.status = 'Sales Order'
        #         self.status_updated_on = today()

        # elif self.territory == 'Oman' or self.territory == 'Maldives' or self.territory == 'Bahrain':
        #     if self.irf and self.passport and self.photo:
        #         if self.status == 'Sales Order Confirmed' or self.sales_order_confirmed_date:
        #             if self.offer_letter:
        #                 if self.premedical:
        #                     if self.stamped_visa:
        #                         if self.ecr_status != 'ECR' or self.poe:
        #                             # if self.payment_reciept:
        #                             if self.ticket:
        #                                 if self.status == 'Onboarded':
        #                                     self.status = 'Onboarded'
        #                                     self.boarded_date = today()
        #                                 else:
        #                                     self.status = 'Onboarding'
        #                                     self.status_updated_on = today()
        #                             else:
        #                                 self.status = 'Ticket Details'
        #                                 self.ticket_date = today()
        #                             # else:
        #                             #     self.status = 'Payment Receipt'
        #                             #     self.payment_receipt_date = today()
        #                         else:
        #                             self.status = 'PoE'
        #                             self.poe_date = today()
        #                     else:
        #                         self.status = 'Visa'
        #                         self.visa_date = today()
        #                 else:
        #                     self.status = 'Premedical'
        #                     self.premedical_date = today()
        #             else:
        #                 self.status = 'Client Offer Letter'
        #                 self.offer_letter_date = today()
        #         else:
        #             self.status = 'Sales Order'
        #             self.status_updated_on = today()
        #     else:
        #         self.status = 'PSL'
        #         self.status = 'Sales Order'
        #         self.status_updated_on = today()

        # elif self.territory == 'Kuwait' or self.territory == 'Singapore':
        #     if self.irf and self.passport and self.photo:
        #         if self.status == 'Sales Order Confirmed' or self.sales_order_confirmed_date:
        #             if self.offer_letter:
        #                 if self.premedicalpremedical:
        #                     if self.pcc:
        #                         if self.visa:
        #                             if self.final_medical:
        #                                 if self.stamped_visa:
        #                                     if self.ecr_status != 'ECR' or self.poe:
        #                                         # if self.payment_reciept:
        #                                         if self.ticket:
        #                                             if self.status == 'Onboarded':
        #                                                 self.status = 'Onboarded'
        #                                                 self.boarded_date = today()
        #                                             else:
        #                                                 self.status = 'Onboarding'
        #                                                 self.status_updated_on = today()
        #                                         else:
        #                                             self.status = 'Ticket Details'
        #                                             self.ticket_date = today()
        #                                     # else:
        #                                     #     self.status = 'Payment Receipt'
        #                                     #     self.payment_receipt_date = today()
        #                                     else:
        #                                         self.status = 'PoE'
        #                                         self.poe_date = today()
        #                                 else:
        #                                     self.status = 'Visa Stamping'
        #                                     self.stamped_visa_date = today()
        #                             else:
        #                                 self.status = 'Final Medical'
        #                                 self.final_medical_date = today()
        #                         else:
        #                             self.status = 'Visa'
        #                             self.visa_date = today()
        #                     else:
        #                         self.status = 'PCC'
        #                         self.pcc_date = today()
        #                 else:
        #                     self.status = 'Premedical'
        #                     self.premedical_date = today()
        #             else:
        #                 self.status = 'Client Offer Letter'
        #                 self.offer_letter_date = today()
        #         else:
        #             self.status = 'Sales Order'
        #             self.status_updated_on = today()
        #     else:
        #         self.status = 'PSL'
        #         self.status = 'Sales Order'
        #         self.status_updated_on = today()


# def closure_payment_entry(doc, method):
#     if doc.payment_type == "Receive":
#         given_name= doc.party
#         split = given_name.split('-',1)
#         fs = split[0]
#         closure = frappe.db.exists('Closure', {'given_name': fs})
#         if closure:
#             clid = frappe.get_doc('Closure', closure)
#             current_outstanding = clid.outstanding_amount
#             outstanding = current_outstanding - doc.paid_amount
#             current_outstanding = outstanding
#             clid.append('part_payment_collection', {
#                 'date': today(),
#                 'amount': doc.paid_amount
#             })
#             clid.save(ignore_permissions=True)
#             frappe.log_error(message=doc)
               