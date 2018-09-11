<cfparam name="url.category_id" default="0">
<cfif url.category_id eq ""><cfset url.category_id = 0></cfif>

<!--- Again, I am building a query here but normally this would be a query against a categories table
   and in reall life you would probably add a where clause on this page to only get the categories
   where parentID = #url.categoryID# but my cfif later takes care of that for me and this is just
   a demo so whatever. --->
<cfset getcategories = querynew("category_id,Name,ParentID")>
<cfset queryaddrow(getcategories)>
<cfset querysetcell(getcategories,"category_id","1")>
<cfset querysetcell(getcategories,"Name","Category1")>
<cfset querysetcell(getcategories,"ParentID","0")>
<cfset queryaddrow(getcategories)>
<cfset querysetcell(getcategories,"category_id","2")>
<cfset querysetcell(getcategories,"Name","Category2")>
<cfset querysetcell(getcategories,"ParentID","1")>
<cfset queryaddrow(getcategories)>
<cfset querysetcell(getcategories,"category_id","3")>
<cfset querysetcell(getcategories,"Name","Category3")>
<cfset querysetcell(getcategories,"ParentID","1")>
<cfset queryaddrow(getcategories)>
<cfset querysetcell(getcategories,"category_id","4")>
<cfset querysetcell(getcategories,"Name","Category4")>
<cfset querysetcell(getcategories,"ParentID","0")>

<cfoutput>
<b>Your are viewing Category #url.category_id#</b><br>
Below are the child categories(if any):<br>
<table>
<cfloop query="getcategories">
<cfif getcategories.parentID eq url.category_id>
<tr>
<td><img src="/CFIDE/scripts/ajax/resources/cf/images/FolderClose.gif" alt="" width="24" height="24" border="0"></td>
    <!--- Here is where I call the function that is in the main layout page. --->
    <td><a href="javascript:catTreeNodeSelection('#getcategories.category_id#')">#getcategories.Name#</a></td>
</tr>
</cfif>
</cfloop>
</table>
</cfoutput>