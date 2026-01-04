import smtplib
import socket
import sys

def test_smtp():
    host = 'smtp.gmail.com'
    port = 587
    print(f"Testing connectivity to {host}:{port}...")
    
    try:
        # Resolve hostname first
        print(f"Resolving {host}...")
        try:
            ips = socket.getaddrinfo(host, port)
            print(f"  IPs: {[ip[4][0] for ip in ips]}")
        except Exception as e:
            print(f"  DNS Resolution failed: {e}")
        
        # Connect
        print("Connecting...")
        server = smtplib.SMTP(host, port, timeout=10)
        server.set_debuglevel(1)
        
        print("Sending EHLO...")
        server.ehlo()
        
        print("Starting TLS...")
        server.starttls()
        
        print("Sending EHLO after TLS...")
        server.ehlo()
        
        print("SUCCESS: Connection established and TLS negotiated.")
        server.quit()
        return True
        
    except Exception as e:
        print(f"\nFAILURE: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_smtp()
    sys.exit(0 if success else 1)
