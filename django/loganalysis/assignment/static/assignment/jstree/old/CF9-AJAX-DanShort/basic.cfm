<html><head></head><body><cfform>	<cftree format="html" name="basictree">			<cftreeitem display="Accounting" value="Folder1" img="folder" imgopen="folder" />
			<cftreeitem display="IT" value="Folder2" img="computer" expand="false" />
			<cftreeitem display="Human Resources" value="Folder3" img="folder" imgopen="folder" />
			<cftreeitem display="The Budget" parent="Folder1" value="TreeItem1" href="/cf9/cftree/basic.cfm" />
			<cftreeitem display="Calculator" parent="Folder1" value="TreeItem2" href="/cf9/cftree/basic.cfm" />
			<cftreeitem display="Checkbook" parent="Folder1" value="TreeItem3" href="/cf9/cftree/basic.cfm" />
			<cftreeitem display="CDs" img="cd" parent="Folder2" value="TreeItem4" href="/cf9/cftree/basic.cfm" />
			<cftreeitem display="Floppies (yea right)" img="floppy" parent="Folder2" value="TreeItem5" href="/cf9/cftree/basic.cfm" />
			<cftreeitem display="Serial Numbers" img="document" parent="Folder2" value="TreeItem6" href="/cf9/cftree/basic.cfm" />
			<cftreeitem display="Tree Item 7" parent="Folder3" value="TreeItem7" href="/cf9/cftree/basic.cfm" />
			<cftreeitem display="Tree Item 8" parent="Folder3" value="TreeItem8" href="/cf9/cftree/basic.cfm" />
			<cftreeitem display="Tree Item 9" parent="Folder3" value="TreeItem9" href="/cf9/cftree/basic.cfm" />
			<cftreeitem display="Tree Item 10" parent="Folder3" value="TreeItem10" href="/cf9/cftree/basic.cfm" />
	</cftree></cfform></body></html>
