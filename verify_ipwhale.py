#!/usr/bin/env python3
"""
Quick verification script for IPWhale functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_basic_functionality():
    """Test basic IPWhale functionality"""
    print("🐋 IPWhale Verification Script")
    print("=" * 40)
    
    try:
        # Test imports
        from main import app, is_valid_ipv4, is_valid_ipv6, detect_ip_version
        print("✅ All imports successful")
        
        # Test IP validation
        assert is_valid_ipv4("192.168.1.1") == True
        assert is_valid_ipv4("256.1.1.1") == False
        assert is_valid_ipv6("::1") == True
        assert is_valid_ipv6("invalid") == False
        print("✅ IP validation functions working")
        
        # Test IP version detection
        assert detect_ip_version("192.168.1.1") == 4
        assert detect_ip_version("::1") == 6
        assert detect_ip_version("invalid") == None
        print("✅ IP version detection working")
        
        # Test Flask app creation
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/api/health')
            assert response.status_code == 200
            data = response.get_json()
            assert data['status'] == 'healthy'
            assert data['service'] == 'ipwhale'
            print("✅ Health endpoint working")
            
            # Test main page
            response = client.get('/')
            assert response.status_code == 200
            print("✅ Main page loads successfully")
            
            # Test API endpoints
            response = client.get('/api/ip')
            assert response.status_code == 200
            print("✅ IP API endpoint working")
            
            response = client.get('/api/full')
            assert response.status_code == 200
            data = response.get_json()
            assert 'timestamp' in data
            print("✅ Full API endpoint working")
        
        print("\n🎉 All tests passed! IPWhale is fully functional.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_basic_functionality()
    sys.exit(0 if success else 1)
