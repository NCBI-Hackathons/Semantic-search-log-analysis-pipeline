<!---
Name:        http://localhost:8500/_pubmed2015/mesh/old/eUtils_oneOff-Table.cfm
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

 --->

<cfsilent>
   <cfparam name="FORM.treeNo" type="string" default="M01">
   <cfparam name="FORM.charCnt" type="string" default="7">
   <cfparam name="URL.DataSetID" type="string" default="71">
   <cfparam name="FORM.encoding" type="string" default="%28%28%28comprehension%5Ball+fields%5D+AND+english%5Bla%5D%29+AND+%28compliance+OR+adherence%29%29+OR+%28health%5Bti%5D+AND+literacy%5Bti%5D%29+OR+%28%22health+literacy%22+OR+%22health+literate%22+OR+%22medical+literacy%22%29+OR+%28functional%5Btw%5D+AND+health%5Btw%5D+AND+literacy%5Btw%5D%29+OR+numeracy+OR+%28%28low+literate%5Bti%5D+OR+low+literacy%5Bti%5D+OR+literacy%5Bti%5D+OR+illiteracy%5Bti%5D+OR+literate%5Bti%5D+OR+illiterate%5Bti%5D+OR+reading%5Bmh%5D+OR+comprehension%5Bmh%5D%29+AND+%28health+promotion%5Bmajor%5D+OR+health+education%5Bmajor%5D+OR+patient+education%5Bmajor%5D+OR+Communication+Barriers%5Bmajor%5D+OR+communication%5Bmajor%3Anoexp%5D+OR+Health+Knowledge%2C+Attitudes%2C+Practice%5Bmajor%5D+OR+attitude+to+health%5Bmajor%5D%29%29+OR+%28comprehension%5Bmajor%5D+AND+educational+status%5Bmajor%5D%29+OR+%28family%5Bti%5D+AND+literacy%5Bti%5D%29+OR+%28%28%22drug+labeling%22+OR+Prescriptions+%5Bmh%5D%29+AND+%28%22comprehension%22+OR+%22numeracy%22%29%29+OR+%28%28cancer%5Bti%5D+OR+diabetes%5Bti%5D%29+AND+%28literacy%5Bti%5D+OR+comprehension%5Bti%5D%29%29+OR+%22adult+literacy%22+OR+%22limited+literacy%22+OR+%22patient+understanding%22%5Bti%5D+OR+%28self+care+%5Bmajor%5D+AND+perception%5Bmh%5D%29+OR+%28comprehension+AND+food+labeling%5Bmh%5D%29+AND+English%5Bla%5D%29">
</cfsilent>


<cfquery name="eUtils" datasource="pubmed">
    select t.DescriptorName, t.TreeNumber, t.trLevel, count(m.DescriptorName) as citeCnt
    from mesh_tree t left join mesh m on t.DescriptorName = m.DescriptorName and m.DataSetID like '#DataSetID#'
    where t.TreeNumber like '#treeNo#%'
    and t.TreeNumber REGEXP '^.{#charCnt#}$'
    group by t.DescriptorName, t.TreeNumber
    order by t.TreeNumber
</cfquery>
<!---Add mesh_descriptor.DescriptorUI to mesh_tree so you can link to the term pages at NCBI. But this is yet another parameter to pass through jsTree (if that is used). I don't think jsTree can do it. --->



<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>eUtils_oneOff-Table</title>
<link href="bibliometrics.css" rel="stylesheet" type="text/css" media="all" />


<!--- jQuery-AJAX --->
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>

<!---reportresearch[sb]--->
    <script type="text/javascript">

    $(document).ready(function(){
		getRecordCount();
	});
      function getRecordCount() {
		  <cfoutput query="eUtils">
		  var dbSearch = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=#DescriptorName#[mh]+AND+#encoding#&rettype=count";
      	$.get( dbSearch, function(result) {
      		var theCnt = result.getElementsByTagName('Count')[0];
			var descriptor = "#DescriptorName#";
			var treeNumber = '#TreeNumber#'
			var treeLevel = #trLevel# + 1
			var encodingEUtils = '#encoding#'
      		var val = '<tr><td>' + descriptor + '</a></td><td>' + treeNumber + '</td><td align="right"><a href="http://pubmed.gov/?term=' + descriptor  + '[mh]+AND+' + encodingEUtils + '">' + theCnt.firstChild.nodeValue + '</a></td></tr>';
			$("##content").append(val);

	  });</cfoutput>
      }
  </script>

</head>


<body>

  <div id="mainContent">


      <h1>Browse your record set using MeSH Tree Numbers</h1>

<p>This tool helps you understand the levels of specificity applied by human indexers to records at pubmed.gov. Enter a MeSH tree number from the <a href="http://www.nlm.nih.gov/mesh/2014/mesh_browser/MeSHtree.M.html#link_id">MeSH Tree Structure</a> and see how the "health disparities" record set was indexed from that term DOWN the tree. This search is not restricted by year.</p>

<p>Starting points: Consider  <a href="http://www.nlm.nih.gov/cgi/mesh/2014/MB_cgi?mode=dcms&term=Social+Sciences&field=entry#TreeI01" target="_blank">Social Sciences</a> at i01 and 7, the <a href="http://www.nlm.nih.gov/cgi/mesh/2014/MB_cgi?mode=dcms&term=Persons&field=entry#TreeM01" target="_blank">Persons</a> category at m01 and 7, <a href="http://www.nlm.nih.gov/cgi/mesh/2014/MB_cgi?term=Health+Occupations&field=entry#TreeH02" target="_blank">Health Occupations</a> at H02 and 7, or Publication Characteristics at V and 7 (the last retrieves "siblings" under 4 sub-categories).</p>

<hr>




    <form action="eUtils_oneOff-Table.cfm?treeNumber=<cfif isDefined("form.treeNo")><cfoutput>#form.treeNo#&charCnt=#form.charCnt#</cfoutput></cfif>" method="post" name="oneOff">
        <label = "treeNo">Parent number: <input type="text" name="treeNo" id="treeNo" /></label>
        <label = "charCnt" style="margin-left:2em;">Your number's character count + 4 = <input type="text" name="charCnt" id="charCnt" /></label>
        <input type="submit" value="Submit" style="margin-left:2em;"></input>
    </form>



<cfif isDefined("form.treeNo")>
	<p>Output for Health Disparities AND (<cfoutput>#treeNo#</cfoutput> and <cfoutput>#charCnt#</cfoutput>).</p>
</cfif>


    <table border="1" style="margin-top:1em;">
        <thead>
            <th>Term</th>
            <th>Tree number</th>
            <th>Count</th>
        </thead>
        <tbody id="content">
        </tbody>
    </table>


<p>MeSH Browser on NLM Main: <a href="http://www.nlm.nih.gov/mesh/2014/mesh_browser/MeSHtree.M.html#link_id">MeSH Browser</a>
    <p>My Broad Topics page: <a href="http://localhost:8500/_pubmed2015/topicReports/03_BroadTopics.cfm?CurrDataSetID=86#skip">(top)</a></p>


    <p>&nbsp;</p>

  </div><!-- end #mainContent -->

</body>
</html>

