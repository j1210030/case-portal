$(document).ready(function() {
	
	
	
	$('#gcaseForm').validate({
      
         rules:
        {
           id:{
               required: true,
               maxlength: 50
            },
            subject:{
                required: true,
                maxlength: 200
            },
            case_date:{
            	required: true,
                maxlength: 19
            },
            language:{
                required: true,
                maxlength: 10
            },
            status:{
                required: true,
                maxlength: 15
            },
            gcase_user:{
            	required: true,
            	number: true
            },
            difficulty_level:{
            	required: true,
            },
            submitHandler: function(form) {
            	alert('valid form submitted');
                return false;
            }
        }
        
     });
	
	
	$("#id_id").blur(function() {
		if ( this.value ){
			isCaseExist($.trim(this.value));
		}
	});
	
	$("input:radio[name=product]").change(function() {
		console.log('Radio Clicked ');
		var pid = this.value ; 
		console.log(' Product id: ' + pid );
		setComponents4Products(pid,'id_component','Select','');
	});
	
	var selected_product = $('input:radio[name=product]:checked').val();
	if ( selected_product ){
		console.log(' Component Id: ' + $('#curr_component_id').val() + ' ,Selected product: ' + selected_product );
		var comp_id = $('#curr_component_id').val();
		setComponents4Products(selected_product,'id_component','Select',comp_id);
	}
	
	$("#product").on('change', function() {
		
		var pid = this.value ; 
		console.log(' Product id: ' + pid );
		$('#id_component').empty();
		setComponents4Products(pid,'component','Component','');
	});
	
	$("#id_status").on('change', function() {
		var status = this.value ; 
		if ( status == 'solution_offered' ){
			$('#so_date_div').show();
			$('#buganizer_id_div').hide();
		}else if ( status == 'blocked' ){
			$('#buganizer_id_div').show();
			$('#so_date_div').hide();
		}else{
			$('#buganizer_id_div').hide();
			$('#so_date_div').hide();
		}
		
	});
	
	
	// Get week by date
	$("#id_case_date").blur(function() { 
		console.log(' Date : ' + this.value );
		if ( this.value )
		getWeekByDate($.trim(this.value));
	});
	
	if ( $('#curr_partner_id').val() !='' ){
		var lang =  $('input:radio[name=language]:checked').val();
        console.log(' Language: ' + lang );
        $("#id_partner_geo").val(lang);
        $('#partner_load_msg').hide(); 
        setPartnersByLang(lang,$('#curr_partner_id').val());
        $('#partner_select_div').show();
        
	}
	
	$("#id_partner_geo").on('change', function() {
        var hl = this.value;
        console.log(' Hl is: ' + hl);
        if ( !hl ) {
        	$('#partner_load_msg').show(); 
        }else{
        	setPartnersByLang(hl,'');
        	$('#partner_select_div').show();
        }
    }); 
	
	$( "#caseSubmitBtn" ).click(function() {
		
		var status = $("#id_status option:selected").val();
		console.log('Status: ' + status );
		if ( status == 'blocked' ){
			var buganizer = $('#id_buganizer_number').val();
			
			if ( buganizer == '' || !$.isNumeric(buganizer)){
				$('#id_buganizer_number').css('border-color', 'red');
				$( "#id_buganizer_number" ).focus();
				alert('Please input a valid buganizer number!!');
				return false;
			}
			
		}
		
		if ( status == 'solution_offered' ){
			
			var so_date = $('#id_so_date').val();
			if ( so_date == '' || !isValidDate(so_date)){
				$('#id_so_date').css('border-color', 'red');
				$( "#id_so_date" ).focus();
				alert('Please input a valid SO date!');
				return false;
			}
		}
		$( "#gcaseForm" ).submit();
	});
	
});
