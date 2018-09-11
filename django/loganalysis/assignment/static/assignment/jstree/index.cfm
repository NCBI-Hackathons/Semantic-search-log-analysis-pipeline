<!---
Name:        http://localhost:8500/_pubmed2015/130/index.cfm
Author:      Dan Wendling (dan.wendling@nih.gov)
Description: Record Set Analyzer - Browse records through the MeSH tree
Created:     1/26/2015
Modified:    10/1/2017

ENCODING IS AUTOMATIC HERE, BUT YOU MUST ADD IT TO ajax_childrenCF.cfm

Help from:
- http://www.jstree.com/
	[docs]: http://jstree.com/docs
	[demo]: http://jstree.com/demo
- http://simpledotnetsolutions.wordpress.com/2012/11/25/jstree-few-examples-with-asp-netc/

Later:
- Disambiguate "Information Science" branch; will not load for some reason.
- Add leaf node icon using test on new column, leafNodeYN.
- Radio button to browse either all descriptors, or just [majr].
 --->


<!--- Variables --->
	<cfparam name="url.CurrDataSetID" default="180" />

<!--- Don't need the below any more; gotten from the dataset table.
<cfparam name="FORM.encoding" type="string" default="%28mindfulness%29">
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
  variables.drilldown = CreateObject("component", "cfc.drilldown");

//Info about the data set we're working with
variables.qDataSetInfo = drilldown.getDataSetInfo();

//Total count of records in record set
  variables.TotDataSetCnt = drilldown.getTotDataSetCnt();


//searchLimits -----------------------------------------------------------------------------
  variables.qRecordscount = meshTree.getRecords(filter);

//Branches -----------------------------------------------
variables.intCount="1";


variables.qBranchMCnt = meshTree.getBranchMCnt(filter);
variables.qBranchM = meshTree.getBranchM(filter);

</cfscript>


<cfparam name="url.FullName" default="">
<cfparam name="url.CollectiveName" default="">
<cfparam name="url.NameOfSubstance" default="">
<cfparam name="url.Agency" default="">
<cfparam name="url.GrantID" default="">
<cfparam name="url.GrantCountry" default="">
<cfparam name="url.DescriptorName" default="">
<cfparam name="url.DescriptorNameMajor" default="">
<cfparam name="url.MeshMajorTopicYN" default="">
<cfparam name="url.PublicationType" default="">
<cfparam name="url.DateCreated" default="">
<cfparam name="url.DateCreatedYear" default="">
<cfparam name="url.PubPreferredCiteYear" default="">
<cfparam name="url.PubModel" default="">
<cfparam name="url.PubDateYear" default="">
<cfparam name="url.ArticleDateType" default="">
<cfparam name="url.ArticleDateYear" default="">
<cfparam name="url.CitationStatus" default="">
<cfparam name="url.JournalTitle" default="">
<cfparam name="url.JournalCountry" default="">

<cfset todayDate = Now()>



<!DOCTYPE html>
<html lang="en"><head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <!--- <link rel="icon" href="http://getbootstrap.com/favicon.ico"> --->

    <title>MeSH tree browser - Record Set Analyzer</title>


    <!-- Bootstrap core CSS -->
    <link href="/_pubmed2015/assets/styles/bootstrap332.css" rel="stylesheet">
<link rel="stylesheet" type="text/css" href="/_pubmed2015/assets/styles/bootstrap332_dashboard.css"/>

    <!-- Custom styles for this template -->
    <link href="/_pubmed2015/assets/styles/bootstrap332_dashboard.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
<link rel="stylesheet" type="text/css" href="/_pubmed2015/assets/styles/boilerplate.css"/>

<!--[if lt IE 9]>
<script src="//html5shiv.googlecode.com/svn/trunk/html5.js"></script>
<![endif]-->
<script src="../_scripts/respond.min.js"></script>
<link rel="stylesheet" href="dist/themes/default/style.min.css" />

	<script src="/_pubmed2015/assets/scripts/jquery-1.11.2.min.js"></script>
    <script src="/_pubmed2015/assets/scripts/bootstrap332.js"></script>


  </head>

  <body>
	<a href="#content" class="sr-only sr-only-focusable">Skip to main content</a>

    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="/_pubmed2015/index.cfm">Record Set Analyzer for data from pubmed.gov</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav navbar-right">
             <li><a href="https://wiki.nlm.nih.gov/confluence/display/common/Record+Set+Analyzer+for+PubMed" target="_blank">Wiki support</a></li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-3 col-md-2 sidebar">
          <ul class="nav nav-sidebar">
			<li><a href="/_pubmed2015/index.cfm" title="Record sets">List of record sets</a></li>
			<cfoutput>
            <li><a href="/_pubmed2015/topicReports/index.cfm?CurrDataSetID=#CurrDataSetID#" title="Topic reports">Topic reports</a></li>
            <li><a href="/_pubmed2015/drillDown/index.cfm?CurrDataSetID=#CurrDataSetID#">Analyst interface with drill-downs</a></li>
            <li class="active"><a href="/_pubmed2015/treeBrowser/#CurrDataSetID#/index.cfm?CurrDataSetID=#CurrDataSetID#" title="Subject headings tree-MeSH">MeSH tree browser <span class="sr-only">(current)</span></a></li>
			<li><a href="/_pubmed2015/exportBroadTopics/index.cfm?CurrDataSetID=#CurrDataSetID#">Export broad topics</a></li>

  			<!--- <li><a href="pdf_export.cfm?CurrDataSetID=#CurrDataSetID#">Create a PDF report</a></li> --->
			</cfoutput>
          </ul>
        </div>

        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
<div id="content">

<cfoutput>
          <h1 class="page-header" style="font-size:1.5em;margin-top:-8px;font-weight:600;"><em><u>Me</u></em>dical <em><u>S</u></em>ubject <em><u>H</u></em>eadings (MeSH) tree browser for <strong>'#qDataSetInfo.DataSetName#'</strong></h1>


<p><strong>#numberFormat(qRecordscount,'9,999')#</strong> records retrieved for this search as of #dateFormat(qDataSetInfo.DateRetrieved, "mm/dd/yyyy")#.</p>
</cfoutput>

<p class="bg-info"><strong>Click the triangles to browse by topic.</strong><br>
Any term with a record count after it can be clicked upon, and this will take you to that group of records at <a href="http://pubmed.gov">pubmed.gov</a>, within a new browser tab or window. Below the tree you will find <a href="#whatYourSeeing">caveats, limitations and assistance</a>. To start with, you should know that <a href="http://www.nlm.nih.gov/mesh/introduction.html">2015 MeSH from the U.S. National Library of Medicine</a> contains 27,455 descriptor terms; in this hierarchical tree, some of the 27,455 descriptors appear more than once (<a href="http://www.ncbi.nlm.nih.gov/mesh/68017624">WAGR Syndrome</a> appears in 20 tree locations); with this redunancy the tree contains 56,341 total &quot;nodes.&quot; Also, one PubMed record can have 15 MeSH terms assigned (some have more than 25). This is a very large information space with a lot of redundancy - great for learners but not so great for accountants looking for exclusive categories! Lastly, some records that you would be able to retrieve from pubmed.gov using search terms in the title and abstract field may not have MeSH terms assigned to them yet, so they won't appear here. Usually these are records added to the database in the past month or two.
</p>

<p class="bg-danger">Start by clicking a triangle.</p>


<div id="tree"></div><!---end meshTree--->

<!-- include the jQuery library -->
<script src="dist/libs/jquery.js"></script>
<!---Bootstrap for leaf node icons--->
<!--- <link rel="stylesheet" href="bootstrap/css/bootstrap.min.css"> --->
<script src="bootstrap/js/bootstrap.min.js"></script>

<!-- include the minified jstree source -->
<script src="dist/jstree.min.js"></script>

<script>
$(function () {
	$('#tree').jstree({
		'core' : {
		  'data' : {
			'url' : function (node) {
			  return node.id === '#' ?
				'ajax_treeTop.html' :
				'ajax_childrenCF.cfm';
			},
			'state' : {'opened' : true},
			'data' : function (node) {
			  return { 'id' : node.id };
			}
		  }
		}
	});
});

$('#tree').delegate('a','click',function () {
       var newTerm = $(this).parent().attr('id');
	   var viewRecords = window.open('http://www.ncbi.nlm.nih.gov/pubmed/?report=abstract&term=' + newTerm  + '%5Bmh%5D+AND+' + '<cfoutput>#qDataSetInfo.EncodedSearchURL#</cfoutput>',
	   '_blank',
	   '');
});

</script>



<a id="whatYourSeeing" name="whatYourSeeing"></a>
<h2 class="sub-header" style="font-size:1.2em;">More about this tool</h2>

<ul>

<li>The 2014 MeSH (Medical Subject Headings) tree structure and pubmed.gov are products of the National Library of Medicine. For more information see:
        <ul>
            <li><a href="http://www.ncbi.nlm.nih.gov/mesh/1000048">NCBI MeSH tree top</a></li>
			<li><a href="http://www.nlm.nih.gov/mesh/meshhome.html" target="_blank">http://www.nlm.nih.gov/mesh/meshhome.html</a></li>
            <li><a href="http://www.ncbi.nlm.nih.gov/mesh" target="_blank">http://www.ncbi.nlm.nih.gov/mesh</a></li>
            <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/" target="_blank">http://www.ncbi.nlm.nih.gov/pubmed/</a></li>
            <li><a href="http://www.nlm.nih.gov/bsd/disted/pubmed.html" target="_blank">http://www.nlm.nih.gov/bsd/disted/pubmed.html</a></li>
        </ul></li>

<li><cfoutput>This is <a href="http://www.ncbi.nlm.nih.gov/pubmed/?term=<cfoutput>#qDataSetInfo.EncodedSearchURL#</cfoutput>" target="_blank">your search strategy at pubmed.gov</a></cfoutput>, with no MeSH terms paired with it. </li>

<li>If you would like a more targeted version of the MeSH tree for your project, contact <a href="mailto:wendlingd@mail.nlm.nih.gov">Dan Wendling</a>.</li>

<li><strong>Contact Dan if you want to view Publication Characteristics at pubmed.gov; I have to manually change my code from a trailing &quot;[mh]&quot; to a trailing &quot;[Publication Type].&quot;</strong> Workaround: You can activate the pubmed search, and at pubmed.gov, change the address bar tag from mh (MeSH terms) to pt (publication type).</li>

<li>This version of the <a href="http://www.ncbi.nlm.nih.gov/mesh/1000048" target="_blank">MeSH tree</a> helps literature analysis projects in the <strong>exploration and drilldown</strong> phase. People doing other tasks, such as accounting for grantee research outputs, should keep in mind that one PubMed record can have 15 terms applied, so one PubMed record can be counted within several or many of these branches.</li>

<li>While the tree is currently set to return any assigned MeSH terms, Dan is able to restrict retrievals to records that were designated as major topics of the article. However the current setting provides more coverage of audiences and other metadata that would otherwise be lost.</li>

<li>Unlike the drilldown interface, these counts are from the live pubmed.gov database.</li>
    <li>This interface was designed to give experienced PubMed searchers a way to more deeply understand how the records in their search retrievals have been indexed.</li>
    <li>PubMed records, which are usually descriptions of journal articles, are assigned MeSH controlled vocabulary within a month or so of their arrival in PubMed.</li>
    <li>The MeSH tree is a hierarchical view of more than 12,000 terms; one term can appear in many places within the MeSH tree. This interface does not tell you whether this is happening; when you go to pubmed.gov, the term name is used, not the MeSH tree number, so you are crossing branches of the MeSH tree when you go to pubmed.gov. (Just like a typical pubmed.gov search session would.)</li>
	<li>Because some of the 12,000 terms in this hierarchy appear in multiple branches within the tree, the number of nodes available in this drill-down interface is approximately 50,000.</li>
    <li>While some terms appear in one area of the tree with no narrower terms, and in other areas of the tree <em>with</em> narrower terms, this tool will currently show all child terms, whether they are in the current branch of the tree or not.</li>
    <li>For those whose primary interest is learning MeSH: the click that currently takes the user to records at pubmed.gov, can be changed to point to that term's page in NCBI's MeSH database.</li>
    <li>Record counts will get smaller as you go down the tree, most of the time. This is how it is supposed to work, mirroring the &quot;explode down&quot; function of PubMed. However, numbers will rise as you drill down when a term appears in multiple branches but the term's child elements are different across the branches. For example, Disciplines and Occupations &gt; Health Occupations &gt; Medicine &gt; Physical and Rehabilitation Medicine, and the item below it, Rehabilitation - in one case, PRM had a count of 15 and Rehabilitation beneath it had a count of 457; then Self Care below Rehabilitation had a count of 462. This is not a counting error in this interface, although it's puzzling to see.</li>
    <li><strong>report=abstract:</strong> Currently, the pubmed.gov reports here are verbose (called the Abstract report). Other available reports include DocSum (default display on pubmed.gov, except for a single citation), MEDLINE, and XML.</li>
	<li>Frequent users should read NCBI's <a href="http://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.Usage_Guidelines_and_Requiremen" target="_blank">Usage Guidelines and Requirements</a>.</li>
</ul>

</div>
        </div>
      </div>
    </div>

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="/_pubmed2015/assets/scripts/ie10-viewport-bug-workaround.js"></script>


<!---
<div data-original-title="Copy to clipboard" title="" style="position: absolute; left: 0px; top: -9999px; width: 15px; height: 15px; z-index: 999999999;" class="global-zeroclipboard-container" id="global-zeroclipboard-html-bridge">      <object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" id="global-zeroclipboard-flash-bridge" height="100%" width="100%">         <param name="movie" value="/assets/flash/ZeroClipboard.swf?noCache=1422282377118">         <param name="allowScriptAccess" value="sameDomain">         <param name="scale" value="exactfit">         <param name="loop" value="false">         <param name="menu" value="false">         <param name="quality" value="best">         <param name="bgcolor" value="#ffffff">         <param name="wmode" value="transparent">         <param name="flashvars" value="trustedOrigins=getbootstrap.com%2C%2F%2Fgetbootstrap.com%2Chttp%3A%2F%2Fgetbootstrap.com">
<embed src="../assets/styles/ZeroClipboard.swf" loop="false" menu="false" quality="best" bgcolor="#ffffff" name="global-zeroclipboard-flash-bridge" allowscriptaccess="sameDomain" allowfullscreen="false" type="application/x-shockwave-flash" wmode="transparent" pluginspage="http://www.macromedia.com/go/getflashplayer" flashvars="trustedOrigins=getbootstrap.com%2C%2F%2Fgetbootstrap.com%2Chttp%3A%2F%2Fgetbootstrap.com" scale="exactfit" height="100%" width="100%">                </object></div><svg style="visibility: hidden; position: absolute; top: -100%; left: -100%;" preserveAspectRatio="none" viewBox="0 0 200 200" height="200" width="200"><defs></defs><text style="font-weight:bold;font-size:10pt;font-family:Arial, Helvetica, Open Sans, sans-serif;dominant-baseline:middle" y="10" x="0">200x200</text></svg>
 --->

	</body>
</html>