$headers = @{
    'Content-Type' = 'application/json'
}

$body = @{
    email = 'coach@fitness.com'
    password = 'password123'
} | ConvertTo-Json

try {
    Write-Host "Getting coach token..."
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/auth/login' -Method Post -Headers $headers -Body $body
    Write-Host "SUCCESS: Coach token obtained"
    $token = $response.data.access_token
    Write-Host "Token: $token"
    
    # Save token to file for next test
    $token | Out-File -FilePath "coach_token.txt" -Encoding UTF8
    Write-Host "Token saved to coach_token.txt"
    
} catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Status: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
}
