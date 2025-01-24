# PowerView Dependant script. Need to ensure PowerView.ps1 is located in the same folder as the ObjectACLScript
Import-Module .\PowerView.ps1

# Add as many valid Domain Objects as possible.
$names = @("robert", "jen", "Management Department")


foreach ($name in $names) {
    Get-ObjectAcl -Identity $name |
      # "GenricAll" can be replaced with "AllExtendedRights; ForceChangePassword" and more. For more ACL permissions https://learn.microsoft.com/en-us/windows/win32/secauthz/access-rights-and-access-masks
        Where-Object {$_.ActiveDirectoryRights -eq "GenericAll"} |
        Select-Object SecurityIdentifier, ActiveDirectoryRights |
        ForEach-Object {
            $sid = $_.SecurityIdentifier
            $userName = Convert-SidToName -Sid $sid
            [PSCustomObject]@{
                SecurityIdentifier = $sid
                UserName = $userName
                ActiveDirectoryRights = $_.ActiveDirectoryRights
            }
        }
}
