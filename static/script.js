// get user input
document.getElementById("channel").addEventListener("input", updateUrl);
document.getElementById("use_atom").addEventListener("input", updateUrl);

function updateUrl() {
	var base_url = document.getElementById("base_url").href;
	var feed_type = "rss";
	// url parameters
	var params = [];

	var channel = document.getElementById("channel").value;
	var use_atom = document.getElementById("use_atom").checked;


	if (channel) {
		url = base_url + "/" + channel;
	} else {
		url = base_url;
	}

	if (use_atom) {
		feed_type = "atom";
	}
	params.push("ft=" + feed_type);

	// add params to url
	url = url + "?" + params.join("&");

	document.getElementById("dynamic_url").href = url;
	document.getElementById("dynamic_url").text = url;
}

// initial update
updateUrl();
