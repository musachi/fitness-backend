$headers = @{
    'Content-Type' = 'application/json'
    'Authorization' = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkMzYyYmVkMC02ZGJjLTQyMGUtODk2Ni1kMjdmNjQ4MjdjYjkiLCJleHAiOjE3NzA3Nzg4MDUsInR5cGUiOiJhY2Nlc3MifQ.-Rbrlb3opkBBs7RhuGf74DHSqX_l1oy5pWrst34jgXI'
}

# Test 1: Try templates endpoint (no auth required)
try {
    Write-Host "Testing templates endpoint..."
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/plans/templates/available' -Method Get
    Write-Host "SUCCESS: Templates endpoint works"
    $response.data.templates.Count | Write-Host
} catch {
    Write-Host "ERROR in templates:" $_.Exception.Message
}

# Test 2: Try public plans endpoint (no auth required)
try {
    Write-Host "Testing public plans endpoint..."
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/plans/' -Method Get
    Write-Host "SUCCESS: Public plans endpoint works"
    $response.data.plans.Count | Write-Host
} catch {
    Write-Host "ERROR in public plans:" $_.Exception.Message
}

# Test 3: Try my plans endpoint (auth required)
try {
    Write-Host "Testing my plans endpoint..."
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/plans/my-plans' -Method Get -Headers $headers
    Write-Host "SUCCESS: My plans endpoint works"
    $response.data.plans.Count | Write-Host
} catch {
    Write-Host "ERROR in my plans:" $_.Exception.Message
    Write-Host "Status:" $_.Exception.Response.StatusCode.value__
}
