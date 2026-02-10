# Authenticated API Test Script for Plan endpoints
# Replace YOUR_JWT_TOKEN_HERE with your actual token

$BASE_URL = "http://127.0.0.1:8000"
$API_BASE = "$BASE_URL/api/v1"

# 🔐 SET YOUR JWT TOKEN HERE
$JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkMzYyYmVkMC02ZGJjLTQyMGUtODk2Ni1kMjdmNjQ4MjdjYjkiLCJleHAiOjE3NzA3Nzg4MDUsInR5cGUiOiJhY2Nlc3MifQ.-Rbrlb3opkBBs7RhuGf74DHSqX_l1oy5pWrst34jgXI"

$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer $JWT_TOKEN"
}

Write-Host "🚀 Testing Fitness Backend Plan API with Authentication" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

if ($JWT_TOKEN -eq "YOUR_JWT_TOKEN_HERE") {
    Write-Host "⚠️  Please update the JWT_TOKEN variable with your actual token" -ForegroundColor Yellow
    Write-Host "   You can get a token by logging in at: $BASE_URL/api/v1/auth/login" -ForegroundColor Yellow
    Write-Host ""
    return
}

# Function to write colored output
function Write-Status {
    param(
        [string]$Status,
        [string]$Message
    )
    
    switch ($Status) {
        "SUCCESS" { Write-Host "✅ $Message" -ForegroundColor Green }
        "ERROR"   { Write-Host "❌ $Message" -ForegroundColor Red }
        "INFO"    { Write-Host "ℹ️  $Message" -ForegroundColor Blue }
        "WARNING" { Write-Host "⚠️  $Message" -ForegroundColor Yellow }
        default   { Write-Host $Message }
    }
}

# Function to test endpoint with authentication
function Test-AuthEndpoint {
    param(
        [string]$Method,
        [string]$Endpoint,
        [string]$Data,
        [string]$Description
    )
    
    Write-Host ""
    Write-Host "Testing: $Description" -ForegroundColor Blue
    Write-Host "Request: $Method $Endpoint"
    
    try {
        if ($Method -eq "GET") {
            $response = Invoke-RestMethod -Uri "$API_BASE$Endpoint" -Method Get -Headers $headers -ErrorAction Stop
            Write-Status "SUCCESS" "HTTP 200 - $Description"
            $response | ConvertTo-Json -Depth 3 | Write-Host
            return $response
        }
        elseif ($Method -eq "POST") {
            $body = $Data | ConvertFrom-Json
            $response = Invoke-RestMethod -Uri "$API_BASE$Endpoint" -Method Post -Headers $headers -Body (ConvertTo-Json $body) -ErrorAction Stop
            Write-Status "SUCCESS" "HTTP 200 - $Description"
            $response | ConvertTo-Json -Depth 3 | Write-Host
            return $response
        }
        elseif ($Method -eq "PUT") {
            $body = $Data | ConvertFrom-Json
            $response = Invoke-RestMethod -Uri "$API_BASE$Endpoint" -Method Put -Headers $headers -Body (ConvertTo-Json $body) -ErrorAction Stop
            Write-Status "SUCCESS" "HTTP 200 - $Description"
            $response | ConvertTo-Json -Depth 3 | Write-Host
            return $response
        }
        elseif ($Method -eq "DELETE") {
            $response = Invoke-RestMethod -Uri "$API_BASE$Endpoint" -Method Delete -Headers $headers -ErrorAction Stop
            Write-Status "SUCCESS" "HTTP 200 - $Description"
            $response | ConvertTo-Json -Depth 3 | Write-Host
            return $response
        }
    }
    catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        if ($statusCode) {
            Write-Status "ERROR" "HTTP $statusCode - $Description"
            Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        } else {
            Write-Status "ERROR" "Connection failed - $Description"
            Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        }
        return $null
    }
}

Write-Host "Starting authenticated API tests..."
Write-Host "Using token: ${JWT_TOKEN.Substring(0,20)}..." -ForegroundColor Gray
Write-Host ""

# Test 1: Get my plans (should be empty initially)
Write-Host "🔍 Checking existing plans..." -ForegroundColor Cyan
$myPlans = Test-AuthEndpoint "GET" "/plans/my-plans" "" "Get my existing plans"

# Test 2: Generate plan from beginner template
Write-Host "🏋️‍♂️ Generating beginner plan..." -ForegroundColor Cyan
$beginnerData = @{
    "template_name" = "beginner_full_body"
    "custom_name" = "My Beginner Plan - API Test"
} | ConvertTo-Json -Depth 3
$beginnerPlan = Test-AuthEndpoint "POST" "/plans/generate-from-template" $beginnerData "Generate beginner plan from template"

# Store plan ID for later tests
$planId = $null
if ($beginnerPlan -and $beginnerPlan.data.plan_id) {
    $planId = $beginnerPlan.data.plan_id
    Write-Host "📝 Generated plan ID: $planId" -ForegroundColor Green
}

# Test 3: Generate PPL plan
Write-Host "💪 Generating PPL plan..." -ForegroundColor Cyan
$pplData = @{
    "template_name" = "ppl_intermediate"
    "custom_name" = "My PPL Plan - API Test"
} | ConvertTo-Json -Depth 3
$pplPlan = Test-AuthEndpoint "POST" "/plans/generate-from-template" $pplData "Generate PPL intermediate plan"

# Test 4: Generate Upper/Lower plan
Write-Host "🎯 Generating Advanced plan..." -ForegroundColor Cyan
$advancedData = @{
    "template_name" = "upper_lower_advanced"
    "custom_name" = "My Advanced Plan - API Test"
} | ConvertTo-Json -Depth 3
$advancedPlan = Test-AuthEndpoint "POST" "/plans/generate-from-template" $advancedData "Generate Upper/Lower advanced plan"

# Test 5: Create custom plan
Write-Host "✨ Creating custom plan..." -ForegroundColor Cyan
$customPlanData = @{
    "name" = "Custom API Test Plan"
    "description" = "My custom workout plan created via API"
    "duration_weeks" = 8
    "goal" = "muscle_gain"
    "level" = "intermediate"
} | ConvertTo-Json -Depth 3
$customPlan = Test-AuthEndpoint "POST" "/plans/" $customPlanData "Create custom plan"

# Store custom plan ID
$customPlanId = $null
if ($customPlan -and $customPlan.data.plan.id) {
    $customPlanId = $customPlan.data.plan.id
    Write-Host "📝 Custom plan ID: $customPlanId" -ForegroundColor Green
}

# Test 6: Get my plans again (should show new plans)
Write-Host "📋 Checking updated plans list..." -ForegroundColor Cyan
Test-AuthEndpoint "GET" "/plans/my-plans" "" "Get my updated plans list"

# Test 7: Get specific plan details (if we have a plan ID)
if ($planId) {
    Write-Host "🔍 Getting plan details..." -ForegroundColor Cyan
    Test-AuthEndpoint "GET" "/plans/$planId" "" "Get specific plan details"
    
    # Test 8: Get plan sessions
    Write-Host "📅 Getting plan sessions..." -ForegroundColor Cyan
    Test-AuthEndpoint "GET" "/plans/$planId/sessions" "" "Get plan workout sessions"
    
    # Test 9: Update plan
    Write-Host "✏️ Updating plan..." -ForegroundColor Cyan
    $updateData = @{
        "name" = "My Updated Beginner Plan"
        "description" = "Updated description via API test"
    } | ConvertTo-Json -Depth 3
    Test-AuthEndpoint "PUT" "/plans/$planId" $updateData "Update plan details"
}

# Test 10: Try invalid template (should fail)
Write-Host "❌ Testing invalid template..." -ForegroundColor Cyan
$invalidData = @{
    "template_name" = "non_existent_template"
    "custom_name" = "Should Fail"
} | ConvertTo-Json -Depth 3
Test-AuthEndpoint "POST" "/plans/generate-from-template" $invalidData "Generate plan with invalid template (should fail)"

# Test 11: Try to access non-existent plan (should fail)
Write-Host "❌ Testing non-existent plan..." -ForegroundColor Cyan
Test-AuthEndpoint "GET" "/plans/99999" "" "Get non-existent plan (should fail)"

# Test 12: Clean up - Delete test plans (optional)
Write-Host ""
Write-Host "🧹 Cleanup - Delete test plans?" -ForegroundColor Yellow
Write-Host "Uncomment the cleanup section below if you want to delete the test plans" -ForegroundColor Gray

# Cleanup section (uncomment to enable)
# if ($planId) {
#     Write-Host "🗑️ Deleting generated plan..." -ForegroundColor Red
#     Test-AuthEndpoint "DELETE" "/plans/$planId" "" "Delete generated plan"
# }
# 
# if ($customPlanId) {
#     Write-Host "🗑️ Deleting custom plan..." -ForegroundColor Red
#     Test-AuthEndpoint "DELETE" "/plans/$customPlanId" "" "Delete custom plan"
# }

Write-Host ""
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "🎉 Authenticated API Testing Complete!" -ForegroundColor Green
Write-Host "📊 Summary:" -ForegroundColor Blue
Write-Host "   • Generated plans: $([bool]$beginnerPlan + [bool]$pplPlan + [bool]$advancedPlan)" -ForegroundColor Gray
Write-Host "   • Custom plan created: $([bool]$customPlan)" -ForegroundColor Gray
Write-Host "   • Check server logs for detailed information" -ForegroundColor Blue
Write-Host "   • Visit $BASE_URL/docs for interactive API documentation" -ForegroundColor Blue
