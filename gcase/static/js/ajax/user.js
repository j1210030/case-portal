$(document).ready(function() {
	
	//$.validator.setDefaults({
		//submitHandler: function() {
			
		//}
	//});

	
	 $('#id_joined_on').datetimepicker({
	        format: 'MM/DD/YYYY'
	 });
	 $('#id_released_on').datetimepicker({
	        format: 'MM/DD/YYYY'
	 });
	
	$('#userRegisterForm').validate({
      
         rules:
        {
            first_name:{
                required: true,
                maxlength: 50
            },
            last_name:{
                required: true,
                maxlength: 50
            },
            joined_on:{
            	required: true,
                maxlength: 19
            },
            gender:{
                required: true
            },
            username:{
                required: true,
                ascii:true,
                maxlength: 20,
                minlength:6
            },
            
            submitHandler: function(form) {
            	alert('valid form submitted');
                return true;
           }
        }
        
     });
	
	
	var id = $('#id').val();
	
		if ( id != '' ){
		
			$( "#password" ).rules( "add", {
				required: true,
				ascii:true,
				minlength:6,
				maxlength: 20
			});
	 
			$('#confirm_password')rules( "add", {
				required: false,
				ascii:true,
				minlength:6,
				maxlength: 20,
				equalTo: "#id_password"
			});
		}else{
			
			
			
		}
     
     
     
	$("#id_username").blur(function() {
		if ( this.value ){
			isUsernameExist($.trim(this.value));
		}
	});
	
});


$("#id_confirm_password").blur(function() {
	
	var pass = $('#id_password').val() ;
	if ( this.value && pass != '' ){
		if ( $('#id_password').val() !=  this.value ){
			$('#password_didnot_match').show();
			$('#userSubmitBtn').attr("disabled", true);
		}else{
			$('#password_didnot_match').hide();
			$('#userSubmitBtn').attr("disabled", false);
		}
	}
});


function isUsernameExist(username){
	
	var url = '/user/check_username';
	if ( username == '') {
		return false;
	}
	if ( username.length <6 || username.length > 20 || ! isASCII(username)){
		$('#username_invalid_msg').show();
		$('#username_already_exist_msg').hide();
		$('#username_available_msg').hide();
		$('#id_username').css('border-color', '#cc0000');
		$('#userSubmitBtn').attr("disabled", true);
		return false;
	}else{
		$('#username_invalid_msg').hide();
	}
	var uid= $('#uid').val();
	$('#username_loading').show();
	$.ajax({
		url : url,
		data : {
			'uid' : uid,
			'username' : username
		},
		type : 'GET',
		cache : false,
		dataType : 'json',
		contentType : 'application/json',
		success : function(response) {
			$('#username_loading').hide();
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
				$('#userSubmitBtn').attr("disabled", true);
				$('#username_already_exist_msg').show();
				$('#username_available_msg').hide();
				$('#id_username').css('border-color', '#cc0000');
				return true;
			} else if ( data.status == 'OK') {
				$('#username_already_exist_msg').hide();
				$('#username_available_msg').show();
				$('#userSubmitBtn').attr("disabled", false);
				$('#id_username').css('border-color', '');
				return false;
			}
		},
		error : function(jqXHR, textStatus, errorThrown) {
			alert("Error Encountered!!!")
		}
	});
}

