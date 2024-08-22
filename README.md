Simple script so not bothering to make an extensive readme. Existing scripts suck for extracting JWT's from things like CobaltStrike log files and even worse they typically don't parse out and give you the valid tokens.

This saves a lot of time. Just go to your team server, grep out eyJ and output to a file. ./dudewheresmytokens <pathtofileyoucreated> and you'll get a nice pretty and useful output.

Note, this extracts all the information from the JWT and stores in a dict. If you find you need things like the RH field then you can edit the script to display that as well.
