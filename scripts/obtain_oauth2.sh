#!/usr/bin/env sh

# Documentation: https://dev.twitch.tv/docs/authentication/getting-tokens-oauth#oauth-authorization-code-flow

ID="${1}"
SEC="${2}"

curl -sX POST "https://id.twitch.tv/oauth2/token?client_id=${ID}&client_secret=${SEC}&grant_type=client_credentials" | jq
