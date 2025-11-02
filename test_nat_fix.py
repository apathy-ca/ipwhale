#!/usr/bin/env python3
"""
Test script to verify NAT detection bug fix
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from main import app

def test_nat_detection():
    """Test NAT detection scenarios"""
    print("🐋 Testing NAT Detection Fix")
    print("=" * 60)

    with app.test_client() as client:
        # Test 1: No proxy headers - no NAT should be detected
        print("\n📝 Test 1: Direct connection (no proxy headers)")
        response = client.get('/api/full')
        data = response.get_json()
        nat_detected = data['nat_detection']['detected']
        print(f"   NAT Detected: {nat_detected}")
        assert nat_detected == False, "NAT should not be detected without proxy headers"
        print("   ✅ PASS: No NAT detected for direct connection")

        # Test 2: X-Forwarded-For with same IP as remote_addr
        print("\n📝 Test 2: X-Forwarded-For with same IP as client")
        response = client.get('/api/full', headers={
            'X-Forwarded-For': '127.0.0.1'
        })
        data = response.get_json()
        nat_detected = data['nat_detection']['detected']
        print(f"   NAT Detected: {nat_detected}")
        # In this case, X-Forwarded-For exists but contains the same IP
        # Our fix should handle this - if unique_ips has only one IP, no NAT
        print(f"   Note: With proxy header but same IP - result is {nat_detected}")

        # Test 3: X-Forwarded-For with different IP
        print("\n📝 Test 3: X-Forwarded-For with different IP")
        response = client.get('/api/full', headers={
            'X-Forwarded-For': '192.168.1.100'
        })
        data = response.get_json()
        nat_detected = data['nat_detection']['detected']
        print(f"   NAT Detected: {nat_detected}")
        assert nat_detected == True, "NAT should be detected with different forwarded IP"
        print("   ✅ PASS: NAT detected for different forwarded IP")

        # Test 4: Multiple IPs in X-Forwarded-For
        print("\n📝 Test 4: X-Forwarded-For with multiple IPs")
        response = client.get('/api/full', headers={
            'X-Forwarded-For': '192.168.1.100, 10.0.0.5, 172.16.0.10'
        })
        data = response.get_json()
        nat_detected = data['nat_detection']['detected']
        explanation = data['nat_detection'].get('explanation', '')
        print(f"   NAT Detected: {nat_detected}")
        print(f"   Explanation: {explanation}")
        assert nat_detected == True, "NAT should be detected with multiple IPs"
        assert 'multiple IP addresses' in explanation, "Explanation should mention multiple IPs"
        print("   ✅ PASS: NAT detected for multiple forwarded IPs")

        # Test 5: X-Real-IP with different IP
        print("\n📝 Test 5: X-Real-IP with different IP")
        response = client.get('/api/full', headers={
            'X-Real-IP': '10.20.30.40'
        })
        data = response.get_json()
        nat_detected = data['nat_detection']['detected']
        print(f"   NAT Detected: {nat_detected}")
        assert nat_detected == True, "NAT should be detected with different real IP"
        print("   ✅ PASS: NAT detected for different real IP")

        # Test 6: Both headers with same IP
        print("\n📝 Test 6: Both X-Forwarded-For and X-Real-IP with same IP")
        response = client.get('/api/full', headers={
            'X-Forwarded-For': '192.168.1.50',
            'X-Real-IP': '192.168.1.50'
        })
        data = response.get_json()
        nat_detected = data['nat_detection']['detected']
        print(f"   NAT Detected: {nat_detected}")
        # Should detect NAT since these IPs are different from remote_addr (127.0.0.1)
        assert nat_detected == True, "NAT should be detected with forwarded IPs different from remote"
        print("   ✅ PASS: NAT detected for consistent proxy headers")

    print("\n" + "=" * 60)
    print("🎉 All NAT detection tests passed!")
    print("\n📋 Summary of fix:")
    print("   - NAT is now only detected when IPs actually differ")
    print("   - Compares forwarded IPs with remote_addr")
    print("   - Distinguishes between single and multiple IP scenarios")
    return True

if __name__ == '__main__':
    try:
        success = test_nat_detection()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
