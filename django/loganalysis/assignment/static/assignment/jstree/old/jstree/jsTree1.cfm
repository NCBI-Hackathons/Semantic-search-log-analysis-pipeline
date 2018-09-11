<!---
Name:        http://localhost:8500/_pubmed2015/mesh/jstree/jsTree1.cfm
Author:      Dan Wendling (dan.wendling@nih.gov)
Description: Record Set Analyzer - Browse records through the MeSH tree
Created:     2/3/2014
Modified:    2/3/2014

Help from:
- http://www.jstree.com/
	[docs]: http://jstree.com/docs
	[demo]: http://jstree.com/demo
- http://simpledotnetsolutions.wordpress.com/2012/11/25/jstree-few-examples-with-asp-netc/
--->


<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>jsTree1</title>

<link rel="stylesheet" href="dist/themes/default/style.min.css" />
<script src="dist/libs/jquery.js"></script>
<script src="dist/jstree.min.js"></script>
<script>
$(function() {
  $('#container').jstree(/* optional config object here */);
});
</script>

</head>

<body>

<h1>jsTree1</h1>


<!---<div id="container">
  <ul>
    <li>Root node
      <ul>
        <li id="child_node">Child node</li>
      </ul>
    </li>
  </ul>
</div>--->


<div id="container">
    <ul >

    <li><a>Analytical, Diagnostic and Therapeutic Techniques and Equipment Category +</a>
        <ul>
        <li id="child_node">Anesthesia and Analgesia</li>
        </ul>
    </li>
    <li><a>Anatomy Category +</a></li>
    <li><a>Anthropology, Education, Sociology and Social Phenomena Category +</a></li>
    <li><a>Check Tags Category +</a></li>
    <li><a>Chemicals and Drugs Category +</a></li>
    <li><a> Disciplines and Occupations Category +</a></li>
    <li><a>Diseases Category +</a></li>
    <li><a>Geographical Locations Category +</a></li>
    <li><a>Health Care Category +</a></li>
    <li><a>Humanities Category +</a></li>
    <li><a>Information Science Category +</a></li>
    <li><a>Organisms Category +</a></li>
    <li><a>Persons Category +</a></li>
    <li><a>Pharmacological Actions Category +</a></li>
    <li><a>Phenomena and Processes Category +</a></li>
    <li><a>Psychiatry and Psychology Category +</a></li>
    <li><a>Publication Type Category +</a></li>
    <li><a>Subheadings Category +</a></li>
    <li><a>Technology and Food and Beverages Category +</a></li>
</ul>

</div><!---end container--->


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


</body>
</html>