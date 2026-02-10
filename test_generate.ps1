$body = @{
    template_name='beginner_full_body'
    custom_name='My Test Plan'
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/plans/generate-from-template' -Method Post -Body $body -ContentType 'application/json'
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "Error:" $_.Exception.Message
    Write-Host "Status Code:" $_.Exception.Response.StatusCode.value__
}
