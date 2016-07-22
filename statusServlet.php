<?php
/**
 * <p>This file calculates the difference from the client's timestamp and the current server
 * timestamp, and responses with an JSON object which includes three key/value pairs:</p>
 * <ul>
 * <li>resultCode: 0 if everything is okay; 1 if the difference is greater than two minutes; other values for incorrect usage</li> 
 * <li>timeDelta: absolute time difference in seconds. 'NULL' for incorrect usage</li> 
 * <li>resultText: a textual description of the script result</li></ul>
 *
 * This file can be tested with PHPs commandline interface php like this:
 * <code>php statusServlet.php 'ts=1469167424'</code>
 */
define("TIMESTAMP_GET_PARAMETER_NAME", "ts");
define("TWO_MINUTES_IN_SECONDS", 120);
define("DEBUG", false);
define("RETURN_CODE_OK", 0);
define("RETURN_CODE_UNSYNCED", 1);
define("RETURN_CODE_WRONG_TS_FORMAT", 2);
define("RETURN_CODE_NO_TS_PARAMETER", 4);

/**
 * Validates if a GET parameter is set.
 * Converts commandline parameters to GET parameters if run on commandline.
 */
function setupCliParameter($cliParameter) {
	if(! (isset($cliParameter) || isset($_GET[TIMESTAMP_GET_PARAMETER_NAME]))) {
		print "No parameter. Sorry, I am giving up.";
		exit(254);
	}
	
	if (!isset($_SERVER["REQUEST_METHOD"])) {
		// script is not interpreted due to some call via http, so it must be called from the commandline
		parse_str($cliParameter, $_GET); //convert CLI parameters to GET parameters
	}
	
	if(!isset($_GET[TIMESTAMP_GET_PARAMETER_NAME])) {
		print "No get parameter. Sorry, I am giving up.";
		exit(253);
	}
}

/**
 * Validates the timestamp parameter. Exits with an error response if the timestamp is empty.
 */
function assertNonEmptyParameter() {
	if (empty(getApplicationTimestamp())) { 
		$responseData = buildResponse(
			RETURN_CODE_NO_TS_PARAMETER, 
			'NULL', 
			'Could not check status. No timestamp was given.');
		deliverResponse($responseData, RETURN_CODE_NO_TS_PARAMETER);
	}
}

/**
 * Validates the timestamp parameter. Exits with an error response if the timestamp does not consist of 10 decimal ciphers.
 */
function assertTimestampFormat() {
	$timestampPattern = "/\d{10}/";
	$timestamp = getApplicationTimestamp();
	if(preg_match($timestampPattern, $timestamp) != 1) {
		$responseData = buildResponse(
			RETURN_CODE_WRONG_TS_FORMAT, 
			'NULL', 
			'Could not check status. The timestamp (epoch time in gmt) does not seem to be valid.');
		deliverResponse($responseData, RETURN_CODE_WRONG_TS_FORMAT);
	}
}

/**
 * compares both client and server timestamp. Then the function responses with JSON and exits.
 */
function checkApplicationStatus() {
	$lastApplicationTimestamp = getApplicationTimestamp();
	$currentUtcTimestamp = buildCurrentUtcTimestamp();
	
	debugln("lastApplicationTimestamp is $lastApplicationTimestamp");
	debugln("currentUtcTimestamp is $currentUtcTimestamp");
	
	$timeDelta = abs($currentUtcTimestamp - $lastApplicationTimestamp);
	
	if($timeDelta > TWO_MINUTES_IN_SECONDS) {
		$responseData = buildResponse(
			RETURN_CODE_UNSYNCED, 
			$timeDelta, 
			"Application timing doesn't look too well. Time differs by $timeDelta seconds.");
		deliverResponse($responseData, RETURN_CODE_UNSYNCED);
	} else {
		$responseData = buildResponse(
			RETURN_CODE_OK, 
			$timeDelta, 
			"Application seems to do it's job. Time differs by $timeDelta seconds.");
		deliverResponse($responseData, RETURN_CODE_OK);
	}
}

/** 
 * returns the server timestamp. The local timezone is substracted from 
 */
function buildCurrentUtcTimestamp() {
	$timeZoneOffset = date('Z');
	debugln("timezone offset is $timeZoneOffset seconds");
	return time() - $timeZoneOffset;
}

/**
 * returns the client timestamp via GET parameter. This timestamp is regarded as GMT/UTC.
 */
function getApplicationTimestamp() {
	return $_GET[TIMESTAMP_GET_PARAMETER_NAME];
}

/**
 * prints the result data as JSON to STDOUT and exits with a given exit code
 */
function deliverResponse($resultData, $exitCode) {
	echo json_encode($resultData);
	exit($exitCode);
}

function debugln($data) {
	if(DEBUG === true) {
		print $data . "\n";
	}
}

function buildResponse($resultCode, $timeDelta, $resultText) {
	return array('resultCode' => $resultCode, 
		'timeDelta' => $timeDelta,
		'resultText' => $resultText
		);
}

setupCliParameter($argv[1]);

assertNonEmptyParameter();
assertTimestampFormat();
checkApplicationStatus();

exit(255); //fallback if things go bad
?>