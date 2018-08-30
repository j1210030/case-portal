
(function($,sr){
    // debouncing function from John Hann
    // http://unscriptable.com/index.php/2009/03/20/debouncing-javascript-methods/
    var debounce = function (func, threshold, execAsap) {
      var timeout;

        return function debounced () {
            var obj = this, args = arguments;
            function delayed () {
                if (!execAsap)
                    func.apply(obj, args); 
                timeout = null; 
            }

            if (timeout)
                clearTimeout(timeout);
            else if (execAsap)
                func.apply(obj, args);

            timeout = setTimeout(delayed, threshold || 100); 
        };
    };

    // smartresize 
    jQuery.fn[sr] = function(fn){  return fn ? this.bind('resize', debounce(fn)) : this.trigger(sr); };

})(jQuery,'smartresize');

var CURRENT_URL = window.location.href.split('#')[0].split('?')[0],
    $BODY = $('body'),
    $MENU_TOGGLE = $('#menu_toggle'),
    $SIDEBAR_MENU = $('#sidebar-menu'),
    $SIDEBAR_FOOTER = $('.sidebar-footer'),
    $LEFT_COL = $('.left_col'),
    $RIGHT_COL = $('.right_col'),
    $NAV_MENU = $('.nav_menu'),
    $FOOTER = $('footer');

	
	
// Sidebar
function init_sidebar() {
// TODO: This is some kind of easy fix, maybe we can improve this
var setContentHeight = function () {
	// reset height
	$RIGHT_COL.css('min-height', $(window).height());

	var bodyHeight = $BODY.outerHeight(),
		footerHeight = $BODY.hasClass('footer_fixed') ? -10 : $FOOTER.height(),
		leftColHeight = $LEFT_COL.eq(1).height() + $SIDEBAR_FOOTER.height(),
		contentHeight = bodyHeight < leftColHeight ? leftColHeight : bodyHeight;

	// normalize content
	contentHeight -= $NAV_MENU.height() + footerHeight;

	$RIGHT_COL.css('min-height', contentHeight);
};

  $SIDEBAR_MENU.find('a').on('click', function(ev) {
	  console.log('clicked - sidebar_menu');
        var $li = $(this).parent();

        if ($li.is('.active')) {
            $li.removeClass('active active-sm');
            $('ul:first', $li).slideUp(function() {
                setContentHeight();
            });
        } else {
            // prevent closing menu if we are on child menu
            if (!$li.parent().is('.child_menu')) {
                $SIDEBAR_MENU.find('li').removeClass('active active-sm');
                $SIDEBAR_MENU.find('li ul').slideUp();
            }else
            {
				if ( $BODY.is( ".nav-sm" ) )
				{
					$SIDEBAR_MENU.find( "li" ).removeClass( "active active-sm" );
					$SIDEBAR_MENU.find( "li ul" ).slideUp();
				}
			}
            $li.addClass('active');

            $('ul:first', $li).slideDown(function() {
                setContentHeight();
            });
        }
    });

// toggle small or large menu 
$MENU_TOGGLE.on('click', function() {
		console.log('clicked - menu toggle');
		
		if ($BODY.hasClass('nav-md')) {
			$SIDEBAR_MENU.find('li.active ul').hide();
			$SIDEBAR_MENU.find('li.active').addClass('active-sm').removeClass('active');
		} else {
			$SIDEBAR_MENU.find('li.active-sm ul').show();
			$SIDEBAR_MENU.find('li.active-sm').addClass('active').removeClass('active-sm');
		}

	$BODY.toggleClass('nav-md nav-sm');

	setContentHeight();

	$('.dataTable').each ( function () { $(this).dataTable().fnDraw(); });
});

	// check active menu
	$SIDEBAR_MENU.find('a[href="' + CURRENT_URL + '"]').parent('li').addClass('current-page');

	$SIDEBAR_MENU.find('a').filter(function () {
		return this.href == CURRENT_URL;
	}).parent('li').addClass('current-page').parents('ul').slideDown(function() {
		setContentHeight();
	}).parent().addClass('active');

	// recompute content when resizing
	$(window).smartresize(function(){  
		setContentHeight();
	});

	setContentHeight();

	// fixed sidebar
	if ($.fn.mCustomScrollbar) {
		$('.menu_fixed').mCustomScrollbar({
			autoHideScrollbar: true,
			theme: 'minimal',
			mouseWheel:{ preventDefault: true }
		});
	}
};
// /Sidebar

	var randNum = function() {
	  return (Math.floor(Math.random() * (1 + 40 - 20))) + 20;
	};


// Panel toolbox
$(document).ready(function() {
    $('.collapse-link').on('click', function() {
        var $BOX_PANEL = $(this).closest('.x_panel'),
            $ICON = $(this).find('i'),
            $BOX_CONTENT = $BOX_PANEL.find('.x_content');
        
        // fix for some div with hardcoded fix class
        if ($BOX_PANEL.attr('style')) {
            $BOX_CONTENT.slideToggle(200, function(){
                $BOX_PANEL.removeAttr('style');
            });
        } else {
            $BOX_CONTENT.slideToggle(200); 
            $BOX_PANEL.css('height', 'auto');  
        }

        $ICON.toggleClass('fa-chevron-up fa-chevron-down');
    });

    $('.close-link').click(function () {
        var $BOX_PANEL = $(this).closest('.x_panel');

        $BOX_PANEL.remove();
    });
});
// /Panel toolbox

// Tooltip
$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip({
        container: 'body'
    });
});
// /Tooltip

// Progressbar
if ($(".progress .progress-bar")[0]) {
    $('.progress .progress-bar').progressbar();
}
// /Progressbar






$(document).ready(function() {
	$('#id_created').datetimepicker({ format: 'YYYY-MM-DD'})
    
    $('#myDatepicker2').datetimepicker({
        format: 'DD.MM.YYYY'
    });
   
   $('#id_so_date').datetimepicker({ format: 'YYYY-MM-DD'})
    
    $('#myDatepicker3').datetimepicker({
        format: 'hh:mm A'
    });
    
    $('#myDatepicker4').datetimepicker({
        ignoreReadonly: true,
        allowInputToggle: true
    });

    $('#datetimepicker6').datetimepicker();
    
    $('#datetimepicker7').datetimepicker({
        useCurrent: false
    });
    
    $("#datetimepicker6").on("dp.change", function(e) {
        $('#datetimepicker7').data("DateTimePicker").minDate(e.date);
    });
    
    $("#datetimepicker7").on("dp.change", function(e) {
        $('#datetimepicker6').data("DateTimePicker").maxDate(e.date);
    });
    
    $('#from_dt').datetimepicker({
        format: 'MM/DD/YYYY'
    });
});



/* DATA TABLES */
	
	function init_DataTables() {
		
		console.log('run_datatables');
		
		if( typeof ($.fn.DataTable) === 'undefined'){ return; }
		console.log('init_DataTables');
		
		var handleDataTableButtons = function() {
		  if ($("#datatable-buttons").length) {
			$("#datatable-buttons").DataTable({
			  dom: "Bfrtip",
			  buttons: [
				{
				  extend: "copy",
				  className: "btn-sm"
				},
				{
				  extend: "csv",
				  className: "btn-sm"
				},
				{
				  extend: "excel",
				  className: "btn-sm"
				},
				{
				  extend: "pdfHtml5",
				  className: "btn-sm"
				},
				{
				  extend: "print",
				  className: "btn-sm"
				},
			  ],
			  responsive: true
			});
		  }
		};

		TableManageButtons = function() {
		  "use strict";
		  return {
			init: function() {
			  handleDataTableButtons();
			}
		  };
		}();

		$('#datatable').dataTable(
				{
					'pageLength': 50,
				}
		);

		$('#datatable-keytable').DataTable({
		  keys: true
		});

		$('#datatable-responsive').DataTable(
			{
				"iDisplayLength": 30,
				"ordering": false
			}
		);
		
		$('#datatable-responsive-assigned').DataTable(
				{
					"iDisplayLength": 30,
					"ordering": false
				}
		);
		$('#datatable-responsive-blocked').DataTable(
				{
					"iDisplayLength": 30,
					"ordering": false
				}
		);
		$('#datatable-responsive-solution_offered').DataTable(
				{
					"iDisplayLength": 30,
					"ordering": false
				}
		);
		$('#datatable-responsive-forwarded').DataTable(
				{
					"iDisplayLength": 30,
					"ordering": false
				}
		);
		$('#datatable-responsive-routed').DataTable(
				{
					"iDisplayLength": 30,
					"ordering": false
				}
		);
		$('#datatable-responsive-needinfo').DataTable(
				{
					"iDisplayLength": 30,
					"ordering": false
				}
		);
			
		
		

		$('#datatable-scroller').DataTable({
		  ajax: "js/datatables/json/scroller-demo.json",
		  deferRender: true,
		  scrollY: 380,
		  scrollCollapse: true,
		  scroller: true
		});

		$('#datatable-fixed-header').DataTable({
		  fixedHeader: true
		});

		var $datatable = $('#datatable-checkbox');

		$datatable.dataTable({
			//'order': [[ 1, 'asc' ]],
			'columnDefs': [
			{ orderable: false, targets: [0] }
		  ]
		});
		$datatable.on('draw.dt', function() {
		  $('checkbox input').iCheck({
			checkboxClass: 'icheckbox_flat-green'
		  });
		});

		TableManageButtons.init();
		
	};

$(document).ready(function() {
		init_sidebar();
		init_DataTables();
});	

function isValidDate(dateString) {
	return true;
	
	//var regEx = /^\d{2}\/\d{2}\/\d{2,4}$/;
	//return dateString.match(regEx) != null;
}

function isASCII(str) {
    return /^[\x00-\x7F]*$/.test(str);
}

jQuery.validator.addMethod("ascii", function(value, element) {
	return this.optional( element ) || /^[\x00-\x7F]*$/.test(value);
	}, 'Please enter valid value( asii only)');
	
