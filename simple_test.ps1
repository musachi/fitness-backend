$headers = @{
    'Content-Type' = 'application/json'
    'Authorization' = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkMzYyYmVkMC02ZGJjLTQyMGUtODk2Ni1kMjdmNjQ4MjdjYjkiLCJleHAiOjE3NzA3Nzg4MDUsInR5cGUiOiJhY2Nlc3MifQ.-Rbrlb3opkBBs7RhuGf74DHSqX_l1oy5pWrst34jgXI'
}

Write-Host "Testing user permissions..." -ForegroundColor Cyan

# Test 1: Try to create plan (should fail)
Write-Host "Test 1: Create plan (should fail)" -ForegroundColor Yellow
$body = '{"name":"Test Plan","duration_weeks":4}' | ConvertFrom-Json

try {
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/plans/' -Method Post -Headers $headers -Body (ConvertTo-Json $body)
    Write-Host "ERROR: User should not be able to create plans!" -ForegroundColor Red
} catch {
    if ($_.Exception.Response.StatusCode.value__ -eq 403) {
        Write-Host "SUCCESS: Create plan correctly denied (403)" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Unexpected status code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
    }
}

# Test 2: Try to generate plan (should fail)
Write-Host ""
Write-Host "Test 2: Generate plan (should fail)" -ForegroundColor Yellow
$body2 = '{"template_name":"beginner_full_body","custom_name":"Test"}' | ConvertFrom-Json

try {
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/plans/generate-from-template' -Method Post -Headers $headers -Body (ConvertTo-Json $body2)
    Write-Host "ERROR: User should not be able to generate plans!" -ForegroundColor Red
} catch {
    if ($_.Exception.Response.StatusCode.value__ -eq 403) {
        Write-Host "SUCCESS: Generate plan correctly denied (403)" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Unexpected status code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
    }
}

# Test 3: View plans (should work)
Write-Host ""
Write-Host "Test 3: View plans (should work)" -ForegroundColor Yellow

try {
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/plans/my-plans' -Method Get -Headers $headers
    Write-Host "SUCCESS: User can view their plans ($($response.data.plans.Count) plans)" -ForegroundColor Green
} catch {
    Write-Host "ERROR: User should be able to view their plans" -ForegroundColor Red
}

Write-Host ""
Write-Host "Permissions test complete!" -ForegroundColor Cyan
