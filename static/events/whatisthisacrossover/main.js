$(function() {
    $('.content').removeClass('fade-out');
});


const TRANSITION_SECONDS = 12


var req = new XMLHttpRequest(); 
req.onreadystatechange = handleResponse


var stateListIdx = 0
let stateList = ["Alabama", "Arkansas", "California", "Colorado", "Maine", "Massachusetts", "Minnesota", 
    "North Carolina", "Oklahoma", "Tennessee", "Texas", "Utah", "Vermont", "Virginia"]

function nextState() {
    currIdx = stateListIdx % stateList.length
    stateListIdx++ 
    return stateList[currIdx]
}


function g() {
    let state = nextState()
    let request = "?state=" + state
    req.open('GET', '/retrieve_next' + request, true)
    req.send() 
}

g()

window.setInterval(g, TRANSITION_SECONDS * 1000) 


function handleResponse() {
    if (req.readyState === XMLHttpRequest.DONE) {
        if (req.status === 200) {
            json = JSON.parse(req.responseText)


            $('.content').animate({ opacity: 0 })

            setTimeout(function() {
                handleState(json.info, json.candidates)
                $('.content').animate({ opacity: 1 })

            }, 1500)


        }
    }

}

function infoBarDom(info) {
    var infoBar = $("<div class=info-bar></div>")
    var percentReporting = $("<div class='info-item percent-reporting'></div>")
    percentReporting.text(info.percentage_reporting)
    var precinctsReporting = $("<div class='info-item precincts-reporting'></div>")
    precinctsReporting.text(info.precincts_reporting); 
    var totalVotes = $("<div class='info-item total-votes'></div>")
    totalVotes.text(info.total_votes)

    infoBar.append(percentReporting)
    infoBar.append(precinctsReporting)
    infoBar.append(totalVotes)

    return infoBar


}

function constructVotingTableHeader() {
    var header = $("<div class=voting-table-header></div>")

    var col1 = $("<div class='voting-table-cell names header-cell'>Candidate</div>")
    col1.text("Candidate")

    var col2 = $("<div class='voting-table-cell avatars header-cell'></div>")
    
    var col3 = $("<div class='voting-table-cell votes header-cell'>Votes</div>")
    col3.text("Votes")

    var col4 = $("<div class='voting-table-cell percentages header-cell'></div>")
    col4.text("Percentage")

    var col5 = $("<div class='voting-table-cell delegates header-cell'></div>")
    col5.text("Pledged Delegates")


    header.append(col1)
    header.append(col2)
    header.append(col3)
    header.append(col4)
    header.append(col5)

    return header
}

function constructVotingTableRowset(info, candidates) {
    var votingTableRowset = $("<div class=voting-table-rowset></div>")

    var isWinner = info.winner

    for (idx in candidates){
        candidate = candidates[idx]

        var row = $("<div class=voting-table-row></div>")
        
        var name = $("<div class='voting-table-cell names normal-cell'></div>")
        if(candidate.winner) {
            name.addClass("winner")
        }else if(isWinner) {
            row.addClass("loser")
        }
        name.text(candidate.name)
        var avatar_div = $("<div class='voting-table-cell avatars normal-cell'></div>")
        var avatar = $("<img class=avatar height='80' width='80'>")
        avatar.attr("src", candidate.avatar)
        avatar_div.append(avatar)

        var votes = $("<div class='voting-table-cell votes normal-cell'></div>")
        votes.text(candidate.votes)

        var percentages = $("<div class='voting-table-cell percentages normal-cell'></div>")
        percentages.text(candidate.percentage)

        var delegates = $("<div class='voting-table-cell delegates normal-cell'></div>")
        delegates.text(candidate.delegates)
        row.append(avatar_div)

        row.append(name)
        
        row.append(votes)
        row.append(percentages)
        row.append(delegates)
        votingTableRowset.append(row)

    }

    return votingTableRowset
}

function constructVotingTable(info, candidates) {
    var votingTable = $("<div class='voting-table'></div>")
    var header = constructVotingTableHeader()

    var rowset = constructVotingTableRowset(info, candidates)

    votingTable.append(header)
    votingTable.append(rowset)


    return votingTable

}


function handleState(info, candidates) {
    
    var state = $("<div class=state>Now Reporting...</div>")
    state.text(info.state)

    var infoBar = infoBarDom(info)
    var votingTable = constructVotingTable(info, candidates)
    
    $(".content").empty()
    $(".content").append(state)
    $(".content").append(infoBar)
    $(".content").append(votingTable)


}

