# Nominet EPP Client

## Examples Running on command line

```
pip install -r requirements.txt
python -m ds_nominet hello -uDOMAINSNIPE -pSECRET
python -m ds_nominet domain_check -uDOMAINSNIPE -pSECRET --parameters domain:nominet.uk
```

## API
```
from ds_nominet import EPPConnection, EPP

user = "DOMAINSNIPE"
password = "SECRET"

epp_connection = EPPConnection('epp.nominet.org.uk', 700)
epp = EPP(epp_connection)

epp.login(user, password)
epp.domain_create(user=user, password=password, domain=domain)
```

## Note: KeepAlive

Connections can be kept alive.

Login once then call hello every 59mins.

```
user = "DOMAINSNIPE"
password = "SECRET"

epp_connection = EPPConnection('epp.nominet.org.uk', 700)
epp = EPP(epp_connection)
epp.login(user, password)
# every 59 mins 
epp.hello()
```
