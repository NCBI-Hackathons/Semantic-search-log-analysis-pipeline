<!---
Name:        http://localhost:8500/_pubmed2015/mesh/index.cfm
Author:      Dan Wendling (dan.wendling@nih.gov)
Description: Record Set Analyzer - Browse records through the MeSH tree
Created:     1/5/2014
Modified:    1/20/2015

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


<cfparam name="description" type="string" default="Clinical Trials Strategy 1">
<cfparam name="recCount" type="string" default="5,337">
<cfparam name="dateRetrieved" type="string" default="1/20/2015">
<!---Search strategy; for syntax use cf. http://meyerweb.com/eric/tools/dencoder/ --->
<cfparam name="FORM.encoding" type="string" default="%28%28randomized%20controlled%20trial%5Bpt%5D%20OR%20controlled%20clinical%20trial%5Bpt%5D%20AND%20randomized%5BTitle%2FAbstract%5D%20OR%20randomised%5BTitle%2FAbstract%5D%20OR%20placebo%5BTitle%2FAbstract%5D%20OR%20%22clinical%20trials%20as%20topic%22%5BMeSH%20Terms%3Anoexp%5D%20OR%20randomly%5BTitle%2FAbstract%5D%20OR%20trial%5BTi%5D%20NOT%20%22meta-analysis%22%5BTitle%2FAbstract%5D%20NOT%20retrospective%5BTitle%2FAbstract%5D%29%20AND%20medline%5Bsb%5D%20AND%20%282013%3A2013%5Bdp%5D%29%20AND%20%22humans%22%5BMeSH%20Terms%5D%20AND%20hasabstract%5Btext%5D%20AND%20English%5Blang%5D%20AND%20%28ANZCTR%5Bsi%5D%20OR%20ReBec%5Bsi%5D%20OR%20ChiCTR%5Bsi%5D%20OR%20CRiS%5Bsi%5D%20OR%20CTRI%5Bsi%5D%20OR%20RPCEC%5Bsi%5D%20OR%20EudraCT%5Bsi%5D%20OR%20DRKS%5Bsi%5D%20OR%20IRCT%5Bsi%5D%20OR%20JPRN%5Bsi%5D%20OR%20NTR%5Bsi%5D%20OR%20PACTR%5Bsi%5D%20OR%20SLCTR%5Bsi%5D%20OR%20clinicaltrials.gov%5Bsi%5D%20OR%20ISRCTN%5Bsi%5D%20OR%20TCTR%5Bsi%5D%20OR%20%22trial%20registration%22%5BTitle%2FAbstract%5D%20OR%20%22trial%20registry%22%5BTitle%2FAbstract%5D%29%20NOT%20%22observational%20study%22%5BTi%5D%20NOT%20%22prospective%22%5BTi%5D%29">
<cfparam name="URL.CurrDataSetID" type="string" default="109">




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


variables.qBranchMCnt = meshTree.getBranchMCnt(filter);
variables.qBranchM = meshTree.getBranchM(filter);

</cfscript>

<cfparam name="url.DescriptorName" default="">
<cfparam name="url.MeshMajorTopicYN" default="">

<cfset todayDate = Now()>


<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><cfoutput>#description#</cfoutput> - MeSH Explorer</title>
<link href="../_styles/boilerplate.css" rel="stylesheet" type="text/css">
<link href="../_styles/main.css" rel="stylesheet" type="text/css">
<!--[if lt IE 9]>
<script src="//html5shiv.googlecode.com/svn/trunk/html5.js"></script>
<![endif]-->
<script src="../_scripts/respond.min.js"></script>
<link rel="stylesheet" href="dist/themes/default/style.min.css" />
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
            <li><a href="#request.cfg.applicationUrlPath()#index.cfm" title="Home">Home (record sets)</a></li>
            <li><a href="#request.cfg.applicationUrlPath()#/drilldown/index.cfm?CurrDataSetID=#CurrDataSetID#" title="drilldown">drilldown interface</li>
			<li><a href="#request.cfg.applicationUrlPath()#/topicReports/index.cfm?CurrDataSetID=#CurrDataSetID#" title="Static reports">Static-report generator</li>
			<li>MeSH Explorer</li>
        </cfoutput></ul>

  </div><!-- end #siteNav -->

  </div><!--end header-->

  <div id="mainContent">
    <a id="skipnav" name="skip"></a>


<h1>Tree of medical subject headings - the MeSH Explorer for PubMed</h1>

<p>This cut-down, browse-able version of the <a href="http://www.ncbi.nlm.nih.gov/mesh/1000048" target="_blank">MeSH tree</a> was designed for the stage of literature analysis projects when <strong>exploration and drilldown</strong> are ends in themselves. Click on the "expand" triangle icons on the left side of the entries below to understand how the items in your record set have been indexed. Any term with a record count behind it can be clicked upon, and this will take you to that group of records at <a href="http://pubmed.gov">pubmed.gov</a>. If you would like to see the more complicated, full MeSH tree for your project, contact <a href="mailto:wendlingd@mail.nlm.nih.gov">Dan Wendling</a>. More information about what you're seeing here, and a few caveats/limitations, are <a href="#whatYourSeeing">below</a>.</p>

<p>Here is your search without modification - <a href="http://www.ncbi.nlm.nih.gov/pubmed/?term=<cfoutput>#encoding#</cfoutput>" target="_blank"><cfoutput>#encoding#</cfoutput></a></p>


<h2>Browse topics in <cfoutput><em>#description#</em> record set: #recCount# records (as of #dateRetrieved#)</cfoutput><!---for the record set <cfoutput>#qDataSetInfo.DataSetName#</cfoutput>---></h2>

<div id="tree"></div><!---end meshTree--->

<!-- include the jQuery library -->
<script src="dist/libs/jquery.js"></script>
<!---Bootstrap for leaf node icons--->
<link rel="stylesheet" href="bootstrap/css/bootstrap.min.css">
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
	   var viewRecords = window.open('http://www.ncbi.nlm.nih.gov/pubmed/?report=abstract&term=' + newTerm  + '%5Bmh%5D+AND+' + '<cfoutput>#encoding#</cfoutput>',
	   '_blank',
	   '');
});

</script>

<!--- Doesn't work - call to NCBI's MeSH database upon double-clicking. Google setTimeOut jQuery

$('#tree').delegate('a','dblclick',function () {
       var newTerm = $(this).parent().attr('id');
	   var viewRecords = window.open('http://www.ncbi.nlm.nih.gov/mesh/?term=' + newTerm,
	   '_blank',
	   '');
});
--->


<!---
https://groups.google.com/forum/#!searchin/jstree/dblclick/jstree/7k6KQ2FS9K0/FnyaQ2ltg40J
$.jstree._reference(e.target);

$("#tree").delegate("a","dblclick",function () {
  $("#tree").jstree("remove", this);
})

$('a').on('dblclick', (function() {

--->
<h2><a id="whatYourSeeing" name="whatYourSeeing"></a>What you're seeing here</h2>

<p><strong>Contact Dan if you want to view Publication Characteristics; I have to manually change the code from a trailing &quot;[mh]&quot; to a trailing &quot;[Publication Type].&quot;</strong> Later I can update the code so this is not a problem.</p>

<ul>
    <li>The 2014 MeSH (Medical Subject Headings) tree structure and pubmed.gov are products of the National Library of Medicine. For more information see:
        <ul>
            <li><a href="http://www.nlm.nih.gov/mesh/meshhome.html" target="_blank">http://www.nlm.nih.gov/mesh/meshhome.html</a></li>
            <li><a href="http://www.ncbi.nlm.nih.gov/mesh" target="_blank">http://www.ncbi.nlm.nih.gov/mesh</a></li>
            <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/" target="_blank">http://www.ncbi.nlm.nih.gov/pubmed/</a></li>
            <li><a href="http://www.nlm.nih.gov/bsd/disted/pubmed.html" target="_blank">http://www.nlm.nih.gov/bsd/disted/pubmed.html</a></li>
        </ul></li>
    <li>This interface was designed to give experienced PubMed searchers a way to more deeply understand how the records in their search retrievals have been indexed.</li>
    <li>PubMed records, which are usually descriptions of journal articles, are assigned MeSH controlled vocabulary within a month or so of their arrival in PubMed.</li>
    <li>The MeSH tree is a hierarchical view of more than 12,000 terms; one term can appear in many places within the MeSH tree. This interface does not tell you whether this is happening; when you go to pubmed.gov, the term name is used, not the MeSH tree number, so you are crossing branches of the MeSH tree when you go to pubmed.gov.</li>
    <li>While some terms appear in one area of the tree with no narrower terms, and in other areas of the tree <em>with</em> narrower terms, this tool will currently show all child terms, whether they are in the current branch of the tree or not.</li>
    <li>For those learning MeSH: the click that currently takes the user to records at pubmed.gov, can be changed to point to that term's page in NCBI's MeSH database.</li>
    <li> Record counts will get smaller as you go down the tree, most of the time. This is how it is supposed to work, mirroring the &quot;explode down&quot; function of PubMed. However, numbers can rise as you drill down, when a term appears in multiple branches but the term's child elements are different across the branches. For example, Disciplines and Occupations &gt; Health Occupations &gt; Medicine &gt; Physical and Rehabilitation Medicine, and the item below it, Rehabilitation - in one case, PRM had a count of 15 and Rehabilitation beneath it had a count of 457; then Self Care below Rehabilitation had a count of 462.</li>
    <li>Frequent users should read NCBI's <a href="http://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.Usage_Guidelines_and_Requiremen" target="_blank">Usage Guidelines and Requirements</a>.</li>
</ul>

  </div><!-- end #mainContent -->



  <div id="footer">

    <p>Updated February 14, 2014</p>
    <p>2008-2014 Daniel Wendling and authors</p>
  </div><!-- end #footer -->

</div>

</body>
</html>

