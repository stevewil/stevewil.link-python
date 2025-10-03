# API Reference: `/users`

This document provides details for the `/api/v1/users` endpoint.

## GET `/users/{id}`

Retrieves a specific user by their unique ID.

<div style="background-color: #e7f3fe; border-left: 6px solid #2196F3; margin: 1.5em 0; padding: 0.5em 1.5em;">
  <h4>Note on Permissions</h4>
  <p>Regular users can only fetch their own data. Administrators can fetch any user's data.</p>
</div>

### Parameters

*   `id` (string, required): The unique identifier for the user.

<div style="background-color: #fff4e5; border-left: 6px solid #ff9800; margin: 1.5em 0; padding: 0.5em 1.5em;">
  <h4>Warning: Deprecation</h4>
  <p>The `email` field in the response will be deprecated in v2 of the API. Please use the `primary_email` field instead.</p>
</div>

The rest of the documentation continues here...