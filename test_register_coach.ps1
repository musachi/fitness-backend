Write-Host "Testing coach registration (new endpoint)..."

$headers = @{
    'Content-Type' = 'application/json'
}

# Test registering a new coach with the special endpoint
$coachData = @{
    name = "Coach Special Test"
    email = "coachspecial@fitness.com"
    password = "password123"
} | ConvertTo-Json

try {
    Write-Host "Registering new coach via special endpoint..."
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/auth/register-coach' -Method Post -Headers $headers -Body $coachData
    Write-Host "SUCCESS: Coach registered (pending approval)"
    $response | ConvertTo-Json -Depth 3
    
    Write-Host ""
    Write-Host "Coach details:"
    Write-Host "   - Name: $($response.name)"
    Write-Host "   - Email: $($response.email)"
    Write-Host "   - Role: $($response.role.name)"
    Write-Host "   - Is Approved: $($response.is_approved)"
    
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
