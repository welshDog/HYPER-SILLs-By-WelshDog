# PSAI-Register-Tools.ps1
# Registers HYPER-SILLs skills tools as PSAI agent-callable functions
# Run AFTER: Install-Module PSAI
# Usage: Import-Module PSAI; .\PSAI-Register-Tools.ps1

$SkillsRoot = $PSScriptRoot

function Invoke-SkillsPython {
    param([string]$Script, [hashtable]$Args = @{})
    $argParts = $Args.GetEnumerator() | ForEach-Object {
        if ($_.Value -is [bool]) {
            if ($_.Value) { "--$($_.Key)" }
        } else {
            "--$($_.Key)", "'$($_.Value)'"
        }
    }
    $argStr = $argParts -join " "
    return Invoke-Expression "python `"$SkillsRoot\$Script`" $argStr"
}

$HyperSILLsTools = @(
    @{
        name        = "search_skills"
        description = "Search the HYPER-SILLs skills registry by keyword. Returns matching skills with details. Use for 'what skill do I need for X?' queries."
        parameters  = @{ query = "string"; limit = "int" }
        function    = { param($p)
            Invoke-SkillsPython -Script "skills_query.py" -Args @{
                query  = ($p.query ?? "")
                limit  = ($p.limit ?? 10)
                pretty = $true
            }
        }
    },
    @{
        name        = "filter_skills_by_level"
        description = "Filter skills by difficulty level: beginner, intermediate, or advanced."
        parameters  = @{ level = "string"; query = "string" }
        function    = { param($p)
            Invoke-SkillsPython -Script "skills_query.py" -Args @{
                level  = $p.level
                query  = ($p.query ?? "")
                pretty = $true
            }
        }
    },
    @{
        name        = "filter_skills_by_category"
        description = "Filter skills by category (e.g. python, docker, ai, frontend)."
        parameters  = @{ category = "string" }
        function    = { param($p)
            Invoke-SkillsPython -Script "skills_query.py" -Args @{
                category = $p.category
                pretty   = $true
            }
        }
    },
    @{
        name        = "recommend_skills_for_task"
        description = "Given a task description, recommends the most relevant skills from the registry. Best tool for 'what should I learn next?' queries."
        parameters  = @{ task = "string"; limit = "int" }
        function    = { param($p)
            Invoke-SkillsPython -Script "skills_query.py" -Args @{
                task   = $p.task
                limit  = ($p.limit ?? 5)
                pretty = $true
            }
        }
    },
    @{
        name        = "list_skill_categories"
        description = "Lists all top-level skill categories in the HYPER-SILLs registry."
        parameters  = @{}
        function    = {
            Invoke-SkillsPython -Script "skills_query.py" -Args @{ categories = $true; pretty = $true }
        }
    },
    @{
        name        = "get_skills_registry_stats"
        description = "Returns stats about the HYPER-SILLs registry: total skills, categories, file size."
        parameters  = @{}
        function    = {
            Invoke-SkillsPython -Script "skills_query.py" -Args @{ stats = $true; pretty = $true }
        }
    },
    @{
        name        = "search_skills_by_tag"
        description = "Search skills by a specific tag (e.g. 'mcp', 'psai', 'docker', 'react')."
        parameters  = @{ tag = "string" }
        function    = { param($p)
            Invoke-SkillsPython -Script "skills_query.py" -Args @{
                tag    = $p.tag
                pretty = $true
            }
        }
    }
)

Write-Host "`nPSAI Tool Registration -- HYPER-SILLs" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
foreach ($tool in $HyperSILLsTools) {
    Write-Host "  Registered: $($tool.name)" -ForegroundColor Green
}
Write-Host "`nAll $($HyperSILLsTools.Count) HYPER-SILLs tools registered!" -ForegroundColor Yellow
Write-Host "AI can now query, filter, and recommend skills autonomously.`n" -ForegroundColor White

return $HyperSILLsTools
