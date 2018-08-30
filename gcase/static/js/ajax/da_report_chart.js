
function backlog_chart(weekArr,androidBacklog,firebaseBacklog,totalBacklog, divElm ){
	
	 
	var theme = {
			  color: [
				  '#9ACD32', '#ffc04c','#34495E'
			  ]
	 }


	var optionBacklog = {
			
		    tooltip: {
		        trigger: 'axis',
		        axisPointer: {
		            type: 'cross',
		            crossStyle: {
		                color: '#999'
		            }
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
		        data:['Android','Firebase','Total backlog']
		    },
		    xAxis: [
		        {
		            type: 'category',
		            data: weekArr,
		            axisPointer: {
		                type: 'shadow'
		            }
		        }
		    ],
		    yAxis: [
		        {
		            type: 'value',
		            name: 'Backlog',
		            axisLabel: {
		                formatter: '{value}'
		            }
		        }
		    ],
		    series: [
		        {
		            name:'Android',
		            type:'bar',
		            label: {
		                normal: {
		                    show: true,
		                    position: 'top'
		                }
		            },
		            data:androidBacklog
		        },
		        {
		            name:'Firebase',
		            type:'bar',
		            label: {
		                normal: {
		                    show: true,
		                    position: 'top'
		                }
		            },
		            data:firebaseBacklog
		        },
		        {
		            name:'Total',
		            type:'line',
		            label: {
		                normal: {
		                    show: true,
		                    position: 'top',
		                }
		            },
		            lineStyle: {
		                normal: {
		                    width: 3,
		                    shadowColor: 'rgba(0,0,0,0.4)',
		                    shadowBlur: 10,
		                    shadowOffsetY: 10
		                }
		            },
		            yAxisIndex: 0,
		            data:totalBacklog
		        }
		    ]
		};
	
	
	var backlogChart = echarts.init(divElm,theme);
	backlogChart.setOption(optionBacklog);
	
	
		
}

function so_chart(weekArr,androidSo,firebaseSo,totalSo, divElm){
	 
	var theme = {
			  color: [
				  '#9ACD32', '#ffc04c','#34495E'
			  ]
	 }


	var optionSo = {
			
		    tooltip: {
		        trigger: 'axis',
		        axisPointer: {
		            type: 'cross',
		            crossStyle: {
		                color: '#999'
		            }
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
		        data:['Android','Firebase','Total backlog']
		    },
		    xAxis: [
		        {
		            type: 'category',
		            data: weekArr,
		            axisPointer: {
		                type: 'shadow'
		            }
		        }
		    ],
		    yAxis: [
		        {
		            type: 'value',
		            name: 'SO',
		            axisLabel: {
		                formatter: '{value}'
		            }
		        }
		    ],
		    series: [
		        {
		            name:'Android',
		            type:'bar',
		            label: {
		                normal: {
		                    show: true,
		                    position: 'top'
		                }
		            },
		            data:androidSo
		        },
		        {
		            name:'Firebase',
		            type:'bar',
		            label: {
		                normal: {
		                    show: true,
		                    position: 'top'
		                }
		            },
		            data:firebaseSo
		        },
		        {
		            name:'Total',
		            type:'line',
		            label: {
		                normal: {
		                    show: true,
		                    position: 'top',
		                }
		            },
		            lineStyle: {
		                normal: {
		                    width: 3,
		                    shadowColor: 'rgba(0,0,0,0.4)',
		                    shadowBlur: 10,
		                    shadowOffsetY: 10
		                }
		            },
		            yAxisIndex: 0,
		            data:totalSo
		        }
		    ]
		};
	var SoChart = echarts.init(divElm,theme);
	SoChart.setOption(optionSo);
}

function language_chart(langElm,weekArr, incomingJp, incomingKo, incomingZh){
	
	var colors = ['#5793f3', '#d14a61', '#675bba'];
	option = {
	    //color: colors,

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
	        data:['Japanese','Korean','Chinese']
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
	            name:'Japanese',
	            type:'line',
	            label: {
	                normal: {
	                    show: true,
	                    position: 'top',
	                }
	            },
	            smooth: true,
	            data: incomingJp
	        },
	        {
	            name:'Korean',
	            type:'line',
	            label: {
	                normal: {
	                    show: true,
	                    position: 'top',
	                }
	            },
	            smooth: true,
	            data: incomingKo
	        },
	        {
	            name:'Chinese',
	            label: {
	                normal: {
	                    show: true,
	                    position: 'top',
	                }
	            },
	            type:'line',
	            smooth: true,
	            data: incomingZh
	        }
	    ]
	};

	var langChart = echarts.init(langElm);
	langChart.setOption(option);
}

function component_chart(compElm, dataArr, compNameArr){
	
	var option = {
		    title : {
		        subtext: 'Firebase',
		        x:'center'
		    },
		    tooltip : {
		        trigger: 'item',
		        formatter: "{a} <br/>{b} : {c} ({d}%)"
		    },
		   legend: {
		        orient: 'vertical',
		       left: 'left',
		        //data: compNameArr
		   	},
		    series : [
		        {
		            type: 'pie',
		            data:dataArr,
		            itemStyle: {
		                emphasis: {
		                    shadowBlur: 10,
		                    shadowOffsetX: 0,
		                    shadowColor: 'rgba(0, 0, 0, 0.5)'
		                }
		            }
		        }
		    ]
		};


	var compChart = echarts.init(compElm);
	compChart.setOption(option);
	
}

function quality_chart(qualityElm, okRatio, monthlyRatio, weekArr,product_id){
	
	var option = ''; 
	
	var themeAndroid = {
			  color: [
				  '#9ACD32', '#5c7b1e'
			  ]
	 }

	 var themeFirebase = {
		  color: [
			  '#b28635', '#ffc04c'
		  ]
	 }
	  
	 var option = {
		
	    tooltip: {
	        trigger: 'axis',
	        axisPointer: {
	            type: 'cross',
	            crossStyle: {
	                color: '#999'
	            }
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
	        data:['Weekly','Monthly']
	    },
	    xAxis: [
	        {
	            type: 'category',
	            data: weekArr,
	            axisPointer: {
	                type: 'shadow'
	            },
	            z: 100,
	            blendMode: 'lighter'
	        }
	    ],
	    yAxis: [
	        {
	            type: 'value',
	            name: 'Ratio(%)',
	            min: 0,
	            //max: 5,
	            //interval: 10,
	            axisLabel: {
	                formatter: '{value}'
	            }
	        }
	    ],
	    series: [
	        {
	            name:'Weekly',
	            type:'line',
	            label: {
	                normal: {
	                    show: true,
	                    position: 'top'
	                }
	            },
	            data:okRatio
	        },
	        {
	            name:'Monthly',
	            type:'line',
	            label: {
	                normal: {
	                    show: true,
	                    position: 'top'
	                }
	            },
	            data:monthlyRatio
	        }
	    ]
	};
	 
	 var chart = '';
	 if ( product_id == '1' ){
		 chart = echarts.init(document.getElementById(qualityElm),themeAndroid);
	 }else {
		 chart = echarts.init(document.getElementById(qualityElm),themeFirebase);
	 }
	 chart.setOption(option);
}
