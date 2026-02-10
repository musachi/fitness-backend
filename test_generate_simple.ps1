# Test simple plan generation
$body = @{
    template_name='beginner_full_body'
    custom_name='My Test Plan'
} | ConvertTo-Json

$headers = @{
    'Content-Type' = 'application/json'
    'Authorization' = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkMzYyYmVkMC02ZGJjLTQyMGUtODk2Ni1kMjdmNjQ4MjdjYjkiLCJleHAiOjE3NzA3Nzg4MDUsInR5cGUiOiJhY2Nlc3MifQ.-Rbrlb3opkBBs7RhuGf74DHSqX_l1oy5pWrst34jgXI'
}

Write-Host "Testing plan generation..."
Write-Host "Request body: $body"

try {
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/plans/generate-from-template' -Method Post -Headers $headers -Body $body
    Write-Host "SUCCESS: Plan generated"
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "ERROR: Plan generation failed"
    Write-Host "Status:" $_.Exception.Response.StatusCode.value__
    Write-Host "Message:" $_.Exception.Message
    
    # Try to get more error details if available
    if ($_.Exception.Response) {
        $reader = [System.IO.StreamReader]::new($_.Exception.Response.GetResponseStream())
        $reader.BaseStream.Position = 0
        $errorBody = $reader.ReadToEnd()
        Write-Host "Error body: $errorBody"
        $reader.Close()
    }
}
