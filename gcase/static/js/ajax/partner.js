$(document).ready(function() {

});


function showDetail(product_id){
	
	console.log('Product id is: ' + product_id + " from month: " + $('#from_month').val() );
	
	$.ajax({
        type: "GET",
        url: '/report/partner/details',
        data : {
			from_year : $('#from_year').val(),
			from_month : $('#from_month').val(),
			to_year : $('#to_year').val(),
			to_month : $('#to_month').val(),
			product_id : product_id
		},
        success: function(data) {
        	console.log(data)
            $('#partner-detail-dialog').html(data);
    		$('#partner-detail-dialog').modal('show');
        },
        error: function(xhr, textStatus, errorThrown) {
            alert("Please report this error: "+errorThrown+xhr.status+xhr.responseText);
        }
    });
}