
<cfquery name="test2" datasource="pubmed">
    select t.TreeNumber, t.DescriptorName, count(m.DescriptorName) as citeCnt
    from mesh_tree t left join mesh m on t.DescriptorName = m.DescriptorName
    where t.TreeNumber like 'M'
    group by t.DescriptorName, t.TreeNumber
    order by t.TreeNumber
</cfquery>

<!---    and t.TreeNumber REGEXP '^.{11}$'--->


<html>
<head>
	<title>Test2-Dynamic CFTREE</title>
	<style type="text/css">
	body {font-family: Verdana, Geneva, Arial, Helvetica, sans-serif;}
	</style>
</head>
<body>
<div>
<cfoutput query="test2">
#DescriptorName#
</cfoutput>

</div>

</body>
</html>

<!---Nest set attempt:
select node.DescriptorName
from mesh_tree as node, mesh_tree as parent
where node.TreeNumber between parent.TreeNumber and parent.TreeNumber
and parent.DescriptorName like 'Anatomy'
order by node.TreeNumber--->