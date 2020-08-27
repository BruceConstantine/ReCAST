var targetBtn = null;


window.onload = function () {

    //TODO: deined JSON data format for post to server here
    function getTargetScenario(btnItem) {
        return btnItem; // type->button
    }

    //Bind event callback to button onclick listener or others listeners....
    var selectableBtnHTMLCollection = document.getElementsByClassName('select-btn')
    var selectableBtnList = [...selectableBtnHTMLCollection]
    var lastSelectedBtn = null;
    //Here the 'scenario_has_selected' is a flag variable showing if one of button is selected.
    //var scenario_has_selected = false;
    //TODO: ASSERT : item here must be button of selectable
    selectableBtnList.forEach(function (item) {
        item.onclick = function () {
            clist = item.classList;
            //If the button has not been selected, user click one button of those all buttons at list.
            if ( lastSelectedBtn != item ){
                item.classList.add("gbtn-selectable");
                if (lastSelectedBtn!=null){
                    lastSelectedBtn.classList.remove("gbtn-selectable")
                }
                display(item.innerText)
                lastSelectedBtn = item;
            } else if (lastSelectedBtn == item) {
            //If the button is selected now, then user click again, button remove the added style.
                lastSelectedBtn.classList.remove("gbtn-selectable");
                lastSelectedBtn = null;
            }
        }
    })

    //targetScenario
}
function display(msg) {
    var finishedList = [...document.getElementsByClassName('finished')]
    var ongoingList  = [...document.getElementsByClassName('ongoing')]
    if (msg=='Finished Task'){      // display Finished
        ongoingList.forEach(function (item) {
            item.style.display = 'none';
        })
        finishedList.forEach(function (item) {
            item.style.display = 'block';
        })
    }
    else if (msg=='Ongoing Task'){
        ongoingList.forEach(function (item) {
            item.style.display = 'block';
        })
        finishedList.forEach(function (item) {
            item.style.display = 'none';
        })
    }
    else if (msg=='All Task'){
        ongoingList.forEach(function (item) {
            item.style.display = 'block';
        })
        finishedList.forEach(function (item) {
            item.style.display = 'block';
        })
    }
}

