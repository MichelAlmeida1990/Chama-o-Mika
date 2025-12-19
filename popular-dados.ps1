# Script PowerShell para popular dados mockups no sistema
# Uso: .\popular-dados.ps1 [secret]

param(
    [string]$Secret = ""
)

$url = "https://chama-o-mika-backend.onrender.com/api/populate-mock-data/"

Write-Host "🚀 Populando dados mockups no sistema..." -ForegroundColor Cyan
Write-Host ""

# Preparar headers
$headers = @{
    "Content-Type" = "application/json"
}

# Se secret foi fornecido, adicionar ao header
if ($Secret) {
    $headers["X-Populate-Secret"] = $Secret
    Write-Host "🔐 Usando secret fornecido" -ForegroundColor Yellow
} else {
    Write-Host "⚠️  Sem secret - se o endpoint exigir, você precisará fornecer" -ForegroundColor Yellow
    Write-Host "   Use: .\popular-dados.ps1 -Secret 'seu-secret-aqui'" -ForegroundColor Gray
}

Write-Host ""
Write-Host "📡 Enviando requisição para: $url" -ForegroundColor Cyan
Write-Host ""

try {
    # Fazer a requisição POST
    $response = Invoke-RestMethod -Uri $url -Method POST -Headers $headers -ErrorAction Stop
    
    Write-Host "✅ SUCESSO!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Resposta:" -ForegroundColor Cyan
    Write-Host ($response | ConvertTo-Json -Depth 10)
    
    if ($response.success) {
        Write-Host ""
        Write-Host "🎉 Dados mockups criados com sucesso!" -ForegroundColor Green
        Write-Host ""
        Write-Host "💡 Próximos passos:" -ForegroundColor Yellow
        Write-Host "   1. Acesse o dashboard para ver os dados" -ForegroundColor White
        Write-Host "   2. Verifique os gráficos e métricas" -ForegroundColor White
        Write-Host "   3. Teste as funcionalidades do sistema" -ForegroundColor White
    }
    
} catch {
    Write-Host ""
    Write-Host "❌ ERRO ao popular dados!" -ForegroundColor Red
    Write-Host ""
    
    $errorResponse = $_.ErrorDetails.Message
    
    if ($errorResponse) {
        try {
            $errorJson = $errorResponse | ConvertFrom-Json
            Write-Host "Erro: $($errorJson.error)" -ForegroundColor Red
            
            if ($errorJson.error -like "*Secret inválido*") {
                Write-Host ""
                Write-Host "🔐 SOLUÇÃO:" -ForegroundColor Yellow
                Write-Host "   O endpoint requer um secret. Você tem duas opções:" -ForegroundColor White
                Write-Host ""
                Write-Host "   Opção 1 - Remover o secret no Render:" -ForegroundColor Cyan
                Write-Host "     1. Render Dashboard → Settings → Environment Variables" -ForegroundColor Gray
                Write-Host "     2. Delete a variável POPULATE_SECRET" -ForegroundColor Gray
                Write-Host "     3. Salve e aguarde o restart" -ForegroundColor Gray
                Write-Host "     4. Execute este script novamente" -ForegroundColor Gray
                Write-Host ""
                Write-Host "   Opção 2 - Fornecer o secret:" -ForegroundColor Cyan
                Write-Host "     .\popular-dados.ps1 -Secret 'seu-secret-aqui'" -ForegroundColor Gray
            }
        } catch {
            Write-Host "Resposta do servidor: $errorResponse" -ForegroundColor Red
        }
    } else {
        Write-Host "Erro: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Gray
}

Write-Host ""

