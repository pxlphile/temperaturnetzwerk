function checkLastUpdateTimestamp() {
	var ts = findTimestamp()
	callStatusServlet(ts);
}

function findTimestamp() {
	return $(".container .date").attr("data-timestamp");
}

function callStatusServlet(timestamp) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			var jsonResult = JSON.parse(xhttp.responseText);
			resolveStatus(jsonResult);
			jsonResult = null;
		}
	};
	xhttp.open("GET", "/klima/statusServlet.php?ts=" + timestamp, true);
	xhttp.send();
}

function resolveStatus(jsonResult) {
	var successDiv = $(".system-state .panel-body div.alert-success");
	var warningDiv = $(".system-state .panel-body div.alert-warning");
	var dangerDiv = $(".system-state .panel-body div.alert-danger");

	if (jsonResult.resultCode == 0) {
		showDiv(successDiv);
		hideDiv(warningDiv);
		hideDiv(dangerDiv);
	} else if (jsonResult.resultCode == 1) {
		hideDiv(successDiv);
		hideDiv(warningDiv);
		showDiv(dangerDiv);
	} else {
		hideDiv(successDiv);
		showDiv(warningDiv);
		hideDiv(dangerDiv);
	}
	$(".panel-body .systemState").attr("title", jsonResult.resultText);
}

function hideDiv(jqueryElement) {
	jqueryElement.addClass("hidden");
}

function showDiv(jqueryElement) {
	jqueryElement.removeClass("hidden");
}
