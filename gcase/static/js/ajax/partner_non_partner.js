function incoming_chart(weekArr, incomingArr, percentArr, theme, divElm) {

	console.log(incomingArr);
	console.log(percentArr);
	
	var option = {
		tooltip : {
			trigger : 'axis',
			axisPointer : {
				type : 'cross',
				crossStyle : {
					color : '#999'
				}
			}
		},
		toolbox : {
			feature : {
				dataView : {
					show : false,
					readOnly : false,
					title : "Data View"
				},
				magicType : {
					show : true,
					type : [ 'line', 'bar' ],
					title : 'Magic Type'
				},
				restore : {
					show : true,
					title : "Restore"
				},
				saveAsImage : {
					show : true,
					title : "Save Image"
				}
			}
		},
		legend : {
			data : [ 'Incoming', 'Incoming %age' ]
		},
		xAxis : [ {
			type : 'category',
			data : weekArr,
			axisPointer : {
				type : 'shadow'
			}
		} ],
		yAxis : [ {
			type : 'value',
			name : 'Percentage',
			min : 0,
			// max: 5,
			// interval: 10,
			axisLabel : {
				formatter : '{value}'
			}
		} ],
		series : [ {
			name : 'Incoming',
			type : 'bar',
			label : {
				normal : {
					show : true,
					position : 'top'
				}
			},
			data : incomingArr
		}, {
			name : '%age',
			type : 'line',
			label : {
				normal : {
					show : true,
					position : 'top',
				}
			},
			lineStyle : {
				normal : {
					width : 3,
					shadowColor : 'rgba(0,0,0,0.4)',
					shadowBlur : 10,
					shadowOffsetY : 10
				}
			},
			yAxisIndex : 0,
			data : percentArr
		} ]
	};

	
	var incomingChart = echarts.init(document.getElementById(divElm),theme);
	incomingChart.setOption(option);
	
	return false;

}


function so_chart(weekArr, soArr, percentArr, theme, divElm) {

	console.log(soArr);
	console.log(percentArr);
	
	var option = {
		tooltip : {
			trigger : 'axis',
			axisPointer : {
				type : 'cross',
				crossStyle : {
					color : '#999'
				}
			}
		},
		toolbox : {
			feature : {
				dataView : {
					show : false,
					readOnly : false,
					title : "Data View"
				},
				magicType : {
					show : true,
					type : [ 'line', 'bar' ],
					title : 'Magic Type'
				},
				restore : {
					show : true,
					title : "Restore"
				},
				saveAsImage : {
					show : true,
					title : "Save Image"
				}
			}
		},
		legend : {
			data : [ 'SO', 'SO %age' ]
		},
		xAxis : [ {
			type : 'category',
			data : weekArr,
			axisPointer : {
				type : 'shadow'
			}
		} ],
		yAxis : [ {
			type : 'value',
			name : 'Percentage',
			min : 0,
			// max: 5,
			// interval: 10,
			axisLabel : {
				formatter : '{value}'
			}
		} ],
		series : [ {
			name : 'Incoming',
			type : 'bar',
			label : {
				normal : {
					show : true,
					position : 'top'
				}
			},
			data : soArr
		}, {
			name : 'Percent',
			type : 'line',
			label : {
				normal : {
					show : true,
					position : 'top',
				}
			},
			lineStyle : {
				normal : {
					width : 3,
					shadowColor : 'rgba(0,0,0,0.4)',
					shadowBlur : 10,
					shadowOffsetY : 10
				}
			},
			yAxisIndex : 0,
			data : percentArr
		} ]
	};

	
	var incomingChart = echarts.init(document.getElementById(divElm),theme);
	incomingChart.setOption(option);
	
	return false;

}