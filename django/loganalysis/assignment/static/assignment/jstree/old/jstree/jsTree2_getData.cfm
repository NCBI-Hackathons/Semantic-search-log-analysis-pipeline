<!---
Name:        http://localhost:8500/_pubmed2015/mesh/jsTree/jsTree2_getData.cfm
Author:      Dan Wendling (wendlingd@icloud.com)
Description: Record Set Analyzer - Browse records through the MeSH tree
Created:     2/1/2014
Modified:    2/1/2014

 --->


   <cfparam name="FORM.parentNumber" type="string" default="M01.060">
   <cfparam name="URL.CurrDataSetID" type="string" default="71">
   <cfparam name="FORM.encoding" type="string" default="%28%28%28comprehension%5Ball+fields%5D+AND+english%5Bla%5D%29+AND+%28compliance+OR+adherence%29%29+OR+%28health%5Bti%5D+AND+literacy%5Bti%5D%29+OR+%28%22health+literacy%22+OR+%22health+literate%22+OR+%22medical+literacy%22%29+OR+%28functional%5Btw%5D+AND+health%5Btw%5D+AND+literacy%5Btw%5D%29+OR+numeracy+OR+%28%28low+literate%5Bti%5D+OR+low+literacy%5Bti%5D+OR+literacy%5Bti%5D+OR+illiteracy%5Bti%5D+OR+literate%5Bti%5D+OR+illiterate%5Bti%5D+OR+reading%5Bmh%5D+OR+comprehension%5Bmh%5D%29+AND+%28health+promotion%5Bmajor%5D+OR+health+education%5Bmajor%5D+OR+patient+education%5Bmajor%5D+OR+Communication+Barriers%5Bmajor%5D+OR+communication%5Bmajor%3Anoexp%5D+OR+Health+Knowledge%2C+Attitudes%2C+Practice%5Bmajor%5D+OR+attitude+to+health%5Bmajor%5D%29%29+OR+%28comprehension%5Bmajor%5D+AND+educational+status%5Bmajor%5D%29+OR+%28family%5Bti%5D+AND+literacy%5Bti%5D%29+OR+%28%28%22drug+labeling%22+OR+Prescriptions+%5Bmh%5D%29+AND+%28%22comprehension%22+OR+%22numeracy%22%29%29+OR+%28%28cancer%5Bti%5D+OR+diabetes%5Bti%5D%29+AND+%28literacy%5Bti%5D+OR+comprehension%5Bti%5D%29%29+OR+%22adult+literacy%22+OR+%22limited+literacy%22+OR+%22patient+understanding%22%5Bti%5D+OR+%28self+care+%5Bmajor%5D+AND+perception%5Bmh%5D%29+OR+%28comprehension+AND+food+labeling%5Bmh%5D%29+AND+English%5Bla%5D%29">





   
<cfquery name="eUtils" datasource="pubmed">
    select t.DescriptorName, t.TreeNumber, t.trLevel, count(m.DescriptorName) as citeCnt
    from mesh_tree t left join mesh m on t.DescriptorName = m.DescriptorName and m.DataSetID like '#CurrDataSetID#'
    where t.parentNumber like '#parentNumber#%'
    group by t.DescriptorName, t.TreeNumber
    order by t.TreeNumber
</cfquery>
<!---Add mesh_descriptor.DescriptorUI to mesh_tree so you can link to the term pages at NCBI. But this is yet another parameter to pass through jsTree (if that is used). I don't think jsTree can do it. --->
    


<!--- jQuery-AJAX --->
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>

<!---Do multiple eUtils calls and return the results as a unit.--->
<script type="text/javascript">
 $(document).ready(function() { 
 
<cfoutput query="eUtils">
	  $.ajax({
		  	url: 
"http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=#DescriptorName#[mh]+AND+#encoding#&rettype=count";
			type: "GET",
			dataType:"xml",
			success: function(response){
				return response;
				console.log( response );
				}
	  });
	  
		var theCnt = result.getElementsByTagName('Count')[0];
		var descriptor = "#DescriptorName#";
		var treeNumber = '#TreeNumber#';
		var treeLevel = #trLevel# + 1;
		var encodingEUtils = '#encoding#';
		var newRow = descriptor + ' ' + treeNumber + ' <a href="http://pubmed.gov/?term=' + descriptor  + '[mh]+AND+' + encodingEUtils + '">' + theCnt.firstChild.nodeValue + '</a>';

  });</cfoutput>

});

	  
  </script>


<!---jQuery:

http://api.jquery.com/jQuery.get/

eUtils:

Quick Start: http://www.ncbi.nlm.nih.gov/books/NBK25500/
In Depth: http://www.ncbi.nlm.nih.gov/books/NBK25499/
ESearch: http://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch

Base eUtils URL: http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=MeSH_TERM&rettype=count
--->