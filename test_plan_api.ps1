# Test script for Plan API endpoints (PowerShell version)
# Run this script to test all plan-related functionality

$BASE_URL = "http://127.0.0.1:8000"
$API_BASE = "$BASE_URL/api/v1"

Write-Host "🚀 Testing Fitness Backend Plan API" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

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

# Function to test endpoint
function Test-Endpoint {
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
            $response = Invoke-RestMethod -Uri "$API_BASE$Endpoint" -Method Get -ErrorAction Stop
            Write-Status "SUCCESS" "HTTP 200 - $Description"
            $response | ConvertTo-Json -Depth 3 | Write-Host
        }
        elseif ($Method -eq "POST") {
            $headers = @{
                "Content-Type" = "application/json"
            }
            $body = $Data | ConvertFrom-Json
            $response = Invoke-RestMethod -Uri "$API_BASE$Endpoint" -Method Post -Headers $headers -Body (ConvertTo-Json $body) -ErrorAction Stop
            Write-Status "SUCCESS" "HTTP 200 - $Description"
            $response | ConvertTo-Json -Depth 3 | Write-Host
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
    }
}

Write-Host "Starting API tests..."
Write-Host "Make sure the server is running on $BASE_URL"
Write-Host ""

# Test 1: Get available templates
Test-Endpoint "GET" "/plans/templates/available" "" "Get available plan templates"

# Test 2: Get all plans (public)
Test-Endpoint "GET" "/plans/" "" "Get all public plans"

# Test 3: Get plans with pagination
Test-Endpoint "GET" "/plans/?skip=0&limit=5" "" "Get plans with pagination"

# Test 4: Generate plan from template (this might fail without auth)
Write-Host ""
Write-Host "Note: The following tests require authentication" -ForegroundColor Yellow
$templateData = @{
    "template_name" = "beginner_full_body"
    "custom_name" = "My Test Plan"
} | ConvertTo-Json -Depth 3
Test-Endpoint "POST" "/plans/generate-from-template" $templateData "Generate plan from beginner template"

# Test 5: Generate PPL plan
$pplData = @{
    "template_name" = "ppl_intermediate"
    "custom_name" = "My PPL Plan"
} | ConvertTo-Json -Depth 3
Test-Endpoint "POST" "/plans/generate-from-template" $pplData "Generate PPL intermediate plan"

# Test 6: Generate Upper/Lower plan
$ulData = @{
    "template_name" = "upper_lower_advanced"
    "custom_name" = "My Advanced Plan"
} | ConvertTo-Json -Depth 3
Test-Endpoint "POST" "/plans/generate-from-template" $ulData "Generate Upper/Lower advanced plan"

# Test 7: Try invalid template
$invalidData = @{
    "template_name" = "non_existent_template"
} | ConvertTo-Json -Depth 3
Test-Endpoint "POST" "/plans/generate-from-template" $invalidData "Generate plan with invalid template (should fail)"

# Test 8: Create custom plan (this might fail without auth)
$customPlanData = @{
    "name" = "Custom Test Plan"
    "description" = "My custom workout plan"
    "duration_weeks" = 6
    "goal" = "muscle_gain"
    "level" = "intermediate"
} | ConvertTo-Json -Depth 3
Test-Endpoint "POST" "/plans/" $customPlanData "Create custom plan"

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "API Testing Complete!" -ForegroundColor Green
Write-Host "Check the server logs for more details" -ForegroundColor Blue
Write-Host "Visit $BASE_URL/docs for interactive API documentation" -ForegroundColor Blue
