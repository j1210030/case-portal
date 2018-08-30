
function so_chart(chartElm,weekArr, soArr, soPartnerArr){
	
	option = {
	 
	    tooltip: {
	        trigger: 'none',
	        axisPointer: {
	            type: 'cross'
	        }
	    },
	    toolbox: {
	        feature: {
	            dataView: {show: false, readOnly: false, title:"Data View"},
	            magicType: {show:true, type: ['line', 'bar'],title:'Magic Type'},
	            restore: {show: true,title: "Restore"},
	            saveAsImage: {show: true,title: "Save Image"}
	        }
	    },
	    legend: {
	        data:['SO','Partner','Chinese']
	    },
	    xAxis: [
	        {
	            type: 'category',
	            axisTick: {
	                alignWithLabel: true
	            },
	            axisLine: {
	                onZero: false
	            },
	            data: weekArr
	        }
	    ],
	    yAxis: [
	        {
	            type: 'value'
	        }
	    ],
	    series: [
	        {
	            name:'SO',
	            type:'line',
	            label: {
	                normal: {
	                    show: true,
	                    position: 'top',
	                }
	            },
	            smooth: true,
	            data: soArr
	        },
	        {
	            name:'Partner',
	            type:'line',
	            label: {
	                normal: {
	                    show: true,
	                    position: 'top',
	                }
	            },
	            smooth: true,
	            data: soPartnerArr
	        }
	    ]
	};

	var soChart = echarts.init(chartElm);
	soChart.setOption(option);
}




function showDetail(week){
	console.log('Week is: ' + week );

	$.ajax({
        type: "GET",
        url: '/report/individual_details?week='+week,
        success: function(data) {
        	console.log(data)
            $('#individual-week-dialog').html(data);
    		$('#individual-week-dialog').modal('show');
        },
        error: function(xhr, textStatus, errorThrown) {
            alert("Please report this error: "+errorThrown+xhr.status+xhr.responseText);
        }
    });
}