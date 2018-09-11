<!---
Name:        http://localhost:8500/_pubmed2015/mesh/index.cfm
Author:      Dan Wendling (dan.wendling@nih.gov)
Description: Record Set Analyzer - Browse records through the MeSH tree
Created:     1/25/2015
Modified:    1/25/2015

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

<!--- From tree file: --->
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



<!--- THE BELOW IS FROM THE BOOTSTRAP PAGE FOR drilldown. --->


<!--- Variables --->
	<cfparam name="url.CurrDataSetID" default="106" />

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
  variables.drilldown = CreateObject("component", "cfc.drilldown");

//Info about the data set we're working with
variables.qDataSetInfo = drilldown.getDataSetInfo();

//Total count of records in record set
  variables.TotDataSetCnt = drilldown.getTotDataSetCnt();

//Starting row count to recordsInventory.cfm; could have a cfparam default there instead?
  variables.MaxRowNo="200";

//searchLimits -----------------------------------------------------------------------------
  variables.qRecordscount = drilldown.getRecords(filter);

//drillDowns -----------------------------------------------
variables.cntAgency = drilldown.getAgency(filter);
variables.cntPubYearPrint = drilldown.getPubYearPrint(filter);
variables.cntPubYearElectronic = drilldown.getPubYearElectronic(filter);
variables.cntPubPreferredCiteYearLine = drilldown.getPubPreferredCiteYearLine(filter);
variables.cntPubPreferredCiteYear = drilldown.getPubPreferredCiteYear(filter);
variables.cntJournalTitle = drilldown.getJournalTitle(filter);

variables.cntAgeToEighteen = drilldown.getAgeToEighteen(filter);
variables.cntAgeNewborn = drilldown.getAgeNewborn(filter);
variables.cntAgeInfantTwo = drilldown.getAgeInfantTwo(filter);
variables.cntAgeInfant = drilldown.getAgeInfant(filter);
variables.cntAgePreschool = drilldown.getAgePreschool(filter);
variables.cntAgeSixTwelve = drilldown.getAgeSixTwelve(filter);
variables.cntAgeThirteenEighteen = drilldown.getAgeThirteenEighteen(filter);
variables.cntAgeNineteenPlus = drilldown.getAgeNineteenPlus(filter);
variables.cntAgeNineteenTwentyfour = drilldown.getAgeNineteenTwentyfour(filter);
variables.cntAgeNineteenFortyfour = drilldown.getAgeNineteenFortyfour(filter);
variables.cntAgeFortyfivePlus = drilldown.getAgeFortyfivePlus(filter);
variables.cntAgeFortyfiveSixtyfour = drilldown.getAgeFortyfiveSixtyfour(filter);
variables.cntAgeSixtyfivePlus = drilldown.getAgeSixtyfivePlus(filter);
variables.cntAgeEightyPlus = drilldown.getAgeEightyPlus(filter);

variables.cntFullName = drilldown.getFullName(filter);
variables.cntCollectiveName = drilldown.getCollectiveName(filter);
variables.cntNameOfSubstance = drilldown.getNameOfSubstance(filter);
variables.cntGrantID = drilldown.getGrantID(filter);
variables.cntGrantCountry = drilldown.getGrantCountry(filter);
variables.cntDescriptorName = drilldown.getDescriptorName(filter);
variables.cntDescriptorNameMajor = drilldown.getDescriptorNameMajor(filter);
variables.cntMeshMajorTopicYN = drilldown.getMeshMajorTopicYN(filter);
variables.cntPublicationType = drilldown.getPublicationType(filter);
variables.cntDateCreated = drilldown.getDateCreated(filter);
variables.cntDateCreatedYear = drilldown.getDateCreatedYear(filter);
variables.cntPubPreferredCiteYear = drilldown.getPubPreferredCiteYear(filter);

variables.cntPubModel = drilldown.getPubModel(filter);
variables.cntPubDateYear = drilldown.getPubDateYear(filter);
variables.cntArticleDateType = drilldown.getArticleDateType(filter);
variables.cntArticleDateYear = drilldown.getArticleDateYear(filter);
variables.cntCitationStatus = drilldown.getCitationStatus(filter);
variables.cntJournalCountry = drilldown.getJournalCountry(filter);
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



<!--- -------------------------------------------------------------------------------------------------- --->
<!--- CODE OF PAGE ------------------------------------------------------------------------------------- --->
<!--- -------------------------------------------------------------------------------------------------- --->

<!DOCTYPE html>
<html lang="en"><head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <!-- <link rel="icon" href="http://getbootstrap.com/favicon.ico"> -->

    <title>Record Set Analyzer - MeSH Tree</title>

    <!-- Bootstrap core CSS -->
    <!--- <link href="../assets/styles/bootstrap332.css" rel="stylesheet"> --->

    <!-- Custom styles for this template -->
    <link href="../assets/styles/bootstrap332_dashboard.css" rel="stylesheet">

	<link href="../assets/styles/dashboard.css" rel="stylesheet" type="text/css" />

	<link href="../assets/styles/pubmed_drilldown.css" rel="stylesheet" type="text/css" />
	<script type="text/javascript" src="../assets/scripts/accessdrilldown.js"></script>

    <script src="../assets/scripts/ie-emulation-modes-warning.js"></script>

	<!--- These run the red x to remove facets from the filter --->
	<link rel="stylesheet" type="text/css" href="../assets/styles/accessInventory.css" />
	<script type="text/javascript" src="../assets/scripts/jquery-1.9.1.js"></script>
	<link rel="stylesheet" href="../assets/styles/jquery.treeview.css" />
	<script src="../assets/scripts/jquery.treeview.js" type="text/javascript"></script>
	<script type="text/javascript" src="../assets/scripts/jstorage.js"></script>
	<script type="text/javascript" src="../assets/scripts/accessdrilldown.js"></script>


    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->

<link rel="stylesheet" href="dist/themes/default/style.min.css" />

  </head>

  <body>

    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">Record Set Analyzer for data from pubmed.gov.gov</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav navbar-right">
            <li><a href="#">Help</a></li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-3 col-md-2 sidebar">
          <ul class="nav nav-sidebar">
			<li><a href="../index2.cfm" title="Record sets">List of record sets</a></li>
			<cfoutput>

            <li><a href="../drillDown/index.cfm">drilldown</a></li>
			<li class="active"><a href="index2.cfm">MeSH tree  <span class="sr-only">(current)</span></a></li>
            <li><a href="../topicReports/index.cfm?CurrDataSetID=#CurrDataSetID#" title="Export HTML reports">Create HTML reports</a></li>
			<!--- <li><a href="pdf_export.cfm?CurrDataSetID=#CurrDataSetID#">Create a PDF report</a></li> --->
			</cfoutput>
          </ul>

        </div><!--- end sidebar --->



<!--- -------------------------------------------------------------------------------------------- --->
<!--- MAIN CONTENT AREA -------------------------------------------------------------------------- --->
<!--- -------------------------------------------------------------------------------------------- --->

<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
          <!--- <h1 class="page-header">drilldown interface</h1> --->


<!--- callout for "Limits imposed" --->
<div id="callout">
<!--- <cfif Recordscount gt 0> --->

	<cfif qRecordscount gt 0>
        <p id="removex">
            <cfoutput>
                <strong>#numberFormat(qRecordscount,'9,999')#</strong> records retrieved from <strong>'#qDataSetInfo.DataSetName#'</strong> downloaded #dateFormat(qDataSetInfo.DateRetrieved, "mm/dd/yyyy")#.<br />

<!--- searchLimits --->
<cfif url.Agency neq "">Agency=#cntAgency.Agency# <span class="AGENCY">X &nbsp;&nbsp;</span></cfif>
<cfif url.JournalTitle neq "">JournalTitle=#cntJournalTitle.JournalTitle# <span class="JOURNALTITLE">X &nbsp;&nbsp;</span></cfif>
<cfif url.PublicationType neq "">PublicationType=#cntPublicationType.PublicationType# <span class="PUBLICATIONTYPE">X &nbsp;&nbsp;</span></cfif>
<cfif url.FullName neq "">FullName=#cntFullName.FullName# <span class="FULLNAME">X &nbsp;&nbsp;</span></cfif>
<cfif url.CollectiveName neq "">CollectiveName=#cntCollectiveName.CollectiveName# <span class="COLLECTIVENAME">X &nbsp;&nbsp;</span></cfif>
<cfif url.DescriptorName neq "">DescriptorName=#cntDescriptorName.DescriptorName# <span class="DESCRIPTORNAME">X &nbsp;&nbsp;</span></cfif>
<cfif url.DescriptorNameMajor neq "">DescriptorNameMajor=#cntDescriptorNameMajor.DescriptorName# <span class="DESCRIPTORNAMEMAJOR">X &nbsp;&nbsp;</span></cfif>
<cfif url.MeshMajorTopicYN neq "">MeshMajorTopicYN=#cntMeshMajorTopicYN.MeshMajorTopicYN# <span class="MESHMAJORTOPICYN">X &nbsp;&nbsp;</span></cfif>
<cfif url.NameOfSubstance neq "">NameOfSubstance=#cntNameOfSubstance.NameOfSubstance# <span class="NAMEOFSUBSTANCE">X &nbsp;&nbsp;</span></cfif>
<cfif url.GrantID neq "">GrantID=#cntGrantID.GrantID# <span class="GRANTID">X &nbsp;&nbsp;</span></cfif>
<cfif url.GrantCountry neq "">GrantCountry=#cntGrantCountry.GrantCountry# <span class="GRANTCOUNTRY">X &nbsp;&nbsp;</span></cfif>
<cfif url.DateCreated neq "">DateCreated=#cntDateCreated.DateCreated# <span class="DATECREATED">X &nbsp;&nbsp;</span></cfif>
<cfif url.DateCreatedYear neq "">DateCreatedYear=#cntDateCreatedYear.DateCreatedYear# <span class="DATECREATEDYEAR">X &nbsp;&nbsp;</span></cfif>
<cfif url.PubPreferredCiteYear neq "">PubPreferredCiteYear=#cntPubPreferredCiteYear.PubPreferredCiteYear# <span class="PUBPREFERREDCITEYEAR">X &nbsp;&nbsp;</span></cfif>
<cfif url.PubModel neq "">PubModel=#cntPubModel.PubModel# <span class="PUBMODEL">X &nbsp;&nbsp;</span></cfif>
<cfif url.PubDateYear neq "">PubDateYear=#cntPubDateYear.PubDateYear# <span class="PUBDATEYEAR">X &nbsp;&nbsp;</span></cfif>
<cfif url.JournalCountry neq "">JournalCountry=#cntJournalCountry.JournalCountry# <span class="JOURNALCOUNTRY">X &nbsp;&nbsp;</span></cfif>

<!--- Limits tester - activate as needed --->
<!---<div style="border:thin solid black; padding: 0.5em;">
<p>Debug</p>
#filter.html()#
</div>--->
            </cfoutput>
        </p>
    </cfif>

</div><!---end of callout--->




<!--- ----------------------------------------------------------------------------------------------- --->
<!--- ROW 1: Tree ----------------------------------------------------------------------------- --->
<!--- ----------------------------------------------------------------------------------------------- --->


 <!---  <div id="mainContent"> --->
    <!--- <a id="skipnav" name="skip"></a> --->


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

  <!--- </div> ---><!-- end #mainContent -->



</div></div>

      </div>
    </div>

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="../assets/styles/jquery.js"></script>
    <script src="../assets/styles/bootstrap.js"></script>
    <script src="../assets/styles/docs.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="../assets/styles/ie10-viewport-bug-workaround.js"></script>


<!--- <div data-original-title="Copy to clipboard" title="" style="position: absolute; left: 0px; top: -9999px; width: 15px; height: 15px; z-index: 999999999;" class="global-zeroclipboard-container" id="global-zeroclipboard-html-bridge">      <object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" id="global-zeroclipboard-flash-bridge" width="100%" height="100%">         <param name="movie" value="/assets/flash/ZeroClipboard.swf?noCache=1422119175515">         <param name="allowScriptAccess" value="sameDomain">         <param name="scale" value="exactfit">         <param name="loop" value="false">         <param name="menu" value="false">         <param name="quality" value="best">         <param name="bgcolor" value="#ffffff">         <param name="wmode" value="transparent">         <param name="flashvars" value="trustedOrigins=getbootstrap.com%2C%2F%2Fgetbootstrap.com%2Chttp%3A%2F%2Fgetbootstrap.com">         <embed src="Bootstrap_files/ZeroClipboard.swf" loop="false" menu="false" quality="best" bgcolor="#ffffff" name="global-zeroclipboard-flash-bridge" allowscriptaccess="sameDomain" allowfullscreen="false" type="application/x-shockwave-flash" wmode="transparent" pluginspage="http://www.macromedia.com/go/getflashplayer" flashvars="trustedOrigins=getbootstrap.com%2C%2F%2Fgetbootstrap.com%2Chttp%3A%2F%2Fgetbootstrap.com" scale="exactfit" width="100%" height="100%">                </object></div><svg style="visibility: hidden; position: absolute; top: -100%; left: -100%;" preserveAspectRatio="none" viewBox="0 0 200 200" height="200" width="200"><defs></defs><text style="font-weight:bold;font-size:10pt;font-family:Arial, Helvetica, Open Sans, sans-serif;dominant-baseline:middle" y="10" x="0">200x200</text></svg> --->

	</body></html>