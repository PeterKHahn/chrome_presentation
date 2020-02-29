$(function() {
    $('.content').removeClass('fade-out');
});


var req = new XMLHttpRequest(); 
req.onreadystatechange = handleResponse


function g() {

    req.open('GET', '/retrieve_next', true)
    req.send() 
}

g()

window.setInterval(g, 500 * 1000) 





function handleResponse() {
    if (req.readyState === XMLHttpRequest.DONE) {
        if (req.status === 200) {
            json = JSON.parse(req.responseText)

            handleState(json.info, json.candidates) ; 


        }
    }

}

function handleState(info, candidates) {
    $('.content').addClass('fade-out'); 


    $('.info-item.percent-reporting').text(info.percentage_reporting);
    $('.info-item.precincts-reporting').text(info.precincts_reporting); 
    $('.info-item.total-votes').text(info.total_votes); 
    $('.state').text(info.state)

    $(".voting-table-rowset").empty()

    for (idx in candidates){
        candidate = candidates[idx]

        var row = $("<div class=voting-table-row></div>")
        


        var name = $("<div class='voting-table-cell names normal-cell'></div>")
        if(candidate.winner) {
            name.addClass("winner")
        }
        name.text(candidate.name)
        var avatar_div = $("<div class='voting-table-cell avatars normal-cell'></div>")
        var avatar = $("<img class=avatar height='80' width='80'>")
        avatar.attr("src", candidate.avatar)
        avatar_div.append(avatar)
        console.log(avatar_div)

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
        $(".voting-table-rowset").append(row)



    }
    
    window.setTimeout(function(){
        $('.content').removeClass('fade-out'); 
    })

}

