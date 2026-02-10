$headers = @{
    'Content-Type' = 'application/json'
    'Authorization' = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkMzYyYmVkMC02ZGJjLTQyMGUtODk2Ni1kMjdmNjQ4MjdjYjkiLCJleHAiOjE3NzA3Nzg4MDUsInR5cGUiOiJhY2Nlc3MifQ.-Rbrlb3opkBBs7RhuGf74DHSqX_l1oy5pWrst34jgXI'
}

Write-Host "Testing plan generation with new fields..."

$body = @{
    template_name = 'beginner_full_body'
    custom_name = 'Plan with Description Test'
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/plans/generate-from-template' -Method Post -Headers $headers -Body $body
    Write-Host "SUCCESS: Plan generated"
    $response.data | ConvertTo-Json -Depth 3
} catch {
    Write-Host "ERROR: Plan generation failed"
    Write-Host "Status: $($_.Exception.Response.StatusCode.value__)"
}
