$(document).ready(function() {
	
	$("#id_id").blur(function() {
		if ( this.value ){
			isCaseExist($.trim(this.value));
		}
	});
	
	
	var selected_product = $('#product').val();
	if ( selected_product != '' ){
		console.log(' Component Id: ' + $('#component').val() + ' ,Selected product: ' + selected_product );
		var comp_id = $('#component').val();
		if ( comp_id != ''){
			setComponents4Products(selected_product,'component','Select',comp_id);
		}
	}
	
	$("#product").on('change', function() {
		
		var pid = this.value ; 
		console.log(' Product id: ' + pid );
		$('#id_component').empty();
		setComponents4Products(pid,'component','Component','');
	});
	
	//$('#id_component').empty();
	//$("#id_component").prepend("<option value=''>" + 'Select' + "</option>");
	
	// Get week by date
	$("#id_case_date").blur(function() {
		
		//var pid = this.value ; 
		console.log(' Date : ' + this.value );
		if ( this.value )
		getWeekByDate($.trim(this.value));
	});
	
	/*
	$(".form-control partner").on('change', function() {
		var elemId = this.value ; 
		var arr = elemId.split("_");
		console.log('  id is : ' + elemId );
		setPartner4Case( arr[0], arr[1]);
	});
	
	*/
	
	
	$('.table table-bordered dt-responsive nowrap').DataTable(
			{
				"iDisplayLength": 30,
				"ordering": false
			}
	);
		
});
