$headers = @{
    'Content-Type' = 'application/json'
}

$body = @{
    email = 'coach@fitness.com'
    password = 'password123'
} | ConvertTo-Json

try {
    Write-Host "Testing coach login..."
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/auth/login' -Method Post -Headers $headers -Body $body
    Write-Host "Response:"
    $response | ConvertTo-Json -Depth 3
    
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
