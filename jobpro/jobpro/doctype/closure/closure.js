// Copyright (c) 2020, teamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Closure', {
	
	// ticket(frm){
	   
	
	// },
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
		var so_created = 'No'
		if(frm.doc.so_created){
			so_created = 'Yes'
		}
		$(frm.fields_dict.html_1.wrapper).html(`
		<table border="1" width="100%">
    <tbody><tr style="">
        <td style = 'background-color:blue;color:white'><b>Document Status</b></td>
        <td style = 'background-color:blue;color:white'><b>Sales Order Status</b></td>
		<td style = 'background-color:blue;color:white'><b>Visa Status</b></td>
        <td style = 'background-color:blue;color:white'><b>Collection Priority</b></td>
        <td style = 'background-color:blue;color:white'><b>Outstanding</b></td>
    </tr>
    <tr>
        <td style = 'color:orange'><b>${frm.doc.status}</b></td>
        <td style = 'color:orange'><b>${so_created}</b></td>
        <td style = 'color:orange'><b>${frm.doc.visa_status}</b></td>
        <td style = 'color:orange'><b>${frm.doc.collection_priority}</b></td>
        <td style = 'color:orange'><b>${frm.doc.outstanding_amount}</b></td>
    </tr>
</tbody></table>`);
		cur_frm.set_df_property("premedical_section", "hidden", 1);
		// cur_frm.set_df_property("pcc_section", "hidden", 1);
		cur_frm.set_df_property("certificate_attestation_section", "hidden", 1);
		// cur_frm.set_df_property("visa_section", "hidden", 1);
		cur_frm.set_df_property("final_medical_section", "hidden", 1);
		cur_frm.set_df_property("visa_stamping_section", "hidden", 1);
		cur_frm.set_df_property("section_break_79", "hidden", 1);
		cur_frm.set_df_property("ticket_section", "hidden", 1);
	},
	setup: function(frm) {
		frm.set_query("associate", function() {
			return {
				filters: {
					'customer_group': "Associate"
				}
			}
		});
		frm.set_query("stamping_vendor", function() {
			return {
				filters: {
					'supplier_group': "Visa Stamping"
				}
			}
		});
	},

	refresh: function (frm) {
		if (!frm.doc.so_created) {
			// if (frm.doc.status == "Visa)
			frm.set_intro(__("<h6 style ='color:red'><b>Alert:</b>Further process is Freezed as Sales Order Submmision is Pending.Please submit <b>Sales Order</b> immediately</h6>"))
		}
		
		if (frm.doc.so_created) {
			if(frm.doc.status == 'Onboarding'){
				frm.add_custom_button(__("Onboard"),
			
				function () {
					if(frm.doc.payment=="Candidate" ){
						    if (frm.doc.outstanding_amount > 0 ){
								// frm.set_value("ticket","")
								frappe.throw("Candidate Outstanding amount should be zero")
								frappe.validated = false;
								
						}
						}
					frm.set_value("status", "Onboarded")
				}
			).addClass('btn btn-success');
			}
			
		}
		if (frm.doc.status != 'Dropped'){
			frm.add_custom_button(__("Drop"),
			function () {
				
				let d = new frappe.ui.Dialog({
					title: "Dropped Reason",
					fields :[
						{
						label: 'Reason',
						fieldname: 'reason',
						fieldtype: 'Data'
					},
					{
						label: 'Drop Approved By',
						fieldname: 'drop_approved_by',
						fieldtype: 'Link',
						options:'User'
					}
				],
					primary_action_label: 'Submit',
					primary_action(values) {
						frm.set_value("drop_reason",values.reason)
						frm.set_value("drop_approved_by",values.drop_approved_by)
						d.hide()
						frm.set_value("status", "Dropped")
						frm.save()
						
    				}
				})
				d.show()

			}
			
		).addClass('btn btn-primary');
		}

		if (frm.doc.status == "Dropped"){
			frm.add_custom_button(__("Re-Open"),
			function () {
				frm.set_value("status", "PSL")
				frm.save()
			}
		).addClass('btn btn-primary');
		}
		
		
		// frm.toggle_display("part_payment_collection", frm.doc.so_created == 1)
		if (frm.doc.sa_owner) {
			frm.add_custom_button(__("SA Candidate"), function () {
				frappe.msgprint(
					"SA ID : " + frm.doc.sa_owner,
					"SA Name : " + frm.doc.sa_name
				)
			}).addClass('btn btn-success');
		}
		if (frm.doc.ecr_status == "ECR") {
			frm.add_custom_button(__("ECR")).addClass('btn btn-success');
		}
		frm.refresh_fields();
		if (!frm.doc.so_created) {
			if (frm.doc.status == "Sales Order") {
				frappe.db.get_value('Territory', frm.doc.territory, 'parent_territory', (r) => {
					if (r) {
						if (r.parent_territory != 'India') {
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

					}
				});

			}
			if (frm.doc.status != "PSL") {
				// if (frm.doc.mobile && frm.doc.candidate_owner && frm.doc.posting_date && frm.doc.payment &&
				// 	 frm.doc.expected_doj && frm.doc.customer && frm.doc.project && frm.doc.territory && frm.doc.task && frm.doc.date_of_birth && frm.doc.irf
				// 	  ) {
				// if( frm.doc.ob_custodian && frm.doc.passport_no &&  frm.doc.offer_letter && frm.doc.sol && frm.doc.photo
				// 	frm.doc.ecr_status && frm.doc.passport && frm.doc.place_of_issue && frm.doc.issued_date && frm.doc.expiry_date ){


				cur_frm.add_custom_button(__("Sale Order"), function () {
					if (frm.doc.payment == 'Client' && frm.doc.client_si <= 0) {
						msgprint("Please Enter Client Service Charge Value")
					} else if (frm.doc.payment == 'Candidate' && frm.doc.candidate_si <= 0) {
						msgprint("Please Enter Candidate Service Charge Value")
					} else if (frm.doc.payment == 'Associate' && frm.doc.associate_si <= 0) {
						msgprint("Please Enter Associate Service Charge Value")
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
										reference_customer_: cur_frm.doc.customer,
										account_manager: cur_frm.doc.account_manager,
										delivery_manager: cur_frm.doc.candidate_owner ||'',
										task: cur_frm.doc.task,
										candidate_name: cur_frm.doc.given_name,
										contact: cur_frm.doc.mobile,
										payment: cur_frm.doc.payment,
										billing_currency: cur_frm.doc.billing_currency,
										client_sc: cur_frm.doc.client_sc || '',
										candidate_dec: cur_frm.doc.candidate_dec,
										candidate_sc: cur_frm.doc.candidate_sc || '',
										territory: cur_frm.doc.territory,
										passport_no: cur_frm.doc.passport_no || '',
										candidate_owner: cur_frm.doc.candidate_owner||'' ,
										sa_id: cur_frm.doc.sa_id ||'',
										passport_number : cur_frm.doc.passport_no ,
										expected_doj: cur_frm.doc.expected_doj ||'',
										project: cur_frm.doc.project,
										// sa_id: cur_frm.doc.supplier
										supplier: cur_frm.doc.sa_id ||'',
										service:cur_frm.doc.service,
										dec:cur_frm.doc.candidate_dec ||cur_frm.doc.client_dec,
										sc:cur_frm.doc.candidate_sc || cur_frm.doc.client_sc,
										client_si:cur_frm.doc.client_si,
										candidate_si:cur_frm.doc.candidate_si,

										associate: cur_frm.doc.associate || '',
										associate_sc: cur_frm.doc.associate_si || '',
										associate_si:cur_frm.doc.associate_si,


									
										// currency:cur_frm.doc.currency
									},
									callback: function (r) {
										frappe.msgprint(r.message);
										cur_frm.reload_doc();

									}
								});

							})
					}
					cur_frm.set_df_property("so_created", 1);

				}).addClass('btn btn-primary');
				// }
				// }
			}
		}
		// cur_frm.set_df_property("pcc_section", "hidden", 1);
		// cur_frm.set_df_property("moh_section", "hidden", 1);
		cur_frm.set_df_property("premedical_section", "hidden", 1);
		cur_frm.set_df_property("certificate_attestation_section", "hidden", 1);
		// cur_frm.set_df_property("visa_section", "hidden", 1);
		cur_frm.set_df_property("final_medical_section", "hidden", 1);
		cur_frm.set_df_property("visa_stamping_section", "hidden", 1);
		cur_frm.set_df_property("section_break_79", "hidden", 1);
		cur_frm.set_df_property("ticket_section", "hidden", 1);
		// cur_frm.set_df_property("emigration_not_applicable", "hidden", 1);

		if (frm.doc.territory == "Qatar") {
			if (frm.doc.sol) {
				cur_frm.set_df_property("pcc_section", "hidden", 0);
				cur_frm.set_df_property("premedical_section", "hidden", 0);

				// frappe.db.set_value('Closure',doc.name,"pcc_not_applicable",1)

			}
			
			// if (frm.doc.pcc) {
			// 	cur_frm.set_df_property("visa_section", "hidden", 0);
			// }
			// if (frm.doc.premedical) {
			// 	cur_frm.set_df_property("certificate_attestation_section", "hidden", 0);
			// }
			if (frm.doc.certificate_attestation) {
				cur_frm.set_df_property("visa_section", "hidden", 0);
			}
			// if(frm.doc.final_medical){
			// 	cur_frm.set_df_property("visa_section", "hidden", 0);

			// }
			if (frm.doc.visa && frm.doc.so_created == 1) {
				cur_frm.set_df_property("visa_stamping_section", "hidden", 0);
			}
			if (frm.doc.visa_stamping){
				cur_frm.set_df_property("section_break_79", "hidden", 0);
			}
			if (frm.doc.emigration || frm.doc.emigration_not_applicable) {
				cur_frm.set_df_property("ticket_section", "hidden", 0);
				}
			// if (frm.doc.final_medical) {
			// 	cur_frm.set_df_property("section_break_79", "hidden", 0);

		// 	// cur_frm.set_df_property("visa_stamping_section", "hidden", 0);
			// }
			// if (!frm.doc.certificate_attestation) {
			// 	cur_frm.set_df_property("visa_section", "hidden", 0);
			// }
			// if(frm.doc.visa_stamping){
			// 	cur_frm.set_df_property("section_break_79", "hidden", 0);
			// }
			// 
		}
		if (frm.doc.territory == "UAE" && frm.doc.visa_state == "Abudhabi") {
			if (frm.doc.sol) {
				cur_frm.set_df_property("pcc_section", "hidden", 0);
			}
			if (frm.doc.pcc || frm.doc.pcc_not_applicable) {
				cur_frm.set_df_property("visa_section", "hidden", 0);
			}
			if (frm.doc.certificate_attestation) {
				cur_frm.set_df_property("visa_section", "hidden", 0);
			}
			if (!frm.doc.certificate_attestation) {
				cur_frm.set_df_property("visa_section", "hidden", 0);
			}
			if (frm.doc.visa && frm.doc.so_created) {
				cur_frm.set_df_property("final_medical_section", "hidden", 0);
			}
			if (frm.doc.final_medical) {
				cur_frm.set_df_property("visa_stamping_section", "hidden", 0);
			}
			if (frm.doc.visa_stamping) {
				cur_frm.set_df_property("section_break_79", "hidden", 0);
			}
			if (frm.doc.emigration || frm.doc.ecr_status == 'ECNR') {
				cur_frm.set_df_property("ticket_section", "hidden", 0);
			}
		}
		if (frm.doc.territory == "UAE" && frm.doc.visa_state == "Dubai") {
			if (frm.doc.sol) {
				cur_frm.set_df_property("pcc_section", "hidden", 0);
			}
			if(frm.doc.pcc || frm.doc.pcc_not_applicable){
				cur_frm.set_df_property("final_medical_section","hidden",0)
			}
			if (frm.doc.final_medical) {
				cur_frm.set_df_property("visa_section", "hidden", 0);
				cur_frm.set_df_property("section_break_79", "hidden", 0)
			}
			// if (frm.doc.certificate_attestation) {
			// 	cur_frm.set_df_property("visa_section", "hidden", 0);
			// }
			// if (!frm.doc.certificate_attestation) {
			// 	cur_frm.set_df_property("visa_section", "hidden", 0);
			// }
			if (frm.doc.visa || frm.doc.so_created) {
				cur_frm.set_df_property("ticket_section", "hidden", 0);
				// cur_frm.set_df_property("final_medical_section", "hidden", 0);
			}
			if (frm.doc.emigration || frm.doc.ecr_status == 'ECNR') {
				cur_frm.set_df_property("ticket_section", "hidden", 0);
			}
			// if(frm.doc.final_medical){
			// 	cur_frm.set_df_property("visa_stamping_section", "hidden", 0);
			// }
			// if(frm.doc.visa_stamping){
			// 	cur_frm.set_df_property("section_break_79", "hidden", 0);
			// }
			
		}
		if (frm.doc.territory == "Oman") {
			if (frm.doc.sol) {
				cur_frm.set_df_property("pcc_section", "hidden", 0);

			}
			if (frm.doc.pcc || frm.doc.pcc_not_applicable){
				cur_frm.set_df_property("final_medical_section","hidden",0)
			}
			// if (frm.doc.pcc_not_applicable == 1) {
			// 	cur_frm.set_df_property("certificate_attestation_section", "hidden", 0);
			// }
			// if (frm.doc.certificate_attestation) {
			// 	cur_frm.set_df_property("visa_section", "hidden", 0);
			// }
			// if (!frm.doc.certificate_attestation) {
			// 	cur_frm.set_df_property("visa_section", "hidden", 0);
			// }
			if (frm.doc.certificate_attestation) {
				cur_frm.set_df_property("visa_section", "hidden", 0);
			}
			if(frm.doc.visa && frm.doc.so_created){
				cur_frm.set_df_property("section_break_79", "hidden", 0);
				// cur_frm.set_df_property("visa_stamping_section", "hidden", 1);

			}
			// if(frm.doc.visa_stamping){
			// 	cur_frm.set_df_property("section_break_79", "hidden", 0);
			// }
			if (frm.doc.emigration || frm.doc.ecr_status == 'ECNR'|| frm.doc.emigration_not_applicable) {
				cur_frm.set_df_property("ticket_section", "hidden", 0);
			}
		}
		if (frm.doc.territory == "Kuwait") {
			 if (frm.doc.sol) {
			 	cur_frm.set_df_property("premedical_section", "hidden", 0);
			 } 
			// if (frm.doc.premedical || frm.doc.premedical_not_applicable == 1) no{
			// 	cur_frm.set_df_property("pcc_section", "hidden", 0);
			// }
			if (frm.doc.pcc || frm.doc.pcc_not_applicable) {
				cur_frm.set_df_property("certificate_attestation_section", "hidden", 0);
				cur_frm.set_df_property("premedical_section", "hidden", 0);

			}
			// if (frm.doc.premedical_not_applicable || frm.doc.premedical||frm.doc.pcc){
			// 	cur_frm.set_df_property("moh_section", "hidden", 0);

			// }
			if (frm.doc.certificate_attestation) {
				cur_frm.set_df_property("visa_section", "hidden", 0);
			}
			if (frm.doc.visa && frm.doc.so_created == 1) {
				cur_frm.set_df_property("final_medical_section", "hidden", 0);
				// if (frm.doc.so_created){
				// 	cur_frm.set_df_property("final_medical_section", "hidden", 0);

				// }
			}
			if (frm.doc.final_medical) {
				cur_frm.set_df_property("visa_stamping_section", "hidden", 0);
			}
			if (frm.doc.visa_stamping) {
				cur_frm.set_df_property("section_break_79", "hidden", 0);
			}
			if (frm.doc.emigration || frm.doc.ecr_status == 'ECNR' || frm.doc.emigration_not_applicable) {
				cur_frm.set_df_property("ticket_section", "hidden", 0);
			}
		}
		if (frm.doc.territory in[ 'Dammam', 'Jeddah', 'Riyadh'] || frm.doc.territory == "KSA") {
			if (frm.doc.sol) {
				cur_frm.set_df_property("certificate_attestation_section", "hidden", 0);
				// cur_frm.set_df_property("premedical_section", "hidden", 0);
			}
			// if(frm.doc.premedical){
			// 	cur_frm.set_df_property("certificate_attestation_section", "hidden", 0);
			// }
			if (frm.doc.certificate_attestation) {
				cur_frm.set_df_property("visa_section", "hidden", 0);
			}
			if (!frm.doc.certificate_attestation) {
				cur_frm.set_df_property("visa_section", "hidden", 0);
			}
			if (frm.doc.visa) {
				cur_frm.set_df_property("final_medical_section", "hidden", 0);
			}
			if (frm.doc.final_medical) {
				cur_frm.set_df_property("visa_stamping_section", "hidden", 0);
			}
			if (frm.doc.visa_stamping) {
				cur_frm.set_df_property("section_break_79", "hidden", 0);
			}
			if (frm.doc.emigration || frm.doc.ecr_status == 'ECNR' || frm.doc.emigration_not_applicable ){
				cur_frm.set_df_property("ticket_section", "hidden", 0);
			}
		}
		if (frm.doc.territory == "Bahrain") {
			if (frm.doc.sol) {
				// cur_frm.set_df_property("premedical_section", "hidden", 0);
				cur_frm.set_df_property("final_medical_section", "hidden", 0);

			}
			// if (frm.doc.premedical) {
			// 	cur_frm.set_df_property("certificate_attestation_section", "hidden", 0);
			// }
			// if (frm.doc.certificate_attestation) {
			// 	cur_frm.set_df_property("visa_section", "hidden", 0);
			// }
			// if (!frm.doc.certificate_attestation) {
			// 	cur_frm.set_df_property("visa_section", "hidden", 0);
			// }
			if (frm.doc.final_medical){
				cur_frm.set_df_property("visa_section", "hidden", 0);

			}
			if (frm.doc.visa && frm.doc.so_created) {
				cur_frm.set_df_property("section_break_79", "hidden", 0);
				// cur_frm.set_df_property("final_medical_section", "hidden", 0);
			}
			
			// if(frm.doc.final_medical){
			// 	cur_frm.set_df_property("visa_stamping_section", "hidden", 0);
			// }
			// if(frm.doc.visa_stamping){
			// 	cur_frm.set_df_property("section_break_79", "hidden", 0);
			// }
			if (frm.doc.emigration || frm.doc.ecr_status == 'ECNR' || frm.doc.emigration_not_applicable) {
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
		if (len.length < 8) {
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
		if (len.length < 10) {
			frappe.throw("Mobile Number must be minimum 10 digits")
			frappe.validated = false;
		}
	},
	validate(frm) {
		if(frm.doc.territory == 'UAE'){
			frm.set_df_property('visa_state','reqd',1)
		}
		// if(frm.doc.territory != India)
		if (frm.doc.client_service_charge <= 0 && frm.doc.candidate_service_charge <= 0 && frm.doc.associate_service_charge <= 0 && frm.doc.associate_dec <= 0 &&  frm.doc.client_dec <= 0 && frm.doc.candidate_dec <= 0) {
			frappe.msgprint(__("Atleast one DEC/SI has to be filled"));
			frappe.validated = false;
		}
		if (frm.doc.payment == 'Client') {
			var client_service_charge = frm.doc.client_si - frm.doc.client_dec
			frm.set_value('client_service_charge', client_service_charge);
			if (frm.doc.client_dec > frm.doc.client_si) {
				frappe.msgprint(__("DEC Cannot be greater than SI in Client Payment"));
				frappe.validated = false;
			}
		}
		if (frm.doc.payment == 'Associate') {
			var associate_service_charge = frm.doc.associate_si - frm.doc.associate_dec
			frm.set_value('associate_service_charge', associate_service_charge);
			if (frm.doc.associate_dec > frm.doc.associate_service_charge) {
				frappe.msgprint(__("DEC Cannot be greater than SI in Associate Payment"));
				frappe.validated = false;
			}
		}
		if (frm.doc.payment == "Candidate") {
			var candidate_service_charge = frm.doc.candidate_si - frm.doc.candidate_dec
			frm.set_value('candidate_service_charge', candidate_service_charge);
			if (frm.doc.candidate_dec > frm.doc.candidate_si) {
				frappe.msgprint(__("DEC Cannot be greater than SI in Candidate Payment"));
				frappe.validated = false;
			}
		}
		// if(frm.doc.payment=="Candidate" ){
	    //     if (frm.doc.outstanding_amount > 0 ){
		// 		// frm.set_value("ticket","")
		// 		frappe.throw("Candidate Outstanding amount should be zero")
		// 		frappe.validated = false;
				
	    // }
	    // }
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
