# pyODStibMivb

A Python wrapper for the Opendata API of Stib-Mivb public transport of brussels. Based on pyRail.

Made because the API that pystibmivb uses will be deprecated: https://opendata.stib-mivb.be/store/forum/topic/9b0a4ae4-5978-4ac2-b2f8-acaf8e2068d4?


You need to get a key from https://opendata.stib-mivb.be/store/subscriptions and subscribe to the api's here https://opendata.stib-mivb.be/store/apis/info

The api-key has an expiration time and you can use a private key to request a new one, but that just seems overcomplicated to me. Just set the expiration date to several years and you're good to go.
If you're willing to add code for this I'm happy to accept it.


In the gtfs folder you can find stops and route info as of 2019-06-03, this information shouldn't change to often. For newer information see the Stib-Mivb Opendata website on how to download them or get it from https://transitfeeds.com/p/societe-des-transports-intercommunaux-de-bruxelles/527/latest.
