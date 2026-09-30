<?php
function pingEndpoint($url, $method = 'GET', $timeoutSeconds = 5) {
    $ch = curl_init();
    
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, $timeoutSeconds);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 3);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_USERAGENT, 'APIMonitor-Engine/2.0');
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, strtoupper($method));
    
    $startTime = microtime(true);
    $response = curl_exec($ch);
    $endTime = microtime(true);
    
    $curlErrno = curl_errno($ch);
    $curlError = curl_error($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $totalTimeMs = round(($endTime - $startTime) * 1000, 2);
    
    curl_close($ch);
    
    if ($curlErrno !== 0 || $httpCode === 0) {
        $status = 'Failed';
        $responseTime = 0.0;
        $httpCode = 0;
    } else {
        $responseTime = $totalTimeMs;
        if ($httpCode >= 200 && $httpCode < 400) {
            $status = ($responseTime < 500) ? 'Healthy' : 'Slow';
        } else {
            $status = 'Failed';
        }
    }
    
    return [
        'status_code'   => (int)$httpCode,
        'response_time' => (float)$responseTime,
        'status'        => $status,
        'error_detail'  => $curlErrno ? $curlError : null
    ];
}
?>
