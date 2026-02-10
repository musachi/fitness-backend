$headers = @{
    'Content-Type' = 'application/json'
    'Authorization' = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkMzYyYmVkMC02ZGJjLTQyMGUtODk2Ni1kMjdmNjQ4MjdjYjkiLCJleHAiOjE3NzA3Nzg4MDUsInR5cGUiOiJhY2Nlc3MifQ.-Rbrlb3opkBBs7RhuGf74DHSqX_l1oy5pWrst34jgXI'
}

try {
    Write-Host "Testing /api/v1/auth/me endpoint..."
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/auth/me' -Method Get -Headers $headers
    Write-Host "SUCCESS: Auth me endpoint works"
    $response | ConvertTo-Json -Depth 3
    
    Write-Host ""
    Write-Host "User object type:" $response.data.GetType().FullName
    Write-Host "User ID:" $response.data.id
    Write-Host "User role_id:" $response.data.role_id
    
} catch {
    Write-Host "ERROR in auth/me:" $_.Exception.Message
    Write-Host "Status:" $_.Exception.Response.StatusCode.value__
}
