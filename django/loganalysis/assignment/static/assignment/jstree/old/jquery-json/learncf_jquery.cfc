<!---cfc file--->

<cfcomponent name="jQueryExample" output="false">

    <cffunction name="getDataSetInfo" access="public" returnType="query" output="false">
    <cfquery name="qDataSetInfo" datasource="pubmed">
        SELECT dataset.DataSetName, dataset.SearchStrategyDetails, dataset.DateRetrieved
        FROM dataset
        WHERE dataset.DataSetID = 71
    </cfquery>
        <cfreturn qDataSetInfo>
    </cffunction>

</cfcomponent>





<!---<cffunction name="getAllPlayers" output="false" access="private" returntype="query">
    <cfset var qAllPlayers = queryNew('playerName, team') />

    <cfset queryAddRow(qAllPlayers, 40) />

    <!--- add 10 Giants players to the "database" --->
    <cfset querySetCell(qAllPlayers, 'playerName', 'Alford, Jay', 1) />
    <cfset querySetCell(qAllPlayers, 'team', 'NY Giants', 1) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Barden, Ramses', 2) />
    <cfset querySetCell(qAllPlayers, 'team', 'NY Giants', 2) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Beckum, Travis', 3) />
    <cfset querySetCell(qAllPlayers, 'team', 'NY Giants', 3) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Bernard, Rocky', 4) />
    <cfset querySetCell(qAllPlayers, 'team', 'NY Giants', 4) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Blackburn, Chase', 5) />
    <cfset querySetCell(qAllPlayers, 'team', 'NY Giants', 5) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Boss, Kevin', 6) />
    <cfset querySetCell(qAllPlayers, 'team', 'NY Giants', 6) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Bradshaw, Ahmad', 7) />
    <cfset querySetCell(qAllPlayers, 'team', 'NY Giants', 7) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Canty, Chris', 8) />
    <cfset querySetCell(qAllPlayers, 'team', 'NY Giants', 8) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Diehl, David', 9) />
    <cfset querySetCell(qAllPlayers, 'team', 'NY Giants', 9) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Feagles, Jeff', 10) />
    <cfset querySetCell(qAllPlayers, 'team', 'NY Giants', 10) />

    <!--- add 10 Cowboys players to the "database" --->
    <cfset querySetCell(qAllPlayers, 'playerName', 'Adams, Flozell', 11) />
    <cfset querySetCell(qAllPlayers, 'team', 'Dallas Cowboys', 11) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Austin, Miles', 12) />
    <cfset querySetCell(qAllPlayers, 'team', 'Dallas Cowboys', 12) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Brown, Courtney', 13) />
    <cfset querySetCell(qAllPlayers, 'team', 'Dallas Cowboys', 13) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Choice, Tashard', 14) />
    <cfset querySetCell(qAllPlayers, 'team', 'Dallas Cowboys', 14) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Colombo, Marc', 15) />
    <cfset querySetCell(qAllPlayers, 'team', 'Dallas Cowboys', 15) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Davis, Leonard', 16) />
    <cfset querySetCell(qAllPlayers, 'team', 'Dallas Cowboys', 16) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Jones, Felix', 17) />
    <cfset querySetCell(qAllPlayers, 'team', 'Dallas Cowboys', 17) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Kitna, Jon', 18) />
    <cfset querySetCell(qAllPlayers, 'team', 'Dallas Cowboys', 18) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Procter, Corey', 19) />
    <cfset querySetCell(qAllPlayers, 'team', 'Dallas Cowboys', 19) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Romo, Tony', 20) />
    <cfset querySetCell(qAllPlayers, 'team', 'Dallas Cowboys', 20) />

    <!--- add 10 Eagles players to the "database" --->
    <cfset querySetCell(qAllPlayers, 'playerName', 'Akers, David', 21) />
    <cfset querySetCell(qAllPlayers, 'team', 'Philadelphia Eagles', 21) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Baskett, Hank', 22) />
    <cfset querySetCell(qAllPlayers, 'team', 'Philadelphia Eagles', 22) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Booker, Lorenzo', 23) />
    <cfset querySetCell(qAllPlayers, 'team', 'Philadelphia Eagles', 23) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Clemons, Chris', 24) />
    <cfset querySetCell(qAllPlayers, 'team', 'Philadelphia Eagles', 24) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Demps, Quintin', 25) />
    <cfset querySetCell(qAllPlayers, 'team', 'Philadelphia Eagles', 25) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Feeley, A.J.', 26) />
    <cfset querySetCell(qAllPlayers, 'team', 'Philadelphia Eagles', 26) />

    <cfset querySetCell(qAllPlayers, 'playerName', 'Hobbs, Ellis', 27) />
    <cfset querySetCell(qAllPlayers, 'team', 'Philadelphia Eagles', 27) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Jackson, DeSean', 28) />
    <cfset querySetCell(qAllPlayers, 'team', 'Philadelphia Eagles', 28) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Klecko, Dan', 29) />
    <cfset querySetCell(qAllPlayers, 'team', 'Philadelphia Eagles', 29) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'McNabb, Donovan', 30) />
    <cfset querySetCell(qAllPlayers, 'team', 'Philadelphia Eagles', 30) />

    <!--- add 10 Redskins players to the "database" --->
    <cfset querySetCell(qAllPlayers, 'playerName', 'Alexander, Lorenzo', 31) />
    <cfset querySetCell(qAllPlayers, 'team', 'Washington Redskins', 31) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Campbell, Jason', 32) />
    <cfset querySetCell(qAllPlayers, 'team', 'Washington Redskins', 32) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Clark, Devin', 33) />
    <cfset querySetCell(qAllPlayers, 'team', 'Washington Redskins', 33) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Cooley, Chris', 34) />
    <cfset querySetCell(qAllPlayers, 'team', 'Washington Redskins', 34) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Dixon, Antonio', 35) />
    <cfset querySetCell(qAllPlayers, 'team', 'Washington Redskins', 35) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Fletcher, London', 36) />
    <cfset querySetCell(qAllPlayers, 'team', 'Washington Redskins', 36) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Hackett, D.J.', 37) />
    <cfset querySetCell(qAllPlayers, 'team', 'Washington Redskins', 37) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Randle El, Antwaan', 38) />
    <cfset querySetCell(qAllPlayers, 'team', 'Washington Redskins', 38) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Smoot, Fred', 39) />
    <cfset querySetCell(qAllPlayers, 'team', 'Washington Redskins', 39) />
    <cfset querySetCell(qAllPlayers, 'playerName', 'Suisham, Shaun', 40) />
    <cfset querySetCell(qAllPlayers, 'team', 'Washington Redskins', 40) />

    <cfreturn qAllPlayers />
</cffunction>
--->

<!---<cffunction name="getAllTeams" access="remote" output="false" returntype="query">
    <cfset var allPlayers   = getAllPlayers() />
    <cfset var qGetAllTeams = "" />

    <cfquery name="qGetAllTeams" dbtype="query">
        SELECT DISTINCT team FROM allPlayers ORDER BY team
    </cfquery>

    <cfreturn qGetAllTeams />
</cffunction>--->

