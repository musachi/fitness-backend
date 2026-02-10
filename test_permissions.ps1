# Test permissions validation
$headers = @{
    'Content-Type' = 'application/json'
    'Authorization' = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkMzYyYmVkMC02ZGJjLTQyMGUtODk2Ni1kMjdmNjQ4MjdjYjkiLCJleHAiOjE3NzA3Nzg4MDUsInR5cGUiOiJhY2Nlc3MifQ.-Rbrlb3opkBBs7RhuGf74DHSqX_l1oy5pWrst34jgXI'
}

Write-Host "🔒 TESTING PERMISSIONS VALIDATION" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Current user role_id: 3 (Normal user)" -ForegroundColor Yellow
Write-Host ""

# Test 1: User CAN view their plans
Write-Host "✅ Testing: User CAN view their plans" -ForegroundColor Green
try {
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/plans/my-plans' -Method Get -Headers $headers
    Write-Host "SUCCESS: User can view their plans ($($response.data.plans.Count) plans found)" -ForegroundColor Green
} catch {
    Write-Host "ERROR: User should be able to view their plans" -ForegroundColor Red
}

# Test 2: User CANNOT create plans
Write-Host ""
Write-Host "❌ Testing: User CANNOT create plans" -ForegroundColor Red
$body = @{
    name = "Test Plan"
    duration_weeks = 4
    goal = "general_fitness"
    level = "beginner"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/plans/' -Method Post -Headers $headers -Body $body
    Write-Host "ERROR: User should NOT be able to create plans!" -ForegroundColor Red
} catch {
    if ($_.Exception.Response.StatusCode.value__ -eq 403) {
        Write-Host "SUCCESS: User correctly denied access to create plans (403)" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Unexpected error: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
    }
}

# Test 3: User CANNOT generate plans from templates
Write-Host ""
Write-Host "❌ Testing: User CANNOT generate plans from templates" -ForegroundColor Red
$body = @{
    template_name = "beginner_full_body"
    custom_name = "Test Template Plan"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/plans/generate-from-template' -Method Post -Headers $headers -Body $body
    Write-Host "ERROR: User should NOT be able to generate plans!" -ForegroundColor Red
} catch {
    if ($_.Exception.Response.StatusCode.value__ -eq 403) {
        Write-Host "SUCCESS: User correctly denied access to generate plans (403)" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Unexpected error: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
    }
}

# Test 4: User CAN view public plans
Write-Host ""
Write-Host "✅ Testing: User CAN view public plans" -ForegroundColor Green
try {
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/plans/' -Method Get
    Write-Host "SUCCESS: User can view public plans" -ForegroundColor Green
} catch {
    Write-Host "ERROR: User should be able to view public plans" -ForegroundColor Red
}

# Test 5: User CAN view templates
Write-Host ""
Write-Host "✅ Testing: User CAN view templates" -ForegroundColor Green
try {
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/plans/templates/available' -Method Get
    Write-Host "SUCCESS: User can view templates ($($response.data.templates.Count) templates available)" -ForegroundColor Green
} catch {
    Write-Host "ERROR: User should be able to view templates" -ForegroundColor Red
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "🎯 PERMISSIONS VALIDATION COMPLETE!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 SUMMARY:" -ForegroundColor Blue
Write-Host "   ✅ Normal users can VIEW their assigned plans" -ForegroundColor Gray
Write-Host "   ✅ Normal users can VIEW public plans" -ForegroundColor Gray
Write-Host "   ✅ Normal users can VIEW templates" -ForegroundColor Gray
Write-Host "   ❌ Normal users CANNOT CREATE plans" -ForegroundColor Gray
Write-Host "   ❌ Normal users CANNOT GENERATE plans" -ForegroundColor Gray
Write-Host ""
Write-Host "🔐 To test admin/coach permissions, you need a token with role_id 1 or 2" -ForegroundColor Yellow
