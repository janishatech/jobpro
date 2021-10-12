# -*- coding: utf-8 -*-
# Copyright (c) 2020, teamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import today, flt, add_days, date_diff
from frappe.utils import cstr,formatdate, add_months, cint, fmt_money, add_days,flt

class Closure(Document):
    def validate(self):
        self.validate_psl()
        
    def validate_psl(self):
        if self.status == 'Dropped':
            frappe.db.set_value("Candidate", self.candidate,
                                "pending_for", "IDB")
            self.status = 'Dropped'

        elif self.status == 'Waitlisted':
            self.status = 'Waitlisted'

        # elif self.status == 'PSL':
        parent_territory = frappe.get_value('Territory',self.territory,'parent_territory')
        if self.territory == 'India' or parent_territory == 'India':
            if self.so_created or self.so_confirmed_date:
                self.status = 'Onboarded'
                self.status_updated_on = today()
            else:
                self.status = 'Sales Order'
                self.status_updated_on = today()
                    
        elif self.territory == 'Qatar':
            if self.irf and self.passport and self.photo:
                # if self.so_created or self.so_confirmed_date:
                if self.sol:
                    if self.premedical:
                        if self.visa:
                            if self.final_medical:
                                if self.ecr_status != 'ECR' or self.emigration:
                                    if self.ticket:
                                        if self.status == 'Onboarded':
                                            self.status = 'Onboarded'
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
                                self.status = 'Final Medical'
                                self.final_medical_date = today()
                        else:
                            if self.is_required:
                                if not self.certificate_attestation:
                                    frappe.errprint("no certificate")
                                    frappe.db.set_value("Closure",self.name,"status","Certificate Attestation")
                                    # self.save(ignore_permissions=True)
                                    frappe.reload_doctype("Closure")
                                else:
                                    frappe.errprint("certificate")
                                    self.status = 'Visa'
                                    self.visa_date = today()
                                    # self.save()
                            else:
                                self.status = 'Visa'
                                self.visa_date = today()
                    else:
                        self.status = 'Premedical'
                        self.premedical_date = today()
                else:
                    self.status = 'Offer Letter'
                    self.offer_letter_date = today()
                # else:
                #     self.status = 'Sales Order'
                #     self.status_updated_on = today()
            else:
                self.status = 'PSL'
                self.status_updated_on = today()

        elif self.territory == 'UAE' and self.visa_state == 'Abu Dhabi':
            if self.irf and self.passport and self.photo:
                # if self.so_created or self.so_confirmed_date:
                if self.sol:
                    if self.premedical:
                        if self.visa:
                            if self.final_medical:
                                if self.visa_stamping:
                                    if self.ecr_status != 'ECR' or self.emigration:
                                        if self.ticket:
                                            if self.status == 'Onboarded':
                                                self.status = 'Onboarded'
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
                                    frappe.errprint("no certificate")
                                    self.status = 'Certificate Attestation'
                                    # self.reload()
                                else:
                                    frappe.errprint("certificate")
                                    self.status = 'Visa'
                                    self.visa_date = today()
                            else:
                                self.status = 'Visa'
                                self.visa_date = today()
                    else:
                        self.status = 'Premedical'
                        self.premedical_date = today()
                else:
                    self.status = 'Offer Letter'
                    self.offer_letter_date = today()
                # else:
                #     self.status = 'Sales Order'
                #     self.status_updated_on = today()
            else:
                self.status = 'PSL'
                self.status_updated_on = today()
        
        elif self.territory == 'UAE' and self.visa_state == 'Dubai':
            if self.irf and self.passport and self.photo:
                # if self.so_created or self.so_confirmed_date:
                if self.sol:
                    if self.premedical:
                        if self.visa:
                            if self.ecr_status != 'ECR' or self.emigration:
                                if self.ticket:
                                    if self.status == 'Onboarded':
                                        self.status = 'Onboarded'
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
                                    frappe.errprint("no certificate")
                                    self.status = 'Certificate Attestation'
                                    # self.reload()
                                else:
                                    frappe.errprint("certificate")
                                    self.status = 'Visa'
                                    self.visa_date = today()
                            else:
                                self.status = 'Visa'
                                self.visa_date = today()
                    else:
                        self.status = 'Premedical'
                        self.premedical_date = today()
                else:
                    self.status = 'Offer Letter'
                    self.offer_letter_date = today()
                # else:
                #     self.status = 'Sales Order'
                #     self.status_updated_on = today()
            else:
                self.status = 'PSL'
                self.status_updated_on = today()

        elif self.territory == 'Oman':
            if self.irf and self.passport and self.photo:
                # if self.so_created:
                if self.sol:
                    if self.premedical:
                        if self.visa:
                            if self.ecr_status != 'ECR' or self.emigration:
                                if self.ticket:
                                    if self.status == 'Onboarded':
                                        self.status = 'Onboarded'
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
                                    frappe.errprint("no certificate")
                                    frappe.db.set_value("Closure",self.name,"status","Certificate Attestation")
                                    # self.reload()
                                else:
                                    frappe.errprint("certificate")
                                    self.status = 'Visa'
                                    self.visa_date = today()
                            else:
                                self.status = 'Visa'
                                self.visa_date = today()
                    else:
                        self.status = 'Premedical'
                        self.premedical_date = today()
                else:
                    self.status = 'Offer Letter'
                    self.offer_letter_date = today()
                # else:
                #     self.status = 'Sales Order'
                #     self.status_updated_on = today()
            else:
                self.status = 'PSL'
                self.status_updated_on = today()      

        elif self.territory == 'Kuwait':
            if self.irf and self.passport and self.photo:
                # if self.so_created or self.so_confirmed_date:
                if self.sol:
                    if self.premedical:
                        if self.visa:
                            if self.final_medical:
                                if self.visa_stamping:
                                    if self.ecr_status != 'ECR' or self.emigration:
                                        if self.ticket:
                                            if self.status == 'Onboarded':
                                                self.status = 'Onboarded'
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
                                    frappe.errprint("no certificate")
                                    self.status = 'Certificate Attestation'
                                    # self.reload()
                                else:
                                    frappe.errprint("certificate")
                                    self.status = 'Visa'
                                    self.visa_date = today()
                            else:
                                self.status = 'Visa'
                                self.visa_date = today()
                    else:
                        self.status = 'Premedical'
                        self.premedical_date = today()
                else:
                    self.status = 'Offer Letter'
                    self.offer_letter_date = today()
                # else:
                #     self.status = 'Sales Order'
                #     self.status_updated_on = today()
            else:
                self.status = 'PSL'
                self.status_updated_on = today()  


        elif self.territory in ['Dammam','Jeddah','Riyadh'] or self.territory == 'KSA':
            if self.irf and self.passport and self.photo:
                # if self.so_created or self.so_confirmed_date:
                if self.sol:
                    if self.visa:
                        if self.final_medical:
                            if self.visa_stamping:
                                if self.ecr_status != 'ECR' or self.emigration:
                                    if self.ticket:
                                        if self.status == 'Onboarded':
                                            self.status = 'Onboarded'
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
                                    frappe.errprint("no certificate")
                                    self.status = 'Certificate Attestation'
                                    # self.reload()
                                else:
                                    frappe.errprint("certificate")
                                    self.status = 'Visa'
                                    self.visa_date = today()
                            else:
                                self.status = 'Visa'
                                self.visa_date = today()
                else:
                    self.status = 'Offer Letter'
                    self.offer_letter_date = today()
                # else:
                #     self.status = 'Sales Order'
                #     self.status_updated_on = today()
            else:
                self.status = 'PSL'
                self.status_updated_on = today()

        elif self.territory == 'Bahrain':
            # if self.irf and self.passport and self.photo:
            if self.so_created or self.so_confirmed_date:
                if self.sol:
                    if self.premedical:
                        if self.visa:
                            if self.ecr_status != 'ECR' or self.emigration:
                                if self.ticket:
                                    if self.status == 'Onboarded':
                                        self.status = 'Onboarded'
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
                                    frappe.errprint("no certificate")
                                    self.status = 'Certificate Attestation'
                                    # self.reload()
                                else:
                                    frappe.errprint("certificate")
                                    self.status = 'Visa'
                                    self.visa_date = today()
                            else:
                                self.status = 'Visa'
                                self.visa_date = today()
                    else:
                        self.status = 'Premedical'
                        self.premedical_date = today()
                else:
                    self.status = 'Offer Letter'
                    self.offer_letter_date = today()
                # else:
                #     self.status = 'Sales Order'
                #     self.status_updated_on = today()
            else:
                self.status = 'PSL'
                self.status_updated_on = today() 


@frappe.whitelist()
def create_sale_order(closure,project, customer, task, candidate_name, contact, payment,currency, client_sc, territory, passport_no,expected_doj, delivery_manager,account_manager):	
    cg = frappe.db.get_value("Customer", customer, "customer_group")
    parent_territory = frappe.get_value('Territory',territory,'parent_territory')
    if payment:
        item_candidate_id = frappe.db.get_value("Item", {"name": contact})
        item_pp_id = frappe.db.get_value("Item", {"name": passport_no})
        if item_candidate_id or item_pp_id:
            pass
        else:
            item = frappe.new_doc("Item")
            if parent_territory == 'India':
                item.item_code = contact
                item.append("taxes", {
                            "item_tax_template":"Tamil Nadu GST @ 18% - THIS",
                            "tax_category":"Professional Service - GST",
                            "valid_from":today()
                        })
            else:
                item.item_code = passport_no
                item.is_non_gst = "0"
            item.item_name = candidate_name
            item.item_group = "Recruitment"
            item.stock_uom = "Nos"
            item.qty = "1"
            item.gst_hsn_code='9985'
            item.is_stock_item = "0"
            item.include_item_in_manufacturing = "0"
            item.description = customer
            item.append("item_defaults", {
                            "company":"TeamPRO HR & IT Services Pvt. Ltd."
                        })
            item.append("customer_items", {
                            "customer_name":customer,
                            "ref_code":contact
                        })
            item.insert()
            item.save(ignore_permissions=True)

            if territory == 'India' or parent_territory == 'India':
                if payment != "Candidate":
                    so = frappe.new_doc("Sales Order")
                    so.naming_series = "REC-I-2021"
                    so.customer = customer
                    so.account_manager = account_manager,
                    so.delivery_manager = delivery_manager,
                    so.project = project
                    so.task = task
                    # so.supplier = supplier
                    so.currency = currency
                    so.transaction_date = today()
                    so.delivery_date = expected_doj
                    so.order_type = "Sales"
                    so.payment_type = "Candidate"
                    so.passport_no = passport_no
                    so.company = "TeamPRO HR & IT Services Pvt. Ltd."
                    so.territory = territory
                    so.passport_no = passport_no
                    so.append("items", {
                        "item_code": item.item_code,
                        "item_name": item.item_name,
                        "payment_type": "Candidate",
                        "description": item.description,
                        "uom": item.stock_uom,
                        "is_stock_item" : "0",
                        "passport_no" : passport_no,
                        "delivery_date" : expected_doj,
                        "qty":"1",
                        "rate": client_sc
                    })                    
                    if territory == 'Tamil Nadu':
                        so.append("taxes", {
                            "charge_type":"On Net Total",
                            "account_head":"CGST @ 9% - THIS",
                            "description":"CGST @ 9%",
                            "rate":"9"
                        })
                        so.append("taxes", {
                            "charge_type":"On Net Total",
                            "account_head":"SGST @ 9% - THIS",
                            "description":"SGST @ 9%",
                            "rate":"9"
                        })
                    else:
                        so.append("taxes", {
                            "charge_type":"On Net Total",
                            "account_head":"IGST @ 18% - THIS",
                            "description":"IGST @ 18%",
                            "rate":"18"
                        })
                    so.insert()
                    so.save(ignore_permissions=True)
                    so.submit()

            if territory != 'India':
                if payment != "Candidate":
                    so = frappe.new_doc("Sales Order")
                    so.naming_series = "REC-O-2021"
                    so.customer = customer
                    so.account_manager = account_manager,
                    so.delivery_manager = delivery_manager,
                    so.project = project
                    so.task = task
                    # so.supplier = supplier
                    so.transaction_date = today()
                    so.currency = currency
                    so.delivery_date = expected_doj
                    so.order_type = "Sales"
                    so.payment_type = "Candidate"
                    so.passport_no = passport_no
                    so.company = "TeamPRO HR & IT Services Pvt. Ltd."
                    so.territory = territory
                    so.passport_no = passport_no
                    so.append("items", {
                        "item_code": item.item_code,
                        "item_name": item.item_name,
                        "payment_type": "Candidate",
                        "description": item.description,
                        "uom": item.stock_uom,
                        "is_stock_item" : "0",
                        "passport_no" : passport_no,
                        "delivery_date" : expected_doj,
                        "qty":"1",
                        "rate": client_sc
                    })
                    so.insert()
                    so.save(ignore_permissions=True)
                    so.submit()
            frappe.set_value('Closure',closure,'so_created',1)
            frappe.set_value('Closure',closure,'so_confirmed_date',today())
            total = cint(client_sc)

            return "Sales Order Created for Total value {0}".format(frappe.bold(fmt_money(total, currency='INR')))


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
        #                 self.status = 'Offer Letter'
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
        #                 self.status = 'Offer Letter'
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
        #                 self.status = 'Offer Letter'
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
        #                 self.status = 'Offer Letter'
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
        #                 self.status = 'Offer Letter'
        #                 self.offer_letter_date = today()
        #         else:
        #             self.status = 'Sales Order'
        #             self.status_updated_on = today()
        #     else:
        #         self.status = 'PSL'
        #         self.status = 'Sales Order'
        #         self.status_updated_on = today()