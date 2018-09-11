<!---
Name:        http://localhost:8500/_pubmed2015/mesh/index.cfm
Author:      Dan Wendling (dan.wendling@nih.gov)
Description: Record Set Analyzer - Browse records through the MeSH tree
Created:     1/5/2014
Modified:    1/11/2014

Based on an example at http://stackoverflow.com/questions/9220172/using-jquery-ajax-json-format-how-do-you-output-a-query-from-a-cfm-page-to-the 
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
<title>PubMed Record Set Analyzer - home</title>
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

    <script type="text/javascript"> 
    $(document).ready(function(){ 

    $("#runQuery").click(function () {

        $.ajax({
            type: "GET",
            url: "getBranches.cfm?CurrDataSetID=#CurrDataSetID#&intCount=#intCount#",
            dataType: "json",
            success: function (resp, textStatus, jqXHR) {
                buildResultsList(resp);
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                alert(errorThrown); 
            }
        });
    });


    function buildResultsList(resp)
    {
        var tmp_html = $("<li/>");
        var j = 0;

            $("#results").html(""); 

            for (j = 0; j < resp["DATA"].length; j++)
            {
                tmp_html = $("<tr />");

                for (var i = 0; i < resp["DATA"][j].length; i++)
                {
                    var tmp_td = $("<td />");   
                    tmp_td.text(resp["DATA"][j][i]);
                    tmp_html.append(tmp_td);
                }
                $("#results").append(tmp_html);
            }

    }

    })
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
<p><strong>(This application needs to access jQuery remotely.)</strong></p>


<p> 
<!--- Anatomy [A] --->
<cfoutput><a href="##" id="runQuery">Anatomy [A]</a> (#qBranchACnt.cnt#)</cfoutput>
<table id="results" cellspacing="0" cellpadding="0" border="1">

</table>

<cfdump var="#resp#">


<!---<cfif qBranchA.citeCnt neq ''>
	<cfoutput query="qBranchA">
	<a href="index.cfm?intCount=#intCount#">#TreeNumber#-#DescriptorName#</a> (<a href="http://pubmed.gov?#citeCnt#">#citeCnt#</a>)
    </cfoutput>
<cfelse>
	Anatomy [A] (0)
</cfif>--->
<br>

<!---    <input type="button" id="runQuery" value="Show Teams" />--->


  </div><!-- end #mainContent --> 
  
  
  
  <div id="footer">

    <p>Updated January 11, 2014</p>
    <p>2008-2014 Daniel Wendling and authors</p>
  </div><!-- end #footer --> 
  
</div>

</body>
</html>

