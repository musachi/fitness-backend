Write-Host "Testing unapproved coach login (should fail)..."

# Test coach login with JSON endpoint
$headers = @{
    'Content-Type' = 'application/json'
}

$coachLogin = @{
    email = 'newcoach@fitness.com'
    password = 'password123'
} | ConvertTo-Json

try {
    Write-Host "Trying login with unapproved coach..."
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/auth/login-json' -Method Post -Headers $headers -Body $coachLogin
    Write-Host "ERROR: Unapproved coach should not be able to login!" -ForegroundColor Red
} catch {
    if ($_.Exception.Response.StatusCode.value__ -eq 403) {
        Write-Host "SUCCESS: Unapproved coach correctly blocked (403)" -ForegroundColor Green
        Write-Host "Message: Coach account is pending approval"
    } else {
        Write-Host "ERROR: Unexpected status: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
    }
}
