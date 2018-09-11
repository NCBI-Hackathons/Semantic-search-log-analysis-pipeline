<!---
Name:        http://localhost:8500/_pubmed2015/mesh/ajax_children.cfm
Author:      Dan Wendling (wendlingd@icloud.com)
Description: Record Set Analyzer - Browse records through the MeSH tree
Created:     2/1/2014
Modified:    2/9/2014

Purpose: Load every item in the CF retrieval into a one-off call to eUtils
Then return term + count to jsTree, either one at a time or all at once.

Help:
- jQuery get: http://api.jquery.com/jQuery.get/
- eUtils Quick Start: http://www.ncbi.nlm.nih.gov/books/NBK25500/
- In Depth: http://www.ncbi.nlm.nih.gov/books/NBK25499/
- ESearch: http://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch
- Base eUtils URL: http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=MeSH_TERM&rettype=count


Adding the data set back in...
this page, invoking search:  CurrDataSetID="#CurrDataSetID#"
cfc: WHERE dataset.DataSetID = #ARGUMENTS.CurrDataSetID#
 --->


<cfparam name="URL.id" type="string" default="Humanities">
<cfparam name="FORM.encoding" type="string" default="%28%28%28comprehension%5Ball+fields%5D+AND+english%5Bla%5D%29+AND+%28compliance+OR+adherence%29%29+OR+%28health%5Bti%5D+AND+literacy%5Bti%5D%29+OR+%28%22health+literacy%22+OR+%22health+literate%22+OR+%22medical+literacy%22%29+OR+%28functional%5Btw%5D+AND+health%5Btw%5D+AND+literacy%5Btw%5D%29+OR+numeracy+OR+%28%28low+literate%5Bti%5D+OR+low+literacy%5Bti%5D+OR+literacy%5Bti%5D+OR+illiteracy%5Bti%5D+OR+literate%5Bti%5D+OR+illiterate%5Bti%5D+OR+reading%5Bmh%5D+OR+comprehension%5Bmh%5D%29+AND+%28health+promotion%5Bmajor%5D+OR+health+education%5Bmajor%5D+OR+patient+education%5Bmajor%5D+OR+Communication+Barriers%5Bmajor%5D+OR+communication%5Bmajor%3Anoexp%5D+OR+Health+Knowledge%2C+Attitudes%2C+Practice%5Bmajor%5D+OR+attitude+to+health%5Bmajor%5D%29%29+OR+%28comprehension%5Bmajor%5D+AND+educational+status%5Bmajor%5D%29+OR+%28family%5Bti%5D+AND+literacy%5Bti%5D%29+OR+%28%28%22drug+labeling%22+OR+Prescriptions+%5Bmh%5D%29+AND+%28%22comprehension%22+OR+%22numeracy%22%29%29+OR+%28%28cancer%5Bti%5D+OR+diabetes%5Bti%5D%29+AND+%28literacy%5Bti%5D+OR+comprehension%5Bti%5D%29%29+OR+%22adult+literacy%22+OR+%22limited+literacy%22+OR+%22patient+understanding%22%5Bti%5D+OR+%28self+care+%5Bmajor%5D+AND+perception%5Bmh%5D%29+OR+%28comprehension+AND+food+labeling%5Bmh%5D%29+AND+English%5Bla%5D%29">

<cfquery name="treeTerm" datasource="pubmed">
    select DescriptorName
    from mesh_tree
    where parentName like '#id#'
    order by DescriptorName
</cfquery>
    
    
<!---Test what cf is returning from mesh_tree--->
<!---<cfoutput query="treeTerm"><li id="#DescriptorName#" class="jstree-closed">#DescriptorName# (42)</li></cfoutput>--->



<!--- jQuery-AJAX --->
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>


<!---Do multiple eUtils calls and return the results as a unit.--->
<script type="text/javascript">
 $(document).ready(function() { 
 
	  $.ajax({
		  	url: 
"http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=<cfoutput>#treeTerm.DescriptorName#[mh]+AND+#encoding#</cfoutput>&rettype=count";
			type: "GET",
			dataType:"xml",
			success: function(data){
				$each()
				var jqObj = jQuery(data);
				var theCnt = result.getElementsByTagName('Count')[0];
				var descriptor = "<cfoutput>#treeTerm.DescriptorName#</cfoutput>";
				var newRow = descriptor + theCnt.firstChild.nodeValue;
				$("ul").add('<li>' + descriptor + theCnt + '</li>);
				}
	  });
	  
  });

});
  </script>


  
<!---  ' <a href="http://pubmed.gov/?term=' + descriptor  + '[mh]+AND+' + encodingEUtils + '">' + theCnt.firstChild.nodeValue + '</a>';--->