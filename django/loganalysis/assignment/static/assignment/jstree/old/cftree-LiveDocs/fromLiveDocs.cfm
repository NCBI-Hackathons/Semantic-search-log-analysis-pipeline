<!---
http://localhost:8500/_pubmed2015/mesh/cftree-LiveDocs/fromLiveDocs.cfm
Source: http://help.adobe.com/en_US/ColdFusion/9.0/Developing/WSc3ff6d0ea77859461172e0811cbec22c24-7a86.html--->


<!--- CFQUERY with an ORDER BY clause. ---> 
<cfquery name="deptquery" datasource="cfdocexamples"> 
    SELECT Dept_ID, FirstName || ' ' || LastName 
    AS FullName 
    FROM Employee 
    ORDER BY Dept_ID 
</cfquery> 

<cfquery name="showDb" datasource="cfdocexamples"> 
    SELECT *
    FROM Employee 
    ORDER BY Dept_ID 
</cfquery> 

<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>cftree from help.adobe.com</title>
</head>

<body>
 
<!--- One-level tree control ---> 
<cfform name="form1" action="../../submit.cfm"> 
 
<cftree name="tree1" 
	format="html"
    height="350" 
    required="Yes"> 
 
<cftreeitem value="Dept_ID, FullName" 
    query="deptquery" 
    queryasroot="no" 
    img="folder,document" 
    imgopen="computer,folder" 
    expand="no"> 
 
</cftree> 
<!---<br> 
<br><input type="Submit" value="Submit"> --->
</cfform>

<p>&nbsp;</p>


<!---Multi-level tree control--->

<cfform name="form2" action="cfform_submit.cfm"> 

<cftree name="tree2"
	format="html"> 

    <cftreeitem value="Development" parent="Divisions" img="folder" expand="no"> 
        <cftreeitem value="Product One" parent="Development" img="document" expand="no"> 
        <cftreeitem value="Product Two" parent="Development" expand="no"> 
        <cftreeitem value="GUI" parent="Product Two" img="document" expand="no"> 
        <cftreeitem value="Kernel" parent="Product Two" img="document"> 
        <cftreeitem value="Product Three" parent="Development" img="document"> 
    <cftreeitem value="QA" parent="Divisions" img="folder" expand="no"> 
        <cftreeitem value="Product One" parent="QA" img="document"> 
        <cftreeitem value="Product Two" parent="QA" img="document"> 
        <cftreeitem value="Product Three" parent="QA" img="document"> 
    <cftreeitem value="Support" parent="Divisions" img="folder" expand="no"> 
        <cftreeitem value="Product Two" parent="Support" img="document"> 
    <cftreeitem value="Sales" parent="Divisions" img="folder"> 
    <cftreeitem value="Marketing" parent="Divisions" img="folder"> 
    <cftreeitem value="Finance" parent="Divisions" img="folder"> 
</cftree> 
</cfform>

<p>&nbsp;</p>


<cfdump var="#showDb#">

</body>
</html>