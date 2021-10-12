// Copyright (c) 2020, teamPRO and contributors
// For license information, please see license.txt

let calculate_age = function (birth) {
	let ageMS = Date.parse(Date()) - Date.parse(birth);
	let age = new Date();
	age.setTime(ageMS);
	let years = age.getFullYear() - 1970;
	return years
};

frappe.ui.form.on('Candidate', {
	validate:function(frm){
		if(frm.doc.pending_for == "Proposed PSL") {
			frm.set_df_property("customer", "reqd", 1);
			frm.set_df_property("project", "reqd", 1);
			frm.set_df_property("territory", "reqd", 1);
			frm.set_df_property("interview_date", "reqd", 1);
			frm.set_df_property("expected_doj", "reqd", 1);
			frm.set_df_property("task", "reqd", 1);
			frappe.db.get_value('Territory',frm.doc.territory, 'parent_territory', (r) => {
				if (r && r.parent_territory == 'India') {
					frm.set_df_property("passport_number", "reqd", 0);
				}
				else{
					frm.set_df_property("passport_number", "reqd", 1);
				}
			});
		
		}
		else{
			frm.set_df_property("customer", "reqd", 0);
			frm.set_df_property("project", "reqd", 0);
			frm.set_df_property("territory", "reqd", 0);
			frm.set_df_property("task", "reqd", 0);
			frm.set_df_property("passport_number", "reqd", 0);
			frm.set_df_property("expected_doj", "reqd", 0);
			frm.set_df_property("interview_date", "reqd", 0);
		}
	
	// frm.set_value('passport_number',frm.doc.passport_number)
	var highest_qualification = 0;
	var latest_work_experience = 0;
	var currently_working = 0;
	$.each(frm.doc.table_28,function(i,d){
		highest_qualification += d.highest_qualification;
	})
	if(highest_qualification > 1){
		frappe.msgprint(__("Only one highest qualification has to be selected"));
		frappe.validated = false;
	}

	$.each(frm.doc.experience_details,function(i,d){
		if(d.from_date > d.to_date){
			frappe.msgprint(__("From Date cannot be Higher than To Date"));
			frappe.validated = false;
		}
		latest_work_experience += d.latest_work_experience;
	})
	if(latest_work_experience > 1){
		frappe.msgprint(__("Only latest experience has to be selected"));
		frappe.validated = false;
	}

	$.each(frm.doc.experience_details,function(i,d){
		currently_working += d.currently_working;
	})
	if(currently_working > 1){
		frappe.msgprint(__("Only one currently working has to be selected"));
		frappe.validated = false;
	}
	$.each(frm.doc.driving_licence,function(i,d){
		if(d.doi > frappe.datetime.get_today()){
			frappe.msgprint(__("DoI cannot be a Future Date"));
			frappe.validated = false;
		}
		latest_work_experience += d.latest_work_experience;
		if(d.doi > d.doe){
			frappe.msgprint(__("DOE cannot be before DOI"));
			frappe.validated = false;
		}
	})
	var len = frm.doc.mobile_number
	if(frm.doc.mobile_number){
		var regex = /[^0-9]/g;
		if (regex.test(frm.doc.mobile_number) === true){
			frappe.msgprint(__("Mobile No.: Only Numbers are allowed."));
			frappe.validated = false;
		}
	// if(len.length < 10 || len.length > 10){
	// 	frappe.throw("Mobile Number must be 10 digits")
	// 	frappe.validated = false;
	// }
}
	
	if (frm.doc.passport_number){
		var regex = /[^0-9A-Za-z]/g;
	if (regex.test(frm.doc.passport_number) === true){
		frappe.msgprint(__("Passport No.: Only letters and numbers are allowed."));
		frappe.validated = false;
	}
		var len = frm.doc.passport_number
		if(len.length > 8 || len.length < 8){
			frappe.throw("Passport Number must be 8 digits")
			frappe.validated = false;
		}
	}
	
	},
	
	pincode: function(frm) {
		$.ajax({
			url: "https://api.postalpincode.in/pincode/"+frm.doc.pincode,
			type: 'GET',
			dataType: 'json',
			success: function (data, textStatus, xhr) {
				console.log(data[0]['PostOffice'][0])
				cur_frm.set_value("temp_location__district", data[0]['PostOffice'][0]['District'])
				cur_frm.set_value("temp_state", data[0]['PostOffice'][0]['State'])
				cur_frm.refresh_fields();
			}
		});
	},
	issued_date: function(frm){
		var me = new Date(frm.doc.issued_date);
        var expiry_date = new Date(me.getFullYear() + 10, me.getMonth(), me.getDate() - 1)
		frm.set_value("expiry_date", expiry_date)
		if(frm.doc.issued_date > frappe.datetime.nowdate()){
			frappe.throw("Date of Issue Can't be Future Date")
		}
	},

	dob: function(frm){
		if(frm.doc.dob > frappe.datetime.nowdate()){
			frappe.throw("Date of Birth Can't be Future Date")
		}

		var age = calculate_age(frm.doc.dob)
		if (age < 18) {
			frm.set_value('dob','')
			frappe.msgprint({
				title: __('Notification'),
				indicator: 'red',
				message: __("Age cannot be lesser than 18")
			});
			
		}
	},
	
	expected_doj: function(frm){
		if(frm.doc.expected_doj < frappe.datetime.nowdate()){
			frappe.throw("Expected DOJ Can't be Past Date")
		}
	},
	
	alternate_contact: function(frm){
		var regex = /[^0-9]/g;
		if (regex.test(frm.doc.alternate_contact) === true){
			frappe.msgprint(__("Alternate Contact No.: Only Numbers are allowed."));
			frappe.validated = false;
		}
	},
	imo_number: function(frm){
		var regex = /[^0-9]/g;
		if (regex.test(frm.doc.imo_number) === true){
			frappe.msgprint(__("IMO No.: Only Numbers are allowed."));
			frappe.validated = false;
		}
	},
	onload:function(frm){
		frm.set_value('mobile',frm.doc.mobile_number)
	}
});