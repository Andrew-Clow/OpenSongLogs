function selectElementText(elt){
    el = elt.childNodes[0];
    var range = document.createRange(); // create new range object
    range.selectNodeContents(el); // set range to encompass desired element text
    var selection = window.getSelection(); // get Selection object from currently user selected text
    selection.removeAllRanges(); // unselect any user selected text (if any)
    selection.addRange(range); // add range to Selection object to select it
    document.execCommand("copy");
}

function selectFullElementText(el){
    var range = document.createRange(); // create new range object
    range.selectNodeContents(el); // set range to encompass desired element text
    var selection = window.getSelection(); // get Selection object from currently user selected text
    selection.removeAllRanges(); // unselect any user selected text (if any)
    selection.addRange(range); // add range to Selection object to select it
    document.execCommand("copy");
}

function toggletooltip(e) {
    if (e.classList.contains('tooltipyes')){
        $('.tooltipyes').removeClass('tooltipyes');
    } else {
        $('.tooltipyes').removeClass('tooltipyes')
        e.classList.add('tooltipyes')
    }
}


function resetsearch(){
    $('.tooltipyes').removeClass('tooltipyes');
    $('#tosong').val('');
    $('#fromsong').val('');
    //$('#to tr').removeClass('goaway');
    $('#searchbox').val('').removeClass('completed');
}

function copyPreviousInto(elt,destination){
	var el = elt.previousElementSibling;
	//window.alert(el.textContent);
    var range = document.createRange(); // create new range object
    range.selectNodeContents(el); // set range to encompass desired element text
    var selection = window.getSelection(); // get Selection object from currently user selected text
    selection.removeAllRanges(); // unselect any user selected text (if any)
    selection.addRange(range); // add range to Selection object to select it
    document.execCommand("copy");
    var thingy = document.getElementById(destination);
    thingy.value += el.innerText;
    thingy.scrollTop = thingy.scrollHeight;
}

function copyPrevious(elt){
	var el = elt.previousElementSibling;
	//window.alert(el.textContent);
    var range = document.createRange(); // create new range object
    range.selectNodeContents(el); // set range to encompass desired element text
    var selection = window.getSelection(); // get Selection object from currently user selected text
    selection.removeAllRanges(); // unselect any user selected text (if any)
    selection.empty(); // unselect any user selected text (if any)
    selection.addRange(range); // add range to Selection object to select it
	window.alert(range.toString());    
	window.alert(selection.toString());    
    document.execCommand("copy");        
}

function onEnterZapNonMatchingSubthingsOf(e,searchID,subthingType,ofID){
    // look for window.event in case event isn't passed in
    e = e || window.event;
    if (e.keyCode == 13) {
        zapNonMatchingSubthingsOf(searchID,subthingType,ofID);
        return false;
    }
    return true;
}

$.extend($.expr[":"], {
"containsCaseInsensitive": function(elem, i, match, array) {
return (elem.textContent || elem.innerText || "").toLowerCase().indexOf((match[3] || "").toLowerCase()) >= 0;
}
});

/* ________________ zapping stuff ____________________ */

const completedclass = 'completed';

function zapNonMatchingSubthingsOf(searchID,subthingType,ofID){
    $searchthing = $('#'+searchID);
    $them = $('#'+ofID+' '+subthingType);
    $them.addClass('goaway');
    $them.filter(":containsCaseInsensitive("+$searchthing.val()+")").removeClass('goaway');
    $searchthing.addClass(completedclass);    
}

function uncomplete(elt){
    if (typeof elt === 'string' || elt instanceof String) {
        $('#'+elt).removeClass(completedclass);
    } else {
        elt.classList.remove(completedclass);
    }
}

function complete(elt){
    if (typeof elt === 'string' || elt instanceof String) {
        $('#'+elt).addClass(completedclass);
    } else {
        elt.classList.add(completedclass);
    }
}

function zapIfNonEmpty(){
    $searchbox=$('#searchbox');
    if ($searchbox.val()) {
        zapNonMatchingSubthingsOf('searchbox','tr','to');
    } else {
        cancelSearch();
    };
}

function cancelSearch(){
    $('#searchbox').val('');
    $('#to .tooltipyes').removeClass('tooltipyes');
    $('#tosong').val('');
}

function makeReplacement(fromID,toID,replacementID){
    var fromElt = document.getElementById(fromID);
    var toElt = document.getElementById(toID);
    var replacementElt = document.getElementById(replacementID);
    replacementElt.value += '    "' + fromElt.value + '":"' + toElt.value + '",\n'
    replacementElt.scrollTop = replacementElt.scrollHeight;
}

function clearOrCopyPreviousInto(elt,destination,ifclass){
    var thingy = document.getElementById(destination);
    thingy.value = "";
    if (elt.classList.contains(ifclass)) {
        copyPreviousInto(elt,destination);
    } 
}

function clearOrCopySecondInto(elt,destination,ifclass){
    var thingy = document.getElementById(destination);
    thingy.innerHTML = "";
    el = elt.childNodes[1];
    if (elt.classList.contains(ifclass)) {
        thingy.innerHTML = el.innerHTML;
//        window.alert(el.textContent);
    } 
}

function byebye(elt){
    elt
    	.parentElement
    	.style.display = 'none';
}
function byebyetop(elt){
    elt
       	.parentElement
    	.parentElement
    	.parentElement
    	.parentElement
    	.parentElement
    	.parentElement
    	.parentElement
    	.style.display = 'none';
}

