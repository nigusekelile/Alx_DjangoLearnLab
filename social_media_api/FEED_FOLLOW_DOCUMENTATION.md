# Social Media API - Follow & Feed Documentation

## Follow System

### Follow/Unfollow a User
**POST** `/api/auth/users/{user_id}/follow/`

**Description:** Toggle follow/unfollow for a user. If not following, will follow. If already following, will unfollow.

**Headers:**