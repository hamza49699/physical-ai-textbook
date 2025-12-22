# PowerShell script to test deployed backend APIs
$baseUrl = "https://hamzakhan123-physical-ai-textbook.hf.space"

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "Testing Physical AI Textbook Backend" -ForegroundColor Cyan
Write-Host "URL: $baseUrl" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

$results = @{}

# Test 1: Root endpoint
Write-Host "`n=== Testing Root Endpoint ===" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/" -Method Get -ErrorAction Stop
    Write-Host "Status: SUCCESS" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 10
    $results["Root"] = $true
} catch {
    Write-Host "Status: FAILED" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    $results["Root"] = $false
}

# Test 2: Health endpoint
Write-Host "`n=== Testing Health Endpoint ===" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/health" -Method Get -ErrorAction Stop
    Write-Host "Status: SUCCESS" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 10
    $results["Health"] = $true
} catch {
    Write-Host "Status: FAILED" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    $results["Health"] = $false
}

# Test 3: Database Health
Write-Host "`n=== Testing Database Health ===" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/health/db" -Method Get -ErrorAction Stop
    Write-Host "Status: SUCCESS" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 10
    $results["Health/DB"] = $true
} catch {
    Write-Host "Status: FAILED" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    $results["Health/DB"] = $false
}

# Test 4: Qdrant Health
Write-Host "`n=== Testing Qdrant Health ===" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/health/qdrant" -Method Get -ErrorAction Stop
    Write-Host "Status: SUCCESS" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 10
    $results["Health/Qdrant"] = $true
} catch {
    Write-Host "Status: FAILED" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    $results["Health/Qdrant"] = $false
}

# Test 5: Query endpoint
Write-Host "`n=== Testing Query Endpoint ===" -ForegroundColor Yellow
try {
    $body = @{
        query = "What is ROS2?"
        use_rag = $true
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$baseUrl/query" -Method Post -Body $body -ContentType "application/json" -ErrorAction Stop
    Write-Host "Status: SUCCESS" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 10
    $results["Query"] = $true
} catch {
    Write-Host "Status: FAILED" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    $results["Query"] = $false
}

# Test 6: Documents endpoint
Write-Host "`n=== Testing Documents Endpoint ===" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/documents" -Method Get -ErrorAction Stop
    Write-Host "Status: SUCCESS" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 10
    $results["Documents"] = $true
} catch {
    Write-Host "Status: FAILED" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    $results["Documents"] = $false
}

# Summary
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "TEST SUMMARY" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$passed = 0
foreach ($test in $results.Keys) {
    $status = if ($results[$test]) { 
        $passed++
        "✓ PASS" 
    } else { 
        "✗ FAIL" 
    }
    $color = if ($results[$test]) { "Green" } else { "Red" }
    Write-Host ("{0,-20} {1}" -f $test, $status) -ForegroundColor $color
}

$total = $results.Count
Write-Host "`nTotal: $passed/$total tests passed" -ForegroundColor $(if ($passed -eq $total) { "Green" } else { "Yellow" })
