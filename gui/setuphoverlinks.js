function hoverLink(link) { 
    window.location.href = "EVT/HOVER_EVENT_START/" + link;
}
function hoverLinkEnd(link) { 
    window.location.href = "EVT/HOVER_EVENT_END/" + link;
}

function setupHoverLinks(elem) { 
    elem.onmouseover = function() {
        hoverLink(elem.href);
    }
    elem.onmouseout = function() {
        hoverLinkEnd(elem.href);
    }
}

// Loop through all links in the document and
// setup some event listeners.
links = document.getElementsByTagName("a");

for (var i = 0; i < links.length; i++) {
        link = links[i].href;
        setupHoverLinks(links[i]);
}