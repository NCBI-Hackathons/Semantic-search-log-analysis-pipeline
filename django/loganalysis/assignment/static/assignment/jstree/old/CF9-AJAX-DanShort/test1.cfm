<cfquery name="test1" datasource="pubmed">
    select t.TreeNumber, t.DescriptorName, count(m.DescriptorName) as citeCnt
    from mesh_tree t left join mesh m on t.DescriptorName = m.DescriptorName
    where t.TreeNumber like 'M01%'
    and t.TreeNumber REGEXP '^.{11}$'
    group by t.DescriptorName, t.TreeNumber
    order by t.TreeNumber
</cfquery>

<html>
<head>
	<title>Test1-Dynamic CFTREE</title>
	<style type="text/css">
	body {font-family: Verdana, Geneva, Arial, Helvetica, sans-serif;}
	</style>
</head>
<body>
	<cfform>
		<cftree format="html" name="dynamicTree">
	        <cftreeitem
	            query="test1"
	            value="DescriptorName,citeCnt"
	            display="DescriptorName,citeCnt"
				queryasroot="NO"
				img="folder,document"
				href="dynamic.cfm?parent=1,dynamic.cfm"
			/>
		</cftree>

	</cfform>
</body>
</html>

<!---Nest set attempt:
select node.DescriptorName
from mesh_tree as node, mesh_tree as parent
where node.TreeNumber between parent.TreeNumber and parent.TreeNumber
and parent.DescriptorName like 'Anatomy'
order by node.TreeNumber--->