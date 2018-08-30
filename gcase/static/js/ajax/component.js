$(document).ready(function() {
	
});


function addEditComponent(pid, pname,cname,status,cid){
	
	$('#unqNameMsg').hide();
			
	console.log(' pid: ' + pid + 'Name: ' + pname + ' cname: ' + cname + ' Status: ' + status + ' cid: ' + cid);
	if ( status ){
		$('#id_active_0').prop("checked", true);
	}else{
		$('#id_active_1').prop("checked", true);
	}
	$('#productName').empty();
	$('#productName').text(pname);
	
	$('#cname').val('');
	if ( cname != ''){
		$('#cname').val(cname);
	}
	if ( cid != ''){
		$('#cid').val('');
		$('#cid').val(cid);
		$('#formComponent').attr('action', '/component/edit');
	}else{
		$('#formComponent').attr('action', '/component/add');
	}
	$("#componentAddEditModal").modal({show: true});
}

function checkName(){
	
	dispElm= "#unqNameMsg";
	var cname = $("#cname").val().trim();
	
	if( cname == '' ){
		$('#saveBtn').attr('disabled','disabled');
		return false;
	}else{
		$('#saveBtn').removeAttr('disabled');
	}
	var pid = $("#pid").val();
	var cid = $("#cid").val();
	
	console.log('Name to check: ' + cname  + ' pid: ' + pid  + ' cid: ' + cid ); 
	var stat = true;
	$.get("/component/ajax_check_name", {
				pid:pid,
				cid:cid,
				cname:cname
		}, function(response) { 
			response = JSON.stringify(response);
			console.log('Response:' + response );
			var obj = jQuery.parseJSON(response);
			if(obj.status == 'SUCCESS' && obj.allowed == '-1'){
				$(dispElm).show();
				//$('#saveBtn').attr('disabled','disabled');
			}else{
				$(dispElm).hide();
				//$('#saveBtn').removeAttr('disabled');
				$( "#formComponent" ).submit();
			}
		});
	return false;
}