Write-Host "🎯 DEMO SIMPLE DEL SISTEMA" -ForegroundColor Cyan

$headers = @{
    'Content-Type' = 'application/json'
}

Write-Host ""
Write-Host "1. Registrando coach..." -ForegroundColor Yellow

$coachData = @{
    name = "Coach Test Final"
    email = "coachtest@fitness.com"
    password = "password123"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/auth/register-coach' -Method Post -Headers $headers -Body $coachData
    Write-Host "SUCCESS: Coach registrado"
    Write-Host "   Nombre: $($response.name)"
    Write-Host "   Email: $($response.email)"
    Write-Host "   Rol: $($response.role.name)"
    Write-Host "   Aprobado: $($response.is_approved)"
} catch {
    Write-Host "ERROR: $($_.Exception.Message)"
}

Write-Host ""
Write-Host "2. Probando login coach (debe fallar)..." -ForegroundColor Yellow

$loginData = @{
    email = 'coachtest@fitness.com'
    password = 'password123'
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/auth/login-json' -Method Post -Headers $headers -Body $loginData
    Write-Host "ERROR: Coach no aprobado no deberia login"
} catch {
    if ($_.Exception.Response.StatusCode.value__ -eq 403) {
        Write-Host "SUCCESS: Coach bloqueado correctamente (403)"
    } else {
        Write-Host "Status: $($_.Exception.Response.StatusCode.value__)"
    }
}

Write-Host ""
Write-Host "3. Ver planes de usuario normal..." -ForegroundColor Yellow

$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkMzYyYmVkMC02ZGJjLTQyMGUtODk2Ni1kMjdmNjQ4MjdjYjkiLCJleHAiOjE3NzA3Nzg4MDUsInR5cGUiOiJhY2Nlc3MifQ.-Rbrlb3opkBBs7RhuGf74DHSqX_l1oy5pWrst34jgXI"

$headers_auth = @{
    'Content-Type' = 'application/json'
    'Authorization' = "Bearer $token"
}

try {
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/plans/my-plans' -Method Get -Headers $headers_auth
    Write-Host "SUCCESS: Usuario puede ver sus planes"
    Write-Host "   Planes encontrados: $($response.data.plans.Count)"
} catch {
    Write-Host "ERROR: $($_.Exception.Message)"
}

Write-Host ""
Write-Host "🎉 DEMO COMPLETADO!" -ForegroundColor Green
