# netscaler-get-vserver-oid
Get SNMP OID of a list of Netscaler vServer from a JSON input list

## JSON input format:  
{  
  "Name"  : "VSERVER NAME"  
}  
  
## JSON output format:  
{  
  "ID"    : "VSERVER ID"  
  "NAME"  : "VSERVER NAME"  
  "OID"   : "VSERVER OID"  
}  

## Usage:  
python3 netscaler-get-vserver-oid.py  
You will then be required to insert an IP Address and Port for SSH connection and Username and Password for Login.
