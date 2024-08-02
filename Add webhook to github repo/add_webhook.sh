#!/bin/bash

# Function to add webhooks to GitHub repository
add_webhooks() {
    local repo_url=$1
    local token="$TOKEN"

    # Extract owner and repo from the GitHub repository URL
    local owner=$(echo "$repo_url" | awk -F'/' '{print $(NF-1)}')
    local repo=$(echo "$repo_url" | awk -F'/' '{print $NF}' | sed 's/\.git$//')

    # Loop through each webhook URL
    for webhook_url in "${WEBHOOK_URLS[@]}"; do
        # Construct the API request payload
        local payload='{
            "name": "web",
            "active": true,
            "events": ["push"],
            "config": {
                "url": "'"$webhook_url"'",
                "content_type": "json"
            }
        }'

        # Send the POST request to add the webhook
        local response=$(curl -s -w "%{http_code}" -o temp.json -X POST \
            -H "Authorization: token $token" \
            -H "Content-Type: application/json" \
            -d "$payload" \
            "https://api.github.com/repos/$owner/$repo/hooks")

        # Check if the request was successful
        if [ "$response" -eq 201 ]; then
            echo "Webhook added successfully for URL: $webhook_url"
        else
            echo "Failed to add webhook for URL: $webhook_url"
            echo "Response code: $response"
            echo "Response body:"
            cat temp.json
        fi

        # Clean up temporary files
        rm -f temp.json
    done
}

# Main function
main() {
    # Source config file
    source config.sh

    # Prompt user to enter GitHub repository URL
    read -p "Enter GitHub repository URL: " repo_url

    # Call function to add webhooks
    add_webhooks "$repo_url"
}

# Execute main function
main

