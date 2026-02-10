$headers = @{
    'Content-Type' = 'application/json'
}

$loginData = @{
    email = 'admin@fitness.com'
    password = 'password123'
} | ConvertTo-Json

try {
    Write-Host "Testing admin login..."
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/auth/login' -Method Post -Headers $headers -Body $loginData
    Write-Host "SUCCESS: Admin login works!"
    Write-Host "Token: $($response.access_token.Substring(0,20))..."
    Write-Host "Role ID: $($response.role_id)"
    
    # Save token for next test
    $response.access_token | Out-File -FilePath "admin_token.txt" -Encoding UTF8
    Write-Host "Admin token saved to admin_token.txt"
    
} catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Status: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        $reader = [System.IO.StreamReader]::new($_.Exception.Response.GetResponseStream())
        $reader.BaseStream.Position = 0
        $errorBody = $reader.ReadToEnd()
        Write-Host "Error body: $errorBody"
        $reader.Close()
    }
}
