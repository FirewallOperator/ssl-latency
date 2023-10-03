# Prompt for the number of runs and delay between runs
$numRuns = Read-Host "Enter the number of runs"
$delay = Read-Host "Enter delay between runs (in seconds)"

# Read FQDNs from input.txt
$fqdns = Get-Content -Path "input.txt"

# Clear the output file
Clear-Content -Path "output.txt"

# Loop for each run
for ($i = 1; $i -le $numRuns; $i++) {
    foreach ($fqdn in $fqdns) {
        Write-Host "Testing $fqdn (Run $i)..."
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        $latency = (Measure-Command {
            $result = Test-NetConnection -ComputerName $fqdn -Port 443
            $result | Add-Member -MemberType NoteProperty -Name "Timestamp" -Value $timestamp -Force
            $result | Add-Member -MemberType NoteProperty -Name "Run" -Value $i -Force
            $result
        }).TotalMilliseconds

        # Append the result to the output file
        $output = "$($result.Timestamp): Latency to $fqdn (Run $($result.Run)): $($latency) ms"
        $output | Out-File -Append -FilePath "output.txt"

        # Output progress to console
        Write-Host $output
    }
    
    # Insert a blank line in the output file
    Add-Content -Path "output.txt" -Value ""

    if ($i -lt $numRuns) {
        Write-Host "Sleeping for $delay seconds before the next run..."
        Start-Sleep -Seconds $delay
    }
}

Write-Host "Tests completed. Results are saved in output.txt"
