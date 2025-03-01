//this script just handles the fancy backgrounds.
//shout out the Jamie Parker-East for walking around campus with me (James Pursglove) for 3 hours and letting me use his tripod

//sets some tracking values, picks a random next background, loads the backgrounds and initiates the slide
var current = 2;
var image1 = Math.floor(Math.random() * 12) + 2;
//always starts with the ury station background
var image2 = 1;
var div2 = document.getElementById("sliding-background2");
var div1 = document.getElementById("sliding-background1");
div1.style.background =
	"url('static/images/backgrounds/Campus/" + image1 + ".jpg')";
div2.style.background =
	"url('static/images/backgrounds/Campus/" + image2 + ".jpg')";
div2.classList.add("doslide");

//called on animation end
//swaps the current background
function myEndFunction() {
	if (current == 2) {
		do {
			image1 = Math.floor(Math.random() * 13) + 1;
		} while (image1 == image2);
		div1.classList.add("doslide");
		//begins another animation so that the background still moves during the fade
		div2.classList.add("doslidemore");
		div2.style.opacity = 0;
		current = 1;
	} else {
		do {
			image2 = Math.floor(Math.random() * 13) + 1;
		} while (image1 == image2);
		div2.classList.add("doslide");
		div1.classList.add("doslidemore");
		div2.style.opacity = 1;
		current = 2;
	}
}

//called on transition between backgrounds being completed
//clears animation classes so they work when re-applied and loads a new image
function transitionfunction() {
	console.log("transition");
	if (current == 2) {
		div1.classList.remove("doslide");
		div1.classList.remove("doslidemore");
		div1.style.background =
			"url('static/images/backgrounds/Campus/" + image1 + ".jpg')";
		div1.classList.add("sliding-background");
	} else {
		div2.classList.remove("doslide");
		div2.classList.remove("doslidemore");
		div2.style.background =
			"url('static/images/backgrounds/Campus/" + image2 + ".jpg')";
		div1.classList.add("sliding-background");
	}
}

//creates listeners
div1.addEventListener("animationend", myEndFunction);
div2.addEventListener("animationend", myEndFunction);
div1.addEventListener("transitionend", transitionfunction);
div2.addEventListener("transitionend", transitionfunction);
