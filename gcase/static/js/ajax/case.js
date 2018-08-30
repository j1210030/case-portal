

/**
 * Set Client Contact List According to Client Id
 */
function setComponents4Products(pid, componentId, emptyTxt, compId) {
	var component_url = '/component/getbyproduct';
	if ( pid == '') {
		return false;
	}

	$("#"+componentId).empty();
	
	//if (selectedId || contactPerson) {
		$("#"+componentId).prepend("<option value=''>" + emptyTxt + "</option>");
	///} else {
		//$("#id_client_contact").prepend("<option value='' selected='selected'>" + emptyTxt + "</option>");
	//}
	
	$('#component_loading').show();
	
	$.ajax({
		url : component_url,
		data : {
			pid : pid 
		},
		type : 'GET',
		cache : false,
		dataType : 'json',
		contentType : 'application/json',
		success : function(response) {
			$('#component_loading').hide();
			response = JSON.stringify(response);
			//console.log(' Response: ' + response);
			data = '';
			try {
				data = $.parseJSON(response);
			} catch (ex) {
				console.log(" JSON error: " + ex);
			}
			if (data.components.length == 0) {
				$('#caseSubmit').attr("disabled", true);
				return false;
			} else {
				$('#caseSubmit').attr("disabled", false);
			}
			$.each(data.components, function(i, item) {
				
				var option = $('<option/>');
				option.attr({
					'value' : item.id
				}).text(item.name);

				//if (contactPerson != '') {
					//if (value_text == contactPerson) {
						//option.attr('selected', 'selected');
					//}
				//}

				$('#' + componentId).append(option);

			});
			
			if ( compId != ''){
				$('#' + componentId).val(compId);
			}
		},
		error : function(jqXHR, textStatus, errorThrown) {
			alert("Error Encountered!!!")
		}
	});
}


function setPartnersByLang(hl, selectedId) {
	var partner_url = '/partner/get_json';
	if ( hl == '') {
		return false;
	}

	$("#id_partner").empty();
	var emptyTxt = "Select";
	
	//if (selectedId || contactPerson) {
		$("#id_partner").prepend("<option value=''>" + emptyTxt + "</option>");
	///} else {
		//$("#id_client_contact").prepend("<option value='' selected='selected'>" + emptyTxt + "</option>");
	//}
	
	$('#partner_loading').show();
	
	$.ajax({
		url : partner_url,
		data : {
			hl : hl 
		},
		type : 'GET',
		cache : false,
		dataType : 'json',
		contentType : 'application/json',
		success : function(response) {
			$('#partner_loading').hide();
			response = JSON.stringify(response);
			//console.log(' Response: ' + response);
			data = '';
			try {
				data = $.parseJSON(response);
			} catch (ex) {
				console.log(" JSON error: " + ex);
			}
			if (data.partner_list.length == 0) {
				$('#caseSubmit').attr("disabled", true);
				$('#partner_notfound_msg').show();
				$('#partner_select_div').hide();
				return false;
			} else {
				$('#partner_notfound_msg').hide();
				$('#partner_select_div').show();
				$('#caseSubmit').attr("disabled", false);
			}
			$.each(data.partner_list, function(i, item) {
				
				var pText = item.name_english + '(' + item.name_locale + ')';
				var option = $('<option/>');
				option.attr({
					'value' : item.id
				}).text(item.value);

				//if (contactPerson != '') {
					//if (value_text == contactPerson) {
						//option.attr('selected', 'selected');
					//}
				//}

				$('#id_partner').append(option);
			});
			if ( selectedId != ''){
				$('#id_partner').val(selectedId);
			}

		},
		error : function(jqXHR, textStatus, errorThrown) {
			alert("Error Encountered!!!")
		}
	});
}

function getWeekByDate(incoming_dt) {
	var week_url = '/case/getweek';
	if ( incoming_dt == '') {
		return false;
	}

	$("#incoming_date_id").empty();
	
	
	$.ajax({
		url : week_url,
		data : {
			incoming_dt : incoming_dt 
		},
		type : 'GET',
		cache : false,
		dataType : 'json',
		contentType : 'application/json',
		success : function(response) {
			$('#component_loading').hide();
			response = JSON.stringify(response);
			console.log(' Response: ' + response);
			data = '';
			try {
				data = $.parseJSON(response);
			} catch (ex) {
				console.log(" JSON error: " + ex);
			}
			
			console.log(' Data ' + data.status); 
			
			if (data.status == 'ERROR') {
				$('#caseSubmitBtn').attr("disabled", true);
				$('#week-span').removeClass("text-success");
				$('#week-span').addClass("text-danger");
				$('#week-span').html('<i>' + data.message + '</i>');
				$('#week-span').show();
				return false;
			} else {
				$('#caseSubmitBtn').attr("disabled", false);
				$('#week-span').removeClass("text-danger");
				$('#week-span').addClass("text-success");
				$('#week-span').html('<i>Week: ' + data.week + '</i>');
				$('#week-span').show();
				$('#id_week').val(data.week);
			}
		},
		error : function(jqXHR, textStatus, errorThrown) {
			alert("Error Encountered!!!")
		}
	});
}

function isCaseExist(case_id){
	
	var url = '/case/check_id';
	if ( case_id == '') {
		return false;
	}
	
	$.ajax({
		url : url,
		data : {
			case_id : case_id 
		},
		type : 'GET',
		cache : false,
		dataType : 'json',
		contentType : 'application/json',
		success : function(response) {
			$('#component_loading').hide();
			response = JSON.stringify(response);
			console.log(' Response: ' + response);
			data = '';
			try {
				data = $.parseJSON(response);
			} catch (ex) {
				console.log(" JSON error: " + ex);
			}
			
			console.log(' Data ' + data.status); 
			
			if (data.status == 'EXISTS') {
				$('#caseSubmitBtn').attr("disabled", true);
				$('#case_already_exist_msg').show();
				return true;
			} else if ( data.status == 'OK') {
				$('#case_already_exist_msg').hide();
				$('#caseSubmitBtn').attr("disabled", false);
				return false;
			}
		},
		error : function(jqXHR, textStatus, errorThrown) {
			alert("Error Encountered!!!")
		}
	});
}

function setPartner2Case(object,case_id,locale){
	
	console.log('  case id is : ' + case_id);
	
	partner_id = $("#partner-" + case_id + " option:selected").val();
	console.log('partner id: ' + partner_id );
	
	
	$.ajax({
		url : '/case/set_partner',
		data : {
			cid : case_id,
			hl : locale,
			partner_id : partner_id
		},
		type : 'GET',
		cache : false,
		dataType : 'json',
		contentType : 'application/json',
		success : function(response) {
			$('#component_loading').hide();
			response = JSON.stringify(response);
			console.log(' Response: ' + response);
			data = '';
			try {
				data = $.parseJSON(response);
			} catch (ex) {
				console.log(" JSON error: " + ex);
			}
			if (data.status == 'ok') {
				alert('Partner is set successfully.')
				return false;
			} else {
				alert('Failed to set partner!')
			}
		},
		error : function(jqXHR, textStatus, errorThrown) {
			alert("Error Encountered!!!")
		}
	});
	
}

function setSoDate2Case(object,case_id,locale){
	
	console.log('  case id is : ' + case_id + 'locale: ' + locale);
	so_date = object.value.trim();
	console.log('date id: ' + so_date);
	
	if ( !isValidDate(so_date)){
		alert('Enter a valid date in correct format!!');
		return false;
	}
	
	$.ajax({
		url : '/case/set_so_date',
		data : {
			cid : case_id,
			hl : locale,
			so_date : so_date
		},
		type : 'GET',
		cache : false,
		dataType : 'json',
		contentType : 'application/json',
		success : function(response) {
			response = JSON.stringify(response);
			console.log(' Response: ' + response);
			data = '';
			try {
				data = $.parseJSON(response);
			} catch (ex) {
				console.log(" JSON error: " + ex);
			}
			if (data.status == 'ok') {
				$('#so_date-' + case_id).hide();
				$('#so_date_span-' + case_id).text(so_date);
				return false;
			} else if ( data.status == 'invalid_date')  {
				alert('Not a correct date!!')
			}else{
				alert('Failed to save data !!')
			}
		},
		error : function(jqXHR, textStatus, errorThrown) {
			alert("Error Encountered!!!")
		}
	});
	
}

function setBuganizer2Case(object, case_id,locale){
	
	console.log('  case id is : ' + case_id + 'locale: ' + locale);
	buganizer_num = object.value.trim();
	console.log('date id: ' + buganizer_num);
	
	if ( !$.isNumeric( buganizer_num )){
		alert('Enter a valid number!!');
		return false;
	}
	
	$.ajax({
		url : '/case/set_buganizer',
		data : {
			cid : case_id,
			hl : locale,
			buganizer : buganizer_num
		},
		type : 'GET',
		cache : false,
		dataType : 'json',
		contentType : 'application/json',
		success : function(response) {
			response = JSON.stringify(response);
			console.log(' Response: ' + response);
			data = '';
			try {
				data = $.parseJSON(response);
			} catch (ex) {
				console.log(" JSON error: " + ex);
			}
			if (data.status == 'ok') {
				$('#buganizer-' + case_id).hide();
				$('#buganizer_span-' + case_id).text(buganizer_num);
				return false; 
			}else{
				alert('Failed to save data !!')
			}
		},
		error : function(jqXHR, textStatus, errorThrown) {
			alert("Error Encountered!!!")
		}
	});
	
}
	



