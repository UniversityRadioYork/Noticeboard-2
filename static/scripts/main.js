var swapshow = false;
var shownshow = 1;
var shownpos = 2;

async function getshow(box) {
	const api_url = "/nextlisten";
	fetch(api_url)
		.then((response) => {
			return response.json();
		})
		.then((data) => {
			editshow(data, box);
		});
}

async function getevent() {
	const api_url = "/nextevent";
	fetch(api_url)
		.then((response) => {
			return response.json();
		})
		.then((data) => {
			editevent(data);
		});
}

async function getpositions() {
	const api_url = "/openroles";
	fetch(api_url)
		.then((response) => {
			return response.json();
		})
		.then((data) => {
			editpositions(data);
		})
		.catch((err) => {});
}

async function getuserdata() {
	const api_url = "/userdata";
	fetch(api_url)
		.then((response) => {
			return response.json();
		})
		.then((data) => {
			editcontent(data);
		})
		.catch((err) => {});
}

//I am certain there is a better way to do this but I was too lazy to find it
function swaponeandtwo(num) {
	if (num == 1) {
		return 2;
	} else {
		return 1;
	}
}

function brokenshowimg(num) {
	if (
		document.getElementById("showart" + num).src !=
		"/static/images/default_show_profile.png"
	) {
		document.getElementById("showart" + num).src =
			"/static/images/default_show_profile.png";
	} else {
		document.getElementById("showart" + num).src = "";
	}
}

function editshow(showinfo, box) {
	try {
		document.getElementById("showart" + box).src =
			"https://ury.org.uk" + showinfo["art"];
	} catch (err) {
		document.getElementById("showart" + box).src =
			"/static/images/default_show_profile.png";
	}
	try {
		document.getElementById("showtime" + box).innerHTML = showinfo["time"];
		document.getElementById("showtitle" + box).innerHTML =
			showinfo["title"];
		document.getElementById("showdesc" + box).innerHTML =
			showinfo["description"];
	} catch (err) {
		document.getElementById("showart" + box).src = "";
		document.getElementById("showtitle" + box).innerHTML = "On Tap";
		document.getElementById("showtime" + box).innerHTML = "";
		document.getElementById("showdesc" + box).innerHTML =
			"Checkout some of our old shows online at ury.org.uk/ontap or checkout our Mixcloud: URY1350";
	}
}

function editevent(eventinfo) {
	try {
		document.getElementById("eventtitle").innerHTML = eventinfo["title"];
		document.getElementById("eventtime").innerHTML = eventinfo["time"];
		document.getElementById("eventdesc").innerHTML =
			eventinfo["description"];
	} catch (err) {
		document.getElementById("eventtitle").innerHTML = "No Upcoming Events";
		document.getElementById("eventtime").innerHTML = "";
		document.getElementById("eventdesc").innerHTML =
			"<p>We don't have any events scheduled but keep your eye on our Slack for updates!</p>";
	}
}

function editcontent(contentinfo) {
	try {
		console.log(contentinfo);
		for (const key in contentinfo) {
			document.getElementById(key).innerHTML = contentinfo[key];
		}
		if (
			document.getElementById("extralabel").innerHTML == "" &&
			document.getElementById("extrahtml").innerHTML == ""
		) {
			document.getElementById("extrabox").style =
				"opacity: 0; position: absolute;";
		} else {
			document.getElementById("extrabox").style =
				"opacity: 1; position: relative;";
		}
	} catch (err) {}
}

function editpositions(positioninfo) {
	try {
		if (positioninfo.length < 1) {
			document.getElementById("positions").innerHTML =
				"<h4>We don't have any vacancies on our committee at the moment but roles can free up at any time so keep your eye out!</h4>";
			document.getElementById("openpos1").innerHTML = "";
			document.getElementById("openpos2").innerHTML = "";
			document.getElementById("openpos3").innerHTML = "";
			document.getElementById("openpos4").innerHTML = "";
		} else {
			document.getElementById("positions").innerHTML =
				"<br><h2>Open Positions:</h2>";
			let typehtml = {
				Management: "",
				"Team Heads": "",
				"Team Deputies": "",
				"Other Officers": "",
			};
			for (var i = 0; i < positioninfo.length; i++) {
				typehtml[positioninfo[i]["category"]] +=
					"<p>" + positioninfo[i]["name"] + "</p>";
			}
			for (const key in typehtml) {
				if (typehtml[key] != "") {
					typehtml[key] = "<h3>" + key + "</h3>" + typehtml[key];
				}
			}
			document.getElementById("openpos1").innerHTML =
				typehtml["Management"];
			document.getElementById("openpos2").innerHTML =
				typehtml["Team Heads"];
			document.getElementById("openpos3").innerHTML =
				typehtml["Team Deputies"];
			document.getElementById("openpos4").innerHTML =
				typehtml["Other Officers"];
		}
	} catch (err) {
		document.getElementById("positions").innerHTML =
			"<h4>We don't have any vacancies on our committee at the moment but roles can free up at any time so keep your eye out!</h4>";
		document.getElementById("openpos1").innerHTML = "";
		document.getElementById("openpos2").innerHTML = "";
		document.getElementById("openpos3").innerHTML = "";
		document.getElementById("openpos4").innerHTML = "";
	}
}

async function updateshow() {
	if (swapshow) {
		var toswap = swaponeandtwo(shownshow);
		document.getElementById("box" + shownshow).style = "opacity: 0";
		document.getElementById("box" + toswap).style = "opacity: 1";
		shownshow = toswap;
	} else {
		getshow(swaponeandtwo(shownshow));
	}
	swapshow = !swapshow;
}

function rotatepos() {
	var toswap = shownpos;
	var swapped = false;
	while (!swapped) {
		toswap++;
		if (toswap > 4) {
			toswap = 1;
		}
		if (document.getElementById("openpos" + toswap).innerHTML != "") {
			swapped = true;
		}
		if (toswap == shownpos) {
			console.log("noswap");
			return;
		}
	}
	document.getElementById("openpos" + shownpos).style = "opacity: 0";
	document.getElementById("openpos" + toswap).style = "opacity: 1";
	shownpos = toswap;
}

function updateloop() {
	updateshow();
	rotatepos();
	getuserdata();
	getevent();
	getpositions();
}

document.getElementById("showart1").onerror = brokenshowimg(1);
document.getElementById("showart2").onerror = brokenshowimg(2);

getuserdata();
getpositions();
getshow(1);
getshow(2);
getevent();

setInterval(updateloop, 15 * 1000);
