#!/bin/bash

# Test script for Plan API endpoints
# Run this script to test all plan-related functionality

BASE_URL="http://127.0.0.1:8000"
API_BASE="$BASE_URL/api/v1"

echo "🚀 Testing Fitness Backend Plan API"
echo "=================================="
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    
    if [ "$status" = "SUCCESS" ]; then
        echo -e "${GREEN}✅ $message${NC}"
    elif [ "$status" = "ERROR" ]; then
        echo -e "${RED}❌ $message${NC}"
    elif [ "$status" = "INFO" ]; then
        echo -e "${BLUE}ℹ️  $message${NC}"
    elif [ "$status" = "WARNING" ]; then
        echo -e "${YELLOW}⚠️  $message${NC}"
    fi
}

# Function to test endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local description=$4
    
    echo -e "\n${BLUE}Testing: $description${NC}"
    echo "Request: $method $endpoint"
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$API_BASE$endpoint")
    elif [ "$method" = "POST" ]; then
        response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
                   -X POST \
                   -H "Content-Type: application/json" \
                   -d "$data" \
                   "$API_BASE$endpoint")
    fi
    
    # Extract status code
    http_code=$(echo "$response" | grep "HTTP_STATUS:" | cut -d: -f2)
    body=$(echo "$response" | sed -e 's/HTTP_STATUS:.*//g')
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        print_status "SUCCESS" "HTTP $http_code - $description"
        echo "Response: $body" | jq . 2>/dev/null || echo "Response: $body"
    else
        print_status "ERROR" "HTTP $http_code - $description"
        echo "Response: $body"
    fi
}

echo "Starting API tests..."
echo "Make sure the server is running on $BASE_URL"
echo

# Test 1: Get available templates
test_endpoint "GET" "/plans/templates/available" "" "Get available plan templates"

# Test 2: Get all plans (public)
test_endpoint "GET" "/plans/" "" "Get all public plans"

# Test 3: Get plans with pagination
test_endpoint "GET" "/plans/?skip=0&limit=5" "" "Get plans with pagination"

# Test 4: Generate plan from template (this might fail without auth)
echo -e "\n${YELLOW}Note: The following tests require authentication${NC}"
template_data='{"template_name": "beginner_full_body", "custom_name": "My Test Plan"}'
test_endpoint "POST" "/plans/generate-from-template" "$template_data" "Generate plan from beginner template"

# Test 5: Generate PPL plan
ppl_data='{"template_name": "ppl_intermediate", "custom_name": "My PPL Plan"}'
test_endpoint "POST" "/plans/generate-from-template" "$ppl_data" "Generate PPL intermediate plan"

# Test 6: Generate Upper/Lower plan
ul_data='{"template_name": "upper_lower_advanced", "custom_name": "My Advanced Plan"}'
test_endpoint "POST" "/plans/generate-from-template" "$ul_data" "Generate Upper/Lower advanced plan"

# Test 7: Try invalid template
invalid_data='{"template_name": "non_existent_template"}'
test_endpoint "POST" "/plans/generate-from-template" "$invalid_data" "Generate plan with invalid template (should fail)"

# Test 8: Create custom plan (this might fail without auth)
custom_plan_data='{
    "name": "Custom Test Plan",
    "description": "My custom workout plan",
    "duration_weeks": 6,
    "goal": "muscle_gain",
    "level": "intermediate"
}'
test_endpoint "POST" "/plans/" "$custom_plan_data" "Create custom plan"

echo -e "\n${BLUE}==================================${NC}"
echo -e "${GREEN}API Testing Complete!${NC}"
echo -e "${INFO}Check the server logs for more details${NC}"
echo -e "${INFO}Visit $BASE_URL/docs for interactive API documentation${NC}"
