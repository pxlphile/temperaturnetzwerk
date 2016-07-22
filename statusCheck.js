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
	if (jsonResult.returnCode == 0) {
		$(".panel-body .systemState div.alert-success").addClass("hidden");
		$(".panel-body .systemState div.alert-danger").removeClass("hidden");
	} else if (jsonResult.returnCode == 1) {
		$(".panel-body .systemState div.alert-success").addClass("hidden");
		$(".panel-body .systemState div.alert-danger").removeClass("hidden");
	} else {
		$(".panel-body .systemState div.alert-success").removeClass("hidden");
		$(".panel-body .systemState div.alert-danger").removeClass("hidden");
	}
	$(".panel-body .systemState").attr("title", jsonResult.returnText);
}
