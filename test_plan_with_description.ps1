$headers = @{
    'Content-Type' = 'application/json'
    'Authorization' = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkMzYyYmVkMC02ZGJjLTQyMGUtODk2Ni1kMjdmNjQ4MjdjYjkiLCJleHAiOjE3NzA3Nzg4MDUsInR5cGUiOiJhY2Nlc3MifQ.-Rbrlb3opkBBs7RhuGf74DHSqX_l1oy5pWrst34jgXI'
}

Write-Host "🧪 Testing plan generation with description, goal, and level" -ForegroundColor Cyan

$body = @{
    template_name = 'beginner_full_body'
    custom_name = 'Plan Completo con Descripción'
} | ConvertTo-Json

try {
    Write-Host "Generating plan from template..."
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/plans/generate-from-template' -Method Post -Headers $headers -Body $body
    Write-Host "SUCCESS: Plan generated with new fields!"
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Status: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
}

Write-Host ""
Write-Host "📋 Checking plan details..." -ForegroundColor Cyan

try {
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/plans/my-plans' -Method Get -Headers $headers
    Write-Host "SUCCESS: Retrieved user plans"
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
}
