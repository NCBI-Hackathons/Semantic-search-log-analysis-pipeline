<!---http://stackoverflow.com/questions/15551951/sql-coldfusion-get-and-display-full-hierarchical-tree-listing--->

<!--- temp table this uses:

delimiter $$

CREATE TABLE `temp` (
  `folder_id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_folder_id` int(11) DEFAULT NULL,
  `folder_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`folder_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8$$


looks like:

folder_id | parent_folder_id | folder_name
------------------------------------------
1         | null             | Main
2         | null             | Departments
3         | null             | Archived
4         | 2                | IT
5         | 2                | Sales
6         | 4                | Error Logs
7         | 6                | 2012

 --->


<cfquery name="get_folders" datasource="pubmed">
    select folder_id, parent_folder_id, folder_name
    from temp
    order by folder_name
</cfquery>

<!--- Read all roots (no parent ID) --->
<cfquery name="get_parent_folders" dbtype="query">
    select folder_id, folder_name
    from get_folders
    where parent_folder_id is null
</cfquery>


<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Nested <ul> tree structure from db</title>
</head>

<body>

<h1>Nested ul tree structure from db</h1>

<p>Source: <a href="http://stackoverflow.com/questions/15551951/sql-coldfusion-get-and-display-full-hierarchical-tree-listing">http://stackoverflow.com/questions/15551951/sql-coldfusion-get-and-display-full-hierarchical-tree-listing</a></p>

<p>This uses the database table &apos;temp&apos;, which looks like this:</p>

<pre>
folder_id | parent_folder_id | folder_name
------------------------------------------
1         | null             | Main
2         | null             | Departments
3         | null             | Archived
4         | 2                | IT
5         | 2                | Sales
6         | 4                | Error Logs
7         | 6                | 2012
</pre>

<p>&nbsp;</p>

<h2>Query of queries retrieval</h2>

<ul class="tree">
    <cfloop query="get_parent_folders">
        <cfset processTreeNode(folderId=get_parent_folders.folder_id, folderName=get_parent_folders.folder_name) />
    </cfloop>
</ul>

<cffunction name="processTreeNode" output="true">
    <cfargument name="folderId" type="numeric" />
    <cfargument name="folderName" type="string" />
    <!--- Check for any nodes that have *this* node as a parent --->
    <cfquery name="LOCAL.qFindChildren" dbtype="query">
        select folder_id, folder_name
        from get_folders
        where parent_folder_id = <cfqueryparam value="#arguments.folderId#" cfsqltype="cf_sql_integer" />
    </cfquery>
    
    <li>#arguments.folderName#
        <cfif LOCAL.qFindChildren.recordcount>
            <!--- We have another list! --->
            <ul>
                <!--- We have children, so process these first --->
                <cfloop query="LOCAL.qFindChildren">
                    <!--- Recursively call function --->
                    <cfset processTreeNode(folderId=LOCAL.qFindChildren.folder_id, folderName=LOCAL.qFindChildren.folder_name) />
                </cfloop>
            </ul>
        </cfif>
    </li>
</cffunction>


</body>
</html>