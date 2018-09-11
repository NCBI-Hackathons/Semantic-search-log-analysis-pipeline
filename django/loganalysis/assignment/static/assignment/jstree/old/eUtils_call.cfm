<!---
Name:        http://localhost:8500/_pubmed2015/mesh/eUtils_call.cfm
Author:      Dan Wendling (dan.wendling@nih.gov)
Description: Record Set Analyzer - Browse records through the MeSH tree
Created:     1/23/2014
Modified:    1/23/2014

jQuery:

http://api.jquery.com/jQuery.get/


eUtils:

Quick Start: http://www.ncbi.nlm.nih.gov/books/NBK25500/
In Depth: http://www.ncbi.nlm.nih.gov/books/NBK25499/
ESearch: http://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch

Base eUtils URL: http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=MeSH_TERM&rettype=count



Other:

http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2904758/
https://github.com/hubgit/jquery-eutils

 --->


<cfsetting showdebugoutput="false"/>

<!--- Variables --->
	<cfparam name="url.CurrDataSetID" default="71" />
	<cfparam name="url.intCount" default="15" />
<!--- intCounts can be 1, 3, 7, 11, 15... --->

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
</cfscript>

<cfparam name="url.DescriptorName" default="">
<cfparam name="url.MeshMajorTopicYN" default="">

<cfset todayDate = Now()>



<!---
CFC is learncf_jquery.cfc
test.cfm output looks like: {"COLUMNS":["TEAM"],"DATA":[["Dallas Cowboys"],["NY Giants"],["Philadelphia Eagles"],["Washington Redskins"]]}
--->

<!---
A somewhat similar tutorial on reading in the contents of an XML file, 
http://www.lynda.com/CSS-tutorials/Retrieving-displaying-XML-data/133326/145990-4.html, 
Retrieving and Displaying XML Data, Joseph Lowery, Working with Data on the Web
--->


<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>eUtils_call</title>
<link href="../_styles/boilerplate.css" rel="stylesheet" type="text/css">
<link href="../_styles/main.css" rel="stylesheet" type="text/css">
<!--[if lt IE 9]>
<script src="//html5shiv.googlecode.com/svn/trunk/html5.js"></script>
<![endif]-->
<script src="../_scripts/respond.min.js"></script>
<!---<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-43296135-1', 'ponder-matic.com');
  ga('send', 'pageview');
</script>--->

<!--- jQuery-AJAX --->
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>


<!---reportresearch[sb]--->
    <script type="text/javascript">
	
    $(document).ready(function(){ 
		getRecordCount();
	});
      function getRecordCount() {
		  <cfoutput query="qBranchA">
		  var dbSearch = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=#DescriptorName#[mh]+AND+%28%28%28%22delivery+of+health+care%22%5BMeSH+Terms:noexp%5D+OR+%22health+behavior%22%5BMeSH+Terms%5D+OR+%22health+knowledge,+attitudes,+practice%22%5BMeSH+Terms%5D+OR+%22health+services+accessibility%22%5BMeSH+Terms%5D+OR+%22health+services,+indigenous%22%5BMeSH+Terms%5D+OR+%22mass+screening%22%5BMeSH+Terms%5D+OR+mass+screening%5BTIAB%5D+OR+mass+screenings%5BTIAB%5D+OR+health+inequality%5BTIAB%5D+OR+health+inequalities%5BTIAB%5D+OR+health+inequities%5BTIAB%5D+OR+health+inequity%5BTIAB%5D+OR+%22health+services+needs+and+demand%22%5BMeSH+Terms%5D+OR+%22patient+acceptance+of+health+care%22%5BMeSH+Terms%5D+OR+%22patient+selection%22%5BMeSH+Terms%5D+OR+%22quality+of+health+care%22%5BMeSH+Major+Topic:noexp%5D+OR+%22quality+of+life%22%5BMeSH+Terms%5D+OR+quality+of+life%5BTIAB%5D+OR+social+disparities%5BTIAB%5D+OR+social+disparity%5BTIAB%5D+OR+social+inequities%5BTIAB%5D+OR+social+inequity%5BTIAB%5D+OR+%22socioeconomic+factors%22%5BMeSH+Major+Topic%5D+OR+socioeconomic+factor%5BTIAB%5D+OR+socioeconomic+factors%5BTIAB%5D+OR+%22social+determinants+of+health%22%5BMeSH+Terms%5D%29+AND+%28African+American%5BTIAB%5D+OR+African+Americans%5BTIAB%5D+OR+African+ancestry%5BTIAB%5D+OR+%22african+continental+ancestry+group%22%5BMeSH+Terms%5D+OR+AIAN%5BTIAB%5D+OR+%22american+native+continental+ancestry+group%22%5BMeSH+Terms%5D+OR+%22asian+continental+ancestry+group%22%5BMeSH+Terms%5D+OR+Asian%5BTIAB%5D+OR+Asians%5BTIAB%5D+OR+black%5BTIAB%5D+OR+blacks%5BTIAB%5D+OR+Caucasian%5BTIAB%5D+OR+Caucasians%5BTIAB%5D+OR+diverse+population%5BTIAB%5D+OR+diverse+populations%5BTIAB%5D+OR+environmental+justice%5BTIAB%5D+OR+ethnic+group%5BTIAB%5D+OR+%22ethnic+groups%22%5BMeSH+Terms%5D+OR+ethnic+groups%5BTIAB%5D+OR+ethnic+population%5BTIAB%5D+OR+ethnic+populations%5BTIAB%5D+OR+ghetto%5BTIAB%5D+OR+ghettos%5BTIAB%5D+OR+Hispanic%5BTIAB%5D+OR+Hispanics%5BTIAB%5D+OR+Indian%5BTIAB%5D+OR+Indians%5BTIAB%5D+OR+Latino%5BTIAB%5D+OR+Latinos%5BTIAB%5D+OR+Latina%5BTIAB%5D+OR+Latinas%5BTIAB%5D+OR+%22medically+underserved+area%22%5BMeSH+Terms%5D+OR+minority+group%5BTIAB%5D+OR+%22minority+groups%22%5BMeSH+Terms%5D+OR+minority+groups%5BTIAB%5D+OR+minority+population%5BTIAB%5D+OR+minority+populations%5BTIAB%5D+OR+Native+American%5BTIAB%5D+OR+Native+Americans%5BTIAB%5D+OR+%22oceanic+ancestry+group%22%5BMeSH+Terms%5D+OR+pacific+islander%5BTIAB%5D+OR+pacific+islanders%5BTIAB%5D+OR+people+of+color%5BTIAB%5D+OR+%22poverty+areas%22%5BMeSH+Terms%5D+OR+poverty+area%5BTIAB%5D+OR+poverty+areas%5BTIAB%5D+OR+%22rural+health%22%5BMeSH+Terms%5D+OR+rural+health%5BTIAB%5D+OR+%22rural+health+services%22%5BMeSH+Terms%5D+OR+%22rural+population%22%5BMeSH+Terms%5D+OR+rural+population%5BTIAB%5D+OR+rural+populations%5BTIAB%5D+OR+slum%5BTIAB%5D+OR+slums%5BTIAB%5D+OR+%22urban+health%22%5BMeSH+Terms%5D+OR+%22urban+health+services%22%5BMeSH+Terms%5D+OR+%22urban+population%22%5BMeSH+Terms%5D+OR+urban+population%5BTIAB%5D+OR+urban+populations%5BTIAB%5D+OR+%22vulnerable+populations%22%5BMeSH+Terms%5D+OR+vulnerable+population%5BTIAB%5D+OR+vulnerable+populations%5BTIAB%5D+OR+white%5BTIAB%5D+OR+whites%5BTIAB%5D%29+OR+%28ethnic+disparities%5BTIAB%5D+OR+ethnic+disparity%5BTIAB%5D+OR+health+care+disparities%5BTIAB%5D+OR+health+care+disparity%5BTIAB%5D+OR+health+disparities%5BTIAB%5D+OR+health+disparity%5BTIAB%5D+OR+%22health+status+disparities%22%5BMeSH+Terms%5D+OR+%22healthcare+disparities%22%5BMeSH+Terms%5D+OR+healthcare+disparities%5BTIAB%5D+OR+healthcare+disparity%5BTIAB%5D+OR+%22minority+health%22%5BMeSH+Terms%5D+OR+minority+health%5BTIAB%5D+OR+racial+disparities%5BTIAB%5D+OR+racial+disparity%5BTIAB%5D+OR+racial+equality%5BTIAB%5D+OR+racial+equity%5BTIAB%5D+OR+racial+inequities%5BTIAB%5D+OR+racial+inequity%5BTIAB%5D+OR+%22ageism%22%5BMeSH+Terms%5D+OR+%22racism%22%5BMeSH+Terms%5D+OR+%22sexism%22%5BMeSH+Terms%5D+OR+%22social+discrimination%22%5BMeSH+Terms%5D+OR+%22social+marginalization%22%5BMeSH+Terms%5D%29%29+AND+2013%5BPDAT%5D+:+2014%5BPDAT%5D%29&rettype=count";
      	$.get( dbSearch, function(result) {
      		var theCnt = result.getElementsByTagName('Count')[0];
			var descriptor = '#DescriptorName#';
			var treeNumber = '#TreeNumber#'
			var treeLevel = #trLevel# + 1
      		var val = '<li><a href="eUtils_call.cfm?treeNumber=' + treeNumber + '&level=' + treeLevel + '" title="' + treeNumber + '-' + descriptor + '">' + descriptor + '</a> - ' + '<a href="http://pubmed.gov/?term=' + descriptor  + '[mh]+AND+%28%28%28%22delivery+of+health+care%22%5BMeSH+Terms:noexp%5D+OR+%22health+behavior%22%5BMeSH+Terms%5D+OR+%22health+knowledge,+attitudes,+practice%22%5BMeSH+Terms%5D+OR+%22health+services+accessibility%22%5BMeSH+Terms%5D+OR+%22health+services,+indigenous%22%5BMeSH+Terms%5D+OR+%22mass+screening%22%5BMeSH+Terms%5D+OR+mass+screening%5BTIAB%5D+OR+mass+screenings%5BTIAB%5D+OR+health+inequality%5BTIAB%5D+OR+health+inequalities%5BTIAB%5D+OR+health+inequities%5BTIAB%5D+OR+health+inequity%5BTIAB%5D+OR+%22health+services+needs+and+demand%22%5BMeSH+Terms%5D+OR+%22patient+acceptance+of+health+care%22%5BMeSH+Terms%5D+OR+%22patient+selection%22%5BMeSH+Terms%5D+OR+%22quality+of+health+care%22%5BMeSH+Major+Topic:noexp%5D+OR+%22quality+of+life%22%5BMeSH+Terms%5D+OR+quality+of+life%5BTIAB%5D+OR+social+disparities%5BTIAB%5D+OR+social+disparity%5BTIAB%5D+OR+social+inequities%5BTIAB%5D+OR+social+inequity%5BTIAB%5D+OR+%22socioeconomic+factors%22%5BMeSH+Major+Topic%5D+OR+socioeconomic+factor%5BTIAB%5D+OR+socioeconomic+factors%5BTIAB%5D+OR+%22social+determinants+of+health%22%5BMeSH+Terms%5D%29+AND+%28African+American%5BTIAB%5D+OR+African+Americans%5BTIAB%5D+OR+African+ancestry%5BTIAB%5D+OR+%22african+continental+ancestry+group%22%5BMeSH+Terms%5D+OR+AIAN%5BTIAB%5D+OR+%22american+native+continental+ancestry+group%22%5BMeSH+Terms%5D+OR+%22asian+continental+ancestry+group%22%5BMeSH+Terms%5D+OR+Asian%5BTIAB%5D+OR+Asians%5BTIAB%5D+OR+black%5BTIAB%5D+OR+blacks%5BTIAB%5D+OR+Caucasian%5BTIAB%5D+OR+Caucasians%5BTIAB%5D+OR+diverse+population%5BTIAB%5D+OR+diverse+populations%5BTIAB%5D+OR+environmental+justice%5BTIAB%5D+OR+ethnic+group%5BTIAB%5D+OR+%22ethnic+groups%22%5BMeSH+Terms%5D+OR+ethnic+groups%5BTIAB%5D+OR+ethnic+population%5BTIAB%5D+OR+ethnic+populations%5BTIAB%5D+OR+ghetto%5BTIAB%5D+OR+ghettos%5BTIAB%5D+OR+Hispanic%5BTIAB%5D+OR+Hispanics%5BTIAB%5D+OR+Indian%5BTIAB%5D+OR+Indians%5BTIAB%5D+OR+Latino%5BTIAB%5D+OR+Latinos%5BTIAB%5D+OR+Latina%5BTIAB%5D+OR+Latinas%5BTIAB%5D+OR+%22medically+underserved+area%22%5BMeSH+Terms%5D+OR+minority+group%5BTIAB%5D+OR+%22minority+groups%22%5BMeSH+Terms%5D+OR+minority+groups%5BTIAB%5D+OR+minority+population%5BTIAB%5D+OR+minority+populations%5BTIAB%5D+OR+Native+American%5BTIAB%5D+OR+Native+Americans%5BTIAB%5D+OR+%22oceanic+ancestry+group%22%5BMeSH+Terms%5D+OR+pacific+islander%5BTIAB%5D+OR+pacific+islanders%5BTIAB%5D+OR+people+of+color%5BTIAB%5D+OR+%22poverty+areas%22%5BMeSH+Terms%5D+OR+poverty+area%5BTIAB%5D+OR+poverty+areas%5BTIAB%5D+OR+%22rural+health%22%5BMeSH+Terms%5D+OR+rural+health%5BTIAB%5D+OR+%22rural+health+services%22%5BMeSH+Terms%5D+OR+%22rural+population%22%5BMeSH+Terms%5D+OR+rural+population%5BTIAB%5D+OR+rural+populations%5BTIAB%5D+OR+slum%5BTIAB%5D+OR+slums%5BTIAB%5D+OR+%22urban+health%22%5BMeSH+Terms%5D+OR+%22urban+health+services%22%5BMeSH+Terms%5D+OR+%22urban+population%22%5BMeSH+Terms%5D+OR+urban+population%5BTIAB%5D+OR+urban+populations%5BTIAB%5D+OR+%22vulnerable+populations%22%5BMeSH+Terms%5D+OR+vulnerable+population%5BTIAB%5D+OR+vulnerable+populations%5BTIAB%5D+OR+white%5BTIAB%5D+OR+whites%5BTIAB%5D%29+OR+%28ethnic+disparities%5BTIAB%5D+OR+ethnic+disparity%5BTIAB%5D+OR+health+care+disparities%5BTIAB%5D+OR+health+care+disparity%5BTIAB%5D+OR+health+disparities%5BTIAB%5D+OR+health+disparity%5BTIAB%5D+OR+%22health+status+disparities%22%5BMeSH+Terms%5D+OR+%22healthcare+disparities%22%5BMeSH+Terms%5D+OR+healthcare+disparities%5BTIAB%5D+OR+healthcare+disparity%5BTIAB%5D+OR+%22minority+health%22%5BMeSH+Terms%5D+OR+minority+health%5BTIAB%5D+OR+racial+disparities%5BTIAB%5D+OR+racial+disparity%5BTIAB%5D+OR+racial+equality%5BTIAB%5D+OR+racial+equity%5BTIAB%5D+OR+racial+inequities%5BTIAB%5D+OR+racial+inequity%5BTIAB%5D+OR+%22ageism%22%5BMeSH+Terms%5D+OR+%22racism%22%5BMeSH+Terms%5D+OR+%22sexism%22%5BMeSH+Terms%5D+OR+%22social+discrimination%22%5BMeSH+Terms%5D+OR+%22social+marginalization%22%5BMeSH+Terms%5D%29%29+AND+2013%5BPDAT%5D+:+2014%5BPDAT%5D%29">' + theCnt.firstChild.nodeValue + '</a></li>';
			$("##content").append(val);
			  
	  });</cfoutput>
      }
  </script>
        

<!---      //function successFn(result) {
		//$.each(result.items, function(i, item) {
			
			//$("<li>").attr("src", item.media.m).appendTo("#content");
			//if (i === 4) {
			//	return false;
		//	}
		//});
     // }
	  
     // function errorFn(xhr, status, strErr) {
      //  alert(strErr);--->
      

<!---	$.ajax({
		url: "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=MeSH_TERM&rettype=count",
	context: document.body
	}).done(function() {
	$( this ).addClass( "done" );
	})
	.done(function( data ) {
	if ( console && console.log ) {
	console.log( "Sample of data:", data.slice( 0, 100 ) );
	}
});--->
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

        </cfoutput></ul>  

  </div><!-- end #siteNav --> 
  
  </div><!--end header-->
  

  <div id="mainContent">
    <a id="skipnav" name="skip"></a>
  
      <h1>MeSH - Browse the MeSH tree</h1>

    <p>You can use these links to determine whether this record set includes records matching any of MeSH's 26 high-level "<a href="http://www.ncbi.nlm.nih.gov/mesh/1000067">Diseases category</a>" entries. NOTE: Some categories will be empty.</p>
    
    
    <ul id="content"></ul>
    
<p>&nbsp;</p>
    
    <table>
      <tbody>
        <tr>
          <th>MeSH-Diseases</th>
          <th align="right">Count?</th>
          <th align="right">% of cites<br>
            in data set</th>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68000820">Animal Diseases</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Animal+Diseases%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68001423">Bacterial Infections and Mycoses</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Bacterial+Infections+and+Mycoses%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68002318">Cardiovascular Diseases</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Cardiovascular+Diseases%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68009358">Congenital, Hereditary, and Neonatal Diseases and Abnormalities</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Congenital,+Hereditary,+and+Neonatal+Diseases+and+Abnormalities%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68004066">Digestive System Diseases</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Digestive+System+Diseases%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
<!---        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68007280">Disorders of Environmental Origin</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Disorders+of+Environmental+Origin%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68004700">Endocrine System Diseases</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Endocrine+System+Diseases%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68005128">Eye Diseases</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Eye+Diseases%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68005261">Female Urogenital Diseases and Pregnancy Complications</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Female+Urogenital+Diseases+and+Pregnancy+Complications%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68007280">Hemic and Lymphatic Diseases</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Hemic+and+Lymphatic+Diseases%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68007154">Immune System Diseases</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Immune+System+Diseases%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68052801">Male Urogenital Diseases</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Male+Urogenital+Diseases%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68009140">Musculoskeletal Diseases</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Musculoskeletal+Diseases%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68009369">Neoplasms</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Neoplasms%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68009422">Nervous System Diseases</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Nervous+System+Diseases%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68009750">Nutritional and Metabolic Diseases</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Nutritional+and+Metabolic+Diseases%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68009784">Occupational Diseases</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Occupational+Diseases%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68010038">Otorhinolaryngologic Diseases</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Otorhinolaryngologic+Diseases%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68010272">Parasitic Diseases</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Parasitic+Diseases%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68013568">Pathological Conditions, Signs and Symptoms</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Pathological+Conditions,+Signs+and+Symptoms%22[mh]reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68012140">Respiratory Tract Diseases</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Respiratory+Tract+Diseases%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68017437">Skin and Connective Tissue Diseases</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Skin+and+Connective+Tissue+Diseases%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68009057">Stomatognathic Diseases</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Stomatognathic+Diseases%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68017437">Substance-Related Disorders</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Substance-Related+Disorders%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68014777">Virus Diseases</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Virus+Diseases%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>
        <tr>
          <td><a href="http://www.ncbi.nlm.nih.gov/mesh/68014947">Wounds and Injuries</a></td>
          <td align="right"><a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%22Wounds+and+Injuries%22[mh]+AND+reportresearch[sb]">##</a></td>
          <td> </td>
        </tr>--->
      </tbody>
    </table>
    <p><a href="http://localhost:8500/_pubmed2015/topicReports/03_BroadTopics.cfm?CurrDataSetID=77#skip">(top)</a></p>
    <p>&nbsp;</p>





  </div><!-- end #mainContent --> 
  
  
  
  <div id="footer">

    <p>Updated January 23, 2014</p>
    <p>2008-2014 Daniel Wendling and authors</p>
  </div><!-- end #footer --> 
  
</div>

</body>
</html>

