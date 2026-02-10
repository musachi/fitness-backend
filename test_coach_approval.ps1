$headers = @{
    'Content-Type' = 'application/json'
}

Write-Host "🧪 Testing Coach Approval System" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

# Step 1: Register a new coach (should be unapproved)
Write-Host ""
Write-Host "Step 1: Registering new coach..." -ForegroundColor Yellow

$coachData = @{
    name = "New Coach Test"
    email = "newcoach@fitness.com"
    password = "password123"
    role_id = 2  # Coach role
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/auth/register' -Method Post -Headers $headers -Body $coachData
    Write-Host "SUCCESS: Coach registered (pending approval)" -ForegroundColor Green
    $coachId = $response.id
    Write-Host "Coach ID: $coachId"
} catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
}

# Step 2: Try to login as unapproved coach (should fail)
Write-Host ""
Write-Host "Step 2: Trying to login as unapproved coach..." -ForegroundColor Yellow

$loginData = @{
    email = "newcoach@fitness.com"
    password = "password123"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/auth/login' -Method Post -Headers $headers -Body $loginData
    Write-Host "ERROR: Unapproved coach should not be able to login!" -ForegroundColor Red
} catch {
    if ($_.Exception.Response.StatusCode.value__ -eq 403) {
        Write-Host "SUCCESS: Unapproved coach correctly denied access (403)" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Unexpected status: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
    }
}

# Step 3: Create admin user and login
Write-Host ""
Write-Host "Step 3: Creating and logging in as admin..." -ForegroundColor Yellow

# First create admin in database
$adminId = "admin-12345678-1234-1234-1234-123456789012"
$adminData = @{
    id = $adminId
    name = "Admin User"
    email = "admin@fitness.com"
    password_hash = "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f"
    role_id = 1
    is_approved = $true
}

# Login as admin
$adminLogin = @{
    email = "admin@fitness.com"
    password = "password123"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/auth/login' -Method Post -Headers $headers -Body $adminLogin
    Write-Host "SUCCESS: Admin logged in" -ForegroundColor Green
    $adminToken = $response.access_token
    Write-Host "Admin token obtained"
} catch {
    Write-Host "ERROR: Could not login as admin: $($_.Exception.Message)" -ForegroundColor Red
}

# Step 4: Get pending coaches as admin
if ($adminToken) {
    Write-Host ""
    Write-Host "Step 4: Getting pending coaches as admin..." -ForegroundColor Yellow
    
    $adminHeaders = @{
        'Content-Type' = 'application/json'
        'Authorization' = "Bearer $adminToken"
    }
    
    try {
        $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/auth/pending-coaches' -Method Get -Headers $adminHeaders
        Write-Host "SUCCESS: Retrieved pending coaches" -ForegroundColor Green
        $response | ConvertTo-Json -Depth 3
    } catch {
        Write-Host "ERROR: Could not get pending coaches: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Step 5: Approve the coach
    Write-Host ""
    Write-Host "Step 5: Approving coach..." -ForegroundColor Yellow
    
    try {
        $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/auth/approve-coach/$coachId" -Method Post -Headers $adminHeaders
        Write-Host "SUCCESS: Coach approved!" -ForegroundColor Green
        $response | ConvertTo-Json -Depth 3
    } catch {
        Write-Host "ERROR: Could not approve coach: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Step 6: Try to login as approved coach (should work now)
    Write-Host ""
    Write-Host "Step 6: Trying to login as approved coach..." -ForegroundColor Yellow
    
    try {
        $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/auth/login' -Method Post -Headers $headers -Body $loginData
        Write-Host "SUCCESS: Approved coach can now login!" -ForegroundColor Green
        Write-Host "Coach token: $($response.access_token.Substring(0,20))..."
    } catch {
        Write-Host "ERROR: Approved coach should be able to login: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "🎯 Coach Approval System Test Complete!" -ForegroundColor Green
