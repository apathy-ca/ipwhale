#!/usr/bin/env python3
"""
Simple test script for IPWhale functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from main import app, lookup_ptr_record, lookup_asn, detect_ip_version, is_valid_ipv4, is_valid_ipv6

def test_ip_validation():
    """Test IP validation functions"""
    print("Testing IP validation...")
    
    # Test IPv4 validation
    assert is_valid_ipv4("192.168.1.1") == True
    assert is_valid_ipv4("8.8.8.8") == True
    assert is_valid_ipv4("256.1.1.1") == False
    assert is_valid_ipv4("not.an.ip") == False
    print("✓ IPv4 validation works")
    
    # Test IPv6 validation
    assert is_valid_ipv6("::1") == True
    assert is_valid_ipv6("2001:db8::1") == True
    assert is_valid_ipv6("invalid::ipv6::address") == False
    print("✓ IPv6 validation works")
    
    # Test IP version detection
    assert detect_ip_version("192.168.1.1") == 4
    assert detect_ip_version("::1") == 6
    assert detect_ip_version("invalid") == None
    print("✓ IP version detection works")

def test_dns_functions():
    """Test DNS lookup functions"""
    print("\nTesting DNS functions...")
    
    # Test PTR lookup for well-known IPs
    try:
        ptr = lookup_ptr_record("8.8.8.8")
        print(f"✓ PTR lookup for 8.8.8.8: {ptr}")
    except Exception as e:
        print(f"⚠ PTR lookup failed (expected in some environments): {e}")
    
    # Test ASN lookup
    try:
        asn = lookup_asn("8.8.8.8")
        print(f"✓ ASN lookup for 8.8.8.8: {asn}")
    except Exception as e:
        print(f"⚠ ASN lookup failed (expected in some environments): {e}")

def test_flask_app():
    """Test Flask application"""
    print("\nTesting Flask application...")
    
    with app.test_client() as client:
        # Test health endpoint
        response = client.get('/api/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert data['service'] == 'ipwhale'
        print("✓ Health endpoint works")
        
        # Test main page
        response = client.get('/')
        assert response.status_code == 200
        print("✓ Main page loads")
        
        # Test API endpoints
        response = client.get('/api/ip')
        assert response.status_code == 200
        print("✓ IP API endpoint works")
        
        response = client.get('/api/4/ip')
        assert response.status_code == 200
        print("✓ IPv4 API endpoint works")
        
        response = client.get('/api/full')
        assert response.status_code == 200
        data = response.get_json()
        assert 'timestamp' in data
        print("✓ Full API endpoint works")

if __name__ == '__main__':
    print("IPWhale Test Suite")
    print("=" * 50)
    
    try:
        test_ip_validation()
        test_dns_functions()
        test_flask_app()
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed! IPWhale is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
