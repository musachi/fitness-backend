$headers = @{
    'Content-Type' = 'application/json'
    'Authorization' = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkMzYyYmVkMC02ZGJjLTQyMGUtODk2Ni1kMjdmNjQ4MjdjYjkiLCJleHAiOjE3NzA3Nzg4MDUsInR5cGUiOiJhY2Nlc3MifQ.-Rbrlb3opkBBs7RhuGf74DHSqX_l1oy5pWrst34jgXI'
}

try {
    # Try to get user profile to see role information
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/users/me' -Method Get -Headers $headers
    Write-Host "User Profile:"
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "Error getting user profile:" $_.Exception.Message
    Write-Host "Status:" $_.Exception.Response.StatusCode.value__
}

try {
    # Try to get all users to see roles (this might fail due to permissions)
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/users/' -Method Get -Headers $headers
    Write-Host "All Users:"
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "Error getting all users:" $_.Exception.Message
    Write-Host "Status:" $_.Exception.Response.StatusCode.value__
}
