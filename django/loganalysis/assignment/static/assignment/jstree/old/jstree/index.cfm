<!---
Name:        http://localhost:8500/_pubmed2015/mesh/jstree/index.cfm
Author:      Dan Wendling (dan.wendling@nih.gov)
Description: Record Set Analyzer - Browse records through the MeSH tree
Created:     1/5/2014
Modified:    1/11/2014

[docs]: http://jstree.com/docs
[demo]: http://jstree.com/demo

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
/*
variables.qBranchBCnt = meshTree.getBranchBCnt(filter);
//variables.qBranchB = meshTree.getBranchB(filter);

variables.qBranchCCnt = meshTree.getBranchCCnt(filter);
//variables.qBranchC = meshTree.getBranchC(filter);

variables.qBranchDCnt = meshTree.getBranchDCnt(filter);
//variables.qBranchD = meshTree.getBranchD(filter);

variables.qBranchECnt = meshTree.getBranchECnt(filter);
//variables.qBranchE = meshTree.getBranchE(filter);

variables.qBranchFCnt = meshTree.getBranchFCnt(filter);
//variables.qBranchF = meshTree.getBranchF(filter);

variables.qBranchGCnt = meshTree.getBranchGCnt(filter);
//variables.qBranchG = meshTree.getBranchG(filter);

variables.qBranchHCnt = meshTree.getBranchHCnt(filter);
//variables.qBranchH = meshTree.getBranchH(filter);

variables.qBranchICnt = meshTree.getBranchICnt(filter);
//variables.qBranchI = meshTree.getBranchI(filter);

variables.qBranchJCnt = meshTree.getBranchJCnt(filter);
//variables.qBranchJ = meshTree.getBranchJ(filter);

variables.qBranchKCnt = meshTree.getBranchKCnt(filter);
//variables.qBranchK = meshTree.getBranchK(filter);

variables.qBranchLCnt = meshTree.getBranchLCnt(filter);
//variables.qBranchL = meshTree.getBranchL(filter);

variables.qBranchMCnt = meshTree.getBranchMCnt(filter);
variables.qBranchM = meshTree.getBranchM(filter);

variables.qBranchNCnt = meshTree.getBranchNCnt(filter);
//variables.qBranchN = meshTree.getBranchN(filter);

variables.qBranchVCnt = meshTree.getBranchVCnt(filter);
//variables.qBranchV = meshTree.getBranchV(filter);

variables.qBranchZCnt = meshTree.getBranchZCnt(filter);
//variables.qBranchZ = meshTree.getBranchZ(filter);
*/
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
<title>jsTree - 3b4: Browse the MeSH Tree</title>
<link href="../../_styles/boilerplate.css" rel="stylesheet" type="text/css">
<link href="../../_styles/main.css" rel="stylesheet" type="text/css">
<!--[if lt IE 9]>
<script src="//html5shiv.googlecode.com/svn/trunk/html5.js"></script>
<![endif]-->
<script src="../../_scripts/respond.min.js"></script>

<link rel="stylesheet" href="vakata-jstree-1e2e7d9/dist/themes/default/style.min.css" />
<script src="vakata-jstree-1e2e7d9/dist/libs/jquery.js"></script>
<script src="vakata-jstree-1e2e7d9/dist/jstree.min.js"></script>

<script>
$(function() {
  $('#container').jstree(/* optional config object here */);
});
</script>
</head>


<body>
<div class="skipnavigation"><a class="skipnavigation" href="#skip" title="Skip the navigation on this page">Skip Navigation</a></div>

<div class="gridContainer clearfix">

  <div id="header">

    <div id="hgroup">
    <h1>PubMed Record Set Analyzer</h1>
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

<h1>jsTree - 3b4: Browse the MeSH Tree</h1>


<p>Counts and pubmed.gov links to records in the <strong>Research Guidelines specific topic query retrieved 1/4/2014</strong>. Notes:</p>

<ul>
  <li>Counts at pubmed.gov will be more accurate than the ones you see here. </li>
  <li>The top-level labels cannot be retrieved from pubmed.gov, because these terms do not appear in MeSH. Also, while terms are presented in tree structure, many terms appear in other parts of the tree. </li>
  <li>Later: Allow for browsing either all descriptors, or just major descriptors.</li>
  <li>Counts are based on unique PMIDs, representing the number of <em><strong>records</strong></em> you could retrieve by clicking on links to pubmed.gov. </li>
  <li>This application needs to access jQuery remotely.</li>
</ul>
<hr />

<h3>Named Groups [M]</h3>

<div id="container">
  <ul>
    <li>Root node
      <ul>
        <li id="child_node">Child node</li>
      </ul>
    </li>
  </ul>
</div>





<!--- Anatomy [A] --->

<h3>Anatomy</h3>


<!---<a href="http://www.ncbi.nlm.nih.gov/pubmed?term=Anatomy[mh]+AND+reportresearch[sb]" title="Records for Anatomy" target="_blank">item</a>--->


<!--- <cfoutput><a href="##" id="runQuery">Anatomy [A]</a> (#qBranchACnt.cnt#)</cfoutput>
<table id="results" cellspacing="0" cellpadding="0" style="margin-left:2em;">

</table>

<cfif qBranchA.citeCnt neq ''>
	<cfoutput query="qBranchA">
	<a href="index.cfm?intCount=#intCount#">#TreeNumber#-#DescriptorName#</a> (<a href="http://pubmed.gov?#citeCnt#">#citeCnt#</a>)
    </cfoutput>
<cfelse>
	Anatomy [A] (0)
</cfif> --->


<h3>Organisms</h3>
<p>(tree)</p>

<h3>Diseases</h3>
<p>(tree)</p>

<h3>Chemicals and Drugs</h3>
<p>(tree)</p>

<h3>Analytical, Diagnostic and Therapeutic Techniques and Equipment</h3>
<p>(tree)</p>

<h3>Psychiatry and Psychology</h3>
<p>(tree)</p>




<!--
Anatomy [A] (98) 
Organisms [B] (5256)
Diseases [C] (2192)
Chemicals and Drugs [D] (627)
Analytical, Diagnostic and Therapeutic Techniques and Equipment [E] (3902)
Psychiatry and Psychology [F] (4404)
Phenomena and Processes [G] (1130)
Disciplines and Occupations [H] (1466)
Anthropology, Education, Sociology and Social Phenomena [I] (4455)
Technology, Industry, Agriculture [J] (614)
Humanities [K] (535)
Information Science [L] (4099)Anatomy [A] (98)
Named Groups [M] (3840)
Health Care [N] (5274)
Publication Characteristics [V] (0)
Geographicals [Z] (2631) 
-->



<!---Listen for changes on the tree using events:--->

<script>
$(function () {
  $('#container').on('changed.jstree', function (e, data) {
    console.log(data.selected);
  });
});
</script>


<!---And interact with the tree:--->

<script>
$(function () {
	$('#container').jstree(true).select_node('child_node');
});
</script>



  </div><!-- end #mainContent --> 
  
  
  
  <div id="footer">

    <p>Updated January 21, 2014</p>
    <p>2008-2014 Daniel Wendling and authors</p>
  </div><!-- end #footer --> 
  
</div>

</body>
</html>

<!--
Anatomy [A] (98) 
Organisms [B] (5256)
Diseases [C] (2192)
Chemicals and Drugs [D] (627)
Analytical, Diagnostic and Therapeutic Techniques and Equipment [E] (3902)
Psychiatry and Psychology [F] (4404)
Phenomena and Processes [G] (1130)
Disciplines and Occupations [H] (1466)
Anthropology, Education, Sociology and Social Phenomena [I] (4455)
Technology, Industry, Agriculture [J] (614)
Humanities [K] (535)
Information Science [L] (4099)Anatomy [A] (98)
Named Groups [M] (3840)
Health Care [N] (5274)
Publication Characteristics [V] (0)
Geographicals [Z] (2631) 
-->