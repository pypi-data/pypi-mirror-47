### quackmyip

Keep your public IP address updated, when using the [DuckDNS](https://www.duckdns.org/) service. 

##### Requirements
In order to work, this program, needs the following Python 3 libraries:
* [requests](http://docs.python-requests.org/en/master/) (tested with v2.12.4)
* [urllib3](https://urllib3.readthedocs.io/en/latest/)  (tested with v1.19.1)

#### Installation
You can use `pip` to install it:
```
pip install quackmyip
```

##### Syntax
```
usage: quackmyip [-h] FILE

Update your IP address for your duckdns registered domain

positional arguments:
  FILE        The configuration file to use

  optional arguments:
    -h, --help  show this help message and exit

```
For its usage, it's recommended to create a daily cron job!.

##### Configuration
Prior to its usage, a configuration file must be created, as shown in the following example:
```
[duckdns]
token = [YOUR_TOKEN]
domain = [YOUR_DOMAIN]

```
