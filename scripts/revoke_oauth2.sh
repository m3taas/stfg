#!/usr/bin/env sh

# Documentation: https://dev.twitch.tv/docs/authentication#revoking-access-tokens

ID="${1}"
TOKEN="${2}"

curl -sX POST "https://id.twitch.tv/oauth2/revoke?client_id=${ID}&token=${TOKEN}" | jq
