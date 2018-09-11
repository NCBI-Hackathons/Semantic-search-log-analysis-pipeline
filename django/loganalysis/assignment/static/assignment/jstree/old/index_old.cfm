<!---
Name:        http://localhost:8500/_pubmed2015/mesh/index.cfm
Author:      Dan Wendling (dan.wendling@nih.gov)
Description: PubMed Counts project
Created:     1/5/2014
Modified:    1/5/2014
 --->


<!--- Variables --->
	<cfparam name="url.CurrDataSetID" default="71" />
	<cfparam name="url.intCount" default="15" />
<!--- intCounts can be 1, 3, 7, 11, 15... --->

<!---<cfinvoke component="cfc.meshTree" method="getMeSHTreeOne" returnvariable="MeSHTreeOne"></cfinvoke>
--->


<!--- Adding the data set back in...
this page, invoking search:  CurrDataSetID="#CurrDataSetID#"
cfc: WHERE dataset.DataSetID = #ARGUMENTS.CurrDataSetID#
--->


<cfscript>
//START-UP ----------------------------------------------------------------------------------
  //Make URLs work when page is renamed during testing
  variables.selfurl = GetFileFromPath(GetCurrentTemplatePath());
  variables.CurrentPage=GetFileFromPath(GetBaseTemplatePath());

  variables.filter = CreateObject("component", "cfc.filter");
  filter.init();
  WriteDump(var=filter.getVariables().filters, label="Filters", expand="no"); 
  variables.meshTree = CreateObject("component", "cfc.meshTree");

//Info about the data set we're working with
variables.qDataSetInfo = meshTree.getDataSetInfo();

//Total count of records in record set
  variables.TotDataSetCnt = meshTree.getTotDataSetCnt();

//Starting row count to recordsInventory.cfm; could have a cfparam default there instead?
  variables.MaxRowNo="200";

//searchLimits -----------------------------------------------------------------------------
  variables.qRecordscount = meshTree.getRecords(filter);

//Branches -----------------------------------------------
variables.intCount="1";


variables.qBranchACnt = meshTree.getBranchACnt(filter);
variables.qBranchA = meshTree.getBranchA(filter);

variables.qBranchBCnt = meshTree.getBranchBCnt(filter);
variables.qBranchB = meshTree.getBranchB(filter);

variables.qBranchCCnt = meshTree.getBranchCCnt(filter);
variables.qBranchC = meshTree.getBranchC(filter);

variables.qBranchDCnt = meshTree.getBranchDCnt(filter);
variables.qBranchD = meshTree.getBranchD(filter);

variables.qBranchECnt = meshTree.getBranchECnt(filter);
variables.qBranchE = meshTree.getBranchE(filter);

variables.qBranchFCnt = meshTree.getBranchFCnt(filter);
variables.qBranchF = meshTree.getBranchF(filter);

variables.qBranchGCnt = meshTree.getBranchGCnt(filter);
variables.qBranchG = meshTree.getBranchG(filter);

variables.qBranchHCnt = meshTree.getBranchHCnt(filter);
variables.qBranchH = meshTree.getBranchH(filter);

variables.qBranchICnt = meshTree.getBranchICnt(filter);
variables.qBranchI = meshTree.getBranchI(filter);

variables.qBranchJCnt = meshTree.getBranchJCnt(filter);
variables.qBranchJ = meshTree.getBranchJ(filter);

variables.qBranchKCnt = meshTree.getBranchKCnt(filter);
variables.qBranchK = meshTree.getBranchK(filter);

variables.qBranchLCnt = meshTree.getBranchLCnt(filter);
variables.qBranchL = meshTree.getBranchL(filter);

variables.qBranchMCnt = meshTree.getBranchMCnt(filter);
variables.qBranchM = meshTree.getBranchM(filter);

variables.qBranchNCnt = meshTree.getBranchNCnt(filter);
variables.qBranchN = meshTree.getBranchN(filter);

variables.qBranchVCnt = meshTree.getBranchVCnt(filter);
variables.qBranchV = meshTree.getBranchV(filter);

variables.qBranchZCnt = meshTree.getBranchZCnt(filter);
variables.qBranchZ = meshTree.getBranchZ(filter);
</cfscript>

<cfparam name="url.DescriptorName" default="">
<cfparam name="url.MeshMajorTopicYN" default="">

<cfset todayDate = Now()>






 <!doctype html>
<!--[if lt IE 7]> <html class="ie6 oldie"> <![endif]-->
<!--[if IE 7]>    <html class="ie7 oldie"> <![endif]-->
<!--[if IE 8]>    <html class="ie8 oldie"> <![endif]-->
<!--[if gt IE 8]><!-->
<html class="">
<!--<![endif]-->
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PubMed Record Set Analyzer - home</title>
<link href="../_styles/boilerplate.css" rel="stylesheet" type="text/css">
<link href="../_styles/main.css" rel="stylesheet" type="text/css">
<!--[if lt IE 9]>
<script src="//html5shiv.googlecode.com/svn/trunk/html5.js"></script>
<![endif]-->
<script src="../_scripts/respond.min.js"></script>
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-43296135-1', 'ponder-matic.com');
  ga('send', 'pageview');
</script>
</head>

<body>

<div class="skipnavigation"><a class="skipnavigation" href="#skip" title="Skip the navigation on this page">Skip Navigation</a></div>

<div class="gridContainer clearfix">

  <div id="header">

    <div id="hgroup">
    <h1>PubMed Record Set Analyzer - home</h1>
  </div>
  
    <div id="siteNav">
  
      <h2>Site navigation</h2>
        
        <ul class="topMenu"><cfoutput>
            <li><a href="#request.cfg.applicationUrlPath()#index.cfm" title="Home">Home</a></li>
 <!---           <li><a href="#request.cfg.applicationUrlPath()#drilldown/index.cfm?CurrDataSetID=#DataSetID#" title="Analyst interface" class="CurrentPage">Analyst Interface</a></li>
            <li><a href="#request.cfg.applicationUrlPath()#topicReports/index.cfm?CurrDataSetID=#DataSetID#" title="Static reports">Static reports</a></li>
           <li><a href="#request.cfg.applicationUrlPath()#custom/meshTree.cfm" title="Static reports">MeSH tree</a></li>
		   ---> 
        </cfoutput></ul>  

  </div><!-- end #siteNav --> 
  
  </div><!--end header-->
  

  <div id="mainContent">
    <a id="skipnav" name="skip"></a>
  
      <h1>Browse the MeSH Tree for <cfoutput>#qDataSetInfo.DataSetName#</cfoutput> - MeSHTree1</h1>
      
    <p> This is an <em><strong>experimental</strong></em> application for analyzing PubMed record sets.</p>

<p>Later: Allow for browsing either all descriptors, or just major descriptors.</p>
<p>Counts are based on unique PMIDs, representing the number of <em><strong>records</strong></em> you could retrieve by clicking on links to pubmed.gov.</p>


<p> 
<!--- Anatomy [A] --->
<cfoutput><a href="index.cfm?intCount=#intCount#">Anatomy [A]</a> (#qBranchACnt.cnt#)</cfoutput>
<cflayout type="vbox" name="A_anatomy">

</cflayout>


<!---<cfif qBranchA.citeCnt neq ''>
	<cfoutput query="qBranchA">
	<a href="index.cfm?intCount=#intCount#">#TreeNumber#-#DescriptorName#</a> (<a href="http://pubmed.gov?#citeCnt#">#citeCnt#</a>)
    </cfoutput>
<cfelse>
	Anatomy [A] (0)
</cfif>--->
<br>


<!--- Organisms [B] --->
<cfoutput><a href="index.cfm?intCount=#intCount#">Organisms [B]</a> (#qBranchBCnt.cnt#)</cfoutput>
<!---<cfif qBranchB.citeCnt neq ''>
	<cfoutput query="qBranchB">
    <a href="index.cfm?intCount=#intCount#">#TreeNumber#-#DescriptorName#</a> (<a href="http://pubmed.gov?#citeCnt#">#citeCnt#</a>)
    </cfoutput>
<cfelse>
	Organisms [B] (0)
</cfif>--->
<br>


<!--- Diseases [C] --->
<cfoutput><a href="index.cfm?intCount=#intCount#">Diseases [C]</a> (#qBranchCCnt.cnt#)</cfoutput>
<!---<cfif qBranchC.citeCnt neq ''>
	<cfoutput query="qBranchC">
    <a href="item">#TreeNumber#-#DescriptorName#</a> (<a href="http://pubmed.gov?#citeCnt#">#citeCnt#</a>)
    </cfoutput>
<cfelse>
	Diseases [C] (0)
</cfif>--->
<br>


<!--- Chemicals and Drugs [D] --->
<cfoutput><a href="index.cfm?intCount=#intCount#">Chemicals and Drugs [D]</a> (#qBranchDCnt.cnt#)</cfoutput>
<!---<cfif qBranchD.citeCnt neq ''>
    <cfoutput query="qBranchD">
    <a href="item">#TreeNumber#-#DescriptorName#</a> (<a href="http://pubmed.gov?#citeCnt#">#citeCnt#</a>)
    </cfoutput>
<cfelse>
	ITEM (0)
</cfif>--->
<br>


<!--- Analytical, Diagnostic and Therapeutic Techniques and Equipment [E] --->
<cfoutput><a href="index.cfm?intCount=#intCount#">Analytical, Diagnostic and Therapeutic Techniques and Equipment [E]</a> (#qBranchECnt.cnt#)</cfoutput>
<!---<cfif qBranchE.citeCnt neq ''>
	<cfoutput query="qBranchE">
    <a href="item">#TreeNumber#-#DescriptorName#</a> (<a href="http://pubmed.gov?#citeCnt#">#citeCnt#</a>)
    </cfoutput>
<cfelse>
	Chemicals and Drugs [D] (0)
</cfif>--->
<br>


<!--- Psychiatry and Psychology [F] --->
<cfoutput><a href="index.cfm?intCount=#intCount#">Psychiatry and Psychology [F]</a> (#qBranchFCnt.cnt#)</cfoutput>
<!---<cfif qBranchF.citeCnt neq ''>
	<cfoutput query="qBranchF">
    <a href="item">#TreeNumber#-#DescriptorName#</a> (<a href="http://pubmed.gov?#citeCnt#">#citeCnt#</a>)
    </cfoutput>
<cfelse>
	Psychiatry and Psychology [F] (0)
</cfif>--->
<br>


<!--- Phenomena and Processes [G] --->
<cfoutput><a href="index.cfm?intCount=#intCount#">Phenomena and Processes [G]</a> (#qBranchGCnt.cnt#)</cfoutput>
<!---<cfif qBranchG.citeCnt neq ''>
	<cfoutput query="qBranchG">
    <a href="item">#TreeNumber#-#DescriptorName#</a> (<a href="http://pubmed.gov?#citeCnt#">#citeCnt#</a>)
    </cfoutput>
<cfelse>
	Phenomena and Processes [G] (0)
</cfif>--->
<br>


<!--- Disciplines and Occupations [H] --->
<cfoutput><a href="index.cfm?intCount=#intCount#">Disciplines and Occupations [H]</a> (#qBranchHCnt.cnt#)</cfoutput>
<!---<cfif qBranchH.citeCnt neq ''>
	<cfoutput query="qBranchH">
    <a href="item">#TreeNumber#-#DescriptorName#</a> (<a href="http://pubmed.gov?#citeCnt#">#citeCnt#</a>)
    </cfoutput>
<cfelse>
	Disciplines and Occupations [H] (0)
</cfif>--->
<br>


<!--- Anthropology, Education, Sociology and Social Phenomena [I] --->
<cfoutput><a href="index.cfm?intCount=#intCount#">Anthropology, Education, Sociology and Social Phenomena [I]</a> (#qBranchICnt.cnt#)</cfoutput>
<!---<cfif qBranchI.citeCnt neq ''>
	<cfoutput query="qBranchI">
    <a href="item">#TreeNumber#-#DescriptorName#</a> (<a href="http://pubmed.gov?#citeCnt#">#citeCnt#</a>)
    </cfoutput>
<cfelse>
	Anthropology, Education, Sociology and Social Phenomena [I] (0)
</cfif>--->
<br>


<!--- Technology, Industry, Agriculture [J] --->
<cfoutput><a href="index.cfm?intCount=#intCount#">Technology, Industry, Agriculture [J]</a> (#qBranchJCnt.cnt#)</cfoutput>
<!---<cfif qBranchJ.citeCnt neq ''>
	<cfoutput query="qBranchJ">
    <a href="item">#TreeNumber#-#DescriptorName#</a> (<a href="http://pubmed.gov?#citeCnt#">#citeCnt#</a>)
    </cfoutput>
<cfelse>
	Technology, Industry, Agriculture [J] (0)
</cfif>--->
<br>


<!--- Humanities [K] --->
<cfoutput><a href="index.cfm?intCount=#intCount#">Humanities [K]</a> (#qBranchKCnt.cnt#)</cfoutput>
<!---<cfif qBranchK.citeCnt neq ''>
	<cfoutput query="qBranchK">
    <a href="item">#TreeNumber#-#DescriptorName#</a> (<a href="http://pubmed.gov?#citeCnt#">#citeCnt#</a>)
    </cfoutput>
<cfelse>
	Humanities [K] (0)
</cfif>--->
<br>


<!--- Information Science [L] --->
<cfoutput><a href="index.cfm?intCount=#intCount#">Information Science [L]</a> (#qBranchLCnt.cnt#)</cfoutput>
<!---<cfif qBranchL.citeCnt neq ''>
	<cfoutput query="qBranchL">
    <a href="item">#TreeNumber#-#DescriptorName#</a> (<a href="http://pubmed.gov?#citeCnt#">#citeCnt#</a>)
    </cfoutput>
<cfelse>
	Information Science [L] (0)
</cfif>--->
<br>


<!--- Named Groups [M] --->
<cfoutput><a href="index.cfm?intCount=#intCount#">Named Groups [M]</a> (#qBranchMCnt.cnt#)</cfoutput>
<!---<cfif qBranchM.citeCnt neq ''>
	<cfoutput query="qBranchM">
    <a href="item">#TreeNumber#-#DescriptorName#</a> (<a href="http://pubmed.gov?#citeCnt#">#citeCnt#</a>)
    </cfoutput>
<cfelse>
	Named Groups [M] (0)
</cfif>--->
<br>


<!--- Health Care [N] --->
<cfoutput><a href="index.cfm?intCount=#intCount#">Health Care [N]</a> (#qBranchNCnt.cnt#)</cfoutput>
<!---<cfif qBranchN.citeCnt neq ''>
	<cfoutput query="qBranchN">
    <a href="item">#TreeNumber#-#DescriptorName#</a> (<a href="http://pubmed.gov?#citeCnt#">#citeCnt#</a>)
    </cfoutput>
<cfelse>
	Health Care [N] (0)
</cfif>--->
<br>


<!--- Publication Characteristics [V] --->
<cfoutput><a href="index.cfm?intCount=#intCount#">Publication Characteristics [V]</a> (#qBranchVCnt.cnt#)</cfoutput>
<!---<cfif qBranchV.citeCnt neq ''>
	<cfoutput query="qBranchV">
    <a href="item">#TreeNumber#-#DescriptorName#</a> (<a href="http://pubmed.gov?#citeCnt#">#citeCnt#</a>)
    </cfoutput>
<cfelse>
	Publication Characteristics [V] (0)
</cfif>--->
<br>


<!--- Geographicals [Z]  --->
<cfoutput><a href="index.cfm?intCount=#intCount#">Geographicals [Z]</a> (#qBranchZCnt.cnt#)</cfoutput>
<!---<cfif qBranchZ.citeCnt neq ''>
	<cfoutput query="qBranchZ">
    <a href="item">#TreeNumber#-#DescriptorName#</a> (<a href="http://pubmed.gov?#citeCnt#">#citeCnt#</a>)
    </cfoutput>
<cfelse>
	Geographicals [Z] (0)
</cfif>--->
<br>

</p>    

  </div><!-- end #mainContent --> 
  
  
  
  <div id="footer">

    <p>Updated January 9, 2014</p>
    <p>2008-2014 Daniel Wendling and authors</p>
  </div><!-- end #footer --> 
  
</div>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script> 
<script>
// variable to hold current window state - small, medium, or large
var windowState = 'large';

// check intital screen width, respond with appropriate menu
$(document).ready(function() {
    var sw = document.body.clientWidth;
    if (sw < 481) {
       smMenu();
    } else if (sw >= 481 && sw <= 768) {
		medMenu();
	} else {
		lgMenu();
	}
});

// take care of resizing the window
$(window).resize(function() {
	var sw = document.body.clientWidth;
    if (sw < 481 && windowState != 'small') {
       smMenu();
    }
	if (sw > 480 && sw < 769 && windowState != 'medium') {
       medMenu();
    }  
    if (sw > 768 && windowState != 'large') {
       lgMenu();
    } 
});

function smMenu() {
	// since we may be switching from another menu, reset the menu first
	//unbind click and touch events    
    $('.menuToggle a').off('click');
    $('.topMenu').off('click touchstart');
	$('html').off('touchstart');
	$('#siteNav').off('touchstart');
	//reset the menu in case it's being resized from a medium screen    
    // remove any expanded menus
	$('.expand').removeClass('expand');
	$('.menuToggle').remove();
    //now that the menu is reset, add the toggle and reinitialize the indicator
     $('.topMenu').before('<div class="menuToggle"><a href="#">MENU<span class="indicator">+</span></a></div>');
    // append the + indicator
// for multi-intCount menues  $('.topMenu').append('<span class="indicator">+</span>');

    // wire up clicks and changing the various menu states
	//we'll use clicks instead of touch in case a smaller screen has a pointer device
	//first, let's deal with the menu toggle
	$('.menuToggle a').click(function() {
		//expand the menu
		$('.topMenu').toggleClass('expand');
		// figure out whether the indicator should be changed to + or -
		var newValue = $(this).find('span.indicator').text() == '+' ? '-' : '+';
		// set the new value of the indicator
		$(this).find('span.indicator').text(newValue);
	});
	
	//now we'll wire up the submenus
	$(".topMenu h3").click(function() {
		//find the current submenu
		var currentItem = $(this).siblings('.submenu');
		//remove the expand class from other submenus to close any currently open submenus
		$('ul.submenu').not(currentItem).removeClass('expand');
		//change the indicator of any closed submenus 
		$('.topMenu h3').not(this).find('span.indicator:contains("-")').text('+');
		//open the selected submenu
		$(this).siblings('.submenu').toggleClass('expand');
		//change the selected submenu indicator
		var newValue = $(this).find('span.indicator').text() == '+' ? '-' : '+';
        $(this).find('span.indicator').text(newValue);
	});
	//indicate current window state
	windowState = 'small';
}

function medMenu() {
	//reset the menu in case it's being resized from a small screen
	// unbind click events    
    $('.menuToggle a').off('click');
    $('.topMenu').off('click');
    // remove any expanded menus
	$('.expand').removeClass('expand');
    // remove the span tags inside the menu
    $('.topMenu').find('span.indicator').remove();
    // remove the "menu" element
    $('.menuToggle').remove();
	
	//check to see if the device supports touch
	//we'll use touch events instead of click as it will allow us
	//to support both a CSS-driven hover and touch enabled
	//menu for this screen range
	if ('ontouchstart' in document.documentElement)
    {
		//find all 'hover' class and strip them
		 $('.topMenu').find('li.hover').removeClass('hover');
		 //add touch events to submenu headings
		 $(".topMenu").bind('touchstart', function(e){
			//find the current submenu
			var currentItem = $(this).siblings('.submenu');
			//remove the expand class from other submenus to close any currently open submenus
			$('ul.submenu').not(currentItem).removeClass('expand');
			//open the selected submenu
			$(this).siblings('.submenu').toggleClass('expand');
		});
		//close submenus if users click outside the menu
		$('html').bind('touchstart', function(e) {
			$('.topMenu').find('ul.submenu').removeClass('expand');
		});
		//stop clicks on the menu from bubbling up
		$('#siteNav').bind('touchstart', function(e){
          	e.stopPropagation();
       });
	}
	//indicate current window state
	windowState = 'medium';
}

function lgMenu() {
    //largely what we'll do here is simple remove functionality that
	//may be left behind by other screen sizes
	//at this size the menu will function as a pure-css driven dropdown
	//advances in touch screen are beginning to make us re-think
	//this approach
    // unbind click and touch events    
    $('.menuToggle a').off('click');
    $('.topMenu').off('click touchstart');
	$('html').off('touchstart');
	$('#siteNav').off('touchstart');
    
    // remove any expanded submenus
    $('.topMenu').find('ul.submenu').removeClass('expand');
    
    // remove the span tags inside the menu
    $('.topMenu').find('span.indicator').remove();
    
    // remove the "menu" element
    $('.menuToggle').remove();
	
    //indicate current window state
    windowState = 'large';
}

</script>
</body>
</html>
