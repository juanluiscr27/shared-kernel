$input = [Console]::In.ReadToEnd() | ConvertFrom-Json
$filePath = $input.tool_input.file_path

$repoRoot = "D:\Projects\Python\shared-kernel"

if ($filePath -and $filePath.StartsWith($repoRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    $branch = git -C $repoRoot branch --show-current 2>$null
    if ($branch -eq "main") {
        $reason = "You are on the 'main' branch. Direct changes to main are prohibited by project rules (CLAUDE.md). Create a feature branch first: git checkout -b <type>/<short-description>"
        $response = @{
            hookSpecificOutput = @{
                hookEventName          = "PreToolUse"
                permissionDecision     = "deny"
                permissionDecisionReason = $reason
            }
        } | ConvertTo-Json -Compress
        Write-Output $response
    }
}
