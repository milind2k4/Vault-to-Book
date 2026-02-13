Links: 
___
# Computer Networks 


## TCP/IP Protocol Suit/Model 

This is the implementation of the OSI model?

Protocols is a set of rules to establish data communication. 

It defines what is communicated, how it is communicated,  and when it is communicated. 

Elements of Protocol:
1. Syntax 
2. Semantics 
3. Timing 

TCP/IP: Transmission control protocol and internet protocol 
It was developed by DOD (Department of Defense) to connect remote machines in 1974. 

It converts the 7 OSI layers into 4 TCP/IP layer. 
- Application Layer (Application + Presentation + Session )
- Transport (as it is)
- Internet (Renamed Network Layer)
- Host to Network (Network Access Layer) (Data link + Physical)


Protocols in TCP/IP:
Application:
- HTTP (Hyper Text Transfer Protocol): Transfers webpages from server to client. 
- FTP (File Transfer Protocol): Transfer files from sender to receiver. 
- SMTP (Simple Mail Transfer Protocol): Transfer email from sender to server. (Is there a complex mail transfer protocol?)
	  - POP (Post office Protocol): Transfer mail from server to user.
- Telnet (Telephonic Network): This protocol allows to remotely access devices. 
- DNS (Domain Name Server):  
- SNMP (Simple Network Management Protocol): use for monitoring, managing and configuring IP network devices. (e.g. Router)


Transport:
- TCP (Transmission Control Protocol): It manages the transmission of data. It establish connection oriented communication.
- UDP (User Datagram Protocol): Establish Connection Less communication. Transfers datagrams. (Datagrams are just packets being transferred through UDP.)
- SCTP (Stream Control Transmission Protocol): transfers multiple streams of data between two points. Combines features of TCP and UDP.

Internet:
- IP (Internet Protocol):
- ICMP (Internet Control Message Protocol): Used by routers to diagnose, report errors and manage IP network communication. 
- ARP (Address Resolution Protocol): Converts Logical Address to Physical Address.
- RARP (Reverse Address Resolution Protocol): Converts Physical Address to Logical Address.
- IGMP (Internet Group Management Protocol): Allows host and adjacent routers to manage multicasting. 



Address Are of Types:
- Specific (domain name)
- Physical (MAC which is on NIC (Network Interface Chip))
- Logical (IPv4 or IPv6)

## Physical Layer 
### Devices 
The devices here are dumb. 

#### Repeater
Regenerates the signal to extend the range. 
Applications: Extending wifi 

#### Hub 
It takes incoming signal on one port and blindly broadcasts it to all other ports.

Disadvantage is that security is at risk. 

#### Modem 
Modulator Demodulator 

Modulator: Digital to analog conversion 
Demodulation: Analog to Digital conversion. 

Digital Signal: 
Analog Signal: