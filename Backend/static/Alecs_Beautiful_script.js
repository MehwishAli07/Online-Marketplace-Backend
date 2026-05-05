

// Alec's javascript stuff below -----------------------------------------------------------------------//

// this is javacript function which is called by onclick in the html file.. it reveals a larger hidden image
function enlargeImage(src) {
    // image container and the empty image tag inside it
    const overlay = document.getElementById('imageOverlay');
    const bigImg = document.getElementById('overlayImg');
        
    // put the same image as the one clicked intide the larger image container 
    bigImg.src = src;
        
    // put the image display to flex to ensure it doesn't break... the default is hidden so anything will work here 
    overlay.style.display = 'flex';
}

// this is the javascript functhion which makes the large popup of the image go away.. called by onclick in the html file 
function closeImage() {
    const overlay = document.getElementById('imageOverlay');
    overlay.style.display = 'none';
}

// end Alec's Javascript stuff  -----------------------------------------------------------------------//