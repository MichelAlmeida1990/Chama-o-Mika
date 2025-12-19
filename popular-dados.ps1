# Script PowerShell para popular dados mockups no sistema
# Uso: .\popular-dados.ps1 [secret]

param(
    [string]$Secret = ""
)

$url = "https://chama-o-mika-backend.onrender.com/api/populate-mock-data/"

Write-Host "Populando dados mockups no sistema..." -ForegroundColor Cyan
Write-Host ""

# Preparar headers
$headers = @{
    "Content-Type" = "application/json"
}

# Se secret foi fornecido, adicionar ao header
if ($Secret) {
    $headers["X-Populate-Secret"] = $Secret
    Write-Host "Usando secret fornecido" -ForegroundColor Yellow
} else {
    Write-Host "Sem secret - se o endpoint exigir, voce precisara fornecer" -ForegroundColor Yellow
    Write-Host "   Use: .\popular-dados.ps1 -Secret seu-secret-aqui" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Enviando requisicao para: $url" -ForegroundColor Cyan
Write-Host ""

try {
    # Fazer a requisição POST
    $response = Invoke-RestMethod -Uri $url -Method POST -Headers $headers -ErrorAction Stop
    
    Write-Host "SUCESSO!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Resposta:" -ForegroundColor Cyan
    Write-Host ($response | ConvertTo-Json -Depth 10)
    
    if ($response.success) {
        Write-Host ""
        Write-Host "Dados mockups criados com sucesso!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Proximos passos:" -ForegroundColor Yellow
        Write-Host "   1. Acesse o dashboard para ver os dados" -ForegroundColor White
        Write-Host "   2. Verifique os graficos e metricas" -ForegroundColor White
        Write-Host "   3. Teste as funcionalidades do sistema" -ForegroundColor White
    }
    
} catch {
    Write-Host ""
    Write-Host "ERRO ao popular dados!" -ForegroundColor Red
    Write-Host ""
    
    $errorResponse = $_.ErrorDetails.Message
    
    if ($errorResponse) {
        try {
            $errorJson = $errorResponse | ConvertFrom-Json
            Write-Host "Erro: $($errorJson.error)" -ForegroundColor Red
            
            if ($errorJson.error -like "*Secret invalido*" -or $errorJson.error -like "*Secret inválido*") {
                Write-Host ""
                Write-Host "SOLUCAO:" -ForegroundColor Yellow
                Write-Host "   O endpoint requer um secret. Voce tem duas opcoes:" -ForegroundColor White
                Write-Host ""
                Write-Host "   Opcao 1 - Remover o secret no Render:" -ForegroundColor Cyan
                Write-Host "     1. Render Dashboard -> Settings -> Environment Variables" -ForegroundColor Gray
                Write-Host "     2. Delete a variavel POPULATE_SECRET" -ForegroundColor Gray
                Write-Host "     3. Salve e aguarde o restart" -ForegroundColor Gray
                Write-Host "     4. Execute este script novamente" -ForegroundColor Gray
                Write-Host ""
                Write-Host "   Opcao 2 - Fornecer o secret:" -ForegroundColor Cyan
                Write-Host "     .\popular-dados.ps1 -Secret seu-secret-aqui" -ForegroundColor Gray
            }
        } catch {
            Write-Host "Resposta do servidor: $errorResponse" -ForegroundColor Red
        }
    } else {
        Write-Host "Erro: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Tentar obter mais detalhes do erro
    if ($_.Exception.Response) {
        try {
            $stream = $_.Exception.Response.GetResponseStream()
            $reader = New-Object System.IO.StreamReader($stream)
            $responseBody = $reader.ReadToEnd()
            Write-Host ""
            Write-Host "Detalhes do erro:" -ForegroundColor Yellow
            Write-Host $responseBody -ForegroundColor Red
        } catch {
            # Ignorar se não conseguir ler o stream
        }
        Write-Host ""
        Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Gray
    }
}

Write-Host ""
