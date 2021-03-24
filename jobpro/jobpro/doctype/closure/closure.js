// Copyright (c) 2020, teamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Closure', {

	payment: function (frm) {
		if (frm.doc.payment == 'Client') {
			frm.set_value('candidate_service_charge', 0)
			frm.set_value('candidate_dec', 0)
			frm.set_value('candidate_si', 0)
		}
		if (frm.doc.payment == 'Candidate') {
			frm.set_value('client_service_charge', 0)
			frm.set_value('client_dec', 0)
			frm.set_value('client_si', 0)
		}
		if (frm.doc.payment == 'Both') {
			frm.set_value('candidate_service_charge', 0)
			frm.set_value('candidate_dec', 0)
			frm.set_value('candidate_si', 0)
			frm.set_value('client_service_charge', 0)
			frm.set_value('client_dec', 0)
			frm.set_value('client_si', 0)
		}
	},
	onload: function (frm) {
		cur_frm.set_df_property("premedical_section", "hidden", 1);
		cur_frm.set_df_property("certificate_attestation_section", "hidden", 1);
		cur_frm.set_df_property("visa_section", "hidden", 1);
		cur_frm.set_df_property("final_medical_section", "hidden", 1);
		cur_frm.set_df_property("visa_stamping_section", "hidden", 1);
		cur_frm.set_df_property("section_break_79", "hidden", 1);
		cur_frm.set_df_property("ticket_section", "hidden", 1);		
	},

	refresh: function (frm) {
		if (frm.doc.status == 'Onboarding') {
			frm.add_custom_button(__("Onboard"),
				function () {
					frm.set_value("status", "Onboarded")
				}
			).addClass('btn btn-success');
			frm.add_custom_button(__("Drop"),
				function () {
					frm.set_value("status", "Dropped")
				}
			).addClass('btn btn-primary');
		}
		frm.toggle_display("part_payment_collection", frm.doc.so_created == 1)
		if (frm.doc.sa_owner) {
			frm.add_custom_button(__("SA Candidate"),function(){
				frappe.msgprint(
					"SA ID : "+frm.doc.sa_owner,
					"SA Name : "+frm.doc.sa_name
				)
			}).addClass('btn btn-success');
		}
		if (frm.doc.ecr_status == "ECR") {
			frm.add_custom_button(__("ECR")).addClass('btn btn-success');
		}
		frm.refresh_fields();
		if (!frm.doc.so_created) {
			if(frm.doc.status == "Sales Order") {
				frm.set_df_property("ob_custodian", "reqd", 1);
				frm.set_df_property("passport_no", "reqd", 1);
				frm.set_df_property("offer_letter", "reqd", 1);
				frm.set_df_property("sol", "reqd", 1);
				frm.set_df_property("photo", "reqd", 1);
				frm.set_df_property("ecr_status", "reqd", 1);
				frm.set_df_property("passport", "reqd", 1);
				frm.set_df_property("place_of_issue", "reqd", 1);
				frm.set_df_property("issued_date", "reqd", 1);
				frm.set_df_property("expiry_date", "reqd", 1);
			}
			if (frm.doc.mobile && frm.doc.candidate_owner && frm.doc.posting_date && frm.doc.payment &&
				 frm.doc.expected_doj && frm.doc.customer && frm.doc.project && frm.doc.territory && frm.doc.task && frm.doc.date_of_birth && frm.doc.irf
				  ) {
					// if( frm.doc.ob_custodian && frm.doc.passport_no &&  frm.doc.offer_letter && frm.doc.sol && frm.doc.photo
					// 	frm.doc.ecr_status && frm.doc.passport && frm.doc.place_of_issue && frm.doc.issued_date && frm.doc.expiry_date ){

				cur_frm.add_custom_button(__("Confirm Sale Order"), function () {
					if (frm.doc.payment == 'Client' && frm.doc.client_si <= 0) {
						msgprint("Please Enter Client Service Charge Value")
					} else if (frm.doc.payment == 'Candidate' && frm.doc.candidate_si <= 0) {
						msgprint("Please Enter Candidate Service Charge Value")
					} else if (frm.doc.payment == 'Both' && frm.doc.client_si <= 0 && frm.doc.candidate_si <= 0) {
						msgprint("Please Enter Client and Candidate Service Charge Value")
					} else {
						frappe.confirm('Did you verified the payment terms?',
							function () {
								frappe.call({
									method: "jobpro.jobpro.doctype.closure.closure.create_sale_order",
									freeze: true,
									freeze_message: __("Creating Sales Order..."),
									args: {
										closure: cur_frm.doc.name,
										project: cur_frm.doc.project,
										customer: cur_frm.doc.customer,
										account_manager: cur_frm.doc.account_manager,
										delivery_manager:cur_frm.doc.candidate_owner,
										task: cur_frm.doc.task,
										candidate_name: cur_frm.doc.given_name,
										contact: cur_frm.doc.mobile,
										payment: cur_frm.doc.payment,
										currency: cur_frm.doc.billing_currency,
										client_sc: cur_frm.doc.client_si || '',
										territory: cur_frm.doc.territory,
										passport_no: cur_frm.doc.passport_no || '',
										expected_doj: cur_frm.doc.expected_doj,
										supplier: cur_frm.doc.sa_owner
									},
									callback: function (r) {

										frappe.db.get_value('Territory', frm.doc.territory, 'parent_territory', (r) => {
											if (r) {
												if (r.parent_territory == 'India') {
													frm.set_value("status", "Onboarded")
												}
												else {
													frm.set_value("status", "Visa")
												}
											}
										});
										frappe.msgprint(__(r.message));
									}
								});

							})
					}
				}).addClass('btn btn-primary');
			// }
			}
		}
		cur_frm.set_df_property("premedical_section", "hidden", 1);
		cur_frm.set_df_property("certificate_attestation_section", "hidden", 1);
		cur_frm.set_df_property("visa_section", "hidden", 1);
		cur_frm.set_df_property("final_medical_section", "hidden", 1);
		cur_frm.set_df_property("visa_stamping_section", "hidden", 1);
		cur_frm.set_df_property("section_break_79", "hidden", 1);
		cur_frm.set_df_property("ticket_section", "hidden", 1);
		if(frm.doc.territory == "Qatar"){
			if(frm.doc.sol){
				cur_frm.set_df_property("premedical_section", "hidden", 0);
			}
			if(frm.doc.premedical){
				cur_frm.set_df_property("certificate_attestation_section", "hidden", 0);
			}
			if(frm.doc.certificate_attestation){
				cur_frm.set_df_property("visa_section", "hidden", 0);
			}
			if(frm.doc.visa){
				cur_frm.set_df_property("final_medical_section", "hidden", 0);
			}
			if(frm.doc.final_medical){
				cur_frm.set_df_property("section_break_79", "hidden", 0);
				// cur_frm.set_df_property("visa_stamping_section", "hidden", 0);
			}
			if(!frm.doc.certificate_attestation){
				cur_frm.set_df_property("visa_section", "hidden", 0);
			}
			// if(frm.doc.visa_stamping){
			// 	cur_frm.set_df_property("section_break_79", "hidden", 0);
			// }
			if(frm.doc.emigration){
				cur_frm.set_df_property("ticket_section", "hidden", 0);
			}
		}
		if(frm.doc.territory == "UAE" && frm.doc.visa_state == "Abu Dhabi"){
			if(frm.doc.sol){
				cur_frm.set_df_property("premedical_section", "hidden", 0);
			}
			if(frm.doc.premedical){
				cur_frm.set_df_property("certificate_attestation_section", "hidden", 0);
			}
			if(frm.doc.certificate_attestation){
				cur_frm.set_df_property("visa_section", "hidden", 0);
			}
			if(!frm.doc.certificate_attestation){
				cur_frm.set_df_property("visa_section", "hidden", 0);
			}
			if(frm.doc.visa){
				cur_frm.set_df_property("final_medical_section", "hidden", 0);
			}
			if(frm.doc.final_medical){
				cur_frm.set_df_property("visa_stamping_section", "hidden", 0);
			}
			if(frm.doc.visa_stamping){
				cur_frm.set_df_property("section_break_79", "hidden", 0);
			}
			if(frm.doc.emigration){
				cur_frm.set_df_property("ticket_section", "hidden", 0);
			}
		}
		if(frm.doc.territory == "UAE" && frm.doc.visa_state == "Dubai"){
			if(frm.doc.sol){
				cur_frm.set_df_property("premedical_section", "hidden", 0);
			}
			if(frm.doc.premedical){
				cur_frm.set_df_property("certificate_attestation_section", "hidden", 0);
			}
			if(frm.doc.certificate_attestation){
				cur_frm.set_df_property("visa_section", "hidden", 0);
			}
			if(!frm.doc.certificate_attestation){
				cur_frm.set_df_property("visa_section", "hidden", 0);
			}
			if(frm.doc.visa){
				cur_frm.set_df_property("section_break_79", "hidden", 0);
				// cur_frm.set_df_property("final_medical_section", "hidden", 0);
			}
			// if(frm.doc.final_medical){
			// 	cur_frm.set_df_property("visa_stamping_section", "hidden", 0);
			// }
			// if(frm.doc.visa_stamping){
			// 	cur_frm.set_df_property("section_break_79", "hidden", 0);
			// }
			if(frm.doc.emigration){
				cur_frm.set_df_property("ticket_section", "hidden", 0);
			}
		}
		if(frm.doc.territory == "Oman"){
			if(frm.doc.sol){
				cur_frm.set_df_property("premedical_section", "hidden", 0);
			}
			if(frm.doc.premedical){
				cur_frm.set_df_property("certificate_attestation_section", "hidden", 0);
			}
			if(frm.doc.certificate_attestation){
				cur_frm.set_df_property("visa_section", "hidden", 0);
			}
			if(!frm.doc.certificate_attestation){
				cur_frm.set_df_property("visa_section", "hidden", 0);
			}
			if(frm.doc.visa){
				cur_frm.set_df_property("section_break_79", "hidden", 0);
				// cur_frm.set_df_property("final_medical_section", "hidden", 0);
			}
			// if(frm.doc.final_medical){
			// cur_frm.set_df_property("visa_stamping_section", "hidden", 1);
			// }
			// if(frm.doc.visa_stamping){
			// 	cur_frm.set_df_property("section_break_79", "hidden", 0);
			// }
			if(frm.doc.emigration){
				cur_frm.set_df_property("ticket_section", "hidden", 0);
			}
		}
		if(frm.doc.territory == "Kuwait"){
			if(frm.doc.sol){
				cur_frm.set_df_property("premedical_section", "hidden", 0);
			}
			if(frm.doc.premedical){
				cur_frm.set_df_property("certificate_attestation_section", "hidden", 0);
			}
			if(frm.doc.certificate_attestation){
				cur_frm.set_df_property("visa_section", "hidden", 0);
			}
			if(!frm.doc.certificate_attestation){
				cur_frm.set_df_property("visa_section", "hidden", 0);
			}
			if(frm.doc.visa){
				cur_frm.set_df_property("final_medical_section", "hidden", 0);
			}
			if(frm.doc.final_medical){
				cur_frm.set_df_property("visa_stamping_section", "hidden", 0);
			}
			if(frm.doc.visa_stamping){
				cur_frm.set_df_property("section_break_79", "hidden", 0);
			}
			if(frm.doc.emigration){
				cur_frm.set_df_property("ticket_section", "hidden", 0);
			}
		}
		if(frm.doc.territory == 'Dammam','Jeddah','Riyadh' || frm.doc.territory == "KSA"){
			if(frm.doc.sol){
				cur_frm.set_df_property("certificate_attestation_section", "hidden", 0);
				// cur_frm.set_df_property("premedical_section", "hidden", 0);
			}
			// if(frm.doc.premedical){
			// 	cur_frm.set_df_property("certificate_attestation_section", "hidden", 0);
			// }
			if(frm.doc.certificate_attestation){
				cur_frm.set_df_property("visa_section", "hidden", 0);
			}
			if(!frm.doc.certificate_attestation){
				cur_frm.set_df_property("visa_section", "hidden", 0);
			}
			if(frm.doc.visa){
				cur_frm.set_df_property("final_medical_section", "hidden", 0);
			}
			if(frm.doc.final_medical){
				cur_frm.set_df_property("visa_stamping_section", "hidden", 0);
			}
			if(frm.doc.visa_stamping){
				cur_frm.set_df_property("section_break_79", "hidden", 0);
			}
			if(frm.doc.emigration){
				cur_frm.set_df_property("ticket_section", "hidden", 0);
			}
		}
		if(frm.doc.territory == "Bahrain"){
			if(frm.doc.sol){
				cur_frm.set_df_property("premedical_section", "hidden", 0);
			}
			if(frm.doc.premedical){
				cur_frm.set_df_property("certificate_attestation_section", "hidden", 0);
			}
			if(frm.doc.certificate_attestation){
				cur_frm.set_df_property("visa_section", "hidden", 0);
			}
			if(!frm.doc.certificate_attestation){
				cur_frm.set_df_property("visa_section", "hidden", 0);
			}
			if(frm.doc.visa){
				cur_frm.set_df_property("section_break_79", "hidden", 0);
				// cur_frm.set_df_property("final_medical_section", "hidden", 0);
			}
			// if(frm.doc.final_medical){
			// 	cur_frm.set_df_property("visa_stamping_section", "hidden", 0);
			// }
			// if(frm.doc.visa_stamping){
			// 	cur_frm.set_df_property("section_break_79", "hidden", 0);
			// }
			if(frm.doc.emigration){
				cur_frm.set_df_property("ticket_section", "hidden", 0);
			}
		}

	},
	
	passport_no: function (frm) {
		var regex = /[^0-9A-Za-z]/g;
		if (regex.test(frm.doc.passport_no) === true) {
			frappe.msgprint(__("Passport No.: Only letters and numbers are allowed."));
			frappe.validated = false;
		}
		var len = frm.doc.passport_no
	    if(len.length < 8){
			frappe.throw("Passport Number must be minimum 8 digits")
			frappe.validated = false;
	    }
	},
	mobile: function (frm) {
		var regex = /[^0-9]/g;
		if (regex.test(frm.doc.passport_no) === true) {
			frappe.msgprint(__("Mobile No.: Only Numbers are allowed."));
			frappe.validated = false;
		}
		var len = frm.doc.mobile
	    if(len.length < 10){
			frappe.throw("Mobile Number must be minimum 10 digits")
			frappe.validated = false;
	    }
	},
	validate(frm) {
		// if(frm.doc.territory != India)
		if( frm.doc.client_service_charge <= 0 &&frm.doc.candidate_service_charge <= 0 && frm.doc.client_dec <= 0 && frm.doc.candidate_dec <= 0){
			frappe.msgprint(__("Atleast one DEC/SI has to be filled"));
			frappe.validated = false;
		}
		if (frm.doc.payment == 'Client') {
			var client_service_charge = frm.doc.client_si - frm.doc.client_dec
			frm.set_value('client_service_charge', client_service_charge);
		if (frm.doc.client_dec > frm.doc.client_service_charge) {
			frappe.msgprint(__("DEC Cannot be greated than SI in Client Payment"));
			frappe.validated = false;
		}
	}
		if(frm.doc.payment=="Candidate"){
			var candidate_service_charge = frm.doc.candidate_si - frm.doc.candidate_dec
			frm.set_value('candidate_service_charge', candidate_service_charge);
		if (frm.doc.candidate_dec > frm.doc.candidate_service_charge) {
			frappe.msgprint(__("DEC Cannot be greated than SI in Candidate Payment"));
			frappe.validated = false;
		}
	}
		// if (frm.doc.payment == 'Client') {
		// 	var client_si = frm.doc.client_service_charge + frm.doc.client_dec
		// 	frm.set_value('client_si', client_si);
		// }
		
		// if (frm.doc.payment == 'Candidate') {
		// 	var candidate_si = frm.doc.candidate_service_charge + frm.doc.candidate_dec
		// 	frm.set_value('candidate_si', candidate_si);
		// }
		if (frm.doc.payment == 'Both') {
			var client_service_charge = frm.doc.client_si - frm.doc.client_dec
			frm.set_value('client_service_charge', client_service_charge);
			var candidate_service_charge = frm.doc.candidate_si - frm.doc.candidate_dec
			frm.set_value('candidate_service_charge', candidate_service_charge);
		}
		var total_si = frm.doc.client_service_charge + frm.doc.candidate_service_charge + frm.doc.client_dec + frm.doc.candidate_dec;
		var sum = 0;
		var candidate_si = frm.doc.candidate_si;
		frm.set_value("outstanding_amount", candidate_si)
		// frm.set_value("outstanding_amount", sum)
		if (frm.doc.part_payment_collection) {
			$.each(frm.doc.part_payment_collection, function (i, item) {
				sum += item.amount;
			})
			if (sum > total_si) {
				frappe.msgprint(__("Total Collection should not be greater than SI"));
				frappe.validated = false;
			}
			if (sum == 0) {
				frm.set_value("collection_status", "YTS")
			}
			else if (sum >= frm.doc.candidate_si) {
				var amount = frm.doc.candidate_si - sum
				frm.set_value("outstanding_amount", amount)
				frm.set_value("collection_status", "PAID")
			}
			else {
				var amount = frm.doc.candidate_si - sum
				frm.set_value("outstanding_amount", amount)
				frm.set_value("collection_status", "Partially Paid")
			}
		}
	},
});
